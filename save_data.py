import numpy as np
import pandas as pd
import time as tm
import playsound as ps
import keyboard as key

#-----save data to csv-----
def save_to_csv(save_data, seconds):
         
    #-----seperate sensor datas then transpose-----
    sensor01 = np.transpose(save_data[0])
    sensor02 = np.transpose(save_data[1])
    sensor03 = np.transpose(save_data[2])
    sensor04 = np.transpose(save_data[3])
    sensor05 = np.transpose(save_data[4])
    sensor06 = np.transpose(save_data[5])
    sensor07 = np.transpose(save_data[6])
    sensor08 = np.transpose(save_data[7])
    #-----transpose time-----
    secondsc = np.transpose(seconds)
        
    #-----set columns label-----
    label1 = ['ch1(sensor01)', 'ch2(sensor01)', 'ch3(sensor01)', 'ch4(sensor01)']
    label2 = ['ch1(sensor02)', 'ch2(sensor02)', 'ch3(sensor02)', 'ch4(sensor02)']
    label3 = ['ch1(sensor03)', 'ch2(sensor03)', 'ch3(sensor03)', 'ch4(sensor03)']
    label4 = ['ch1(sensor04)', 'ch2(sensor04)', 'ch3(sensor04)', 'ch4(sensor04)']
    label5 = ['ch1(sensor05)', 'ch2(sensor05)', 'ch3(sensor05)', 'ch4(sensor05)']
    label6 = ['ch1(sensor06)', 'ch2(sensor06)', 'ch3(sensor06)', 'ch4(sensor06)']
    label7 = ['ch1(sensor07)', 'ch2(sensor07)', 'ch3(sensor07)', 'ch4(sensor07)']
    label8 = ['ch1(sensor08)', 'ch2(sensor08)', 'ch3(sensor08)', 'ch4(sensor08)']
    #-----set time label-----
    timems = ['time(s)']
    
    #-----convert data to pandas dataframe-----
    df01 = pd.DataFrame(sensor01 , columns = label1)
    df02 = pd.DataFrame(sensor02 , columns = label2)
    df03 = pd.DataFrame(sensor03 , columns = label3)
    df04 = pd.DataFrame(sensor04 , columns = label4)
    df05 = pd.DataFrame(sensor05 , columns = label5)
    df06 = pd.DataFrame(sensor06 , columns = label6)
    df07 = pd.DataFrame(sensor07 , columns = label7)
    df08 = pd.DataFrame(sensor08 , columns = label8)
    #-----convert time data to pandas dataframe-----
    dfms = pd.DataFrame(secondsc , columns = timems)
        
    #-----merge all sensors dataframe on axis 1-----
    frames = [dfms, df01, df02, df03, df04, df05, df06, df07, df08]
    df = pd.concat(frames, axis=1)
    
    #-----save as .csv file-----
    file_name = tm.strftime("%Y%m%d_%H;%M;%S_raw.csv", tm.localtime())
    df.to_csv(file_name, index=False)
    
    return file_name
    
       
        
    
        
        
        
