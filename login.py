import os
import tkinter as tk
from tkinter import messagebox as ms
from tkinter import simpledialog as sim


# 获取当前脚本所在的文件夹路径
文件路径 = os.path.dirname(os.path.abspath(__file__))
# 构建data_file.txt文件的绝对路径
data_file = os.path.join(文件路径, 'data/passwd_file.txt')



def 获得输入(名称):
    while True:
        内容 = sim.askstring("登录",f"请输入{名称}")
        if 内容 != None and 内容 != "":
            break
        else:
            ms.showerror("登录",f"{名称}不能为空！")
    return 内容
        

def 新建用户(username):
    with open(data_file,mode="r",encoding="utf-8") as d:
        username_passwd_data = d.read()
        username_passwd_data = eval(username_passwd_data)
    with open(data_file,mode="w",encoding="utf-8") as d:
        ms.showinfo("登录",f"你将要创建一个新用户{username}")
        passwd = 获得输入(f"{username}的密码")
        username_passwd_data[username] = passwd
        d.write(str(username_passwd_data))
        ms.showinfo("登录",f"{username}注册成功")




while True:

    username = 获得输入("用户名")

    try:
        with open(data_file,mode="r",encoding="utf-8") as d:
            data = d.read()
            data = eval(data)
    except:
        with open(data_file,mode="w",encoding="utf-8") as d:
            d.write("{}")
        
        ms.showinfo("登录","该应用程序目前没有账户，现在进入新建用户向导")
        新建用户(username)
        break
    else:
        if not username in data.keys():
            if ms.askyesno("登录",f"{username}不在已有的用户中，是否新建？"):
                新建用户(username)
                break
        else:
            if 获得输入(f"{username}的密码") == data[username]:
                break
            else:
                ms.showwarning("登录","密码错误！")




