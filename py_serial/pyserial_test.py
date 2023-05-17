import serial, platform, sys, threading
import time

class SerialCommunication():
    def __init__(self, port = None, baudrate = None):
        if port == None:
            if platform.system() == 'Windows':
                self.port = 'COM0'
            elif platform.system() == 'Linux':
                self.port = '/dev/ttyUSB0' 
        else:
            self.port = port
        
        if baudrate == None:
            self.baudrate = 115200
        else:
            self.baudrate = baudrate
        
        self.serial_com = serial.Serial(self.port, self.baudrate, timeout=1)
    
    def serial_write(self, message):
        self.serial_com.write(message.encode('utf-8'))

    def serial_readline(self):
        read_value = self.serial_com.readline()
        return read_value.decode('utf-8')

def parse_args():
    port, baudrate = None, None
    if len(sys.argv) == 2:
        port, baudrate = sys.argv[0], sys.argv[1]
    elif len(sys.argv) == 1:
        port = sys.argv[0]
    return (port, baudrate)

def serial_constant_reading(serial_con):
        while True:
            serial_data = serial_con.serial_readline()
            if serial_data != '':
                print("Reviced ->", serial_data)

def serial_constant_writing(serial_con):
    while True:
        serial_con.serial_write('Sent -> Serial test communication')
        time.sleep(2)

def main():
    port, baudrate = parse_args()

    serial_communication = SerialCommunication(port, baudrate)

    reading_thread = threading.Thread(target=serial_constant_reading, args=(serial_communication,))
    writing_thread = threading.Thread(target=serial_constant_writing, args=(serial_communication,))

    reading_thread.start()
    writing_thread.start()

    reading_thread.join()
    writing_thread.join()
    exit(0)

if __name__ == '__main__':
    main()