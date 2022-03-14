import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import readSerial as rd
import tkinter as tk
import time
import keyboard as key
import sys


class run_serial:
    
    def __init__(self):
        self.read = rd.read_sensors()
        # self.data = np.zeros([8,4,100])
        
    def reset(self):
        self.read.serialFlush(False)
        self.data = np.zeros([8,4,100])
        
    def create_gui(self):
        self.root = tk.Tk()
        self.root.geometry('1020x930')
        self.root.title('Signal plot')
        self.plot_signals()
        self.read.serialFlush(False)
        self.root.after(1,self.read_sensor())
        
        self.root.mainloop()
        
    def read_sensor(self):
        self.data = np.zeros([8,4,100])
        self.final_data = pd.DataFrame([])
        self.sc = []
        c_time = time.time()    #set time
        
        #-----loop data-----
        while True:
            try:
                data_sensor = np.zeros([8,4])
                self.read.continous_data()
                #-----read data-----
                for sensor in range(0,8):
                    sensorData = self.read.get_data()
                    print('input:',sensorData)
                    
                    for ch in range(0,4):
                        data_sensor[sensor][ch] = int(sensorData[ch+1])
                
                self.read.continous_data()
                self.sc.append(time.time() - c_time)
                self.animate(data_sensor)
                self.root.update()
                
                df_data = pd.DataFrame(data_sensor.reshape(1,8*4))
                self.final_data = pd.concat([self.final_data, df_data], axis=0)
                #----Add key 'w' as stop button-----
                if key.is_pressed('p'):
                    while True:
                        if key.is_pressed('o'):
                            break

                if key.is_pressed('w'):
                    print('Stop reading data')
                    break

            except KeyboardInterrupt:
                self.read.continous_data()
                self.read.serialFlush(None)
            
            except:
                self.read.continous_data()
                self.read.serialFlush(None)
                break
            
        self.root.destroy()
        time.sleep(0.2)
        
    def plot_signals(self):
        self.fig, self.ax = plt.subplots(nrows=8, ncols=1 ,figsize=(5,10))
        self.plot_cvs1 = FigureCanvasTkAgg(self.fig, master=self.root)
        self.plot_cvs1.get_tk_widget().place(x=-30, y=-60, width=900, height=1010)
        self.plot_cvs1.draw()
        
        self.fig2 = plt.figure(2,figsize=(3,10))
        self.plot_cvs2 = FigureCanvasTkAgg(self.fig2, master=self.root)
        self.plot_cvs2.get_tk_widget().place(x=810, y=-60, width=210, height=1010)
        self.plot_cvs2.draw()
        
    def animate(self, data):
        self.data = np.roll(self.data, -1) 
        self.data[:,:,-1] = data
        self.bar_y = np.mean(data, axis=1).reshape(8)
        # self.fig.clear()
        self.sns = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
        for x in range(8):
            MAX = self.data[x,:,:].max()
            MIN = self.data[x,:,:].min()
            self.ax[x].cla()
            self.ax[x].set_ylim(MIN-20, MAX+20)
            self.ax[x].set_xlim(0,100)
            self.ax[x].set_ylabel(self.sns[x])
            for y in range(4):
                self.ax[x].plot(self.data[x,y,:], linewidth=0.5)
                
            self.ax[x].tick_params(axis='x', labelbottom=False, bottom=False)
        
        self.plot_cvs1.draw()
        
        self.fig2.clear()
        plt.xlim(0, 200)
        self.y_pos = np.arange(len(self.sns))
        plt.grid(linestyle='--')
        plt.barh(self.y_pos, self.bar_y, 0.7)
        plt.xlabel('Amplitude')
        plt.yticks(self.y_pos, self.sns)
        plt.gca().invert_yaxis()
        self.plot_cvs2.draw()
        
    def save_data(self):
        self.final_data.columns = ['S1ch1', 'S1ch2', 'S1ch3', 'S1ch4',
                                   'S2ch1', 'S2ch2', 'S2ch3', 'S2ch4',
                                   'S3ch1', 'S3ch2', 'S3ch3', 'S3ch4',
                                   'S4ch1', 'S4ch2', 'S4ch3', 'S4ch4',
                                   'S5ch1', 'S5ch2', 'S5ch3', 'S5ch4',
                                   'S6ch1', 'S6ch2', 'S6ch3', 'S6ch4',
                                   'S7ch1', 'S7ch2', 'S7ch3', 'S7ch4',
                                   'S8ch1', 'S8ch2', 'S8ch3', 'S8ch4']
        
        self.final_data.reset_index(drop=True)
        # df_sc = pd.DataFrame(np.array(self.sc).reshape(-1,1), columns=['time[s]']).reset_index(drop=True)
        # save_file = pd.concat([df_sc, self.final_data], axis=1)
        # print(save_file.shape)
        # # sys.exit()
        tm = time.strftime("%Y%m%d_%H;%M;%S", time.localtime())
        self.final_data.to_csv(tm + '_raw.csv') 
        
    
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
    2) Press "p" to pause
    3) Press "o" to play
    4) Press "w" to stop
    5) Press "r" to reset
    6) Press "s" to save data to csv file
    7) Press "x" to end application
    
    {Press "q" to start}
        
==========================================================================================
    '''

    
    #-----initialize app-----
    run = run_serial()
    print(instruction)
    
    while True:
            
        if key.is_pressed('q'):
            run.create_gui()
            print(instruction)
            
        if key.is_pressed('s'):
            print('Saving...')
            run.save_data()
            time.sleep(2)
            print(instruction)
            
        if key.is_pressed('x'):
            print('End Application')
            break
        
        if key.is_pressed('r'):
            print('Resetting...')
            run.reset()
            time.sleep(2)
            print(instruction)
    