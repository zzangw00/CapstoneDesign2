import sys
import wiringPi as w


class SoilMoisture:

    def __init__(self):
        self.CS_MCP3208 = 8
        self.SPI_CHANNEL = 0
        self.SPI_SPEED = 1000000
        self.LED_PIN = 4
        self.BUZZER_PIN = 17
        self.MOISTURE_LEVEL = 300

    def setupWiringPiGpio(self):
        if w.wiringPiSetupGpio() == -1:
            print("[ERROR] Error in setupWiringPiGpio")
            sys.exit(1)

    def ReadMcp3208ADC(self, adcChannel):

        buff = [0] * 3
        nAdcValue = 0

        buff[0] = 0x06 | ((adcChannel & 0x07) >> 2)
        buff[1] = ((adcChannel & 0x07) << 6)
        buff[2] = 0x00
    

        w.digitalWrite(self.CS_MCP3208, 0)
        w.wiringPiSPIDataRW(self.SPI_CHANNEL, buff, 3)

        buff[1] = 0x0F & buff[1]
        nAdcValue = (buff[1] << 8) | buff[2]

        w.digitalWrite(self.CS_MCP3208, 1)

        return nAdcValue

    def playBuzzer(self, status):

        if status == 1:
            w.digitalWrite(self.BUZZER_PIN, 1)
            w.delay(10)
            w.digitalWrite(self.BUZZER_PIN, 0)
            w.delay(10)

    def turnOnLED(self, status):

        if status == 1:
            w.digitalWrite(self.LED_PIN, 1)
            w.delay(500)
            w.digitalWrite(self.LED_PIN, 0)
            w.delay(500)

    def getSensorData(self):

        nAdcChannel = 0
        nAdcValue = 0

        if w.wiringPiSPISetup(self.SPI_CHANNEL, self.SPI_SPEED) == -1:
            print("[ERROR] Error in wiringPiSPISetup")
            sys.exit(1)

        w.pinMode(self.CS_MCP3208, 1) //output

        w.pinMode(self.LED_PIN, 1)
        w.digitalWrite(self.LED_PIN, 0)

        w.pinMode(self.BUZZER_PIN, 1)
        w.digitalWrite(self.BUZZER_PIN, 0)

        nAdcValue = self.ReadMcp3208ADC(nAdcChannel)
        print("Soil Moisture Sensor Value = %u"%(nAdcValue))

        if nAdcValue < self.MOISTURE_LEVEL:
            self.playBuzzer(1)
            self.turnOnLED(1)
        else:
            self.playBuzzer(0)
            self.turnOnLED(0)

        return nAdcValue