#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-26 12:14:26
# @Author  : ${guoshengkang} (${kangguosheng@gmail.com})
import sys
from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = "C:\\Anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Anaconda3\\tcl\\tk8.6"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["tkinter","idna.idnadata"], "optimize":1}
# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32": 
	base = "Win32GUI"
setup(name = "wechat_helper", 
	version = "0.1", 
	description = "My GUI application!", 
	options = {"build_exe": build_exe_options}, 
	executables = [Executable(script="wechat_helper.py",icon = "./wechat_helper.ico")]
	)

# Executable(script="wechat_helper.py",base=base)
# 注意：去掉 base="Win32GUI"，否则如下报错：
# AttributeError: 'NoneType' object has no attribute 'write' 