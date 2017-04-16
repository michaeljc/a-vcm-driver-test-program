#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''-----------------------------导入模块--------------------------------'''
import matplotlib.pyplot as plt
import serial
import time
from tkinter import *
from Laser_measure_function import *
import tkinter.messagebox as messagebox

laser_measure=La_Mes()
'''-----------------------------laser_measure函数--------------------------------'''
#laser_measure.SC9800_osc_measure(400,300,700,300)
#laser_measure.SC9800_stroke_measure(400,300,700)

'''-------------------------------GUI-----------------------------------------'''
#create GUI class
class App(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.initialize()

	def initialize(self):
		self.grid()
		self.i2c=400
		self.str_i2c=StringVar()
		self.str_i2c.set('打开I2C')
		self.ic_int=StringVar()
		self.ic_int.set("9800")
		self.str_9714v_mode=StringVar()
		self.str_9714v_mode.set('Normal')

		self.af_mode_variable = StringVar()
		self.af_mode_variable.set("Direct")
		self.measure_mode_variable = StringVar()
		self.measure_mode_variable.set("振荡曲线测量")
		self.i2c_status=NORMAL
		self.i2c_display_data=StringVar()
		self.i2c_display_data.set('')
		self.mode_int=IntVar()
		self.str_int=StringVar()
		self.str_int.set('disabled')
		self.str_data=[IntVar(),IntVar()]
		self.osc_int=StringVar()
		self.osc_int.set('disabled')
		self.osc_data=[IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
		self.osc_staytime=StringVar()
		self.I2C_Open_status=DISABLED
		self.osc_num=IntVar()
		self.reg0_str=StringVar()
		self.reg1_str=StringVar()
		self.reg2_str=StringVar()
		self.reg3_str=StringVar()
		self.reg4_str=StringVar()
		self.reg5_str=StringVar()
		self.reg6_str=StringVar()
		self.reg7_str=StringVar()
		self.device_addr=IntVar()
		self.device_list=[hex(i) for i in list(range(0,256,2))]
		self.reg_addr_list=[hex(i) for i in list(range(0,256))]
		self.reg_len=IntVar()
		self.reg_addr=IntVar()
		self.reg_len.set('1')
		self.reg_status=NORMAL
		self.data_len=IntVar()
		self.reg_data=[IntVar(),IntVar(),IntVar()]
		self.require_osctime=IntVar()
		
		self.method_label1_status=StringVar()
		self.method_reg1_entry_status=StringVar()
		self.method_label2_status=StringVar()
		self.method_reg2_entry_status=StringVar()
		self.method_label3_status=StringVar()
		self.method_reg3_entry_status=StringVar()
		self.method_label4_status=StringVar()
		self.method_reg4_entry_status=StringVar()
		self.method_reg1_entry_status.set('normal')
		self.method_reg2_entry_status.set('normal')
		self.method_reg3_entry_status.set('disabled')
		self.method_reg4_entry_status.set('disabled')
		self.method_label1_status.set('normal')
		self.method_label2_status.set('normal')
		self.method_label3_status.set('disabled')
		self.method_label4_status.set('disabled')

		self.method_reg1=IntVar()
		self.method_reg2=IntVar()
		self.method_reg3=IntVar()
		self.method_reg4=IntVar()
		
		self.method1_value=[bin(i) for i in list(range(0,255))]
		self.method2_value=[bin(i) for i in list(range(0,255))]
		self.method3_value=[bin(i) for i in list(range(0,255))]
		self.method4_value=[bin(i) for i in list(range(0,255))]
		
		self.method_list=["Direct", "LSC","SAC2","SAC3","SAC4","SAC5"]
		self.method_reg1_label=StringVar()
		self.method_reg1_label.set('Divider[2:0]')
		self.method_reg2_label=StringVar()
		self.method_reg2_label.set('SAC Tvib[5:0]')
		self.method_reg3_label=StringVar()
		self.method_reg3_label.set('Reserved')
		self.method_reg4_label=StringVar()
		self.method_reg4_label.set('Reserved')
		self.nrc_mode=StringVar()




		'''2---------------------Frame设置---------------------------
		数据设置'''
		self.group1=LabelFrame(self,text="数据设置",height=650,width=420,padx=5,pady=5)
		self.group1.grid_propagate(0)
		self.group1.grid(column=0,padx=10,row=0,sticky=N)

		'''2.3----------------------打开关闭I2C-按钮-------------------------------'''

		I2C_label = Label(self.group1, text='I2C', width=10,relief = GROOVE)
		I2C_label.grid(column =0, padx = 10, row = 0,sticky = NW)
		Display_I2C_label = Entry(self.group1,  textvariable = self.i2c_display_data,width=10, 
			relief = SUNKEN,state=self.i2c_status)
		Display_I2C_label.grid(column = 0, padx = 10, row = 1, sticky = NW)
		I2C_button=Button(self.group1,textvariable=self.str_i2c,command=self.ShiftI2C)
		I2C_button.grid(column=0,padx=10,row=2,sticky=NW)

		'''------------------------芯片类型选择------------------------------------'''
		Label(self.group1, text='芯片类型', width=10,relief = GROOVE).grid(column =0, padx = 5, row = 3,sticky = NW)
		self.c = OptionMenu(self.group1,self.ic_int,"9714","9800","9714V",command=self.SHIFT_AF)
		self.c.grid(column=0,padx=5,row=4,sticky = NW)
		self.SC9714V_label = Label(self.group1, text='9714V_MODE', width=10,relief = GROOVE)
		self.SC9714V_label.grid(column =0, padx = 10, row = 5,sticky = NW)
		self.SC9714V_button=Button(self.group1,width=10,textvariable=self.str_9714v_mode,command=self.SFT_9714V_MODE)
		self.SC9714V_button.grid(column=0,padx=10,row=6,sticky = NW)
		self.nrc_label=Label(self.group1, text='NRC开关', width=10,relief = GROOVE)
		self.nrc_label.grid(column =0, padx = 10,pady = 5 ,row = 7,sticky = NW)
		self.nrc_switch = OptionMenu(self.group1, self.nrc_mode,'close','start','landing',command=self.switchnrc)
		self.nrc_switch.grid(column=0,padx=10,row=8,sticky = NW)
		self.nrc_label.grid_forget()
		self.nrc_switch.grid_forget()
		self.SC9714V_label.grid_forget()
		self.SC9714V_button.grid_forget()

		'''-----------------------------测试模式选择------------------------------------------'''

		measuremode_label = Label(self.group1, text='测试模式选择', width=15,relief = GROOVE)
		measuremode_label.grid(column =1, padx = 10, row = 0,sticky = NW)
		self.b = Radiobutton(self.group1, text="振荡曲线测量", variable=self.mode_int, value=1,
			command=self.SHIFT_AF_MODE,indicatoron=False)
		self.b.grid(column=1,padx=10,row=1)
		self.b = Radiobutton(self.group1, text="行程曲线测量", variable=self.mode_int, value=2,
			command=self.SHIFT_AF_MODE,indicatoron=False)
		self.b.grid(column=1,padx=10,row=2)
		Label(self.group1, text='需求的稳定时间', width=15,relief = GROOVE).grid(column=1,padx=10,row=3,pady=5,sticky=N)
		Entry(self.group1,  textvariable = self.require_osctime,width=15, 
			relief = SUNKEN).grid(column=1,padx=10,row=4,sticky=N)
		Button(self.group1,text='search',width=15, state=self.I2C_Open_status,
			command=self.search).grid(column=1,padx=10,row=5,sticky=N)

		'''2.1----------------------振荡曲线测量相关widget-------------------------------'''

		af_mode_label = Label(self.group1, text='芯片方法选择', width=15,relief = GROOVE)
		af_mode_label.grid(column =2, padx = 10, row = 0,sticky = NW)
		self.af_mode = OptionMenu(self.group1, self.af_mode_variable,*self.method_list,command=self.changemode)
		self.af_mode.grid(column=2,padx=10,row=1,sticky = NW)
		self.method_label1=Label(self.group1, textvariable=self.method_reg1_label, width=15,relief = GROOVE,
			state=self.method_label1_status.get())
		self.method_label1.grid(column =2, padx = 10,pady = 5 ,row = 2,sticky = NW)
		self.method_reg1_entry= Spinbox(self.group1,  textvariable = self.method_reg1,width=15,value=self.method1_value,
			state=self.method_reg1_entry_status.get())
		self.method_reg1_entry.grid(column =2, padx = 10, row = 3,pady = 5,sticky = NW)
		self.method_label2=Label(self.group1, textvariable=self.method_reg2_label, width=15,relief = GROOVE,
			state=self.method_label2_status.get())
		self.method_label2.grid(column =2, pady = 5,padx = 10, row = 4,sticky = NW)
		self.method_reg2_entry= Spinbox(self.group1,  textvariable = self.method_reg2,width=15,value=self.method2_value,
			state=self.method_reg2_entry_status.get())
		self.method_reg2_entry.grid(column =2, padx = 10, row = 5,sticky = NW)
		self.method_label3=Label(self.group1, textvariable=self.method_reg3_label, width=15,relief = GROOVE,
			state=self.method_label3_status.get())
		self.method_label3.grid(column =2, padx = 10,pady = 5 ,row = 6,sticky = NW)
		self.method_reg3_entry= Spinbox(self.group1,  textvariable = self.method_reg3,width=15,value=self.method3_value,
			state=self.method_reg3_entry_status.get())
		self.method_reg3_entry.grid(column =2, padx = 10, row = 7,pady = 5,sticky = NW)
		self.method_label4=Label(self.group1, textvariable=self.method_reg4_label, width=15,relief = GROOVE,
			state=self.method_label4_status.get())
		self.method_label4.grid(column =2, pady = 5,padx = 10, row = 8,sticky = NW)
		self.method_reg4_entry= Spinbox(self.group1,  textvariable = self.method_reg4,width=15,value=self.method4_value,
			state=self.method_reg4_entry_status.get())
		self.method_reg4_entry.grid(column =2, padx = 10, row = 9,sticky = NW)




		Button(self.group1,text='写入DIV&SACT',width=15, state=self.I2C_Open_status,
			command=self.ACT_SACT_DIV).grid(column=2,padx=10,row=10,sticky=N)



		'''------------------------------开始测量按钮---------------------------------------------------'''
		START_Me_button=Button(self.group1,text='开始测量',width=10,command=self.START_ME,
			state=self.I2C_Open_status)
		START_Me_button.grid(column=0,padx=10,row=11,sticky=N)
		'''-----------------------------------------PD-------------------------------'''
		self.PD_button=Button(self.group1,text='PD按钮',width=10,command=self.soft_Pd,state=self.I2C_Open_status)
		self.PD_button.grid(column=0,padx=10,pady=5,row=12,sticky=N)

		'''----------------------------------振荡曲线设置-------------------------------------'''
		self.osc_label = Label(self.group1, text='振荡曲线设置', width=16,relief = GROOVE,
			state=self.osc_int.get())
		self.osc_label.grid(column =1, padx = 10, row = 11)
		self.sta_label = Label(self.group1, text='稳定时间', width=16,relief = GROOVE)
		self.sta_label.grid(column =1, padx = 10, row = 12)
		self.sta_display = Label(self.group1, textvariable=self.osc_staytime, width=16,relief = SUNKEN)
		self.sta_display.grid(column =1, padx = 10, row = 13)
		self.osc_num_label = Label(self.group1, text='写入数据数量', width=16,relief = GROOVE)
		self.osc_num_label.grid(column =1, padx = 10, row = 14)
		self.osc_num_entry=Spinbox(self.group1,width=12,from_=1,to=5,textvariable=self.osc_num,
			command=self.SHIFT_AF_MODE)
		self.osc_num_entry.grid(column =1, padx = 10, row = 15)

		self.osc_Entry1 = Entry(self.group1,  textvariable = self.osc_data[0],width=10, 
				relief = SUNKEN,state=self.i2c_status)
		self.osc_Entry1.grid(column = 1, padx = 10, row = 16, sticky = W)
		self.osc_Entry2 = Entry(self.group1,  textvariable = self.osc_data[1],width=10, 
				relief = SUNKEN,state=self.i2c_status)
		self.osc_Entry2.grid(column = 1, padx = 10, row = 17, sticky = W)
		self.osc_Entry3 = Entry(self.group1,  textvariable = self.osc_data[2],width=10, 
				relief = SUNKEN,state=self.i2c_status)
		self.osc_Entry3.grid(column = 1, padx = 10, row = 18, sticky = W)
		self.osc_Entry4 = Entry(self.group1,  textvariable = self.osc_data[3],width=10, 
				relief = SUNKEN,state=self.i2c_status)
		self.osc_Entry4.grid(column = 1, padx = 10, row = 19, sticky = W)
		self.osc_Entry5 = Entry(self.group1,  textvariable = self.osc_data[4],width=10, 
				relief = SUNKEN,state=self.i2c_status)
		self.osc_Entry5.grid(column = 1, padx = 10, row = 20, sticky = W)


		self.osc_num_label.grid_forget()
		self.osc_num_entry.grid_forget()
		self.osc_Entry1.grid_forget()
		self.osc_Entry2.grid_forget()
		self.osc_Entry3.grid_forget()
		self.osc_Entry4.grid_forget()
		self.osc_Entry5.grid_forget()
		self.sta_label.grid_forget()
		self.sta_display.grid_forget()

#---------------------------行程曲线设置-----------------------------------------
		self.str_label = Label(self.group1, text='行程曲线设置', width=16,relief = GROOVE,
			state=self.str_int.get())
		self.str_label.grid(column =2, padx = 10, row = 11)
		self.str_Entry1 = Entry(self.group1,  textvariable = self.str_data[0],width=10, 
				relief = SUNKEN)
		self.str_Entry1.grid(column = 2, padx = 10, row = 12, sticky = W)
		self.str_Entry2 = Entry(self.group1,  textvariable = self.str_data[1],width=10, 
				relief = SUNKEN)
		self.str_Entry2.grid(column = 2, padx = 10, row = 13, sticky = W)
		self.str_Entry1.grid_forget()
		self.str_Entry2.grid_forget()

#'''3--------------------寄存器---------------------------'''
		self.group2=LabelFrame(self,text="寄存器",height=650,width=650,padx=5,pady=5)
		self.group2.grid_propagate(0)
		self.group2.grid(column=1,padx=10,row=0,columnspan=200,sticky=W)
		self.Exe = Button(self.group2, text='读取',width=10, state=self.I2C_Open_status,command = self.Get_AF_Reg)
		self.Exe.grid(column = 0, pady = 10, row = 0, sticky = W)

		Label(self.group2, text='0x00寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 2)
		Label(self.group2, text='0x01寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 3)
		Label(self.group2, text='0x02寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 4)
		Label(self.group2, text='0x03寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 5)
		Label(self.group2, text='0x04寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 6)
		Label(self.group2, text='0x05寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 7)
		Label(self.group2, text='0x06寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 8)
		Label(self.group2, text='0x07寄存器', width=10,height=1,pady = 5,
			relief = GROOVE).grid(column =0,pady =5, padx = 10, row = 9)
		self.reg0_label=Label(self.group2,textvariable=self.reg0_str, 
			padx = 5, pady = 5,height=1, width=10, relief = SUNKEN)
		self.reg1_label=Label(self.group2,textvariable=self.reg1_str, 
			padx = 5, pady = 5, height=1, width=10,relief = SUNKEN)
		self.reg2_label=Label(self.group2,textvariable=self.reg2_str, 
			padx = 5, pady = 5,height=1,  width=10,relief = SUNKEN)
		self.reg3_label=Label(self.group2,textvariable=self.reg3_str, 
			padx = 5, pady = 5,height=1, width=10, relief = SUNKEN)
		self.reg4_label=Label(self.group2,textvariable=self.reg4_str, 
			padx = 5, pady = 5,height=1, width=10, relief = SUNKEN)
		self.reg5_label=Label(self.group2,textvariable=self.reg5_str, 
			padx = 5, pady = 5,height=1, width=10, relief = SUNKEN)		
		self.reg6_label=Label(self.group2,textvariable=self.reg6_str, 
			padx = 5, pady = 5,height=1, width=10, relief = SUNKEN)
		self.reg7_label=Label(self.group2,textvariable=self.reg7_str, 
			padx = 5, pady = 5,height=1,  width=10,relief = SUNKEN)

		self.reg0_label.grid(column = 1, padx = 10,pady =5, row =2 )
		self.reg1_label.grid(column = 1, padx = 10,pady =5, row =3 )
		self.reg2_label.grid(column = 1, padx = 10,pady =5, row =4 )
		self.reg3_label.grid(column = 1, padx = 10,pady =5, row =5 )
		self.reg4_label.grid(column = 1, padx = 10,pady =5, row =6 )
		self.reg5_label.grid(column = 1, padx = 10,pady =5, row =7 )
		self.reg6_label.grid(column = 1, padx = 10,pady =5, row =8 )
		self.reg7_label.grid(column = 1, padx = 10,pady =5, row =9 )
		'''
		self.reg0_label.grid_forget()
		self.reg1_label.grid_forget()
		self.reg2_label.grid_forget()
		self.reg3_label.grid_forget()
		self.reg4_label.grid_forget()
		self.reg5_label.grid_forget()
		self.reg6_label.grid_forget()
		self.reg7_label.grid_forget()
		'''
#-------------------------------寄存器读取----------------------------------------------
		self.Exe1 = Button(self.group2, text='写入',width=10, state=self.I2C_Open_status,command = self.Write_AF_Reg)
		self.Exe1.grid(column = 3, pady = 10, row = 0)
		Label(self.group2, text='设备地址', width=15,height=1,pady = 5
			,relief = GROOVE).grid(column =3,pady =5, padx = 10, row = 1)
		
		self.device_entry=Spinbox(self.group2,width=5,textvariable=self.device_addr,value=self.device_list)
		self.device_entry.grid(column =4, padx = 5, row = 1)

		Label(self.group2, text='寄存器地址长度', width=15,height=1,pady = 5
			,relief = GROOVE).grid(column =3,pady =5, padx = 10, row = 2)
		self.reg_len_entry=Spinbox(self.group2,width=5,textvariable=self.reg_len,
			command=self.shift_reg_len,from_=0,to=1)
		self.reg_len_entry.grid(column =4, padx = 5, row = 2)
		Label(self.group2, text='寄存器地址', width=15,height=1,pady = 5
			,relief = GROOVE).grid(column =5,pady =5, padx = 10, row = 2)
		self.reg_addr_entry=Spinbox(self.group2,width=5,textvariable=self.reg_addr,value=self.reg_addr_list,state=self.reg_status)
		self.reg_addr_entry.grid(column =6, padx = 5, row = 2)

		Label(self.group2, text='寄存器数据长度', width=15,height=1,pady = 5
			,relief = GROOVE).grid(column =3,pady =5, padx = 10, row = 3)
		self.data_len_entry=Spinbox(self.group2,width=5,textvariable=self.data_len,
			command=self.shift_data_len,from_=0,to=3)
		self.data_len_entry.grid(column =4, padx = 5, row = 3)
		Label(self.group2, text='寄存器数据', width=15,height=1,pady = 5
			,relief = GROOVE).grid(column =5,pady =5, padx = 10, row = 3)
		self.reg_data_entry1=Entry(self.group2,width=5,textvariable=self.reg_data[0])
		self.reg_data_entry1.grid(column =6, padx = 5, row = 3)
		self.reg_data_entry2=Entry(self.group2,width=5,textvariable=self.reg_data[1])
		self.reg_data_entry2.grid(column =6, padx = 5, row = 4)
		self.reg_data_entry3=Entry(self.group2,width=5,textvariable=self.reg_data[2])
		self.reg_data_entry3.grid(column =6, padx = 5, row = 5)
		self.reg_data_entry1.grid_forget()
		self.reg_data_entry2.grid_forget()
		self.reg_data_entry3.grid_forget()

		


#'''4------------------------画布--------------------------'''
	

#-------------------------------函数定义-----------------------------
	def switchnrc(self,master):
		if laser_measure.I2C_Open_Ok==0:
			messagebox.showinfo('Message', '请打开I2C')
		else:
			if self.nrc_mode.get()=='start':
				a=laser_measure.switch_NRC_Mode(self.nrc_mode.get())
			elif self.nrc_mode.get()=='landing':
				a=laser_measure.switch_NRC_Mode(self.nrc_mode.get())
			else:
				a=laser_measure.switch_NRC_Mode(self.nrc_mode.get())
			if a==self.nrc_mode.get():
				pass
			else:
				messagebox.showinfo('Message', '设置芯片模式失败')


	def search(self):
		if self.af_mode_variable.get()=="Direct":
			messagebox.showinfo('Message', 'Direct模式无需设置此参数')
			return
		if self.require_osctime.get()==0:
			messagebox.showinfo('Message', '请输入需求的稳定时间')	
			return
		(reg6,reg7)=laser_measure.Read_i2c(0x18,2,1,0x6)
		for delta_div in range(8):
			for delta_sact in range(0,64,2):
				write_reg6=(reg6|(delta_div>>2))&0xff
				write_reg7=(((delta_div&0x03)<<6)|delta_sact)
				writeok=laser_measure.Write_i2c(0x18,2,1,write_reg6,write_reg7,regaddr1=0x06)
				if writeok==0:
					messagebox.showinfo('Message', 'I2C写失败')
				staytime,position=laser_measure.SC9800_osc_measure(300,700,300)
				if staytime[0]<=self.require_osctime.get() and staytime[1]<=self.require_osctime.get():
					
					require_sact=delta_sact
					require_div=delta_div
					self.method_reg1.set(require_div)
					self.method_reg2.set(require_sact)
					self.ACT_SACT_DIV()
					messagebox.showinfo('Message', 'search已完成')	
					return None
		messagebox.showinfo('Message', '未找到合适参数')				
		return None

	def ACT_SACT_DIV(self):
		(reg6,reg7)=laser_measure.Read_i2c(0x18,2,1,0x6)
		reg6=(reg6|(self.method_reg1.get()>>2))&0xff
		reg7=(((self.method_reg1.get()&0x03)<<6)|self.method_reg2.get())
		writeok=laser_measure.Write_i2c(0x18,2,1,reg6,reg7,regaddr1=0x06)
		if writeok==0:
			messagebox.showinfo('Message', 'I2C写失败')	
			
	def shift_data_len(self):
		if self.data_len.get()==0:
			self.reg_data_entry1.grid_forget()
			self.reg_data_entry2.grid_forget()
			self.reg_data_entry3.grid_forget()
		else:
			self.reg_data_entry1.grid_forget()
			self.reg_data_entry2.grid_forget()
			self.reg_data_entry3.grid_forget()
			for x in range(1,self.data_len.get()+1):
				if x==1:
					self.reg_data_entry1.grid(column =6, padx = 5, row = 3)
				elif x==2:
					self.reg_data_entry2.grid(column =6, padx = 5, row = 4)
				elif x==3:
					self.reg_data_entry3.grid(column =6, padx = 5, row = 5)	


	def shift_reg_len(self):
		if self.reg_len.get()==0:
			self.reg_status=DISABLED
			self.reg_addr_entry=Spinbox(self.group2,width=5,textvariable=self.reg_addr,value=self.reg_addr_list,
				state=self.reg_status)
			self.reg_addr_entry.grid(column =6, padx = 5, row = 2)
		else:
			self.reg_status=NORMAL
			self.reg_addr_entry=Spinbox(self.group2,width=5,textvariable=self.reg_addr,value=self.reg_addr_list,
				state=self.reg_status)
			self.reg_addr_entry.grid(column =6, padx = 5, row = 2)

	def Write_AF_Reg(self):
		writedata=[]
		for x in range(self.data_len.get()):
			writedata.append(self.reg_data[x].get())
		if self.reg_len.get()==0:
			writeok=laser_measure.Write_i2c(self.device_addr.get(),self.data_len.get(),self.reg_len.get(),*writedata)
		else:
			writeok=laser_measure.Write_i2c(self.device_addr.get(),self.data_len.get(),self.reg_len.get(),*writedata,
				regaddr1=self.reg_addr.get())
		if writeok==0:
			messagebox.showinfo('Message', 'I2C写失败')		
	def Get_AF_Reg(self):
		if self.ic_int.get()=='9714':
			(read_reg0,read_reg1)=laser_measure.Read_i2c(0x18,2)
			self.reg0_str.set(hex(read_reg0))
			self.reg1_str.set(hex(read_reg1))
		else:
			(read_reg0,read_reg1,read_reg2,read_reg3,
				read_reg4,read_reg5,read_reg6,read_reg7)=laser_measure.Read_i2c(0x18,8,1,0x00)
			self.reg0_str.set(hex(read_reg0))
			self.reg1_str.set(hex(read_reg1))
			self.reg2_str.set(hex(read_reg2))
			self.reg3_str.set(hex(read_reg3))
			self.reg4_str.set(hex(read_reg4))
			self.reg5_str.set(hex(read_reg5))
			self.reg6_str.set(hex(read_reg6))
			self.reg7_str.set(hex(read_reg7))


	'''------------------------切换芯片类型------------------------------'''
	def SHIFT_AF(self,master):
		self.SC9714V_label.grid_forget()
		self.SC9714V_button.grid_forget()
		self.reg0_label.grid_forget()
		self.reg1_label.grid_forget()
		self.reg2_label.grid_forget()
		self.reg3_label.grid_forget()
		self.reg4_label.grid_forget()
		self.reg5_label.grid_forget()
		self.reg6_label.grid_forget()
		self.reg7_label.grid_forget()

		self.method_reg1_entry_status.set('disabled')
		self.method_reg2_entry_status.set('disabled')
		self.method_reg3_entry_status.set('disabled')
		self.method_reg4_entry_status.set('disabled')
		self.method_label1_status.set('disabled')
		self.method_label2_status.set('disabled')
		self.method_label3_status.set('disabled')
		self.method_label4_status.set('disabled')
		self.method_reg1_label.set('Reserved')
		self.method_reg2_label.set('Reserved')
		self.method_reg3_label.set('Reserved')
		self.method_reg4_label.set('Reserved')
		self.nrc_label.grid_forget()
		self.nrc_switch.grid_forget()

		if self.ic_int.get()=='9714':
			self.method_list=['Direct','DLC','LSC']
			self.method_reg1_label.set('S[3:0]')
			self.method_reg1_entry_status.set('normal')
			self.method_label1_status.set('normal')
			self.af_mode = OptionMenu(self.group1, self.af_mode_variable,*self.method_list,command=self.changemode)
			self.af_mode.grid(column=2,padx=10,row=1,sticky = NW)
			self.method_label1=Label(self.group1, textvariable=self.method_reg1_label, width=15,relief = GROOVE,
				state=self.method_label1_status.get())
			self.method_label1.grid(column =2, padx = 10,pady = 5 ,row = 2,sticky = NW)
			self.method_reg1_entry= Spinbox(self.group1,  textvariable = self.method_reg1,width=15,value=self.method1_value,
				state=self.method_reg1_entry_status.get())
			self.method_reg1_entry.grid(column =2, padx = 10, row = 3,pady = 5,sticky = NW)
			self.method_label2=Label(self.group1, textvariable=self.method_reg2_label, width=15,relief = GROOVE,
				state=self.method_label2_status.get())
			self.method_label2.grid(column =2, pady = 5,padx = 10, row = 4,sticky = NW)
			self.method_reg2_entry= Spinbox(self.group1,  textvariable = self.method_reg2,width=15,value=self.method2_value,
				state=self.method_reg2_entry_status.get())
			self.method_reg2_entry.grid(column =2, padx = 10, row = 5,sticky = NW)
			self.method_label3=Label(self.group1, textvariable=self.method_reg3_label, width=15,relief = GROOVE,
				state=self.method_label3_status.get())
			self.method_label3.grid(column =2, padx = 10,pady = 5 ,row = 6,sticky = NW)
			self.method_reg3_entry= Spinbox(self.group1,  textvariable = self.method_reg3,width=15,value=self.method3_value,
				state=self.method_reg3_entry_status.get())
			self.method_reg3_entry.grid(column =2, padx = 10, row = 7,pady = 5,sticky = NW)
			self.method_label4=Label(self.group1, textvariable=self.method_reg4_label, width=15,relief = GROOVE,
				state=self.method_label4_status.get())
			self.method_label4.grid(column =2, pady = 5,padx = 10, row = 8,sticky = NW)
			self.method_reg4_entry= Spinbox(self.group1,  textvariable = self.method_reg4,width=15,value=self.method4_value,
				state=self.method_reg4_entry_status.get())
			self.method_reg4_entry.grid(column =2, padx = 10, row = 9,sticky = NW)

			self.reg0_label.grid(column = 1, padx = 10,pady =5, row =2 )
			self.reg1_label.grid(column = 1, padx = 10,pady =5, row =3)



		elif self.ic_int.get()=='9800':
			self.method_list=["Direct", "LSC","SAC2","SAC3","SAC4","SAC5"]
			self.method_reg1_label.set('Divider[2:0]')
			self.method_reg2_label.set('SAC Tvib[5:0]')
			self.method_reg1_entry_status.set('normal')
			self.method_reg2_entry_status.set('normal')
			self.method_label1_status.set('normal')
			self.method_label2_status.set('normal')
			self.af_mode = OptionMenu(self.group1, self.af_mode_variable,*self.method_list,command=self.changemode)
			self.af_mode.grid(column=2,padx=10,row=1,sticky = NW)
			self.method_label1=Label(self.group1, textvariable=self.method_reg1_label, width=15,relief = GROOVE,
				state=self.method_label1_status.get())
			self.method_label1.grid(column =2, padx = 10,pady = 5 ,row = 2,sticky = NW)
			self.method_reg1_entry= Spinbox(self.group1,  textvariable = self.method_reg1,width=15,value=self.method1_value,
				state=self.method_reg1_entry_status.get())
			self.method_reg1_entry.grid(column =2, padx = 10, row = 3,pady = 5,sticky = NW)
			self.method_label2=Label(self.group1, textvariable=self.method_reg2_label, width=15,relief = GROOVE,
				state=self.method_label2_status.get())
			self.method_label2.grid(column =2, pady = 5,padx = 10, row = 4,sticky = NW)
			self.method_reg2_entry= Spinbox(self.group1,  textvariable = self.method_reg2,width=15,value=self.method2_value,
				state=self.method_reg2_entry_status.get())
			self.method_reg2_entry.grid(column =2, padx = 10, row = 5,sticky = NW)
			self.method_label3=Label(self.group1, textvariable=self.method_reg3_label, width=15,relief = GROOVE,
				state=self.method_label3_status.get())
			self.method_label3.grid(column =2, padx = 10,pady = 5 ,row = 6,sticky = NW)
			self.method_reg3_entry= Spinbox(self.group1,  textvariable = self.method_reg3,width=15,value=self.method3_value,
				state=self.method_reg3_entry_status.get())
			self.method_reg3_entry.grid(column =2, padx = 10, row = 7,pady = 5,sticky = NW)
			self.method_label4=Label(self.group1, textvariable=self.method_reg4_label, width=15,relief = GROOVE,
				state=self.method_label4_status.get())
			self.method_label4.grid(column =2, pady = 5,padx = 10, row = 8,sticky = NW)
			self.method_reg4_entry= Spinbox(self.group1,  textvariable = self.method_reg4,width=15,value=self.method4_value,
				state=self.method_reg4_entry_status.get())
			self.method_reg4_entry.grid(column =2, padx = 10, row = 9,sticky = NW)
			
			self.reg0_label.grid(column = 1, padx = 10,pady =5, row =2)
			self.reg1_label.grid(column = 1, padx = 10,pady =5, row =3 )
			self.reg2_label.grid(column = 1, padx = 10,pady =5, row =4 )
			self.reg3_label.grid(column = 1, padx = 10,pady =5, row =5)
			self.reg4_label.grid(column = 1, padx = 10,pady =5, row =6)
			self.reg5_label.grid(column = 1, padx = 10,pady =5, row =7)
			self.reg6_label.grid(column = 1, padx = 10,pady =5, row =8 )
			self.reg7_label.grid(column = 1, padx = 10,pady =5, row =9)

		elif self.ic_int.get()=='9714V':
			self.SC9714V_label = Label(self.group1, width=12,text='9714V_MODE',relief = GROOVE)
			self.SC9714V_label.grid(column =0, padx = 10, row = 5,sticky = NW)
			self.SC9714V_button=Button(self.group1,width=10,textvariable=self.str_9714v_mode,command=self.SFT_9714V_MODE)
			self.SC9714V_button.grid(column=0,padx=10,row=6,sticky = NW)		

	def SFT_9714V_MODE(self):
		if self.str_9714v_mode.get()=='Normal':
			write_ok=laser_measure.Write_i2c(0x18,2,0,0xED,0xAB)
			if write_ok==1:
				readdata=laser_measure.Read_i2c(0x18,1,1,0x00)
				print(readdata[0])
				if readdata[0]==0xFE:
					self.str_9714v_mode.set('Advanced')

					self.reg0_label.grid_forget()
					self.reg1_label.grid_forget()
					self.reg2_label.grid_forget()
					self.reg3_label.grid_forget()
					self.reg4_label.grid_forget()
					self.reg5_label.grid_forget()
					self.reg6_label.grid_forget()
					self.reg7_label.grid_forget()

					self.method_reg1_entry_status.set('disabled')
					self.method_reg2_entry_status.set('disabled')
					self.method_reg3_entry_status.set('disabled')
					self.method_reg4_entry_status.set('disabled')
					self.method_label1_status.set('disabled')
					self.method_label2_status.set('disabled')
					self.method_label3_status.set('disabled')
					self.method_label4_status.set('disabled')
					self.method_reg1_label.set('Reserved')
					self.method_reg2_label.set('Reserved')
					self.method_reg3_label.set('Reserved')
					self.method_reg4_label.set('Reserved')

					self.method_list=["Direct", "LSCStep1","LSCStep2","LSCStep4","SAC2","SAC3","SAC3.5","SLSC"]
					self.method_reg1_label.set('NRC(INF+TIME)')
					self.method_reg2_label.set('PRESC[1:0]')
					self.method_reg3_label.set('SACT[6:0]')
					self.method_reg4_label.set('PRESET[7:0]')

					self.method_reg1_entry_status.set('normal')
					self.method_label1_status.set('normal')
					self.method_reg2_entry_status.set('normal')
					self.method_label2_status.set('normal')
					self.method_reg3_entry_status.set('normal')
					self.method_label3_status.set('normal')
					self.method_reg4_entry_status.set('normal')
					self.method_label4_status.set('normal')

					self.nrc_label=Label(self.group1, text='NRC开关', width=10,relief = GROOVE)
					self.nrc_label.grid(column =0, padx = 10,pady = 5 ,row = 7,sticky = NW)
					self.nrc_switch = OptionMenu(self.group1, self.nrc_mode,'close','start','landing'
						,command=self.switchnrc)
					self.nrc_switch.grid(column=0,padx=10,row=8,sticky = NW)
					self.af_mode = OptionMenu(self.group1, self.af_mode_variable,*self.method_list,command=self.changemode)
					self.af_mode.grid(column=2,padx=10,row=1,sticky = NW)
					self.method_label1=Label(self.group1, textvariable=self.method_reg1_label, width=15,relief = GROOVE,
						state=self.method_label1_status.get())
					self.method_label1.grid(column =2, padx = 10,pady = 5 ,row = 2,sticky = NW)
					self.method_reg1_entry= Spinbox(self.group1,  textvariable = self.method_reg1,width=15,value=self.method1_value,
						state=self.method_reg1_entry_status.get())
					self.method_reg1_entry.grid(column =2, padx = 10, row = 3,pady = 5,sticky = NW)
					self.method_label2=Label(self.group1, textvariable=self.method_reg2_label, width=15,relief = GROOVE,
						state=self.method_label2_status.get())
					self.method_label2.grid(column =2, pady = 5,padx = 10, row = 4,sticky = NW)
					self.method_reg2_entry= Spinbox(self.group1,  textvariable = self.method_reg2,width=15,value=self.method2_value,
						state=self.method_reg2_entry_status.get())
					self.method_reg2_entry.grid(column =2, padx = 10, row = 5,sticky = NW)
					self.method_label3=Label(self.group1, textvariable=self.method_reg3_label, width=15,relief = GROOVE,
						state=self.method_label3_status.get())
					self.method_label3.grid(column =2, padx = 10,pady = 5 ,row = 6,sticky = NW)
					self.method_reg3_entry= Spinbox(self.group1,  textvariable = self.method_reg3,width=15,value=self.method3_value,
						state=self.method_reg3_entry_status.get())
					self.method_reg3_entry.grid(column =2, padx = 10, row = 7,pady = 5,sticky = NW)
					self.method_label4=Label(self.group1, textvariable=self.method_reg4_label, width=15,relief = GROOVE,
						state=self.method_label4_status.get())
					self.method_label4.grid(column =2, pady = 5,padx = 10, row = 8,sticky = NW)
					self.method_reg4_entry= Spinbox(self.group1,  textvariable = self.method_reg4,width=15,value=self.method4_value,
						state=self.method_reg4_entry_status.get())
					self.method_reg4_entry.grid(column =2, padx = 10, row = 9,sticky = NW)
					self.reg0_label.grid(column = 1, padx = 10,pady =5, row =2)
					self.reg1_label.grid(column = 1, padx = 10,pady =5, row =3 )
					self.reg2_label.grid(column = 1, padx = 10,pady =5, row =4 )
					self.reg3_label.grid(column = 1, padx = 10,pady =5, row =5)
					self.reg4_label.grid(column = 1, padx = 10,pady =5, row =6)
					self.reg5_label.grid(column = 1, padx = 10,pady =5, row =7)
					self.reg6_label.grid(column = 1, padx = 10,pady =5, row =8 )
					self.reg7_label.grid(column = 1, padx = 10,pady =5, row =9)
				else:
					messagebox.showinfo('Message', '9714V切换MODE失败')
			else:
				messagebox.showinfo('Message', 'I2C写失败')
		else:
			write_ok=laser_measure.Write_i2c(0x18,2,0,0xDF,0x5B)
			if write_ok==1:
				readdata=laser_measure.Read_i2c(0x18,2,0)
				print(readdata[0])
				if readdata[0]!=0xFE:
					self.str_9714v_mode.set('Normal')
					self.nrc_label.grid_forget()
					self.nrc_switch.grid_forget()
					self.reg0_label.grid_forget()
					self.reg1_label.grid_forget()
					self.reg2_label.grid_forget()
					self.reg3_label.grid_forget()
					self.reg4_label.grid_forget()
					self.reg5_label.grid_forget()
					self.reg6_label.grid_forget()
					self.reg7_label.grid_forget()

					self.method_reg1_entry_status.set('disabled')
					self.method_reg2_entry_status.set('disabled')
					self.method_reg3_entry_status.set('disabled')
					self.method_reg4_entry_status.set('disabled')
					self.method_label1_status.set('disabled')
					self.method_label2_status.set('disabled')
					self.method_label3_status.set('disabled')
					self.method_label4_status.set('disabled')
					self.method_reg1_label.set('Reserved')
					self.method_reg2_label.set('Reserved')
					self.method_reg3_label.set('Reserved')
					self.method_reg4_label.set('Reserved')

					self.method_list=['Direct','DLC','LSC']
					self.method_reg1_label.set('S[3:0]')
					self.method_reg2_label.set('MCLK[1:0]')
					self.method_reg3_label.set('T_SRC[4:0]')

					self.method_reg1_entry_status.set('normal')
					self.method_label1_status.set('normal')
					self.method_reg2_entry_status.set('normal')
					self.method_label2_status.set('normal')
					self.method_reg3_entry_status.set('normal')
					self.method_label3_status.set('normal')
					
					self.af_mode = OptionMenu(self.group1, self.af_mode_variable,*self.method_list,command=self.changemode)
					self.af_mode.grid(column=2,padx=10,row=1,sticky = NW)
					self.method_label1=Label(self.group1, textvariable=self.method_reg1_label, width=15,relief = GROOVE,
						state=self.method_label1_status.get())
					self.method_label1.grid(column =2, padx = 10,pady = 5 ,row = 2,sticky = NW)
					self.method_reg1_entry= Spinbox(self.group1,  textvariable = self.method_reg1,width=15,value=self.method1_value,
						state=self.method_reg1_entry_status.get())
					self.method_reg1_entry.grid(column =2, padx = 10, row = 3,pady = 5,sticky = NW)
					self.method_label2=Label(self.group1, textvariable=self.method_reg2_label, width=15,relief = GROOVE,
						state=self.method_label2_status.get())
					self.method_label2.grid(column =2, pady = 5,padx = 10, row = 4,sticky = NW)
					self.method_reg2_entry= Spinbox(self.group1,  textvariable = self.method_reg2,width=15,value=self.method2_value,
						state=self.method_reg2_entry_status.get())
					self.method_reg2_entry.grid(column =2, padx = 10, row = 5,sticky = NW)
					self.method_label3=Label(self.group1, textvariable=self.method_reg3_label, width=15,relief = GROOVE,
						state=self.method_label3_status.get())
					self.method_label3.grid(column =2, padx = 10,pady = 5 ,row = 6,sticky = NW)
					self.method_reg3_entry= Spinbox(self.group1,  textvariable = self.method_reg3,width=15,value=self.method3_value,
						state=self.method_reg3_entry_status.get())
					self.method_reg3_entry.grid(column =2, padx = 10, row = 7,pady = 5,sticky = NW)
					self.method_label4=Label(self.group1, textvariable=self.method_reg4_label, width=15,relief = GROOVE,
						state=self.method_label4_status.get())
					self.method_label4.grid(column =2, pady = 5,padx = 10, row = 8,sticky = NW)
					self.method_reg4_entry= Spinbox(self.group1,  textvariable = self.method_reg4,width=15,value=self.method4_value,
						state=self.method_reg4_entry_status.get())
					self.method_reg4_entry.grid(column =2, padx = 10, row = 9,sticky = NW)
					self.reg0_label.grid(column = 1, padx = 10,pady =5, row =2 )
					self.reg1_label.grid(column = 1, padx = 10,pady =5, row =3)
				else:
					messagebox.showinfo('Message', '9714V切换MODE失败')
			else:
				messagebox.showinfo('Message', 'I2C写失败')

	def soft_Pd(self):
		pd_flag=laser_measure.soft_PD()
		if pd_flag==1:
			messagebox.showinfo('Message', 'PD成功')
		else:
			messagebox.showinfo('Message', 'PD失败')

	def ShiftI2C (self):
		if len(self.i2c_display_data.get())>3:
			self.i2c=int(self.i2c_display_data.get()[0:-3])
		else :
			if len(self.i2c_display_data.get())==0:
				pass
			else:
				self.i2c=int(self.i2c_display_data.get())
		if laser_measure.I2C_Open_Ok==0:
			self.Is_Open_Ok_list=laser_measure.Open_i2c(self.i2c)
			if laser_measure.I2C_Open_Ok==1:
				myapp.str_i2c.set('关闭I2C')
				self.i2c_display_data.set(str(self.Is_Open_Ok_list)+'KHz')
				self.i2c_status=DISABLED
				Display_I2C_label = Entry(self.group1,  textvariable = self.i2c_display_data, 
					width=10, relief = SUNKEN,state=self.i2c_status)
				Display_I2C_label.grid(column = 0, padx = 10, row = 1, sticky = W)
				self.I2C_Open_status=NORMAL
				START_Me_button=Button(self.group1,text='开始测量',width=10,command=self.START_ME,
					state=self.I2C_Open_status)
				START_Me_button.grid(column=0,padx=10,row=11,sticky=N)
				self.PD_button=Button(self.group1,text='PD按钮',width=10,command=self.soft_Pd,state=self.I2C_Open_status)
				self.PD_button.grid(column=0,padx=10,pady=5,row=12,sticky=N)
				self.Exe = Button(self.group2, text='读取', width=10,state=self.I2C_Open_status,command = self.Get_AF_Reg)
				self.Exe.grid(column = 0, pady = 10, row = 0, sticky = W)
				self.Exe1 = Button(self.group2, text='写入',width=10, state=self.I2C_Open_status,command = self.Write_AF_Reg)
				self.Exe1.grid(column = 3, pady = 10, row = 0)
				Button(self.group1,text='写入DIV&SACT',width=15, state=self.I2C_Open_status,
					command=self.ACT_SACT_DIV).grid(column=2,padx=10,row=10,sticky=N)
				Button(self.group1,text='search',width=15, state=self.I2C_Open_status,
					command=self.search).grid(column=1,padx=10,row=5,sticky=N)
			else:
				messagebox.showinfo('Message', 'I2C打开失败')	
		else:
			self.Is_Close_Ok_list=laser_measure.Close_i2c()
			if self.Is_Close_Ok_list==1:
				myapp.str_i2c.set('打开I2C')
				self.i2c_status=NORMAL
				Display_I2C_label = Entry(self.group1,  textvariable = self.i2c_display_data,
					width=10, relief = SUNKEN,state=self.i2c_status)
				Display_I2C_label.grid(column = 0, padx = 10, row = 1, sticky = W)
				self.I2C_Open_status=DISABLED
				START_Me_button=Button(self.group1,text='开始测量',width=10,command=self.START_ME,
					state=self.I2C_Open_status)
				START_Me_button.grid(column=0,padx=10,row=11,sticky=N)
				self.PD_button=Button(self.group1,text='PD按钮',width=10,command=self.soft_Pd,state=self.I2C_Open_status)
				self.PD_button.grid(column=0,padx=10,pady=5,row=12,sticky=N)
				self.Exe = Button(self.group2, text='读取', width=10,state=self.I2C_Open_status,command = self.Get_AF_Reg)
				self.Exe.grid(column = 0, pady = 10, row = 0, sticky = W)
				self.Exe1 = Button(self.group2, text='写入',width=10, state=self.I2C_Open_status,command = self.Write_AF_Reg)
				self.Exe1.grid(column = 3, pady = 10, row = 0)
				Button(self.group1,text='写入DIV&SACT',width=15, state=self.I2C_Open_status,
					command=self.ACT_SACT_DIV).grid(column=2,padx=10,row=10,sticky=N)
				Button(self.group1,text='search',width=15, state=self.I2C_Open_status,
					command=self.search).grid(column=1,padx=10,row=5,sticky=N)
			else:
				messagebox.showinfo('Message', 'I2C关闭失败')
		
		

	def SHIFT_AF_MODE(self):
		self.osc_num_label.grid_forget()
		self.osc_num_entry.grid_forget()
		self.osc_Entry1.grid_forget()
		self.osc_Entry2.grid_forget()
		self.osc_Entry3.grid_forget()
		self.osc_Entry4.grid_forget()
		self.osc_Entry5.grid_forget()
		self.sta_label.grid_forget()
		self.sta_display.grid_forget()
		self.str_Entry1.grid_forget()
		self.str_Entry2.grid_forget()


		if self.mode_int.get()==1:
			self.osc_int.set('normal')
			self.str_int.set('disabled')
			self.str_label = Label(self.group1, text='行程曲线设置', width=16,relief = GROOVE,
				state=self.str_int.get())
			self.str_label.grid(column =2, padx = 10, row = 11)
			self.osc_label = Label(self.group1, text='振荡曲线设置', width=16,relief = GROOVE,
				state=self.osc_int.get())
			self.osc_label.grid(column =1, padx = 10, row = 11)
			self.sta_label = Label(self.group1, text='稳定时间', width=16,relief = GROOVE)
			self.sta_label.grid(column =1, padx = 10, row = 12)
			self.sta_display = Label(self.group1, textvariable=self.osc_staytime, width=16,relief = SUNKEN)
			self.sta_display.grid(column =1, padx = 10, row = 13)
			self.osc_num_label.grid(column =1, padx = 10, row = 14)
			self.osc_num_entry.grid(column =1, padx = 10, row = 15)
			for x in range(1,self.osc_num.get()+1):
				if x==1:
					self.osc_Entry1.grid(column = 1, padx = 10, row =x+15 , sticky = W)
				elif x==2:
					self.osc_Entry2.grid(column = 1, padx = 10, row =x+15 , sticky = W)
				elif x==3:
					self.osc_Entry3.grid(column = 1, padx = 10, row =x+15 , sticky = W)
				elif x==4:
					self.osc_Entry4.grid(column = 1, padx = 10, row =x+15 , sticky = W)
				elif x==5:
					self.osc_Entry5.grid(column = 1, padx = 10, row =x+15 , sticky = W)
				else:
					pass

		else:
			self.str_int.set('normal')
			self.osc_int.set('disabled')
			self.str_label = Label(self.group1, text='行程曲线设置', width=16,relief = GROOVE,
				state=self.str_int.get())
			self.str_label.grid(column =2, padx = 10, row = 11)
			self.osc_label = Label(self.group1, text='振荡曲线设置', width=16,relief = GROOVE,
				state=self.osc_int.get())
			self.osc_label.grid(column =1, padx = 10, row = 11)
			self.str_Entry1.grid(column = 2, padx = 10, row = 12, sticky = W)
			self.str_Entry2.grid(column = 2, padx = 10, row = 13, sticky = W)

	def START_ME(self):
		if self.mode_int.get()==1:
			wirtedata_list=[]
			for x in range(self.osc_num.get()):
				wirtedata_list.append(self.osc_data[x].get())
			if self.ic_int.get()=='9800':
				staytime,position=laser_measure.SC9800_osc_measure(*wirtedata_list)
			elif self.ic_int.get()=='9714':
				staytime,position=laser_measure.SC9714_osc_measure(*wirtedata_list)
			elif self.ic_int.get()=='9714V' and self.str_9714v_mode.get()=='Normal':
				staytime,position=laser_measure.SC9714_osc_measure(*wirtedata_list,S4=self.method_reg1.get())
			else:
				staytime,position=laser_measure.SC9714V_Advanced_osc_measure(*wirtedata_list)

				
			self.osc_staytime.set(staytime)
			#self.sta_display = Label(self.group1, textvariable=self.osc_staytime, width=16,relief = SUNKEN)
			#self.sta_display.grid(column =0, padx = 10, row = 2)
			messagebox.showinfo('Message', '振荡曲线读取成功')
			oscnum=[i*0.1  for i in range(len(position))]
			plt.title("The OSC curves of voice motor")
			plt.plot(oscnum,position,label=self.af_mode_variable.get())
			plt.grid()
			plt.ylabel('delta(um)')
			plt.xlabel('time(ms)')
			#plt.ylim(-150,300)
			plt.legend()
			plt.show()
		else:
			if self.ic_int.get()=='9800':
				position1=laser_measure.SC9800_stroke_measure(self.str_data[0].get(),self.str_data[1].get())
			elif self.ic_int.get()=='9714':
				position1=laser_measure.SC9714_stroke_measure(self.str_data[0].get(),self.str_data[1].get())
			elif self.ic_int.get()=='9714V' and self.str_9714v_mode.get()=='Normal':
				position1=laser_measure.SC9714_stroke_measure(self.str_data[0].get(),self.str_data[1].get())
			else:
				position1=laser_measure.SC9714V_Advanced_stroke_measure(self.str_data[0].get(),self.str_data[1].get())
			messagebox.showinfo('Message', '行程曲线读取成功')
			strdac=list(range(self.str_data[0].get(),self.str_data[1].get()+1))
			plt.title("The STR curves of voice motor")
			plt.plot(strdac,position1,label=self.af_mode_variable.get())
			plt.grid()
			plt.ylabel('delta(um)')
			plt.xlabel('dac')
			#plt.ylim(-150,300)
			plt.legend()
			plt.show()
			
	def changemode(self,master):
		if laser_measure.I2C_Open_Ok==0:
			messagebox.showinfo('Message', '请打开I2C')
		else:
			if self.ic_int.get()=='9800':
				a=laser_measure.Shift_9800_Mode(self.af_mode_variable.get())
			elif self.ic_int.get()=='9714V' and self.str_9714v_mode.get()=='Advanced':
				a=laser_measure.Shift_9714V_Ad_Mode(self.af_mode_variable.get(),
					self.method_reg1.get(),self.method_reg3.get(),self.method_reg2.get())
			else:
				a=laser_measure.Shift_9714_Mode(self.af_mode_variable.get(),self.method_reg2.get(),self.method_reg3.get())
			if a==self.af_mode_variable.get():
				pass
			else:
				messagebox.showinfo('Message', '设置芯片模式失败')






#'''1------------------------app根窗口---------------------'''	
root=Tk()
myapp=App(root)

myapp.master.title('VCM_TEST_PROGRAM_V3.0')
root.update() # update window , must do
curWidth = 1120#root.winfo_reqwidth() # get current width
curHeight = 650#root.winfo_height() # get current height
scnWidth, scnHeight = root.maxsize() # get screen width and height
# now generate configuration information
tmpcnf = '%dx%d+%d+%d'%(curWidth, curHeight, (scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
root.geometry(tmpcnf)
myapp.mainloop()
