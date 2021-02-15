"""Sensor for monitoring the size of a file."""
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import TEMP_CELSIUS
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.reload import setup_reload_service

from .digienergy import DigiEnergy

ICON = "mdi:mdi-thermometer"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required("url"): vol.Url(),
        "username": str,
        "password": str,
        vol.Required("sensors"): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Required("name"): str,
                    vol.Required("sensor"): str,
                }
            ],
        ),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the file size sensor."""

    url = config.get("url")
    username = config.get("username")
    password = config.get("password")

    digi = DigiEnergy(url, username, password)

    sensors = []
    for s in config.get("sensors"):
        sensors.append(DigiEnergySensor(digi, s.get("name"), s.get("sensor")))

    if sensors:
        add_entities(sensors, True)


class DigiEnergySensor(Entity):
    def __init__(self, digi, name, sensor):
        """Initialize the data object."""
        self._digi = digi
        self._name = name
        self._sensor = sensor

        self.value = 0

    def update(self):
        """Update the sensor."""
        self.value = self._digi.get_sensor_value([self._sensor])[0]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the size of the file in MB."""
        return self.value

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return TEMP_CELSIUS