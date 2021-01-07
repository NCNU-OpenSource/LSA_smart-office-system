import subprocess

subprocess.run("python access_control.py & python fan_manul.py & python rain.py & python temp_control_fan.py & python temp_control_fan_auto.py & python temp_mqtt.py & python temp_outdoor.py", shell=True)
