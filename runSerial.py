
import readSerial as rd
import numpy as np
import pandas as pd
import time
import keyboard as key


#----run application app-----
class runApp:
    
    def __init__(self):
        self.read = rd.read_sensors()
        self.time_rate = 1
        self.read.save_data
        
    #-----read data from serial----- 
    def read_data(self, sensors):
        
        self.sensorNo = int(sensors)          #number of sensors
        
        self.data_sensor = [[[], [], [], []], #sensor01
                            [[], [], [], []], #sensor02
                            [[], [], [], []], #sensor03
                            [[], [], [], []], #sensor04
                            [[], [], [], []], #sensor05
                            [[], [], [], []], #sensor06
                            [[], [], [], []], #sensor07
                            [[], [], [], []]] #sensor08
        
        self.seconds = [] #save time in seconds

    def start_read(self):
        self.continue_data()    
            
        c_time = time.time()    #set time
        
        #-----loop data-----
        while True: 
            #-----read data-----
            for sensor in range(0,self.sensorNo):
                sensorData = self.read.get_data()
                # print('input:',sensorData)
                
                for ch in range(0,4):
                    self.data_sensor[sensor][ch] = sensorData[ch+1]
                
            self.seconds = time.time()-c_time
            print(f'Time: {self.seconds} \n01:{self.data_sensor[0]}\n02:{self.data_sensor[1]}\n03:{self.data_sensor[2]}\n04:{self.data_sensor[3]}\n05:{self.data_sensor[4]}\n06:{self.data_sensor[5]}\n07:{self.data_sensor[6]}\n08:{self.data_sensor[7]}')
            
            #----Add key 'w' as stop button-----
            if key.is_pressed('w'):
                print('Stop reading data')
                break
        
        
        self.continue_data()
        #self.read.close_serial()
        print('==========================================================================================')    
           
    
    #-----get continous data-----
    def continue_data(self):
        self.read.continous_data()  
        
    def end_serial(self):
        self.read.close_serial()
    

        
#-----run application-----        
if __name__ == '__main__':
    print('\n')
    print('============Application Start===============================================================')
    time.sleep(0.5)
    instruction = '''
    ——————————————————————————————
    Instruction 
    ——————————————————————————————
    1) Press "q" to start
    2) Press "w" to stop
    3) Press "r" to reset
    4) Press "s" to save data to csv file
    5) Press "x" to end application
    
    {Press "q" to start}
        
==========================================================================================
    '''

    
    #-----initialize app-----
    run = runApp()
    run.read_data(8)
    print(instruction)
    
    while True:
        if key.is_pressed('q'):
            run.start_read()
            print(instruction)
            
        if key.is_pressed('s'):
            run.save_data()
            
        if key.is_pressed('x'):
            print('End Application')
            break
        
        if key.is_pressed('r'):
            print('Resetting...')
            run.read_data(8)
            time.sleep(2)
            print(instruction)
    
    