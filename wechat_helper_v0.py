#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-26 12:14:26
# @Author  : ${guoshengkang} (${kangguosheng1@gmail.com})
import tkinter # 默认显示宋体
import tkinter.messagebox
import tkinter.font as tkFont
from tkinter import scrolledtext
from tkinter import ttk
from wxpy import *
import re
import os

##############################################
def mClick():
	'''获取微信群成员按钮事件'''
	global monty
	if monty.winfo_exists():
		monty.destroy()
	if txt1.get()=='':
		tkinter.messagebox.showinfo('提示','请输入群名称！')
		return
	mygroups=groups.search(txt1.get()) # 搜索群
	if len(mygroups)==0:
		tkinter.messagebox.showerror('错误','没有该群名称，请输入正确的群名称！')
	elif len(mygroups)>1:
		r0='<Group: (.*?)>' # <Group: 学生之家>
		group_names=[]
		for group in mygroups:
			group_name=re.search(r0,str(group)).group(1)
			group_names.append(group_name)
		tkinter.messagebox.showerror('错误','搜索到多个{}群:{}，请输入精确的群名称！'.format(len(group_names),group_names))
	else: # len(mygroups)==1
		r0='<Group: (.*?)>' # <Group: 学生之家>
		group_name=re.search(r0,str(mygroups[0])).group(1)
		# 过滤掉一些图标符号，否则不能显示，会报错
		group_name = [group_name[j] for j in range(len(group_name)) if ord(group_name[j]) in range(65536)]
		group_name=''.join(group_name)
		monty=ttk.Labelframe(win,text=group_name+"-微信群成员({})".format(len(mygroups[0])))
		monty.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
		inner_monty1=ttk.Labelframe(monty)
		inner_monty1.grid(column=1,rowspan=2,padx=10,pady=10)
		inner_monty2=ttk.Labelframe(monty)
		inner_monty2.grid(row=2,columnspan=2)
		global menbers
		menbers=mygroups[0] # 注意：menbers不支持索引，即不能使用menbers[k]形式
		r1='<Member: (.*?)>' # <Member: 赵华杰>
		# 复选框
		chVarDis=tkinter.IntVar()
		num=len(menbers)
		global radVar # 定义单选框状态变量
		radVar=tkinter.IntVar()
		txts=['全   选','全不选']
		for i in range(2):
			curRad=tkinter.Radiobutton(monty,text=txts[i],variable=radVar,value=i,command=radCall)
			curRad.grid(column=0,row=0+i,sticky=tkinter.E)
		global variables # 定义复选框状态变量
		variables=[] # 群昵称->备注->昵称
		for k,member in enumerate(menbers):
			result=re.search(r1,str(member))
			name=result.group(1)
			name = [name[j] for j in range(len(name)) if ord(name[j]) in range(65536)]
			name=''.join(name)
			variables.append(tkinter.IntVar())
			check=tkinter.Checkbutton(inner_monty1,text=name,variable=variables[k])
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
			# print(variables[k].get())
		inputMsg=tkinter.Label(inner_monty2,text='输入发送信息:')
		inputMsg.grid(column=0,row=0)
		global scr
		scr=scrolledtext.ScrolledText(inner_monty2,font=('微软雅黑','16'),width=30,height=5) #,width=30,height=5
		scr.grid(column=1,row=0,columnspan=2)
		send_button=tkinter.Button(inner_monty2,text='发送',command=senMsg)
		send_button.grid(column=3,row=0)

def radCall():
	'''单选框事件'''
	radSel=radVar.get()
	if radSel==0:
		for var in variables:
			var.set(1)
	else:
		for var in variables:
			var.set(0)

def senMsg():
	'''发送按钮事件'''
	selects=[var.get() for var in variables]
	member_num=sum(selects)
	msg=scr.get('1.0', 'end-1c') # 获取滚动框文本
	if len(msg)==0:
		tkinter.messagebox.showinfo('提示','请输入要发送的消息！')
	elif msg==' '*len(msg):
		tkinter.messagebox.showwarning('提示','不能发送空白消息，请重新输入要发送的消息！')
	elif member_num==0:
		tkinter.messagebox.showinfo('提示','您为选定任何好友！')
	else:
		# 确定是否发送信息
		yesNo=tkinter.messagebox.askokcancel('提示','您已选定{}个好友，确定要发送吗？'.format(member_num))
		if yesNo is True: 
			# 发送消息
			success_num=0
			failure_num=0
			for k,menber in enumerate(menbers):
				if variables[k].get()==1:
					try:
						menber.send(msg) # 给群里每个人发送信息，不是好友，不能发送成功
						success_num=success_num+1
					except:
						failure_num=failure_num+1
			tkinter.messagebox.showinfo('提示','消息已发送！{}个发送成功，{}个发送失败！'.format(success_num,failure_num))		
##################################################################
# 扫码登录微信
bot=Bot(cache_path=True)
groups=bot.groups() #获取所有群 
# 创建窗体对象
win=tkinter.Tk()
# win.iconbitmap("C:\\test\\wechat_helper.ico") # 设置窗口图标
win.resizable(False,False) # 不允许改变窗口大小
# 定义窗体标题
win.title('微信群群发助手')
# 设置初始窗体的大小（宽x高）和位置（x,y）
win.geometry()
# 定义标签
L1=tkinter.Label(win,text='----欢迎来到微信群发助手----',font=('宋体','10'),fg='#0000ff')
L2=tkinter.Label(win,text='请输入群名称:')
txt1=tkinter.StringVar()
E1=tkinter.Entry(win,textvariable=txt1)
B1=tkinter.Button(win,text='获取微信群成员',command=mClick)
# 布局设置
L1.grid(row=0,columnspan=3)
L2.grid(row=1,column=0)
E1.grid(row=1,column=1)
B1.grid(row=1,column=2)
# 创建一个标签框架容器
monty=ttk.Labelframe(win,text='')
monty.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
# 表示事件循坏，使窗体一直保持显示状态
win.mainloop()
