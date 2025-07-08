from homeassistant import config_entries
from .const import DOMAIN

class WaterPresenceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Water Presence", data={})
        return self.async_show_form(step_id="user")
