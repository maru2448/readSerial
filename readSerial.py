import serial
import time
import numpy as np
import textwrap as tw


#-----Get data from sensors-----
class read_sensors:
    
    #-----initialize sensors-----
    def __init__(self):
        
        self.save_data = []
        self.TOTAL_SENSOR_NUM = 8
        
        
        #-----Set serial port-----
        platform = input('mac or windows? m/w:')
        if platform == 'm':
            Port = '/dev/tty.usbserial-AK08NMKG'
        elif platform == 'w':
            Port = 'COM3'
            
        BaudRate = 115200
        Timeout = 1
        self.ser = serial.Serial(Port, BaudRate, timeout=Timeout)
        self.serialFlush()
        
        #-----Command to start initial settings-----
        command = 'r'
        self.ser.write(command.encode())
        received = self.ser.readline()
        #print(received)
        
        #-----Number of Sensors-----
        command = f'0{self.TOTAL_SENSOR_NUM}'
        #print(command)
        #command = '08'
        self.ser.write(command.encode())
        received = self.ser.readline()
        #print(received)
        
        #-----Sensor ID-----
        for x in range(0,self.TOTAL_SENSOR_NUM):
            command = '0%d' % (x+1)
            self.ser.write(command.encode())
            time.sleep(0.1)
            received = self.ser.readline()
            print(received)
            received = self.ser.readline()
            print(received)
            #if received.decode() == 
   
    #-----Get sensor data-----
    def get_data(self):
    
        # raw_sensor_data = []
        # decoded_rawdata = []
        
        raw_sensor_data = self.ser.readline()
        decoded_rawdata = str(raw_sensor_data.decode())
        #print(decoded_rawdata)
        
        self.save_data.append(decoded_rawdata)        
        converted_data = self.convert_data(decoded_rawdata)

        return converted_data
    
    def continous_data(self):
        #-----stop aquation of data-----
        command = 'l'
        self.ser.write(command.encode())
        
    #-----close srial-----        
    def close_serial(self):
        
        self.ser.close() 
    
    #-----Flush input-----    
    def serialFlush(self, output = True):
        if output==True:
            self.ser.flushOutput()
        elif output==False:
            self.ser.flushInput()
        else:
            self.ser.flush()
        
    #-----Convert hex data to real number-----    
    def convert_data(self, sensorData):
        
        split_data = tw.wrap(sensorData, 4)
        converted_data = np.zeros(len(split_data))
        
        for y in range(len(split_data)-1):
            converted_data[y+1] = int(split_data[y+1], 16)
            
        converted_data[0] = int(split_data[0]) 
        
        return converted_data
        
    #-----transform data------
    def data_transformer(self, sensorData):
        
        data = sensorData[8:]
        transformed_data = np.zeros([len(data),5])
        
        for x in range(len(data)):
            split_data = tw.wrap(data[x], 4)
            
            for y in range(5):
                transformed_data[x,y] = int(split_data[y], 16)
        
        k = 1                
        for i in range(len(data)):
            transformed_data[i][0] = k
            k = k + 1
            
            if k == 9:
                k = 1
            else:
                pass
           
        return transformed_data


# if __name__ == '__main__':
#     sensor_data = read_sensors()
#     sensor_data.get_data()
#     sensor_data.close_serial()
