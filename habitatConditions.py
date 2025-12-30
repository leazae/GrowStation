import json
from enum import Enum

class ConditionStatus(Enum):
    BELOW_MINIMUM = -1  # EN: Value below minimum / PL: Wartość poniżej minimum
    WITHIN_RANGE = 0    # EN: Value within optimal range / PL: Wartość w optymalnym zakresie
    ABOVE_MAXIMUM = 1   # EN: Value above maximum / PL: Wartość powyżej maksimum



class HabitatConditions:
    def __init__(self, jsonFile):
        try:
            with open(jsonFile, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {jsonFile}")

        self.latinName = data["nameLatin"]
        self.polishName = data["namePl"]
        self.englishName = data["nameEn"]

        optimalConditions = data["optimalConditions"]

        self.minAirTemp = optimalConditions["airTemperature"]["min"]
        self.maxAirTemp = optimalConditions["airTemperature"]["max"]

        self.minAirHumidity = optimalConditions["airHumidity"]["min"]
        self.maxAirHumidity = optimalConditions["airHumidity"]["max"]

        self.minSoilTemp = optimalConditions["soilTemperature"]["min"]
        self.maxSoilTemp = optimalConditions["soilTemperature"]["max"]

    def showInfo(self):
        # POKAZ INFO
        print("========================================")
        print("PLANT / ROŚLINA – HABITAT CONDITIONS")
        print("========================================")

        print(f"Latin name    : {self.latinName}")
        print(f"Polish name   : {self.polishName}")
        print(f"English name  : {self.englishName}")

        print("----------------------------------------")
        print("OPTIMAL ENVIRONMENTAL CONDITIONS")
        print("----------------------------------------")

        print(f"Air temperature    : {self.minAirTemp} °C  –  {self.maxAirTemp} °C")
        print(f"Air humidity       : {self.minAirHumidity} %  –  {self.maxAirHumidity} %")
        print(f"Soil temperature   : {self.minSoilTemp} °C  –  {self.maxSoilTemp} °C")
        print("========================================")

    def checkAirTemperature(self, temperature: float):
        if temperature < self.minAirTemp:
            return ConditionStatus.BELOW_MINIMUM
        elif temperature > self.maxAirTemp:
            return ConditionStatus.ABOVE_MAXIMUM
        else:
            return ConditionStatus.WITHIN_RANGE

    def checkSoilTemperature(self, temperature: float):
        if temperature < self.minSoilTemp:
            return ConditionStatus.BELOW_MINIMUM
        elif temperature > self.maxSoilTemp:
            return ConditionStatus.ABOVE_MAXIMUM
        else:
            return ConditionStatus.WITHIN_RANGE
    
    def checkAirHumidity(self, humidity: float):
        if humidity < self.minAirHumidity:
            return ConditionStatus.BELOW_MINIMUM
        elif humidity > self.maxAirHumidity:
            return ConditionStatus.ABOVE_MAXIMUM
        else:
            return ConditionStatus.WITHIN_RANGE
    

    def checkAllConditions(self, airTemperature, airHumidity, soilTemperature):
        return{
            "airTemperature": self.checkAirTemperature(airTemperature),
            "airHumidity": self.checkAirHumidity(airHumidity),
            "soilTemperature": self.checkSoilTemperature(soilTemperature)
        }


