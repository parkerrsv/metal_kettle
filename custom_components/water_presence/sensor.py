# Sensor platform for water presence detection

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.restore_state import RestoreEntity
from .const import DOMAIN

TEMPERATURE_ENTITY = "sensor.smart_kettle_current_temperature"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([WaterPresenceSensor(hass)], True)

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([WaterPresenceSensor(hass)], True)

class WaterPresenceSensor(SensorEntity, RestoreEntity):
    _attr_name = "Water Presence"
    _attr_unique_id = "water_presence_sensor"
    _attr_unit_of_measurement = None

    def __init__(self, hass):
        self.hass = hass
        self._state = None
        self._history = []  # Store tuples of (temp, time)

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        async_track_state_change_event(self.hass, [TEMPERATURE_ENTITY], self._async_state_changed)
        # Restore previous state if available
        old_state = await self.async_get_last_state()
        if old_state:
            self._state = old_state.state

    async def _async_state_changed(self, event):
        temp = self.hass.states.get(TEMPERATURE_ENTITY)
        if temp:
            try:
                temp_val = float(temp.state)
            except ValueError:
                temp_val = None
            self._history.append((temp_val, event.time_fired))
            # Keep only the last 10 records
            self._history = self._history[-10:]
            self._state = self._analyze_history()
            self.async_write_ha_state()

    def _analyze_history(self):
        # If temperature is above 40°C, assume water is present
        for temp, _ in reversed(self._history):
            if temp is not None and temp > 40:
                return "full"
        return "empty"
