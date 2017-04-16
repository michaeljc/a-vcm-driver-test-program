#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from LKIF_function_class import *
import ctypes
from ctypes import *
'''-----------------------------导入dll动态链接库+初始化函数-----------------------------------'''
Laser=windll.LoadLibrary("LkIF.dll") 
Laser.LKIF_GetCalcData.argtypes=(POINTER(LKIF_FLOATVALUE),POINTER(LKIF_FLOATVALUE))
Laser.LKIF_GetCalcData.restype=c_bool
Laser.LKIF_SetZero.argtypes=(c_int,c_bool)
Laser.LKIF_SetZero.restype=c_bool
Laser.LKIF_SetTiming.argtypes=(c_int,c_bool)
Laser.LKIF_SetTiming.restype=c_bool
Laser.LKIF_SetSamplingCycle.argtypes=(c_int,)
Laser.LKIF_SetSamplingCycle.restype=c_bool
Laser.LKIF_SetDisplayUnit.argtypes=(c_int,c_int)
Laser.LKIF_SetDisplayUnit.restype=c_bool
Laser.LKIF_SetDataStorage.argtypes=(c_int,c_int,c_int)
Laser.LKIF_SetDataStorage.restype=c_bool
Laser.LKIF_DataStorageGetStatus.argtypes=(c_int,c_void_p,c_void_p)
Laser.LKIF_DataStorageGetStatus.restype=c_bool
Laser.LKIF_DataStorageGetData.argtypes=(c_int,c_int,POINTER(LKIF_FLOATVALUE*65536),c_void_p)
Laser.LKIF_DataStorageGetData.restype=c_bool
#Laser.LKIF_DataStorageStart.argtypes=(None)
Laser.LKIF_DataStorageStart.restype=c_bool
#Laser.LKIF_DataStorageStop.argtypes=(None)
Laser.LKIF_DataStorageStop.restype=c_bool
#Laser.LKIF_DataStorageInit.argtypes=(None)
Laser.LKIF_DataStorageInit.restype=c_bool
Laser.LKIF_GetSamplingCycle.argtypes=(c_void_p,)
Laser.LKIF_GetSamplingCycle.restype=c_bool

'''------------------------------LKIF_GetCalcData-------------------------------'''
class LKIF(object):

	def __init__(self):
		self.value1=c_float(1)
		self.value3=c_float(1)
		self.data=[]
#单次数据输出
	def Single_Measure(self):
		CalcData1=LKIF_FLOATVALUE(LKIF_FLOATRESULT=LKIF_FLOATRESULT_VALID,Value=self.value1)
		CalcData2=LKIF_FLOATVALUE(LKIF_FLOATRESULT=LKIF_FLOATRESULT_VALID,Value=self.value3)
		Single_Measure_OK=Laser.LKIF_GetCalcData(byref(CalcData1),byref(CalcData2))
		if Single_Measure_OK==1:
			if CalcData1.LKIF_FLOATRESULT==0:
				Single_Measure_OK=0
			elif CalcData1.LKIF_FLOATRESULT==1:
				print("LKIF_FLOATRESULT_RANGEOVER_P")
				print(CalcData1.Value)
				Single_Measure_OK=0
			elif CalcData1.LKIF_FLOATRESULT==2:
				print("LKIF_FLOATRESULT_RANGEOVER_N")
				print(CalcData1.Value)
				Single_Measure_OK=0
			else:
				print("LKIF_FLOATRESULT_WAITING")
				print(CalcData1.Value)
				Single_Measure_OK=0

			return CalcData1.Value
		else:
			return "Error"
#连续数据输出
	def Continuous_DataOut(self):
		IsStorage=c_bool(0)
		NumStorageData=c_int(0)
		NumReceived=c_int(0)
		self.value2=c_float(0)
		OutBuffer=(LKIF_FLOATVALUE*65536)(LKIF_FLOATRESULT=LKIF_FLOATRESULT_VALID,Value=self.value2)
		Data_Storage_Get_Status_Is_Ok=Laser.LKIF_DataStorageGetStatus(0,byref(IsStorage),byref(NumStorageData))
		if Data_Storage_Get_Status_Is_Ok==True:
			Data_Storage_Get_Data_Is_Ok=Laser.LKIF_DataStorageGetData(0,NumStorageData,byref(OutBuffer),byref(NumReceived))
			if Data_Storage_Get_Data_Is_Ok==True:
				self.data=[]
				for x in range(NumReceived.value):
					self.data.append(OutBuffer[x].Value)
		return self.data


#初始化函数
	def Initialize(self,No=0,sample_time=LKIF_SAMPLINGCYCLE_100USEC,display_unit=LKIF_DISPLAYUNIT_00000_1UM):
		Set_Sampling_Cycle_Is_Ok=Laser.LKIF_SetSamplingCycle(sample_time)
		Set_Display_Unit_Is_Ok=Laser.LKIF_SetDisplayUnit(No,display_unit)
		Set_Data_Storage_Is_Ok=Laser.LKIF_SetDataStorage(LKIF_TARGETOUT_OUT1,c_int(65536),LKIF_STORAGECYCLE_1)
		print("Set_Display_Unit_Is_Ok=",Set_Display_Unit_Is_Ok)
		Set_Zero_Is_Ok=Laser.LKIF_SetZero(No,c_int(1))
		Initialize_Is_ok=False
		if Set_Zero_Is_Ok&Set_Sampling_Cycle_Is_Ok&Set_Display_Unit_Is_Ok&Set_Data_Storage_Is_Ok==1:
			Initialize_Is_ok=True
		return Initialize_Is_ok

#获取采样周期
	def Get_Sampling_Cycle(self):
		SamplingCycle=c_int(0)
		Get_Sampling_Cycle_Is_Ok=Laser.LKIF_GetSamplingCycle(byref(SamplingCycle))
		if Get_Sampling_Cycle_Is_Ok==1:
			if SamplingCycle.value==0:
				Sampling=0.02
			elif SamplingCycle.value==1:
				Sampling=0.05
			elif SamplingCycle.value==2:
				Sampling=0.1
			elif SamplingCycle.value==3:
				Sampling=0.2
			elif SamplingCycle.value==4:
				Sampling=0.5
			else:
				Sampling=1
		else:
			Sampling=0
		return Get_Sampling_Cycle_Is_Ok,Sampling
