import os
import csv
import json
import datetime

from time import sleep


class WriteSensorValue:

    def __init__(self):
        self.MOISTURE_SOCKET = None
        self.LIGHT_SOCKET = None
        self.WRITE_TIME = 60


    def startWriteValue(self):

        if self.MOISTURE_SOCKET == None or self.LIGHT_SOCKET == None:
            return

        timestamp = datetime.datetime.now()
        timestring = timestamp.strftime("%Y%m%d%H%M")

        SAVE_FILE_NAME = 'sensorValue_' + timestring + '.csv'
        SAVE_PATH = os.path.join('result', SAVE_FILE_NAME)

        with open(SAVE_PATH, "w", newline='') as fd:
            writer = csv.writer(fd)
            i = 0

            while True:
                sleep(1.0)
                i += 1

                self.MOISTURE_SOCKET.send(bytes([0x00, 0x00]))
                self.LIGHT_SOCKET.send(bytes([0x00, 0x00]))

                moisture_info = json.loads(self.MOISTURE_SOCKET.recv(1024))
                light_info = json.loads(self.LIGHT_SOCKET.recv(1024))

                writer.writerow([moisture_info['sensor_value'], light_info['sensor_value']])

                if i == self.WRITE_TIME:
                    break

        print("[INFO] Finish File writer.")

    def set_moisture_client(self, socket):
        self.MOISTURE_SOCKET = socket
        self.startWriteValue()

    def set_light_client(self, socket):
        self.LIGHT_SOCKET = socket
        self.startWriteValue()

    def set_write_time(self, t):
        self.WRITE_TIME = t

