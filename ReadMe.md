## Motivation
1. 一般我们会有很多微信群，因此很多人会屏蔽微信群消息，即便@所有人，也不会看，或偶尔选择看一下，这样容易错过一些重要消息，因此为了让群成员看到消息，我们选择单独给每个群成员发，而不是发群消息。
2. 微信群中，有一些成员我们可能觉得他们不需要知道该消息，因此在给群成员发消息时，只选择需要的群成员发送，而非每个人都发，造成打扰。

## 使用包说明
+ Tkinter：Tkinter 是 Python 的标准 GUI 库,是python内置的安装包。
+ wxpy：pip wxpy opencv_python -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

## 打包成安装文件 **.msi
1. 安装cxfreeze：pip cxfreeze opencv_python -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
2. 新建[setup.py](setup.py)文件
3. cmd执行命令行：python setup.py bdist_msi

执行命令后生成两个文件夹：
+ build：免安装文件
+ dist：安装文件**.msi

## 软件使用说明
在安装目下，找到wechat_helper.exe，双击可以运行

首先会弹出命令行，提示扫码登录微信。然后，登录后会弹出窗口。
