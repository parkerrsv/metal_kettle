# Water Presence Detection

A Home Assistant custom integration to detect water presence using historical temperature data.

## Features
- Analyzes recent temperature readings to infer water presence
- Exposes a sensor entity in Home Assistant (`sensor.water_presence_sensor`)
- HACS compatible

## Algorithm (Advanced)
This integration determines if water is present in the kettle by analyzing the temperature sensor (`sensor.smart_kettle_current_temperature`) over time. The algorithm uses a short history of recent temperature readings and applies the following logic:

1. **Temperature Threshold:**
   - If the temperature is above 40°C at any point in the recent history, it is likely that water is present and has been heated.
2. **Temperature Stability:**
   - If the temperature remains stable (within ±2°C) for several consecutive readings and is below the threshold, it may indicate the kettle is empty or cooling down without water.
3. **Temperature Rise Detection:**
   - If a rapid temperature increase (e.g., >10°C within 1 minute) is detected, it suggests the kettle is heating water. If the temperature rises quickly but then plateaus at a low value, it may indicate the kettle is empty and heating the element.
4. **Cooling Pattern:**
   - If the temperature drops slowly after heating, it suggests water is present (water cools slower than an empty kettle). A rapid drop may indicate no water.
5. **Recent Activity:**
   - The algorithm considers only the last 10 readings (or a configurable window) to make the decision more responsive to recent changes.

**Decision Logic:**
- If a recent rapid temperature rise is followed by a plateau above 40°C, report `full`.
- If the temperature is stable and low, or if a rapid rise is followed by a plateau below 40°C, report `empty`.
- If the pattern is ambiguous, the sensor may report `unknown` or the last known state.

This approach is more robust than a simple threshold and can adapt to different kettle behaviors and environments.

## Installation
1. Copy this folder to your Home Assistant `custom_components` directory, or install via HACS as a custom repository.
2. Restart Home Assistant.
3. Add the integration via the UI.

## Configuration
No configuration required yet. The temperature entity is set in the code (`sensor.smart_kettle_current_temperature`).

## Future Work
- **Configurable Threshold:** Allow the temperature threshold to be set via the UI or configuration.
- **Multiple Sensors:** Support for multiple temperature sensors or other water detection methods.
- **UI Options:** Add options flow for easy configuration in Home Assistant.
- **Advanced Algorithms:** Use machine learning or more advanced heuristics to improve detection accuracy.
- **Notifications:** Add built-in notifications or automations for when water is low or empty.
- **Localization:** Add translations for other languages.

## License
MIT
