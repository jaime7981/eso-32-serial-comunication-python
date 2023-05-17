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
    if len(sys.argv) == 3:
        port, baudrate = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        port = sys.argv[1]
    return (port, baudrate)

def serial_constant_reading(serial_con, run_event):
        while run_event.is_set():
            serial_data = serial_con.serial_readline()
            if serial_data != '':
                print("Reviced ->", serial_data)

def serial_constant_writing(serial_con, run_event):
    while run_event.is_set():
        serial_con.serial_write('Sent -> Serial test communication')
        time.sleep(2)

def serial_cli_input_writing(serial_con, run_event):
    while run_event.is_set():
        try:
            user_input = input()
        except:
            user_input = 'Err:Intr'
        serial_con.serial_write(user_input)

def create_communication_threads(serial_communication):
    run_event = threading.Event()
    run_event.set()
    reading_thread = threading.Thread(target=serial_constant_reading, args=(serial_communication, run_event))
    writing_thread = threading.Thread(target=serial_cli_input_writing, args=(serial_communication, run_event))
    reading_thread.start()
    writing_thread.start()
    return (reading_thread, writing_thread, run_event)

def main():
    port, baudrate = parse_args()
    serial_communication = SerialCommunication(port, baudrate)
    reading_thread, writing_thread, run_event = create_communication_threads(serial_communication)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        run_event.clear()
        reading_thread.join()
        writing_thread.join()
        exit(0)
    finally:
        exit(1)

if __name__ == '__main__':
    main()