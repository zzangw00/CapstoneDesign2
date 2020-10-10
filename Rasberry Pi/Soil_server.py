import sys
from socket import *
from SoilMoisture import SoilMoisture


def main():

    print("[DEBUG] Connect Server Start")

    SERVER_ADDR = '192.168.0.101'
    PORT = 2222
    BUFSIZE = 1024

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((SERVER_ADDR, PORT))
    server.listen(0)

    client, client_addr = server.accept()
    print("[DEBUG] Connected IP : {}".format(client_addr))

    soil = SoilMoisture()

    while True:
        server_recv = client.recv(BUFSIZE)

        if server_recv == -1:
            print("[DEBUG] Exit")
            break;

        getData = soil.getSensorData()
        getData_lsb = (getData & 0xff)
        getData_msb ((getData >> 8) & 0xff)

        send_buff = [0] * 5
        send_buff[0] = 0x01
        send_buff[1] = 0x00
        send_buff[2] = getData_lsb
        send_buff[3] = getData_msb
        send_buff[4] = 0x05

        client.send(send_buff)

    print("END")


if __name__ == "__main__":
    main()