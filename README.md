# GrowBox – Intelligent Plant Habitat Controller

GrowBox is a modular Python project designed to automate plant care using sensors and actuators. It evaluates environmental conditions and reacts in real-time to maintain optimal growth parameters.

---

## Features

- **Sensor Integration**: Reads air temperature, air humidity, and soil temperature from your connected PlantHabitatController.
- **Automatic Device Control**: Controls fans and heating mats according to plant-specific optimal conditions.
- **Configurable Plants**: Easily add new plants via JSON configuration files specifying optimal temperature and humidity ranges.
- **Safe Operation**: Implements `try-except` handling to avoid crashes if sensors fail or return invalid data.
- **Scalable Architecture**: Designed for expansion — you can add more devices or sensors with minimal code changes.
- **Continuous Monitoring**: Supports looping execution or scheduling for constant environment monitoring.

---

## Supported Plants

- **Silene capensis** – mild psychoactive “African Dream Root”
- **Tomato** – example edible plant
- Custom plants can be added by creating JSON configuration files under `plants/`.

---

## JSON Plant Configuration Example

```json
{
  "nameLatin": "Silene Capensis",
  "nameEn": "African Dream Root",
  "namePl": "Korzeń Afrykański",
  "optimalConditions": {
      "airTemperature": {"min": 18, "max": 25},
      "soilTemperature": {"min": 20, "max": 26},
      "airHumidity": {"min": 60, "max": 80}
  }
}

GrowBox/
│
├── GrowBox.py            # Main loop & controller execution
├── deviceController.py   # Handles sensors and actuators
├── habitat.py            # Evaluates conditions and controls devices
├── habitatConditions.py  # Plant-specific condition definitions
└── plants/               # JSON files for individual plant configurations
