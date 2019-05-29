#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-26 12:14:26
# @Author  : ${guoshengkang} (${kangguosheng@gmail.com})
import tkinter # 默认显示宋体
import tkinter.messagebox
import tkinter.font as tkFont
from tkinter import scrolledtext
from tkinter import ttk
from wxpy import *
import re
import os

class sendMsgToGroupMembers:
	'''给微信群成员发信息'''
	def __init__(self):
		# 扫码登录微信
		self.bot=Bot(cache_path=True)
		self.groups=self.bot.groups() # 获取所有群 (需保存到通讯录的群才能找到)
		self.mygroups=None # 定义搜索到的微信群
		self.radVar=None # 定义单选框状态变量
		self.variables=None # 定义复选框状态变量
		# 创建窗体对象
		self.win=tkinter.Tk()
		# self.win.iconbitmap("C:\\test\\wechat_helper.ico") # 设置窗口图标
		self.win.resizable(False,False) # 不允许改变窗口大小
		# 定义窗体标题
		self.win.title('微信群群发助手')

		# 设置初始窗体的大小（宽x高）和位置（x,y）
		self.win.geometry()
		# 定义标签
		self.L1=tkinter.Label(self.win,text='----欢迎来到微信群发助手----',font=('宋体','10'),fg='#0000ff')
		self.L2=tkinter.Label(self.win,text='请输入群名称:')
		self.txt1=tkinter.StringVar()
		self.E1=tkinter.Entry(self.win,textvariable=self.txt1)
		self.B1=tkinter.Button(self.win,text='获取微信群成员',command=self.mClick)
		# 布局设置
		self.L1.grid(row=0,columnspan=3)
		self.L2.grid(row=1,column=0)
		self.E1.grid(row=1,column=1)
		self.B1.grid(row=1,column=2)
		# 创建一个标签框架容器
		self.monty=ttk.Labelframe(self.win,text='')
		self.monty.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
		# 表示事件循坏，使窗体一直保持显示状态
		self.win.mainloop()		

	def mClick(self):
		'''获取微信群成员按钮事件'''
		if self.monty.winfo_exists(): # 消除标签框架容器，后续重建
			self.monty.destroy()
		if self.txt1.get()=='':
			tkinter.messagebox.showinfo('提示','请输入群名称！')
			return
		self.mygroups=self.groups.search(self.txt1.get()) # 搜索群
		if len(self.mygroups)==0:
			tkinter.messagebox.showerror('错误','没有该群名称，请输入正确的群名称！')
		elif len(self.mygroups)>1:
			r0='<Group: (.*?)>' # <Group: 学生之家>
			group_names=[]
			for group in self.mygroups:
				group_name=re.search(r0,str(group)).group(1)
				group_name = [group_name[j] for j in range(len(group_name)) if ord(group_name[j]) in range(65536)]
				group_name=''.join(group_name)
				group_names.append(group_name)
			tkinter.messagebox.showerror('错误','搜索到多个{}群:{}，请输入精确的群名称！'.format(len(group_names),group_names))
		else: # len(mygroups)==1
			r0='<Group: (.*?)>' # <Group: 学生之家>
			group_name=re.search(r0,str(self.mygroups[0])).group(1) # 获取群名称
			# 过滤掉一些图标符号，否则不能显示，会报错
			group_name = [group_name[j] for j in range(len(group_name)) if ord(group_name[j]) in range(65536)]
			group_name=''.join(group_name)
			self.monty=ttk.Labelframe(self.win,text=group_name+"-微信群成员({})".format(len(self.mygroups[0])))
			self.monty.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
			inner_monty1=ttk.Labelframe(self.monty)
			inner_monty1.grid(column=1,rowspan=2,padx=10,pady=10)
			inner_monty2=ttk.Labelframe(self.monty)
			inner_monty2.grid(row=2,columnspan=2)
			menbers=self.mygroups[0] # 注意：menbers不支持索引，即不能使用menbers[k]形式
			r1='<Member: (.*?)>' # <Member: 赵华杰>
			# 复选框
			chVarDis=tkinter.IntVar()
			num=len(menbers)
			self.radVar=tkinter.IntVar()
			txts=['全   选','全不选']
			for i in range(2):
				curRad=tkinter.Radiobutton(self.monty,text=txts[i],variable=self.radVar,value=i,command=self.radCall)
				curRad.grid(column=0,row=0+i,sticky=tkinter.E)
			self.variables=[] # 群昵称->备注->昵称
			for k,member in enumerate(menbers):
				result=re.search(r1,str(member))
				name=result.group(1)
				name = [name[j] for j in range(len(name)) if ord(name[j]) in range(65536)]
				name=''.join(name)
				self.variables.append(tkinter.IntVar())
				check=tkinter.Checkbutton(inner_monty1,text=name,variable=self.variables[k])
				check.select()
				add_row=int(k/5)
				if k%5==0:
					check.grid(column=0,row=0+add_row,sticky=tkinter.W)
				elif k%5==1:
					check.grid(column=1,row=0+add_row,sticky=tkinter.W)
				elif k%5==2:
					check.grid(column=2,row=0+add_row,sticky=tkinter.W)
				elif k%5==3:
					check.grid(column=3,row=0+add_row,sticky=tkinter.W)
				else:
					check.grid(column=4,row=0+add_row,sticky=tkinter.W)
				# print(self.variables[k].get())
			inputMsg=tkinter.Label(inner_monty2,text='输入发送信息:')
			inputMsg.grid(column=0,row=0)
			global scr
			scr=scrolledtext.ScrolledText(inner_monty2,font=('微软雅黑','16'),width=30,height=5) #,width=30,height=5
			scr.grid(column=1,row=0,columnspan=2)
			send_button=tkinter.Button(inner_monty2,text='发送',command=self.senMsg)
			send_button.grid(column=3,row=0)

	def radCall(self):
		'''单选框事件'''
		radSel=self.radVar.get()
		if radSel==0:
			for var in self.variables:
				var.set(1)
		else:
			for var in self.variables:
				var.set(0)

	def senMsg(self,menbers=None):
		'''发送按钮事件'''
		selects=[var.get() for var in self.variables]
		member_num=sum(selects)
		msg=scr.get('1.0', 'end-1c') # 获取滚动框文本
		if len(msg)==0:
			tkinter.messagebox.showinfo('提示','请输入要发送的消息！')
		elif msg==' '*len(msg):
			tkinter.messagebox.showwarning('提示','不能发送空白消息，请重新输入要发送的消息！')
		elif member_num==0:
			tkinter.messagebox.showinfo('提示','您为选定任何好友！')
		else:
			menbers=self.mygroups[0]
			# 确定是否发送信息
			yesNo=tkinter.messagebox.askokcancel('提示','您已选定{}个群成员，确定要发送吗？'.format(member_num))
			if yesNo is True: 
				# 发送消息
				success_num=0
				failure_num=0
				for k,menber in enumerate(menbers):
					if self.variables[k].get()==1:
						try:
							menber.send(msg) # 给群里每个人发送信息，不是好友，不能发送成功
							success_num=success_num+1
						except:
							failure_num=failure_num+1
				tkinter.messagebox.showinfo('提示','消息已发送！{}个发送成功，{}个发送失败！'.format(success_num,failure_num))

# 测试代码
if __name__=='__main__':
	sendMsgToGroupMembers()
