from deviceController import PlantHabitatController
from habitatConditions import HabitatConditions, ConditionStatus

class Habitat:
    def __init__(self, deviceController: PlantHabitatController, logicHandler: HabitatConditions):
        self.deviceController = deviceController
        self.logicHandler = logicHandler

        self.isFanOn = False
        self.isHeatmatOn = False
        self.shouldFanBeOn = False
        self.shouldHeatmatBeOn = False

        self.currentAirTemperature = None
        self.currentAirHumidity = None
        self.currentSoilTemperature = None
        self.evaluation = {}

    def getCurrentConditions(self):
        try:
            data = self.deviceController.readAll()
            if not data:
                return

            self.currentAirTemperature = data.get('airTemperature')
            self.currentAirHumidity = data.get('airHumidity')
            self.currentSoilTemperature = data.get('soilTemperature')
        except Exception:
            self.currentAirTemperature = None
            self.currentAirHumidity = None
            self.currentSoilTemperature = None

    def evaluateConditions(self):
        try:
            if self.currentAirTemperature is not None and \
               self.currentAirHumidity is not None and \
               self.currentSoilTemperature is not None:
                self.evaluation = self.logicHandler.checkAllConditions(
                    self.currentAirTemperature,
                    self.currentAirHumidity,
                    self.currentSoilTemperature
                )
            else:
                self.evaluation = {}
        except Exception:
            self.evaluation = {}

    def evaluateActions(self):
        self.shouldFanBeOn = (
            self.evaluation.get('airTemperature') == ConditionStatus.ABOVE_MAXIMUM or
            self.evaluation.get('airHumidity') == ConditionStatus.ABOVE_MAXIMUM or
            self.evaluation.get('soilTemperature') == ConditionStatus.ABOVE_MAXIMUM
        )
        self.shouldHeatmatBeOn = (
            self.evaluation.get('soilTemperature') == ConditionStatus.BELOW_MINIMUM
        )

    def actAccordingToConditions(self):
        if self.shouldFanBeOn and not self.isFanOn:
            self.deviceController.fanOn()
            self.isFanOn = True
        elif not self.shouldFanBeOn and self.isFanOn:
            self.deviceController.fanOff()
            self.isFanOn = False

        if self.shouldHeatmatBeOn and not self.isHeatmatOn:
            self.deviceController.heatmatOn()
            self.isHeatmatOn = True
        elif not self.shouldHeatmatBeOn and self.isHeatmatOn:
            self.deviceController.heatmatOff()
            self.isHeatmatOn = False

    def showStatus(self):
        print("========== CURRENT HABITAT STATUS ==========")
        print(f"Air Temperature : {self.currentAirTemperature if self.currentAirTemperature is not None else 'N/A'} °C")
        print(f"Air Humidity    : {self.currentAirHumidity if self.currentAirHumidity is not None else 'N/A'} %")
        print(f"Soil Temperature: {self.currentSoilTemperature if self.currentSoilTemperature is not None else 'N/A'} °C")
        print("-------------------------------------------")
        print(f"Fan  : {'ON' if self.isFanOn else 'OFF'}")
        print(f"Heatmat: {'ON' if self.isHeatmatOn else 'OFF'}")
        if self.evaluation:
            print("Evaluation:")
            for key, value in self.evaluation.items():
                print(f"  {key} : {value.name}")
        else:
            print("Evaluation: N/A")
        print("===========================================\n")

    def runCycle(self):
        self.getCurrentConditions()
        self.evaluateConditions()
        self.evaluateActions()
        self.actAccordingToConditions()
