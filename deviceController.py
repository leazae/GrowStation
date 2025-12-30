import serial
import json
import time

class PlantHabitatController:
    def __init__(self, port: str, baud: int):
        self.serialCommunication = serial.Serial(port, baud, timeout=5)
        # chwila na wystartowanie
        time.sleep(2)

    # -------------------
    # Pomocnicze metody szeregowe
    # -------------------
    def sendCommand(self, cmd: str) -> None:
        self.serialCommunication.write((cmd + "\n").encode())

    def readLine(self) -> str | None:
        line = self.serialCommunication.readline().decode(errors="ignore").strip()
        return line if line else None

    # -------------------
    #  Odczyty z czujników
    # -------------------
    def readAirTemperature(self) -> float | None:
        self.sendCommand("read air temperature")
        line = self.readLine()
        return float(line) if line else None

    def readAirHumidity(self) -> float | None:
        self.sendCommand("read air humidity")
        line = self.readLine()
        return float(line) if line else None

    def readSoilTemperature(self) -> float | None:
        self.sendCommand("read soil temperature")
        line = self.readLine()
        return float(line) if line else None

    def readAll(self) -> dict | None:
        self.sendCommand("import read all")
        line = self.readLine()
        if line:
            data = json.loads(line)
            return data
        return None

    # -------------------
    # Fan control / Sterowanie wentylatorem
    # -------------------
    def fanOn(self) -> None:
        self.sendCommand("fan on")

    def fanOff(self) -> None:
        self.sendCommand("fan off")

    # -------------------
    # Heatmat control / Sterowanie matą grzewczą
    # -------------------
    def heatmatOn(self) -> None:
        self.sendCommand("heatmat on")

    def heatmatOff(self) -> None:
        self.sendCommand("heatmat off")


