#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
from ctypes import *


'''-----------------------------导入dll动态链接库-----------------------------------'''
I2Cdll=ctypes.windll.LoadLibrary("VCI_GYI2C.dll")

'''----------------GYI2C_DATA_INFO的结构体定义--------------------------------------'''
class GYI2C_DATA_INFO(Structure):
	"""docstring for Point"""
	_fields_=[("SlaveAddr",c_ubyte),("Databuffer",c_ubyte*520),("WriteNum",c_uint),
	("ReadNum",c_uint),("IoSel",c_ubyte),("IoData",c_ubyte),("DlyMsRead",c_uint),("Reserved",c_ubyte*4)]

I2Cdll.GYI2C_Read.argtypes=(c_uint,c_uint,POINTER(GYI2C_DATA_INFO))
I2Cdll.GYI2C_Read.restype=c_uint
I2Cdll.GYI2C_Write.argtypes=(c_uint,c_uint,POINTER(GYI2C_DATA_INFO))
I2Cdll.GYI2C_Write.restype=c_uint
class I2C(object):
	def __init__(self):  
		self.I2C_CLK=1
		self.I2C_Mode=0
		self.I2C_Channel=0
		self.IsOpened=0
		self.DEV_GY7501A=1
		self.DeviceIndex=0
		self.__reg_data=[]
		self.IsWriteOk=0
		self.Get_I2C_Clk=0


	def I2C_Open(self,i2cclk) :
		temp=I2Cdll.GYI2C_Open(self.DEV_GY7501A,self.DeviceIndex,9600)
		self.I2C_CLK=i2cclk
		self.Get_I2C_Clk=0
		if temp==1:
			self.IsOpened=1
			I2C_Set_Ok=I2Cdll.GYI2C_SetMode(self.DEV_GY7501A,self.DeviceIndex,0)
			self.I2C_Mode=I2Cdll.GYI2C_GetMode(self.DEV_GY7501A,self.DeviceIndex) 
			if self.I2C_Mode==0:
				I2Cdll.GYI2C_SetClk(self.DEV_GY7501A,self.DeviceIndex,c_uint(self.I2C_CLK))
				self.Get_I2C_Clk=I2Cdll.GYI2C_GetClk(self.DEV_GY7501A,self.DeviceIndex)
				I2C_Channel=I2Cdll.GYI2C_GetChannel(self.DEV_GY7501A,self.DeviceIndex)
				print("I2C打开成功")
				
			else :
				print("I2C打开失败") 
		else :
			print("I2C打开失败")
		return self.Get_I2C_Clk

	'''--------------------------I2C关闭函数--------------------------------------------'''
	def I2C_Close(self):
		temp=I2Cdll.GYI2C_Close(self.DEV_GY7501A,self.DeviceIndex)
		self.IsOpened=0
		return temp
	'''---------------------I2C读操作函数-----------------------------------------------'''		
	def I2C_Read(self,device_addr,readdatalength,regaddrlength=0,regaddr=0):#设备地址/读取数据位数/寄存器地址位数（0/1）/寄存器地址（如寄存器地址位数为1）
		if self.IsOpened == 1:
			writenum=c_uint(regaddrlength)
			readnum=c_uint(readdatalength)
			iosel=c_ubyte(0)	
			iodata=c_ubyte(0)
			delayms=c_uint(int(10/self.I2C_CLK*(readdatalength+20)))#延时时间——计算方法正确？
			databuffer=(c_ubyte*520)()		
			reserved=(c_ubyte*4)()
			addr=c_ubyte(device_addr)
			if regaddrlength ==1:
				databuffer[0]=c_ubyte(regaddr)
			pGYI2C_DATA_INFO=GYI2C_DATA_INFO(addr,databuffer,writenum,readnum,iosel,iodata,delayms,reserved)
			c=I2Cdll.GYI2C_Read(self.DEV_GY7501A,self.DeviceIndex,byref(pGYI2C_DATA_INFO))
			self.__reg_data=[]
			if c == readdatalength:
				for x in range(readdatalength):
					self.__reg_data.append(pGYI2C_DATA_INFO.Databuffer[x])
			else:
				#print("I2C数据读取失败")
				pass
		else:
			print("I2C已关闭")
		return self.__reg_data

	'''---------------------I2C写操作函数-----------------------------------------------'''		
	def I2C_Write(self,device_addr,writedatalength,writereglength,*writedata,regaddr=0x00):
		if self.IsOpened == 1:
			addr=c_ubyte(device_addr)
			writenum=c_uint(writedatalength+writereglength)
			readnum=c_uint(0)
			iosel=c_ubyte(0)
			iodata=c_ubyte(0)
			delayms=c_uint(int(10/self.I2C_CLK*(writedatalength+20)))#延时时间——计算方法正确<此延时数值跟读写操作都有联系！！！！！（说明手册上写的只跟读有关，为错误的说法）>
			databuffer=(c_ubyte*520)()
			reserved=(c_ubyte*4)()
			if writereglength !=0:
				for x in range(writedatalength+writereglength):
					if x==0:
						databuffer[x]=c_ubyte(regaddr)
					else:
						databuffer[x]=c_ubyte(writedata[x-1])
			else :
				for x in range(writedatalength+writereglength):
					databuffer[x]=c_ubyte(writedata[x])
			pGYI2C_DATA_INFO=GYI2C_DATA_INFO(addr,databuffer,writenum,readnum,iosel,iodata,delayms,reserved)
			self.IsWriteOk=I2Cdll.GYI2C_Write(self.DEV_GY7501A,self.DeviceIndex,byref(pGYI2C_DATA_INFO))
		else:
			print("I2C已关闭")
		return self.IsWriteOk


