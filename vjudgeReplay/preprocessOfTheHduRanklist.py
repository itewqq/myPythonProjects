# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 11:50:54 2019

@author: qushi
"""
import datetime
from openpyxl import Workbook, load_workbook
NoneType=type(None)
wb1=load_workbook('ori.xlsx')
ws1=wb1['Sheet1']
for row in ws1.rows:
    for cl in row:
#        print(type(cl.value))
#        print(str(cl.value))
        if(isinstance(cl.value,datetime.time)):
            cl.value=str(cl.value)+"#"
            print(str(cl.value))
        if(isinstance(cl.value,NoneType)):
            cl.value=str("(-0)")
            print(str(cl.value))

wb1.save('temp.xlsx')
