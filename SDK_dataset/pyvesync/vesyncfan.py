"""VeSync API for controling fans and purifiers."""

import json
import logging
from typing import Any, Dict, List, Tuple, Union, Optional
from pyvesync.vesyncbasedevice import VeSyncBaseDevice
from pyvesync.helpers import Helpers, Timer


humid_features: dict = {
    'Classic300S': {
        'module': 'VeSyncHumid200300S',
        'models': ['Classic300S', 'LUH-A601S-WUSB'],
        'features': ['nightlight'],
        'mist_modes': ['auto', 'sleep', 'manual'],
        'mist_levels': list(range(1, 10))
    },
    'Classic200S': {
        'module': 'VeSyncHumid200S',
        'models': ['Classic200S'],
        'features': [],
        'mist_modes': ['auto', 'manual'],
        'mist_levels': list(range(1, 10))
    },
    'Dual200S': {
        'module': 'VeSyncHumid200300S',
        'models': ['Dual200S',
                   'LUH-D301S-WUSR',
                   'LUH-D301S-WJP',
                   'LUH-D301S-WEU'],
        'features': [],
        'mist_modes': ['auto', 'manual'],
        'mist_levels': list(range(1, 3))
    },
    'LV600S': {
        'module': 'VeSyncHumid200300S',
        'models': ['LUH-A602S-WUSR',
                   'LUH-A602S-WUS',
                   'LUH-A602S-WEUR',
                   'LUH-A602S-WEU',
                   'LUH-A602S-WJP'],
        'features': ['warm_mist', 'nightlight'],
        'mist_modes': ['humidity', 'sleep', 'manual'],
        'mist_levels': list(range(1, 10)),
        'warm_mist_levels': [0, 1, 2, 3]
    },
    'OASISMIST': {
            'module': 'VeSyncHumid200300S',
            'models': ['LUH-O451S-WUS', 'LUH-O451S-WEU'],
            'features': ['warm_mist'],
            'mist_modes': ['humidity', 'sleep', 'manual'],
            'mist_levels': list(range(1, 10)),
            'warm_mist_levels': list(range(4))
    },
    'OASISMIST1000S': {
            'module': 'VeSyncHumid1000S',
            'models': ['LUH-M101S-WUS'],
            'features': [],
            'mist_modes': ['auto', 'sleep', 'manual'],
            'mist_levels': list(range(1, 10))
    }
}


air_features: dict = {
    'Core200S': {
        'module': 'VeSyncAirBypass',
        'models': ['Core200S', 'LAP-C201S-AUSR', 'LAP-C202S-WUSR'],
        'modes': ['sleep', 'off', 'manual'],
        'features': [],
        'levels': list(range(1, 4))
    },
    'Core300S': {
        'module': 'VeSyncAirBypass',
        'models': ['Core300S', 'LAP-C301S-WJP', 'LAP-C302S-WUSB'],
        'modes': ['sleep', 'off', 'auto', 'manual'],
        'features': ['air_quality'],
        'levels': list(range(1, 5))
    },
    'Core400S': {
        'module': 'VeSyncAirBypass',
        'models': ['Core400S',
                   'LAP-C401S-WJP',
                   'LAP-C401S-WUSR',
                   'LAP-C401S-WAAA'],
        'modes': ['sleep', 'off', 'auto', 'manual'],
        'features': ['air_quality'],
        'levels': list(range(1, 5))
    },
    'Core600S': {
        'module': 'VeSyncAirBypass',
        'models': ['Core600S',
                   'LAP-C601S-WUS',
                   'LAP-C601S-WUSR',
                   'LAP-C601S-WEU'],
        'modes': ['sleep', 'off', 'auto', 'manual'],
        'features': ['air_quality'],
        'levels': list(range(1, 5))
    },
    'LV-PUR131S': {
        'module': 'VeSyncAir131',
        'models': ['LV-PUR131S', 'LV-RH131S'],
        'features': ['air_quality']
    },
    'Vital100S': {
        'module': 'VeSyncVital',
        'models': ['LAP-V102S-AASR', 'LAP-V102S-WUS', 'LAP-V102S-WEU',
                   'LAP-V102S-AUSR', 'LAP-V102S-WJP'],
        'modes': ['manual', 'auto', 'sleep', 'off', 'pet'],
        'features': ['air_quality'],
        'levels': list(range(1, 5))
    },
    'Vital200S': {
        'module': 'VeSyncVital',
        'models': ['LAP-V201S-AASR', 'LAP-V201S-WJP', 'LAP-V201S-WEU',
                   'LAP-V201S-WUS', 'LAP-V201-AUSR'],
        'modes': ['manual', 'auto', 'sleep', 'off', 'pet'],
        'features': ['air_quality'],
        'levels': list(range(1, 5))
    }
}


logger = logging.getLogger(__name__)


def model_dict() -> dict:
    """Build purifier and humidifier model dictionary."""
    model_modules = {}
    for dev_dict in {**air_features, **humid_features}.values():
        for model in dev_dict['models']:
            model_modules[model] = dev_dict['module']
    return model_modules


def model_features(dev_type: str) -> dict:
    """Get features from device type."""
    for dev_dict in {**air_features, **humid_features}.values():
        if dev_type in dev_dict['models']:
            return dev_dict
    raise ValueError('Device not configured')


fan_classes: set = {v['module']
                    for k, v in {**air_features, **humid_features}.items()}

fan_modules: dict = model_dict()

__all__: list = list(fan_classes) + ['fan_modules']



class VeSyncAir131(VeSyncBaseDevice):
    """Levoit Air Purifier Class."""

    def __init__(self, details, manager):
        """Initilize air purifier class."""
        super().__init__(details, manager)

        self.details = {}

    def get_details(self) -> None:
        """Build Air Purifier details dictionary."""
        body = Helpers.req_body(self.manager, 'devicedetail')
        body['uuid'] = self.uuid
        head = Helpers.req_headers(self.manager)

        r, _ = Helpers.call_api(
            '/131airPurifier/v1/device/deviceDetail',
            method='post',
            headers=head,
            json_object=body,
        )

        if r is not None and Helpers.code_check(r):
            self.device_status = r.get('deviceStatus', 'unknown')
            self.connection_status = r.get('connectionStatus', 'unknown')
            self.details['active_time'] = r.get('activeTime', 0)
            self.details['filter_life'] = r.get('filterLife', {})
            self.details['screen_status'] = r.get('screenStatus', 'unknown')
            self.mode = r.get('mode', self.mode)
            self.details['level'] = r.get('level', 0)
            self.details['air_quality'] = r.get('airQuality', 'unknown')
        else:
            logger.debug('Error getting %s details', self.device_name)

    def get_config(self) -> None:
        """Get configuration info for air purifier."""
        body = Helpers.req_body(self.manager, 'devicedetail')
        body['method'] = 'configurations'
        body['uuid'] = self.uuid

        r, _ = Helpers.call_api(
            '/131airpurifier/v1/device/configurations',
            'post',
            headers=Helpers.req_headers(self.manager),
            json_object=body,
        )

        if r is not None and Helpers.code_check(r):
            self.config = Helpers.build_config_dict(r)
        else:
            logger.debug('Unable to get config info for %s',
                         self.device_name)

    @property
    def active_time(self) -> int:
        """Return total time active in minutes."""
        return self.details.get('active_time', 0)

    @property
    def fan_level(self) -> int:
        """Get current fan level (1-3)."""
        return self.details.get('level', 0)

    @property
    def filter_life(self) -> int:
        """Get percentage of filter life remaining."""
        try:
            return self.details['filter_life'].get('percent', 0)
        except KeyError:
            return 0

    @property
    def air_quality(self) -> str:
        """Get Air Quality."""
        return self.details.get('air_quality', 'unknown')

    @property
    def screen_status(self) -> str:
        """Return Screen status (on/off)."""
        return self.details.get('screen_status', 'unknown')

    def turn_on_display(self) -> bool:
        """Turn display on."""
        return self.toggle_display('on')

    def turn_off_display(self) -> bool:
        """Turn display off."""
        return self.toggle_display('off')

    def toggle_display(self, status: str) -> bool:
        """Toggle Display of VeSync LV-PUR131."""
        if status.lower() not in ['on', 'off']:
            logger.debug('Invalid display status - %s', status)
            return False
        head = Helpers.req_headers(self.manager)
        body = Helpers.req_body(self.manager, 'devicestatus')
        body['status'] = status.lower()
        r, _ = Helpers.call_api(
            '/131airPurifier/v1/device/updateScreen', 'put',
            json_object=body, headers=head
        )
        if r is not None and Helpers.code_check(r):
            self.details['screen_status'] = status.lower()
            return True
        logger.debug('Error toggling display for %s', self.device_name)
        return False

    def turn_on(self) -> bool:
        """Turn Air Purifier on."""
        if self.device_status != 'on':
            body = Helpers.req_body(self.manager, 'devicestatus')
            body['uuid'] = self.uuid
            body['status'] = 'on'
            head = Helpers.req_headers(self.manager)

            r, _ = Helpers.call_api(
                '/131airPurifier/v1/device/deviceStatus', 'put',
                json_object=body, headers=head
            )

            if r is not None and Helpers.code_check(r):
                self.device_status = 'on'
                return True
            logger.debug('Error turning %s on', self.device_name)
            return False
        return False

    def turn_off(self) -> bool:
        """Turn Air Purifier Off."""
        if self.device_status == 'on':
            body = Helpers.req_body(self.manager, 'devicestatus')
            body['uuid'] = self.uuid
            body['status'] = 'off'
            head = Helpers.req_headers(self.manager)

            r, _ = Helpers.call_api(
                '/131airPurifier/v1/device/deviceStatus', 'put',
                json_object=body, headers=head
            )

            if r is not None and Helpers.code_check(r):
                self.device_status = 'off'
                return True
            logger.debug('Error turning %s off', self.device_name)
            return False
        return True

    def auto_mode(self) -> bool:
        """Set mode to auto."""
        return self.mode_toggle('auto')

    def manual_mode(self) -> bool:
        """Set mode to manual."""
        return self.mode_toggle('manual')

    def sleep_mode(self) -> bool:
        """Set sleep mode to on."""
        return self.mode_toggle('sleep')

    def change_fan_speed(self, speed: Optional[int] = None) -> bool:
        """Adjust Fan Speed for air purifier.

        Specifying 1,2,3 as argument or call without argument to cycle
        through speeds increasing by one.
        """
        if self.mode != 'manual':
            logger.debug('%s not in manual mode, cannot change speed',
                         self.device_name)
            return False

        try:
            level = self.details['level']
        except KeyError:
            logger.debug(
                'Cannot change fan speed, no level set for %s',
                self.device_name
            )
            return False

        body = Helpers.req_body(self.manager, 'devicestatus')
        body['uuid'] = self.uuid
        head = Helpers.req_headers(self.manager)
        if speed is not None:
            if speed == level:
                return True
            if speed in [1, 2, 3]:
                body['level'] = speed
            else:
                logger.debug('Invalid fan speed for %s',
                             self.device_name)
                return False
        else:
            if (level + 1) > 3:
                body['level'] = 1
            else:
                body['level'] = int(level + 1)

        r, _ = Helpers.call_api(
            '/131airPurifier/v1/device/updateSpeed', 'put',
            json_object=body, headers=head
        )

        if r is not None and Helpers.code_check(r):
            self.details['level'] = body['level']
            return True
        logger.debug('Error changing %s speed', self.device_name)
        return False

    def mode_toggle(self, mode: str) -> bool:
        """Set mode to manual, auto or sleep."""
        head = Helpers.req_headers(self.manager)
        body = Helpers.req_body(self.manager, 'devicestatus')
        body['uuid'] = self.uuid
        if mode != self.mode and mode in ['sleep', 'auto', 'manual']:
            body['mode'] = mode
            if mode == 'manual':
                body['level'] = 1

            r, _ = Helpers.call_api(
                '/131airPurifier/v1/device/updateMode', 'put',
                json_object=body, headers=head
            )

            if r is not None and Helpers.code_check(r):
                self.mode = mode
                return True

        logger.debug('Error setting %s mode - %s', self.device_name, mode)
        return False

    def update(self) -> None:
        """Run function to get device details."""
        self.get_details()

    def display(self) -> None:
        """Return formatted device info to stdout."""
        super().display()
        disp = [
            ('Active Time : ', self.active_time(), ' minutes'),
            ('Fan Level: ', self.fan_level(), ''),
            ('Air Quality: ', self.air_quality(), ''),
            ('Mode: ', self.mode, ''),
            ('Screen Status: ', self.screen_status(), ''),
            ('Filter Life: ', json.dumps(self.filter_life()), ' percent')
            ]
        for line in disp:
            print(f'{line[0]:.<30} {line[1]} {line[2]}')

    def displayJSON(self) -> str:
        """Return air purifier status and properties in JSON output."""
        sup = super().displayJSON()
        sup_val = json.loads(sup)
        sup_val.update(
            {
                'Active Time': str(self.active_time()),
                'Fan Level': self.fan_level(),
                'Air Quality': self.air_quality(),
                'Mode': self.mode,
                'Screen Status': self.screen_status(),
                'Filter Life': str(self.filter_life())
            }
        )
        return json.dumps(sup_val, indent=4)


