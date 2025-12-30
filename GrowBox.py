import time
from deviceController import PlantHabitatController
from habitatConditions import HabitatConditions
from habitat import Habitat  # twoja klasa Habitat

# Wczytanie konfiguracji dla rośliny
logicHandler = HabitatConditions('plants/africanDreamRoot.json')
deviceHandler = PlantHabitatController("/dev/ttyUSB0", 9600)

# Stworzenie instancji habitat
habitat = Habitat(deviceHandler, logicHandler)

# --- Pętla główna ---
try:
    while True:
        habitat.runCycle()       # pojedynczy cykl odczytu i sterowania
        habitat.showStatus()     # wypisz aktualny stan
        time.sleep(60)           
except KeyboardInterrupt:
    print("Zatrzymano ręcznie")
    if habitat.isFanOn:
        deviceHandler.fanOff()
    if habitat.isHeatmatOn:
        deviceHandler.heatmatOff()
