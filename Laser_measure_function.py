#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''-----------------------------导入模块--------------------------------'''
from LKIF_function import *
from I2C import *
import time
from tkinter import *
import tkinter.messagebox as messagebox

laser=LKIF()
i2c=I2C()


class La_Mes(object):
	def __init__(self):
		self.TVIB=0
		self.TVIB_reg=0
		self.DIRECT_reg=0x00
		self.RING_reg=0x02
		self.LSC_reg=0x80
		self.SAC2_reg=0x00#需先写Ring
		self.SAC3_reg=0x40#需先写Ring
		self.SAC4_reg=0x80#需先写Ring
		self.SAC5_reg=0xc0#需先写Ring
		self.i2c_clk=400
		self.I2C_Open_Ok=0


	
	def soft_PD(self):
		soft_PD_Is_Ok=0
		write1=i2c.I2C_Write(0x18,1,1,0x01,regaddr=0x02)#9800芯片进行PD复位
		time.sleep(0.5)
		write2=i2c.I2C_Write(0x18,1,1,0x00,regaddr=0x02)
		time.sleep(0.5)
		if write1==1 and write2==1:
			soft_PD_Is_Ok=1
		return soft_PD_Is_Ok

	def SC9714_Zero_Init(self):
		i2c.I2C_Write(0x18,2,0,0x00,0x00)#将马达推至电流为0处
		time.sleep(0.5)
		a=laser.Initialize()#初始化（包括设置零点）
		time.sleep(0.5)
		Laser.LKIF_DataStorageInit()
		return a
	def SC9800_Zero_Init(self):
		i2c.I2C_Write(0x18,2,1,0x02,0x00,regaddr=0x03)#将马达推至电流为0处
		time.sleep(0.5)
		a=laser.Initialize()#初始化（包括设置零点）
		time.sleep(0.5)
		Laser.LKIF_DataStorageInit()
		return a
	def SC9714V_Advanced_Zero_Init(self):
		i2c.I2C_Write(0x18,2,1,0x00,0x00,regaddr=0x03)#将马达推至电流为0处
		time.sleep(0.5)
		a=laser.Initialize()#初始化（包括设置零点）
		time.sleep(0.5)
		Laser.LKIF_DataStorageInit()
		return a

	def Open_i2c(self,clk):
		self.i2c_clk=clk
		get_clk=i2c.I2C_Open(self.i2c_clk)
		self.I2C_Open_Ok=i2c.IsOpened
		return get_clk
	def Close_i2c(self):
		i2c_close=i2c.I2C_Close()
		self.I2C_Open_Ok=i2c.IsOpened
		return i2c_close
	def Read_i2c(self,deviceaddr,readdatalength,regaddrlength1=0,regaddr1=0):
		readdata=i2c.I2C_Read(deviceaddr,readdatalength,regaddrlength=regaddrlength1,regaddr=regaddr1)
		return readdata
	def Write_i2c(self,device_addr,writedatalength,writereglength,*writedata,regaddr1=0x00):
		write_ok=i2c.I2C_Write(device_addr,writedatalength,writereglength,*writedata,regaddr=regaddr1)
		return write_ok


	def SC9714V_Advanced_stroke_measure(self,min,max,step=1):
		self.SC9714V_Advanced_Zero_Init()

		i2c_list=range(min,max+1,step)
		file_name2='.\\'+time.strftime('%Y%m%d_%H%M%S')+'_stroke.csv'
		datatxt=open(file_name2,'a')
		datatxt.write('DAC值'+','+'位移'+','+'MSB值'+','+'LSB值'+','+'日期'+','+'时间'+'\n')
		data1=(min>>8)&0x03
		data2=min&0xff
		i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
		currentlist=[]
		for num in i2c_list:
			data1=(num>>8)&0x03
			data2=num&0xff
			i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
			currentdata=laser.Single_Measure()
			currentlist.append(currentdata)
			datatxt.write(str(num)+','+str(currentdata)+','+str(data1)+','+str(data2)+','+time.strftime('%Y-%m-%d,%H:%M:%S')+'\n')
		datatxt.close()
		print("读取成功")
		return currentlist


	def SC9714V_Advanced_osc_measure(self,*writedata):
		Zero_Init_ok=self.SC9714V_Advanced_Zero_Init()

		Get_Sampling_Cycle_flag,Sampling_Cycle=laser.Get_Sampling_Cycle()
		write_position=[]

		#存储下DAC值对应的Laser测距仪对应的位置
		for num in range(len(writedata)):
			data1=(writedata[num]>>8)&0x03
			data2=writedata[num]&0xff
			i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
			time.sleep(1)
			#采样取平均值
			Laser.LKIF_DataStorageStart()
			time.sleep(1)
			Laser.LKIF_DataStorageStop()
			aver=laser.Continuous_DataOut()
			#print(aver)
			average=(max(aver)+min(aver))/2
			write_position.append(average)
			Laser.LKIF_DataStorageInit()
		if	len(write_position)!=len(writedata):
			messagebox.showinfo('Message', '未写入正确数量的位移位置')
		for x in range(len(write_position)-1):
			if abs(write_position[x]-write_position[x+1])<3:
				messagebox.showinfo('Message', '未正常获取位移值')
		print(write_position)
		#使初始位移停留在writedata[0]对应的位置
		data1=(writedata[0]>>8)&0x03
		data2=writedata[0]&0xff
		i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
		time.sleep(2)
		#开始Laser测距仪的连续测量功能
		Laser.LKIF_DataStorageStart()
		#连续写N个writedata的值每次写完后延时0.5s
		if len(writedata)==1:
			time.sleep(0.5)
		else:
			for num in range(1,len(writedata)):
				data1=(writedata[num]>>8)&0x03
				data2=writedata[num]&0xff
				i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
				time.sleep(0.5)
		#停止Laser测距仪的连续测量功能
		Laser.LKIF_DataStorageStop()
		#输出Laser测距仪所存储下的采样点
		temp=laser.Continuous_DataOut()
		
		#排序算法，找出稳定时间
		#初始化参数
		start_stability=1#start_stability=1代表从稳定状态到开始偏离+3um的采样点
						 #start_stability=0代表从不稳定状态到开始恢复到+3um以内的采样点
		begin_num=0#从何值开始寻找进入稳定点和脱离稳定点	
		stability_num=[]#所有进入稳定点和脱离稳定点的集合
		append_wirte=1
		out_range=0
		
		for loop in range(1,2*(len(write_position)-1)+1):
			if start_stability==1:
				append_wirte=1
				out_range=0
				for x in range(begin_num,len(temp)):
					if abs(temp[x]-write_position[loop//2])<=3:
						out_range=0
						#re_begin_num=x
					else:
						out_range=out_range+1
						out_range_num=x
						while out_range>=100 and append_wirte==1:
							append_wirte=0
							stability_num.append(out_range_num+1-out_range)
				if len(stability_num)==(loop):
					begin_num=stability_num[loop-1]
				else:
					begin_num=len(temp)-1
				start_stability=0
			else:
				append_wirte=1
				in_range=0
				for x in range(begin_num,len(temp)):
					if abs(temp[x]-write_position[loop//2])<=3:
						in_range=in_range+1
						in_range_num=x
						while in_range>=1500 and append_wirte==1:#如软件显示的稳定时间>300ms,可能为此阈值过小，可尝试修改此阈值（）
							append_wirte=0 						 #推荐阈值范围（100~5000）
							stability_num.append(in_range_num+1-in_range)
					else:
						in_range=0
				if len(stability_num)==(loop):
					begin_num=stability_num[loop-1]
				else:
					begin_num=len(temp)-1
				start_stability=1
		stability_list=[]

		for x in range(len(stability_num)//2):
			stability_list.append(round((stability_num[2*x+1]-stability_num[2*x])*Sampling_Cycle,2))



		file_name1='.\\'+time.strftime('%Y%m%d_%H%M%S')+'_osc.csv'
		datatxt=open(file_name1,'a')
		datatxt.write('编号'+','+'采样时间'+','+'位移'+','+'MSB值'+','+'LSB值'+','+'日期'+','+'时间'+'\n')
		for num in range(len(temp)):
			datatxt.write(str(num)+','+str(num*0.1)+','+str(temp[num])+','+str(data1)+','+str(data2)+','+time.strftime('%Y-%m-%d,%H:%M:%S')+'\n')
		datatxt.close()
		return stability_list,temp
	'''-----------------------------9800测量--------------------------------'''
	
	def SC9800_stroke_measure(self,min,max,step=1):
		self.SC9800_Zero_Init()

		i2c_list=range(min,max+1,step)
		file_name2='.\\'+time.strftime('%Y%m%d_%H%M%S')+'_stroke.csv'
		datatxt=open(file_name2,'a')
		datatxt.write('DAC值'+','+'位移'+','+'MSB值'+','+'LSB值'+','+'日期'+','+'时间'+'\n')
		data1=(min>>8)&0x03
		data2=min&0xff
		i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
		currentlist=[]
		for num in i2c_list:
			data1=(num>>8)&0x03
			data2=num&0xff
			i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
			currentdata=laser.Single_Measure()
			currentlist.append(currentdata)
			datatxt.write(str(num)+','+str(currentdata)+','+str(data1)+','+str(data2)+','+time.strftime('%Y-%m-%d,%H:%M:%S')+'\n')
		datatxt.close()
		print("读取成功")
		return currentlist


	def SC9800_osc_measure(self,*writedata):
		Zero_Init_ok=self.SC9800_Zero_Init()

		Get_Sampling_Cycle_flag,Sampling_Cycle=laser.Get_Sampling_Cycle()
		write_position=[]

		#存储下DAC值对应的Laser测距仪对应的位置
		for num in range(len(writedata)):
			data1=(writedata[num]>>8)&0x03
			data2=writedata[num]&0xff
			i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
			time.sleep(1)
			#采样取平均值
			Laser.LKIF_DataStorageStart()
			time.sleep(1)
			Laser.LKIF_DataStorageStop()
			aver=laser.Continuous_DataOut()
			#print(aver)
			average=(max(aver)+min(aver))/2
			write_position.append(average)
			Laser.LKIF_DataStorageInit()
		if	len(write_position)!=len(writedata):
			messagebox.showinfo('Message', '未写入正确数量的位移位置')
		for x in range(len(write_position)-1):
			if abs(write_position[x]-write_position[x+1])<3:
				messagebox.showinfo('Message', '未正常获取位移值')
		print(write_position)
		#使初始位移停留在writedata[0]对应的位置
		data1=(writedata[0]>>8)&0x03
		data2=writedata[0]&0xff
		i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
		time.sleep(2)
		#开始Laser测距仪的连续测量功能
		Laser.LKIF_DataStorageStart()
		#连续写N个writedata的值每次写完后延时0.5s
		if len(writedata)==1:
			time.sleep(0.5)
		else:
			for num in range(1,len(writedata)):
				data1=(writedata[num]>>8)&0x03
				data2=writedata[num]&0xff
				i2c.I2C_Write(0x18,2,1,data1,data2,regaddr=0x03)
				time.sleep(0.5)
		#停止Laser测距仪的连续测量功能
		Laser.LKIF_DataStorageStop()
		#输出Laser测距仪所存储下的采样点
		temp=laser.Continuous_DataOut()
		
		#排序算法，找出稳定时间
		#初始化参数
		start_stability=1#start_stability=1代表从稳定状态到开始偏离+3um的采样点
						 #start_stability=0代表从不稳定状态到开始恢复到+3um以内的采样点
		begin_num=0#从何值开始寻找进入稳定点和脱离稳定点	
		stability_num=[]#所有进入稳定点和脱离稳定点的集合
		append_wirte=1
		out_range=0
		
		for loop in range(1,2*(len(write_position)-1)+1):
			if start_stability==1:
				append_wirte=1
				out_range=0
				for x in range(begin_num,len(temp)):
					if abs(temp[x]-write_position[loop//2])<=3:
						out_range=0
						#re_begin_num=x
					else:
						out_range=out_range+1
						out_range_num=x
						while out_range>=100 and append_wirte==1:
							append_wirte=0
							stability_num.append(out_range_num+1-out_range)
				if len(stability_num)==(loop):
					begin_num=stability_num[loop-1]
				else:
					begin_num=len(temp)-1
				start_stability=0
			else:
				append_wirte=1
				in_range=0
				for x in range(begin_num,len(temp)):
					if abs(temp[x]-write_position[loop//2])<=3:
						in_range=in_range+1
						in_range_num=x
						while in_range>=1500 and append_wirte==1:#如软件显示的稳定时间>300ms,可能为此阈值过小，可尝试修改此阈值（）
							append_wirte=0 						 #推荐阈值范围（100~5000）
							stability_num.append(in_range_num+1-in_range)
					else:
						in_range=0
				if len(stability_num)==(loop):
					begin_num=stability_num[loop-1]
				else:
					begin_num=len(temp)-1
				start_stability=1
		stability_list=[]

		for x in range(len(stability_num)//2):
			stability_list.append(round((stability_num[2*x+1]-stability_num[2*x])*Sampling_Cycle,2))



		file_name1='.\\'+time.strftime('%Y%m%d_%H%M%S')+'_osc.csv'
		datatxt=open(file_name1,'a')
		datatxt.write('编号'+','+'采样时间'+','+'位移'+','+'MSB值'+','+'LSB值'+','+'日期'+','+'时间'+'\n')
		for num in range(len(temp)):
			datatxt.write(str(num)+','+str(num*0.1)+','+str(temp[num])+','+str(data1)+','+str(data2)+','+time.strftime('%Y-%m-%d,%H:%M:%S')+'\n')
		datatxt.close()
		return stability_list,temp

	'''-----------------------------9714测量--------------------------------'''
	def SC9714_stroke_measure(self,min,max,step=1):
			self.SC9714_Zero_Init()
			i2c_list=range(min,max+1,step)
			file_name2='.\\'+time.strftime('%Y%m%d_%H%M%S')+'_stroke.csv'
			datatxt=open(file_name2,'a')
			datatxt.write('DAC值'+','+'位移'+','+'MSB值'+','+'LSB值'+','+'日期'+','+'时间'+'\n')
			data1=(min>>4)&0x3F
			data2=(min<<4)&0xF0
			i2c.I2C_Write(0x18,2,0,data1,data2)
			currentlist=[]
			for num in i2c_list:
				data1=(num>>4)&0x3F
				data2=(num<<4)&0xF0
				i2c.I2C_Write(0x18,2,0,data1,data2)
				currentdata=laser.Single_Measure()
				currentlist.append(currentdata)
				datatxt.write(str(num)+','+str(currentdata)+','+str(data1)+','+str(data2)+','+time.strftime('%Y-%m-%d,%H:%M:%S')+'\n')
			datatxt.close()
			print("读取成功")
			return currentlist

	def SC9714_osc_measure(self,*writedata,S4=0x00):

		Zero_Init_ok=self.SC9714_Zero_Init()
		Get_Sampling_Cycle_flag,Sampling_Cycle=laser.Get_Sampling_Cycle()
		write_position=[]

		#存储下DAC值对应的Laser测距仪对应的位置
		for num in range(len(writedata)):
			data1=(writedata[num]>>4)&0x3F
			data2=((writedata[num]<<4)&0xF0)|S4
			i2c.I2C_Write(0x18,2,0,data1,data2)
			time.sleep(1)
			#采样取平均值
			Laser.LKIF_DataStorageStart()
			time.sleep(1)
			Laser.LKIF_DataStorageStop()
			aver=laser.Continuous_DataOut()
			#print(aver)
			average1=sum(aver)/len(aver)
			average2=(max(aver)+min(aver))/2
			average=(average1+average2)/2
			write_position.append(average)
			Laser.LKIF_DataStorageInit()
		if	len(write_position)!=len(writedata):
			messagebox.showinfo('Message', '未写入正确数量的位移位置')
		for x in range(len(write_position)-1):
			if abs(write_position[x]-write_position[x+1])<3:
				messagebox.showinfo('Message', '未正常获取位移值')
		print(write_position)
		#使初始位移停留在writedata[0]对应的位置
		data1=(writedata[0]>>4)&0x3F
		data2=((writedata[0]<<4)&0xF0)|S4
		i2c.I2C_Write(0x18,2,0,data1,data2)
		time.sleep(2)
		#开始Laser测距仪的连续测量功能
		Laser.LKIF_DataStorageStart()
		#连续写N个writedata的值每次写完后延时0.5s
		if len(writedata)==1:
				time.sleep(0.5)
		else:
			for num in range(1,len(writedata)):
				data1=(writedata[num]>>4)&0x3F
				data2=((writedata[num]<<4)&0xF0)|S4
				i2c.I2C_Write(0x18,2,0,data1,data2)
				time.sleep(0.5)
		#停止Laser测距仪的连续测量功能
		Laser.LKIF_DataStorageStop()
		#输出Laser测距仪所存储下的采样点
		temp=laser.Continuous_DataOut()
		
		#排序算法，找出稳定时间
		#初始化参数
		start_stability=1#start_stability=1代表从稳定状态到开始偏离+3um的采样点
						 #start_stability=0代表从不稳定状态到开始恢复到+3um以内的采样点
		begin_num=0#从何值开始寻找进入稳定点和脱离稳定点	
		stability_num=[]#所有进入稳定点和脱离稳定点的集合
		append_wirte=1
		out_range=0
		
		for loop in range(1,2*(len(write_position)-1)+1):
			if start_stability==1:
				append_wirte=1
				out_range=0
				for x in range(begin_num,len(temp)):
					if abs(temp[x]-write_position[loop//2])<=3:
						out_range=0
						#re_begin_num=x
					else:
						out_range=out_range+1
						out_range_num=x
						while out_range>=100 and append_wirte==1:
							append_wirte=0
							stability_num.append(out_range_num+1-out_range)
				if len(stability_num)==(loop):
					begin_num=stability_num[loop-1]
				else:
					begin_num=len(temp)-1
				start_stability=0
			else:
				append_wirte=1
				in_range=0
				for x in range(begin_num,len(temp)):
					if abs(temp[x]-write_position[loop//2])<=3:
						in_range=in_range+1
						in_range_num=x
						while in_range>=1500 and append_wirte==1:#如软件显示的稳定时间>300ms,可能为此阈值过小，可尝试修改此阈值（）
							append_wirte=0 						 #推荐阈值范围（100~5000）
							stability_num.append(in_range_num+1-in_range)
					else:
						in_range=0
				if len(stability_num)==(loop):
					begin_num=stability_num[loop-1]
				else:
					begin_num=len(temp)-1
				start_stability=1
		stability_list=[]

		for x in range(len(stability_num)//2):
			stability_list.append(round((stability_num[2*x+1]-stability_num[2*x])*Sampling_Cycle,2))



		file_name1='.\\'+time.strftime('%Y%m%d_%H%M%S')+'_osc.csv'
		datatxt=open(file_name1,'a')
		datatxt.write('编号'+','+'采样时间'+','+'位移'+','+'MSB值'+','+'LSB值'+','+'日期'+','+'时间'+'\n')
		for num in range(len(temp)):
			datatxt.write(str(num)+','+str(num*0.1)+','+str(temp[num])+','+str(data1)+','+str(data2)+','+time.strftime('%Y-%m-%d,%H:%M:%S')+'\n')
		datatxt.close()
		return stability_list,temp
#--------------------------模式切换-----------------------------------------
	def Shift_9714V_Ad_Mode(self,AF_mode,NRC,SACT,PRESC):
		result=0
		reg2=PRESC&0x03
		reg3=SACT&0x7F
		if AF_mode=='LSCStep1':
			reg1=0x86|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)
			
			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)
			
			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='LSCStep1'
		elif AF_mode=='LSCStep2':
			reg1=0x8A|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)
			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='LSCStep2'
		elif AF_mode=='LSCStep4':
			reg1=0x8E|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)

			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='LSCStep4'
		elif AF_mode=='SLSC':
			reg1=0x83|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)

			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='SLSC'
		elif AF_mode=='SAC2':
			reg1=0x80|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)

			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='SAC2'
		elif AF_mode=='SAC3':
			reg1=0x84|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)

			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='SAC3'
		elif AF_mode=='SAC3.5':
			reg1=0x88|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)

			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='SAC3.5'		
		elif AF_mode=='Direct':
			reg1=0x00|((NRC<<4)&0x70)
			i2c.I2C_Write(0x18,1,1,reg1,regaddr=0x06)

			i2c.I2C_Write(0x18,1,1,reg2,regaddr=0x07)

			i2c.I2C_Write(0x18,1,1,reg3,regaddr=0x08)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x07)
			self.read3=i2c.I2C_Read(0x18,1,1,regaddr=0x08)
			if len(self.read1)!=0 and len(self.read2)!=0 and len(self.read3)!=0:
				if self.read1[0]==reg1 and self.read2[0]==reg2 and self.read3[0]==reg3:
					result='Direct'		
		else:
			print('模式设置错误')
		return result
	def switch_NRC_Mode(self,NRC_SWITCH):
		result=0
		if NRC_SWITCH=='start':
			i2c.I2C_Write(0x18,1,1,0x02,regaddr=0x0A)
			result='start'
		elif NRC_SWITCH=='landing':
			i2c.I2C_Write(0x18,1,1,0x03,regaddr=0x0A)
			result='landing'
		elif NRC_SWITCH=='close':
			i2c.I2C_Write(0x18,1,1,0x00,regaddr=0x0A)
			result='close'
		else:
			print('模式设置错误')
		return result

	def Shift_9714_Mode(self,AF_mode,MCLK,T_SRC):
		result=0
		if AF_mode=='DLC':
			i2c.I2C_Write(0x18,2,0,0xEC,0xA3)
			dlcreg1=0x0C|(MCLK&0x03)
			print(dlcreg1)
			i2c.I2C_Write(0x18,2,0,0xA1,dlcreg1)
			dlcreg2=T_SRC<<3
			i2c.I2C_Write(0x18,2,0,0xF2,dlcreg2)
			i2c.I2C_Write(0x18,2,0,0xDC,0x51)
			result='DLC'
		elif AF_mode=='LSC':
			i2c.I2C_Write(0x18,2,0,0xEC,0xA3)
			lscreg1=0x05|(MCLK&0x03)
			print(lscreg1)
			i2c.I2C_Write(0x18,2,0,0xA1,lscreg1)
			lscreg2=T_SRC<<3
			i2c.I2C_Write(0x18,2,0,0xF2,lscreg2)
			i2c.I2C_Write(0x18,2,0,0xDC,0x51)
			result='LSC'
		elif AF_mode=='Direct':
			i2c.I2C_Write(0x18,2,0,0x80,0x00)
			i2c.I2C_Write(0x18,2,0,0x00,0x00)
			result='Direct'
		else:
			print('模式设置错误')
		return result

	def Shift_9800_Mode(self,AF_mode):
		result=0
		if AF_mode=='LSC':
			i2c.I2C_Write(0x18,1,1,0x00,regaddr=0x02)
			i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			time.sleep(0.05)
			i2c.I2C_Write(0x18,1,1,self.LSC_reg,regaddr=0x06)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			if len(self.read1)!=0 and len(self.read2)!=0:
				if self.read1[0]==0x00 and self.read2[0]==self.LSC_reg:
					result='LSC'
		elif AF_mode=='SAC2':
			i2c.I2C_Write(0x18,1,1,self.RING_reg,regaddr=0x02)
			time.sleep(0.05)
			i2c.I2C_Write(0x18,1,1,self.SAC2_reg,regaddr=0x06)
			time.sleep(0.05)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			if len(self.read1)!=0 and len(self.read2)!=0:
				if self.read1[0]==self.RING_reg and self.read2[0]==self.SAC2_reg:
					result='SAC2'
		elif AF_mode=='SAC3':
			i2c.I2C_Write(0x18,1,1,self.RING_reg,regaddr=0x02)
			time.sleep(0.05)
			i2c.I2C_Write(0x18,1,1,self.SAC3_reg,regaddr=0x06)
			time.sleep(0.05)
			#i2c.I2C_Write(0x18,1,1,0x39,regaddr=0x07)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			if len(self.read1)!=0 and len(self.read2)!=0:
				if self.read1[0]==self.RING_reg and self.read2[0]==self.SAC3_reg:
					result='SAC3'
		elif AF_mode=='SAC4':
			i2c.I2C_Write(0x18,1,1,self.RING_reg,regaddr=0x02)
			time.sleep(0.05)
			i2c.I2C_Write(0x18,1,1,self.SAC4_reg,regaddr=0x06)
			time.sleep(0.05)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			if len(self.read1)!=0 and len(self.read2)!=0:
				if self.read1[0]==self.RING_reg and self.read2[0]==self.SAC4_reg:
					result='SAC4'
		elif AF_mode=='SAC5':
			i2c.I2C_Write(0x18,1,1,self.RING_reg,regaddr=0x02)
			time.sleep(0.05)
			i2c.I2C_Write(0x18,1,1,self.SAC5_reg,regaddr=0x06)
			time.sleep(0.05)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			if len(self.read1)!=0 and len(self.read2)!=0:
				if self.read1[0]==self.RING_reg and self.read2[0]==self.SAC5_reg:
					result='SAC5'
		elif AF_mode=='Direct':
			i2c.I2C_Write(0x18,1,1,0x00,regaddr=0x02)
			time.sleep(0.05)
			i2c.I2C_Write(0x18,1,1,self.DIRECT_reg,regaddr=0x06)
			self.read1=i2c.I2C_Read(0x18,1,1,regaddr=0x02)
			self.read2=i2c.I2C_Read(0x18,1,1,regaddr=0x06)
			if len(self.read1)!=0 and len(self.read2)!=0:
				if self.read1[0]==0x00 and self.read2[0]==self.DIRECT_reg:
					result='Direct'
		else:
			print('模式设置错误')
		return result
	def read_reg(self,deviceaddr,*read_regaddr):
		read_reg_data_list=[]
		for x in range(len(read_regaddr)):
			read=i2c.I2C_Read(deviceaddr,1,1,regaddr=read_regaddr[x])
			read_reg_data_list.append(read)
		return read_reg_data_list



'''-----------------------------------------------------------------------------'''
