down:
	rsync -av pi@garden:~/pro380-modbus-meter-mqtt-influx/ .

up:
	rsync -av ./ pi@garden:~/pro380-modbus-meter-mqtt-influx