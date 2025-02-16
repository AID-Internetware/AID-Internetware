import subprocess

command0 = [r'python',
        r'AID\__main__.py']

command_out = ['-o',
        'cg.json']


def run_script(command1):

    command = command0 + command1 + command_out
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
        print("Succeed to analyze " + command1[0].split('\\')[1])
        return result
    except subprocess.CalledProcessError as e:
        print("Failed to analyze:" + command1[0].split('\\')[1], e)
        return None


if __name__ == "__main__":

    #1.miio
    command = [r'SDK_dataset\miio\integrations\chuangmi\camera\chuangmi_camera.py',
        r'SDK_dataset\miio\device.py', 
        r'SDK_dataset\miio\miioprotocol.py']
    with open('RQ1-2\\DECG_results\\miio.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #2.broadlink
    command = [r'SDK_dataset\broadlink\light.py']
    with open('RQ1-2\\DECG_results\\broadlink.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #3.kasa
    command = ['SDK_dataset\kasa\smartbulb.py']
    with open('RQ1-2\\DECG_results\\kasa.txt', 'w') as file:
        file.write(str(run_script(command).stdout))
    
    #4.ring_doorbell
    command = [r'SDK_dataset\ring_doorbell\auth.py',
        r'SDK_dataset\ring_doorbell\const.py', 
        r'SDK_dataset\ring_doorbell\doorbot.py',
        r'SDK_dataset\ring_doorbell\generic.py']
    with open('RQ1-2\\DECG_results\\ring_doorbell.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #5.blinkpy
    command = [r'SDK_dataset\blinkpy\api.py',
        r'SDK_dataset\blinkpy\auth.py', ] 
    with open('RQ1-2\\DECG_results\\blinkpy.txt', 'w') as file:
        file.write(str(run_script(command).stdout))
    
    #6.pywizlight
    command = [r'SDK_dataset\pywizlight\bulb.py',
        r'SDK_dataset\pywizlight\bulblibrary.py', 
        r'SDK_dataset\pywizlight\models.py',
        r'SDK_dataset\pywizlight\protocol.py',
        r'SDK_dataset\pywizlight\rgbcw.py',
        r'SDK_dataset\pywizlight\scenes.py',
        r'SDK_dataset\pywizlight\vec.py',
        r'SDK_dataset\pywizlight\_version.py',
        r'SDK_dataset\pywizlight\__init__.py']  
    with open('RQ1-2\\DECG_results\\pywizlight.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #7.amcrest
    command = [r'SDK_dataset\amcrest\http.py',
        r'SDK_dataset\amcrest\motion_detection.py', ]  
    with open('RQ1-2\\DECG_results\\amcrest.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #8.pyvesync
    command = [r'SDK_dataset\pyvesync\helpers.py',
        r'SDK_dataset\pyvesync\vesyncfan.py', ]   
    with open('RQ1-2\\DECG_results\\pyvesync.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #9.pyhomematic
    command = [r'SDK_dataset\pyhomematic\connection.py',
        r'SDK_dataset\pyhomematic\exceptions.py', 
        r'SDK_dataset\pyhomematic\vccu.py',
        r'SDK_dataset\pyhomematic\_hm.py',
        r'SDK_dataset\pyhomematic\__init__.py',
        r'SDK_dataset\pyhomematic\devicetypes\actors.py',
        r'SDK_dataset\pyhomematic\devicetypes\generic.py',
        r'SDK_dataset\pyhomematic\devicetypes\helper.py',
        r'SDK_dataset\pyhomematic\devicetypes\misc.py',
        r'SDK_dataset\pyhomematic\devicetypes\sensors.py',
        r'SDK_dataset\pyhomematic\devicetypes\thermostats.py',
        r'SDK_dataset\pyhomematic\devicetypes\__init__.py']  
    with open('RQ1-2\\DECG_results\\pyhomematic.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #10.flux_led
    command = [r'SDK_dataset\flux_led\aio.py',
        r'SDK_dataset\flux_led\aioprotocol.py', 
        r'SDK_dataset\flux_led\aioutils.py',
        r'SDK_dataset\flux_led\base_device.py',
        r'SDK_dataset\flux_led\const.py',
        r'SDK_dataset\flux_led\device.py',
        r'SDK_dataset\flux_led\models_db.py',
        r'SDK_dataset\flux_led\pattern.py',
        r'SDK_dataset\flux_led\protocol.py',
        r'SDK_dataset\flux_led\sock.py',
        r'SDK_dataset\flux_led\timer.py',
        r'SDK_dataset\flux_led\utils.py',
        r'SDK_dataset\flux_led\__init__.py']
    with open('RQ1-2\\DECG_results\\flux_led.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #11.pylutron_caseta
    command = [r'SDK_dataset\pylutron_caseta\smartbridge.py',]   
    with open('RQ1-2\\DECG_results\\pylutron_caseta.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #12.pysmartthings
    command = [r'SDK_dataset\pysmartthings\api.py',
        r'SDK_dataset\pysmartthings\capability.py', 
        r'SDK_dataset\pysmartthings\const.py',
        r'SDK_dataset\pysmartthings\device.py',
        r'SDK_dataset\pysmartthings\entity.py',
        r'SDK_dataset\pysmartthings\subscription.py',
        r'SDK_dataset\pysmartthings\__init__.py',]  
    with open('RQ1-2\\DECG_results\\pysmartthings.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #13.yeelight
    command = [r'SDK_dataset\yeelight\main.py',]   
    with open('RQ1-2\\DECG_results\\yeelight.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #14.pyezviz
    command = [r'SDK_dataset\pyezviz\camera.py',
               r'SDK_dataset\pyezviz\client.py']   
    with open('RQ1-2\\DECG_results\\pyezviz.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #15.pybotvac
    command = [r'SDK_dataset\pybotvac\neato.py',
        r'SDK_dataset\pybotvac\robot.py', 
        r'SDK_dataset\pybotvac\vorwerk.py',
        r'SDK_dataset\pybotvac\__init__.py']
    with open('RQ1-2\\DECG_results\\pybotvac.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #16.wled
    command = [r'SDK_dataset\wled\exceptions.py',
        r'SDK_dataset\wled\models.py', 
        r'SDK_dataset\wled\wled.py',
        r'SDK_dataset\wled\__init__.py']
    with open('RQ1-2\\DECG_results\\wled.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #17.switchbot
    command = [r'SDK_dataset\switchbot\const.py',
        r'SDK_dataset\switchbot\enum.py', 
        r'SDK_dataset\switchbot\models.py',
        r'SDK_dataset\switchbot\__init__.py',
        r'SDK_dataset\switchbot\devices\base_light.py',
        r'SDK_dataset\switchbot\devices\bulb.py',
        r'SDK_dataset\switchbot\devices\device.py',
        r'SDK_dataset\switchbot\devices\__init__.py']  
    with open('RQ1-2\\DECG_results\\switchbot.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #18.PyTado
    command = [r'SDK_dataset\PyTado\interface.py',
        r'SDK_dataset\PyTado\http\http.py', 
        r'SDK_dataset\PyTado\http\__init__.py']
    with open('RQ1-2\\DECG_results\\PyTado.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #19.aiohue
    command = [r'SDK_dataset\aiohue\__init__.py',
        r'SDK_dataset\aiohue\v2\__init__.py',
        r'SDK_dataset\aiohue\v2\controllers\base.py',
        r'SDK_dataset\aiohue\v2\controllers\devices.py',
        r'SDK_dataset\aiohue\v2\controllers\events.py',
        r'SDK_dataset\aiohue\v2\controllers\lights.py',
        r'SDK_dataset\aiohue\v2\controllers\__init__.py',
        r'SDK_dataset\aiohue\v2\models\behavior_instance.py',
        r'SDK_dataset\aiohue\v2\models\behavior_script.py',
        r'SDK_dataset\aiohue\v2\models\bridge.py',
        r'SDK_dataset\aiohue\v2\models\bridge_home.py',
        r'SDK_dataset\aiohue\v2\models\button.py',
        r'SDK_dataset\aiohue\v2\models\camera_motion.py',
        r'SDK_dataset\aiohue\v2\models\contact.py',
        r'SDK_dataset\aiohue\v2\models\device.py',
        r'SDK_dataset\aiohue\v2\models\device_power.py',
        r'SDK_dataset\aiohue\v2\models\entertainment.py',
        r'SDK_dataset\aiohue\v2\models\entertainment_configuration.py',
        r'SDK_dataset\aiohue\v2\models\feature.py',
        r'SDK_dataset\aiohue\v2\models\geofence_client.py',
        r'SDK_dataset\aiohue\v2\models\grouped_light.py',
        r'SDK_dataset\aiohue\v2\models\homekit.py',
        r'SDK_dataset\aiohue\v2\models\light.py',
        r'SDK_dataset\aiohue\v2\models\light_level.py',
        r'SDK_dataset\aiohue\v2\models\matter.py',
        r'SDK_dataset\aiohue\v2\models\matter_fabric.py',
        r'SDK_dataset\aiohue\v2\models\motion.py',
        r'SDK_dataset\aiohue\v2\models\relative_rotary.py',
        r'SDK_dataset\aiohue\v2\models\resource.py',
        r'SDK_dataset\aiohue\v2\models\smart_scene.py',
        r'SDK_dataset\aiohue\v2\models\tamper.py',
        r'SDK_dataset\aiohue\v2\models\temperature.py',
        r'SDK_dataset\aiohue\v2\models\zgp_connectivity.py',
        r'SDK_dataset\aiohue\v2\models\zigbee_connectivity.py',
        r'SDK_dataset\aiohue\v2\models\zone.py',
        r'SDK_dataset\aiohue\v2\models\__init__.py',
        ]
    with open('RQ1-2\\DECG_results\\aiohue.txt', 'w') as file:
        file.write(str(run_script(command).stdout))


    #20.pydeconz
    command = [r'SDK_dataset\pydeconz\config.py',
        r'SDK_dataset\pydeconz\errors.py',
        r'SDK_dataset\pydeconz\gateway.py',
        r'SDK_dataset\pydeconz\websocket.py',
        r'SDK_dataset\pydeconz\__init__.py',
        r'SDK_dataset\pydeconz\__main__.py',
        r'SDK_dataset\pydeconz\interfaces\api_handlers.py',
        r'SDK_dataset\pydeconz\interfaces\events.py',
        r'SDK_dataset\pydeconz\interfaces\lights.py',
        r'SDK_dataset\pydeconz\interfaces\__init__.py',
        r'SDK_dataset\pydeconz\models\alarm_system.py',
        r'SDK_dataset\pydeconz\models\api.py',
        r'SDK_dataset\pydeconz\models\deconz_device.py',
        r'SDK_dataset\pydeconz\models\event.py',
        r'SDK_dataset\pydeconz\models\group.py',
        r'SDK_dataset\pydeconz\models\scene.py',
        r'SDK_dataset\pydeconz\models\__init__.py',
        r'SDK_dataset\pydeconz\models\light\configuration_tool.py',
        r'SDK_dataset\pydeconz\models\light\cover.py',
        r'SDK_dataset\pydeconz\models\light\light.py',
        r'SDK_dataset\pydeconz\models\light\lock.py',
        r'SDK_dataset\pydeconz\models\light\range_extender.py',
        r'SDK_dataset\pydeconz\models\light\siren.py',
        r'SDK_dataset\pydeconz\models\light\__init__.py',
        ]
    with open('RQ1-2\\DECG_results\\pydeconz.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #21.pyfritzhome
    command = [r'SDK_dataset\pyfritzhome\fritzhome.py',]   
    with open('RQ1-2\\DECG_results\\pyfritzhome.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #22.pyecobee
    command = [r'SDK_dataset\pyecobee\const.py',
        r'SDK_dataset\pyecobee\errors.py', 
        r'SDK_dataset\pyecobee\util.py',
        r'SDK_dataset\pyecobee\__init__.py']
    with open('RQ1-2\\DECG_results\\pyecobee.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #23.env_canada
    command = [r'SDK_dataset\env_canada\constants.py',
        r'SDK_dataset\env_canada\ec_aqhi.py', 
        r'SDK_dataset\env_canada\__init__.py',]
    with open('RQ1-2\\DECG_results\\env_canada.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #24.pyvera
    command = [r'SDK_dataset\pyvera\__init__.py',]   
    with open('RQ1-2\\DECG_results\\pyvera.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #25.reolink_aio
    command = [r'SDK_dataset\reolink_aio\api.py',
        r'SDK_dataset\reolink_aio\enums.py', 
        r'SDK_dataset\reolink_aio\exceptions.py',
        r'SDK_dataset\reolink_aio\software_version.py',
        r'SDK_dataset\reolink_aio\templates.py',
        r'SDK_dataset\reolink_aio\typings.py',
        r'SDK_dataset\reolink_aio\utils.py',
        r'SDK_dataset\reolink_aio\__init__.py',
        ]
    with open('RQ1-2\\DECG_results\\reolink_aio.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #26.pyoverkiz
    command = [r'SDK_dataset\pyoverkiz\client.py',
        r'SDK_dataset\pyoverkiz\const.py',
        r'SDK_dataset\pyoverkiz\obfuscate.py',
        r'SDK_dataset\pyoverkiz\types.py',
        r'SDK_dataset\pyoverkiz\utils.py',
        r'SDK_dataset\pyoverkiz\__init__.py',
        r'SDK_dataset\pyoverkiz\enums\command.py',
        r'SDK_dataset\pyoverkiz\enums\execution.py',
        r'SDK_dataset\pyoverkiz\enums\gateway.py',
        r'SDK_dataset\pyoverkiz\enums\general.py',
        r'SDK_dataset\pyoverkiz\enums\measured_value_type.py',
        r'SDK_dataset\pyoverkiz\enums\protocol.py',
        r'SDK_dataset\pyoverkiz\enums\server.py',
        r'SDK_dataset\pyoverkiz\enums\state.py',
        r'SDK_dataset\pyoverkiz\enums\ui.py',
        r'SDK_dataset\pyoverkiz\enums\__init__.py',
        ]
    with open('RQ1-2\\DECG_results\\pyoverkiz.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #27.rflink
    command = [r'SDK_dataset\rflink\parser.py',
        r'SDK_dataset\rflink\protocol.py', 
        r'SDK_dataset\rflink\__init__.py',
        r'SDK_dataset\rflink\__main__.py']
    with open('RQ1-2\\DECG_results\\rflink.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #28.decora_wifi
    command = [r'SDK_dataset\decora_wifi\base_model.py',
        r'SDK_dataset\decora_wifi\__init__.py', 
        r'SDK_dataset\decora_wifi\models\iot_switch.py',
        r'SDK_dataset\decora_wifi\models\__init__.py']
    with open('RQ1-2\\DECG_results\\decora_wifi.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #29.aioshelly
    command = [r'SDK_dataset\aioshelly\const.py',
        r'SDK_dataset\aioshelly\exceptions.py', 
        r'SDK_dataset\aioshelly\json.py',
        r'SDK_dataset\aioshelly\__init__.py',
        r'SDK_dataset\aioshelly\block_device\device.py',
        r'SDK_dataset\aioshelly\block_device\__init__.py']
    with open('RQ1-2\\DECG_results\\aioshelly.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #30.homeconnect
    command = [r'SDK_dataset\homeconnect\api.py',
        r'SDK_dataset\homeconnect\sseclient.py', 
        r'SDK_dataset\homeconnect\__init__.py',]
    with open('RQ1-2\\DECG_results\\homeconnect.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #31.pyeconet
    command = [r'SDK_dataset\pyeconet\api.py',
        r'SDK_dataset\pyeconet\__init__.py', 
        r'SDK_dataset\pyeconet\equipment\thermostat.py',
        r'SDK_dataset\pyeconet\equipment\__init__.py']
    with open('RQ1-2\\DECG_results\\pyeconet.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #32.pyisy
    command = [r'SDK_dataset\pyisy\connection.py',
        r'SDK_dataset\pyisy\constants.py', 
        r'SDK_dataset\pyisy\__main__.py',
        r'SDK_dataset\pyisy\nodes\group.py',
        r'SDK_dataset\pyisy\nodes\node.py',
        r'SDK_dataset\pyisy\nodes\nodebase.py']
    with open('RQ1-2\\DECG_results\\pyisy.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #33.yalexs
    command = [r'SDK_dataset\yalexs\activity.py',
        r'SDK_dataset\yalexs\api.py']
    with open('RQ1-2\\DECG_results\\yalexs.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #34.elgato
    command = [r'SDK_dataset\elgato\elgato.py']
    with open('RQ1-2\\DECG_results\\elgato.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #35.motioneye_client
    command = [r'SDK_dataset\motioneye_client\client.py',
        r'SDK_dataset\motioneye_client\const.py', 
        r'SDK_dataset\motioneye_client\utils.py',
        r'SDK_dataset\motioneye_client\__init__.py']
    with open('RQ1-2\\DECG_results\\motioneye_client.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #36.apyhiveapi
    command = [r'SDK_dataset\apyhiveapi\hive.py',
        r'SDK_dataset\apyhiveapi\light.py', 
        r'SDK_dataset\apyhiveapi\api\hive_api.py']
    with open('RQ1-2\\DECG_results\\apyhiveapi.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #37.pyatmo
    command = [r'SDK_dataset\pyatmo\auth.py',
        r'SDK_dataset\pyatmo\const.py', 
        r'SDK_dataset\pyatmo\event.py',
        r'SDK_dataset\pyatmo\helpers.py',
        r'SDK_dataset\pyatmo\home.py',
        r'SDK_dataset\pyatmo\schedule.py',
        r'SDK_dataset\pyatmo\__init__.py']
    with open('RQ1-2\\DECG_results\\pyatmo.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #38.pydroid_ipcam
    command = [r'SDK_dataset\pydroid_ipcam\exceptions.py',
        r'SDK_dataset\pydroid_ipcam\__init__.py']
    with open('RQ1-2\\DECG_results\\pydroid_ipcam.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #39.haphilipsjs
    command = [r'SDK_dataset\haphilipsjs\__init__.py']
    with open('RQ1-2\\DECG_results\\haphilipsjs.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #40.onvif
    command = [r'SDK_dataset\onvif\client.py',
        r'SDK_dataset\onvif\const.py', 
        r'SDK_dataset\onvif\definition.py',
        r'SDK_dataset\onvif\exceptions.py',
        r'SDK_dataset\onvif\managers.py',
        r'SDK_dataset\onvif\settings.py',
        r'SDK_dataset\onvif\transport.py',
        r'SDK_dataset\onvif\types.py',
        r'SDK_dataset\onvif\util.py',
        r'SDK_dataset\onvif\wrappers.py',
        r'SDK_dataset\onvif\wsa.py',
        r'SDK_dataset\onvif\__init__.py',
        r'SDK_dataset\onvif\wsdl\__init__.py',
        ]
    with open('RQ1-2\\DECG_results\\onvif.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #41.pymystrom
    command = [r'SDK_dataset\pymystrom\bulb.py',
        r'SDK_dataset\pymystrom\__init__.py']
    with open('RQ1-2\\DECG_results\\pymystrom.txt', 'w') as file:
        file.write(str(run_script(command).stdout))


    #42.aiolifx
    command = [r'SDK_dataset\aiolifx\aiolifx.py']
    with open('RQ1-2\\DECG_results\\aiolifx.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #43.tellduslive
    command = [r'SDK_dataset\tellduslive\tellduslive.py']
    with open('RQ1-2\\DECG_results\\tellduslive.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #44.pysensibo
    command = [r'SDK_dataset\pysensibo\exceptions.py',
        r'SDK_dataset\pysensibo\model.py', 
        r'SDK_dataset\pysensibo\__init__.py']
    with open('RQ1-2\\DECG_results\\pysensibo.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

    #45.ttls
    command = [r'SDK_dataset\ttls\client.py']
    with open('RQ1-2\\DECG_results\\ttls.txt', 'w') as file:
        file.write(str(run_script(command).stdout))

