"""The digienergy component."""

DOMAIN = "digienergy_sensor"
PLATFORMS = ["sensor"]


def setup(hass, config):
    # Return boolean to indicate that initialization was successful.
    return True