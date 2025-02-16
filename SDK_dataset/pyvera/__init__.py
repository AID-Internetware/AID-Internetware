"""Vera Controller Python API.

This lib is designed to simplify communication with Vera controllers
"""
from abc import ABC, abstractmethod
import collections
from datetime import datetime
import json
import logging
import os
import shlex
import threading
import time
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Tuple, Union, cast

import requests

TIMESTAMP_NONE = {"dataversion": 1, "loadtime": 0}

# Time to block on Vera poll if there are no changes in seconds
SUBSCRIPTION_WAIT = 30
# Min time to wait for event in miliseconds
SUBSCRIPTION_MIN_WAIT = 200
# Timeout for requests calls, as vera sometimes just sits on sockets.
TIMEOUT = SUBSCRIPTION_WAIT
# VeraLock set target timeout in seconds
LOCK_TARGET_TIMEOUT_SEC = 30

CATEGORY_DIMMER = 2
CATEGORY_SWITCH = 3
CATEGORY_ARMABLE = 4
CATEGORY_THERMOSTAT = 5
CATEGORY_LOCK = 7
CATEGORY_CURTAIN = 8
CATEGORY_REMOTE = 9
CATEGORY_GENERIC = 11
CATEGORY_SENSOR = 12
CATEGORY_SCENE_CONTROLLER = 14
CATEGORY_HUMIDITY_SENSOR = 16
CATEGORY_TEMPERATURE_SENSOR = 17
CATEGORY_LIGHT_SENSOR = 18
CATEGORY_POWER_METER = 21
CATEGORY_VERA_SIREN = 24
CATEGORY_UV_SENSOR = 28
CATEGORY_GARAGE_DOOR = 32


# How long to wait before retrying Vera
SUBSCRIPTION_RETRY = 9

# Vera state codes see http://wiki.micasaverde.com/index.php/Luup_Requests
STATE_NO_JOB = -1
STATE_JOB_WAITING_TO_START = 0
STATE_JOB_IN_PROGRESS = 1
STATE_JOB_ERROR = 2
STATE_JOB_ABORTED = 3
STATE_JOB_DONE = 4
STATE_JOB_WAITING_FOR_CALLBACK = 5
STATE_JOB_REQUEUE = 6
STATE_JOB_PENDING_DATA = 7

STATE_NOT_PRESENT = 999

ChangedDevicesValue = Tuple[List[dict], dict]
LockCode = Tuple[str, str, str]
UserCode = Tuple[str, str]
SubscriptionCallback = Callable[["VeraDevice"], None]


def init_logging(logger: Any, logger_level: Optional[str]) -> None:
    """Initialize the logger."""
    # Set logging level (such as INFO, DEBUG, etc) via an environment variable
    # Defaults to WARNING log level unless PYVERA_LOGLEVEL variable exists
    if logger_level:
        logger.setLevel(logger_level)
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(
            logging.Formatter("%(levelname)s@{%(name)s:%(lineno)d} - %(message)s")
        )
        logger.addHandler(log_handler)


# Set up the console logger for debugging
LOG = logging.getLogger(__name__)
init_logging(LOG, os.environ.get("PYVERA_LOGLEVEL"))
LOG.debug("DEBUG logging is ON")


# pylint: disable=too-many-instance-attributes
class VeraController:
    """Class to interact with the Vera device."""

    temperature_units = "C"

    def __init__(
        self,
        base_url: str,
        subscription_registry: Optional["AbstractSubscriptionRegistry"] = None,
    ):
        """Init Vera controller at the given URL.

        base_url: Vera API URL, eg http://vera:3480.
        """

        self.base_url = base_url
        self.devices: List[VeraDevice] = []
        self.scenes: List[VeraScene] = []
        self.temperature_units = "C"
        self.version = None
        self.model = None
        self.serial_number = None
        self.device_services_map: Dict[int, List[dict]] = {}
        self.subscription_registry = subscription_registry or SubscriptionRegistry()
        self.subscription_registry.set_controller(self)
        self.categories: Dict[int, str] = {}
        self.device_id_map: Dict[int, VeraDevice] = {}

    def data_request(self, payload: dict, timeout: int = TIMEOUT) -> requests.Response:
        """Perform a data_request and return the result."""
        request_url = self.base_url + "/data_request"
        response = requests.get(request_url, timeout=timeout, params=payload)
        response.encoding = response.encoding if response.encoding else "utf-8"
        return response

    def get_simple_devices_info(self) -> None:
        """Get basic device info from Vera."""
        j = self.data_request({"id": "sdata"}).json()

        self.scenes = []
        items = j.get("scenes")

        for item in items:
            self.scenes.append(VeraScene(item, self))

        if j.get("temperature"):
            self.temperature_units = j.get("temperature")

        self.categories = {}
        cats = j.get("categories")

        for cat in cats:
            self.categories[cat.get("id")] = cat.get("name")

        self.device_id_map = {}

        devs = j.get("devices")
        for dev in devs:
            dev["categoryName"] = self.categories.get(dev.get("category"))
            self.device_id_map[dev.get("id")] = dev

    def get_scenes(self) -> List["VeraScene"]:
        """Get list of scenes."""

        self.get_simple_devices_info()

        return self.scenes

    def get_device_by_name(self, device_name: str) -> Optional["VeraDevice"]:
        """Search the list of connected devices by name.

        device_name param is the string name of the device
        """

        # Find the device for the vera device name we are interested in
        found_device = None
        for device in self.get_devices():
            if device.name == device_name:
                found_device = device
                # found the first (and should be only) one so we will finish
                break

        if found_device is None:
            LOG.debug("Did not find device with %s", device_name)

        return found_device

    def get_device_by_id(self, device_id: int) -> Optional["VeraDevice"]:
        """Search the list of connected devices by ID.

        device_id param is the integer ID of the device
        """

        # Find the device for the vera device name we are interested in
        found_device = None
        for device in self.get_devices():
            if device.device_id == device_id:
                found_device = device
                # found the first (and should be only) one so we will finish
                break

        if found_device is None:
            LOG.debug("Did not find device with %s", device_id)

        return found_device

    def get_devices(self, category_filter: str = "") -> List["VeraDevice"]:
        """Get list of connected devices.

        category_filter param is an array of strings.  If specified, this
        function will only return devices with category names which match the
        strings in this filter.
        """

        # the Vera rest API is a bit rough so we need to make 2 calls to get
        # all the info we need
        self.get_simple_devices_info()

        json_data = self.data_request({"id": "status", "output_format": "json"}).json()

        self.devices = []
        items = json_data.get("devices")
        alerts = json_data.get("alerts", ())

        for item in items:
            item["deviceInfo"] = self.device_id_map.get(item.get("id")) or {}
            item_alerts = [
                alert for alert in alerts if alert.get("PK_Device") == item.get("id")
            ]
            device_category = item.get("deviceInfo", {}).get("category")

            device: VeraDevice
            if device_category == CATEGORY_DIMMER:
                device = VeraDimmer(item, item_alerts, self)
            elif device_category in (CATEGORY_SWITCH, CATEGORY_VERA_SIREN):
                device = VeraSwitch(item, item_alerts, self)
            elif device_category == CATEGORY_THERMOSTAT:
                device = VeraThermostat(item, item_alerts, self)
            elif device_category == CATEGORY_LOCK:
                device = VeraLock(item, item_alerts, self)
            elif device_category == CATEGORY_CURTAIN:
                device = VeraCurtain(item, item_alerts, self)
            elif device_category == CATEGORY_ARMABLE:
                device = VeraBinarySensor(item, item_alerts, self)
            elif device_category in (
                CATEGORY_SENSOR,
                CATEGORY_HUMIDITY_SENSOR,
                CATEGORY_TEMPERATURE_SENSOR,
                CATEGORY_LIGHT_SENSOR,
                CATEGORY_POWER_METER,
                CATEGORY_UV_SENSOR,
            ):
                device = VeraSensor(item, item_alerts, self)
            elif device_category in (CATEGORY_SCENE_CONTROLLER, CATEGORY_REMOTE):
                device = VeraSceneController(item, item_alerts, self)
            elif device_category == CATEGORY_GARAGE_DOOR:
                device = VeraGarageDoor(item, item_alerts, self)
            else:
                device = VeraDevice(item, item_alerts, self)

            self.devices.append(device)

            if device.is_armable() and device_category not in (
                CATEGORY_SWITCH,
                CATEGORY_VERA_SIREN,
                CATEGORY_CURTAIN,
                CATEGORY_GARAGE_DOOR,
            ):
                self.devices.append(VeraArmableDevice(item, item_alerts, self))

        return [
            device
            for device in self.devices
            if not category_filter
            or (
                device.category_name is not None
                and device.category_name != ""
                and device.category_name in category_filter
            )
        ]

    def refresh_data(self) -> Dict[int, "VeraDevice"]:
        """Refresh mapping from device ids to devices."""
        # Note: This function is side-effect free and appears to be unused.
        # Safe to erase?

        # the Vera rest API is a bit rough so we need to make 2 calls
        # to get all the info e need
        j = self.data_request({"id": "sdata"}).json()

        self.temperature_units = j.get("temperature", "C")
        self.model = j.get("model")
        self.version = j.get("version")
        self.serial_number = j.get("serial_number")

        categories = {}
        cats = j.get("categories")

        for cat in cats:
            categories[cat.get("id")] = cat.get("name")

        device_id_map = {}

        devs = j.get("devices")
        for dev in devs:
            dev["categoryName"] = categories.get(dev.get("category"))
            device_id_map[dev.get("id")] = dev

        return device_id_map

    def map_services(self) -> None:
        """Get full Vera device service info."""
        # Note: This function updates the device_services_map, but that map does
        # not appear to be used.  Safe to erase?
        self.get_simple_devices_info()

        j = self.data_request({"id": "status", "output_format": "json"}).json()

        service_map = {}

        items = j.get("devices")

        for item in items:
            service_map[item.get("id")] = item.get("states")

        self.device_services_map = service_map

    def get_changed_devices(self, timestamp: dict) -> ChangedDevicesValue:
        """Get data since last timestamp.

        This function blocks until a change is returned by the Vera, or the
        request times out.

        timestamp param: the timestamp returned by the last invocation of this
        function.  Use a timestamp of TIMESTAMP_NONE for the first invocation.
        """
        payload = {
            "timeout": SUBSCRIPTION_WAIT,
            "minimumdelay": SUBSCRIPTION_MIN_WAIT,
            "id": "lu_sdata",
        }
        payload.update(timestamp)

        # double the timeout here so requests doesn't timeout before vera
        LOG.debug("get_changed_devices() requesting payload %s", str(payload))
        response = self.data_request(payload, TIMEOUT * 2)
        response.raise_for_status()

        # If the Vera disconnects before writing a full response (as lu_sdata
        # will do when interrupted by a Luup reload), the requests module will
        # happily return 200 with an empty string. So, test for empty response,
        # so we don't rely on the JSON parser to throw an exception.
        if response.text == "":
            raise PyveraError("Empty response from Vera")

        # Catch a wide swath of what the JSON parser might throw, within
        # reason. Unfortunately, some parsers don't specifically return
        # json.decode.JSONDecodeError, but so far most seem to derive what
        # they do throw from ValueError, so that's helpful.
        try:
            result = response.json()
        except ValueError as ex:
            raise PyveraError("JSON decode error: " + str(ex))

        if not (
            isinstance(result, dict)
            and "loadtime" in result
            and "dataversion" in result
        ):
            raise PyveraError("Unexpected/garbled response from Vera")

        # At this point, all good. Update timestamp and return change data.
        device_data = result.get("devices", [])
        timestamp = {
            "loadtime": result.get("loadtime", 0),
            "dataversion": result.get("dataversion", 1),
        }
        return device_data, timestamp

    def get_alerts(self, timestamp: dict) -> List[dict]:
        """Get alerts that have triggered since last timestamp.

        Note that unlike get_changed_devices, this is non-blocking.

        timestamp param: the timestamp returned by the prior (not current)
        invocation of get_changed_devices.  Use a timestamp of TIMESTAMP_NONE
        for the first invocation.
        """

        payload = {
            "LoadTime": timestamp["loadtime"],
            "DataVersion": timestamp["dataversion"],
            "id": "status",
        }

        LOG.debug("get_alerts() requesting payload %s", str(payload))
        response = self.data_request(payload)
        response.raise_for_status()

        if response.text == "":
            raise PyveraError("Empty response from Vera")

        try:
            result = response.json()
        except ValueError as ex:
            raise PyveraError("JSON decode error: " + str(ex))

        if not (
            isinstance(result, dict)
            and "LoadTime" in result
            and "DataVersion" in result
        ):
            raise PyveraError("Unexpected/garbled response from Vera")

        return result.get("alerts", [])

    # The subscription thread (if you use it) runs in the background and blocks
    # waiting for state changes (a.k.a. events) from the Vera controller.  When
    # an event occurs, the subscription thread will invoke any callbacks for
    # affected devices.
    #
    # The subscription thread is (obviously) run on a separate thread.  This
    # means there is a potential for race conditions.  Pyvera contains no locks
    # or synchronization primitives.  To avoid race conditions, clients should
    # do the following:
    #
    # (a) set up Pyvera, including registering any callbacks, before starting
    # the subscription thread.
    #
    # (b) Once the subscription thread has started, realize that callbacks will
    # be invoked in the context of the subscription thread.  Only access Pyvera
    # from those callbacks from that point forwards.

    def start(self) -> None:
        """Start the subscription thread."""
        self.subscription_registry.start()

    def stop(self) -> None:
        """Stop the subscription thread."""
        self.subscription_registry.stop()

    def register(self, device: "VeraDevice", callback: SubscriptionCallback) -> None:
        """Register a device and callback with the subscription service.

        The callback will be called from the subscription thread when the device
        is updated.
        """
        self.subscription_registry.register(device, callback)

    def unregister(self, device: "VeraDevice", callback: SubscriptionCallback) -> None:
        """Unregister a device and callback with the subscription service."""
        self.subscription_registry.unregister(device, callback)


# pylint: disable=too-many-public-methods
class VeraDevice:
    """Class to represent each vera device."""

    def __init__(
        self, json_obj: dict, json_alerts: List[dict], vera_controller: VeraController
    ):
        """Init object."""
        self.json_state = json_obj
        self.device_id = self.json_state.get("id")
        self.vera_controller = vera_controller
        self.name = ""
        self.alerts: List[VeraAlert] = []
        self.set_alerts(json_alerts)

        if self.json_state.get("deviceInfo"):
            device_info = self.json_state.get("deviceInfo", {})
            self.category = device_info.get("category")
            self.category_name = device_info.get("categoryName")
            self.name = device_info.get("name")
        else:
            self.category_name = ""

        if not self.name:
            if self.category_name:
                self.name = "Vera " + self.category_name + " " + str(self.device_id)
            else:
                self.name = "Vera Device " + str(self.device_id)

    def __repr__(self) -> str:
        """Get a string representation."""
        return f"{self.__class__.__name__} (id={self.device_id} category={self.category_name} name={self.name})"

    @property
    def switch_service(self) -> str:
        """Vera service string for switch."""
        return "urn:upnp-org:serviceId:SwitchPower1"

    @property
    def dimmer_service(self) -> str:
        """Vera service string for dimmer."""
        return "urn:upnp-org:serviceId:Dimming1"

    @property
    def security_sensor_service(self) -> str:
        """Vera service string for armable sensors."""
        return "urn:micasaverde-com:serviceId:SecuritySensor1"

    @property
    def window_covering_service(self) -> str:
        """Vera service string for window covering service."""
        return "urn:upnp-org:serviceId:WindowCovering1"

    @property
    def lock_service(self) -> str:
        """Vera service string for lock service."""
        return "urn:micasaverde-com:serviceId:DoorLock1"

    @property
    def thermostat_operating_service(self) -> Tuple[str]:
        """Vera service string HVAC operating mode."""
        return ("urn:upnp-org:serviceId:HVAC_UserOperatingMode1",)

    @property
    def thermostat_fan_service(self) -> str:
        """Vera service string HVAC fan operating mode."""
        return "urn:upnp-org:serviceId:HVAC_FanOperatingMode1"

    @property
    def thermostat_cool_setpoint(self) -> str:
        """Vera service string Temperature Setpoint1 Cool."""
        return "urn:upnp-org:serviceId:TemperatureSetpoint1_Cool"

    @property
    def thermostat_heat_setpoint(self) -> str:
        """Vera service string Temperature Setpoint Heat."""
        return "urn:upnp-org:serviceId:TemperatureSetpoint1_Heat"

    @property
    def thermostat_setpoint(self) -> str:
        """Vera service string Temperature Setpoint."""
        return "urn:upnp-org:serviceId:TemperatureSetpoint1"

    @property
    def color_service(self) -> str:
        """Vera service string for color."""
        return "urn:micasaverde-com:serviceId:Color1"

    @property
    def poll_service(self) -> str:
        """Vera service string for poll."""
        return "urn:micasaverde-com:serviceId:HaDevice1"

    def vera_request(self, **kwargs: Any) -> requests.Response:
        """Perfom a vera_request for this device."""
        request_payload = {"output_format": "json", "DeviceNum": self.device_id}
        request_payload.update(kwargs)

        return self.vera_controller.data_request(request_payload)

    def set_service_value(
        self,
        service_id: Union[str, Tuple[str, ...]],
        set_name: str,
        parameter_name: str,
        value: Any,
    ) -> None:
        """Set a variable on the vera device.

        This will call the Vera api to change device state.
        """
        payload = {
            "id": "lu_action",
            "action": "Set" + set_name,
            "serviceId": service_id,
            parameter_name: value,
        }
        result = self.vera_request(**payload)
        LOG.debug(
            "set_service_value: " "result of vera_request with payload %s: %s",
            payload,
            result.text,
        )

    def set_door_code_values(
        self, service_id: Union[str, Tuple[str, ...]], operation: str, parameter: dict
    ) -> requests.Response:
        """Add or remove door code on the vera Lock.

        This will call the Vera api to change Lock code.
        """
        payload = {"id": "lu_action", "action": operation, "serviceId": service_id}
        for param in parameter:
            payload[param] = parameter[param]
        result = self.vera_request(**payload)
        LOG.debug(
            "set_door_code_values: " "result of vera_request with payload %s: %s",
            payload,
            result.text,
        )
        return result

    def call_service(self, service_id: str, action: str) -> requests.Response:
        """Call a Vera service.

        This will call the Vera api to change device state.
        """
        result = self.vera_request(id="action", serviceId=service_id, action=action)
        LOG.debug(
            "call_service: " "result of vera_request for %s with id %s: %s",
            self.name,
            service_id,
            result.text,
        )
        return result

    def poll_device(self) -> None:
        """Poll the device to try and connect."""
        self.call_service(self.poll_service(), "Poll")

    def set_cache_value(self, name: str, value: Any) -> None:
        """Set a variable in the local state dictionary.

        This does not change the physical device. Useful if you want the
        device state to refect a new value which has not yet updated from
        Vera.
        """
        dev_info = self.json_state.get("deviceInfo", {})
        if dev_info.get(name.lower()) is None:
            LOG.error("Could not set %s for %s (key does not exist).", name, self.name)
            LOG.error("- dictionary %s", dev_info)
            return
        dev_info[name.lower()] = str(value)

    def set_cache_complex_value(self, name: str, value: Any) -> None:
        """Set a variable in the local complex state dictionary.

        This does not change the physical device. Useful if you want the
        device state to refect a new value which has not yet updated from
        Vera.
        """
        for item in self.json_state.get("states", []):
            if item.get("variable") == name:
                item["value"] = str(value)

    def get_complex_value(self, name: str) -> Any:
        """Get a value from the service dictionaries.

        It's best to use get_value if it has the data you require since
        the vera subscription only updates data in dev_info.
        """
        for item in self.json_state.get("states", []):
            if item.get("variable") == name:
                return item.get("value")
        return None

    def get_all_values(self) -> dict:
        """Get all values from the deviceInfo area.

        The deviceInfo data is updated by the subscription service.
        """
        return cast(dict, self.json_state.get("deviceInfo"))

    def get_value(self, name: str) -> Any:
        """Get a value from the dev_info area.

        This is the common Vera data and is the best place to get state from
        if it has the data you require.

        This data is updated by the subscription service.
        """
        return self.get_strict_value(name.lower())

    def get_strict_value(self, name: str) -> Any:
        """Get a case-sensitive keys value from the dev_info area."""
        dev_info = self.json_state.get("deviceInfo", {})
        return dev_info.get(name, None)

    def refresh_complex_value(self, name: str) -> Any:
        """Refresh a value from the service dictionaries.

        It's best to use get_value / refresh if it has the data you need.
        """
        for item in self.json_state.get("states", []):
            if item.get("variable") == name:
                service_id = item.get("service")
                result = self.vera_request(
                    **{
                        "id": "variableget",
                        "output_format": "json",
                        "DeviceNum": self.device_id,
                        "serviceId": service_id,
                        "Variable": name,
                    }
                )
                item["value"] = result.text
                return item.get("value")
        return None

    def set_alerts(self, json_alerts: List[dict]) -> None:
        """Convert JSON alert data to VeraAlerts."""
        self.alerts = [VeraAlert(json_alert, self) for json_alert in json_alerts]

    def get_alerts(self) -> List["VeraAlert"]:
        """Get any alerts present during the most recent poll cycle."""
        return self.alerts

    def refresh(self) -> None:
        """Refresh the dev_info data used by get_value.

        Only needed if you're not using subscriptions.
        """
        j = self.vera_request(id="sdata", output_format="json").json()
        devices = j.get("devices")
        for device_data in devices:
            if device_data.get("id") == self.device_id:
                self.update(device_data)

    def update(self, params: dict) -> None:
        """Update the dev_info data from a dictionary.

        Only updates if it already exists in the device.
        """
        dev_info = self.json_state.get("deviceInfo", {})
        dev_info.update({k: params[k] for k in params if dev_info.get(k)})

    @property
    def is_armable(self) -> bool:
        """Device is armable."""
        return self.get_value("Armed") is not None

    @property
    def is_armed(self) -> bool:
        """Device is armed now."""
        return cast(str, self.get_value("Armed")) == "1"

    @property
    def is_dimmable(self) -> bool:
        """Device is dimmable."""
        return cast(int, self.category) == CATEGORY_DIMMER

    @property
    def is_trippable(self) -> bool:
        """Device is trippable."""
        return self.get_value("Tripped") is not None

    @property
    def is_tripped(self) -> bool:
        """Device is tripped now."""
        return cast(str, self.get_value("Tripped")) == "1"

    @property
    def has_battery(self) -> bool:
        """Device has a battery."""
        return self.get_value("BatteryLevel") is not None

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        return cast(int, self.get_value("BatteryLevel"))

    @property
    def last_trip(self) -> str:
        """Time device last tripped."""
        # Vera seems not to update this for my device!
        return cast(str, self.get_value("LastTrip"))

    @property
    def light(self) -> int:
        """Light level in lux."""
        return cast(int, self.get_value("Light"))

    @property
    def level(self) -> int:
        """Get level from vera."""
        # Used for dimmers, curtains
        # Have seen formats of 10, 0.0 and "0%"!
        level = self.get_value("level")
        try:
            return int(float(level))
        except (TypeError, ValueError):
            pass
        try:
            return int(level.strip("%"))
        except (TypeError, AttributeError, ValueError):
            pass
        return 0

    @property
    def temperature(self) -> float:
        """Get the temperature.

        You can get units from the controller.
        """
        return cast(float, self.get_value("Temperature"))

    @property
    def humidity(self) -> float:
        """Get the humidity level in percent."""
        return cast(float, self.get_value("Humidity"))

    @property
    def power(self) -> int:
        """Get the current power useage in watts."""
        return cast(int, self.get_value("Watts"))

    @property
    def energy(self) -> int:
        """Get the energy usage in kwh."""
        return cast(int, self.get_value("kwh"))

    @property
    def room_id(self) -> int:
        """Get the Vera Room ID."""
        return cast(int, self.get_value("room"))

    @property
    def comm_failure(self) -> bool:
        """Return the Communication Failure Flag."""
        status = self.get_strict_value("commFailure")
        if status is None:
            return False
        return cast(str, status) != "0"

    @property
    def vera_device_id(self) -> int:
        """Get the ID Vera uses to refer to the device."""
        return cast(int, self.device_id)

    @property
    def should_poll(self) -> bool:
        """Whether polling is needed if using subscriptions for this device."""
        return self.comm_failure()


class VeraSwitch(VeraDevice):
    """Class to add switch functionality."""

    def set_switch_state(self, state: int) -> None:
        """Set the switch state, also update local state."""
        self.set_service_value(self.switch_service(), "Target", "newTargetValue", state)
        self.set_cache_value("Status", state)

    def switch_on(self) -> None:
        """Turn the switch on, also update local state."""
        self.set_switch_state(1)

    def switch_off(self) -> None:
        """Turn the switch off, also update local state."""
        self.set_switch_state(0)

    def is_switched_on(self, refresh: bool = False) -> bool:
        """Get switch state.

        Refresh data from Vera if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using subscriptions.
        """
        if refresh:
            self.refresh()
        val = self.get_value("Status")
        return cast(str, val) == "1"

