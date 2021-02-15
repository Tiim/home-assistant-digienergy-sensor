# DigiEnergy Sensor

## Usage

* Copy `custom_components/digienergy_sensor` to your config folder
* Add the following config

```yaml
sensor:
  - platform: digienergy_sensor
    url: http://mydigienergy.website.ch:8080 # ip address works too
    username: MyUsername
    password: MyPassword
    sensors:
      - name: "Sensor"
        # sensorcode can be seen under /config -> Temp. PT1000 -> hover over the temperature values
        sensor: "##000[10]" 
        # multiple sensors can be selected
      - name: "test2"
        sensor: "##000[17]"
    # multiple systems at the same time
  - platform: digienergy_sensor
    url: http://192.168.178.10
    sensors:
      - name: "test_no_login"
        sensor: "##000[24]"

```