#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox as ms
from tkinter import simpledialog as sim
from tkinter import ttk
import os
import sys
import random as r
import webbrowser
from datetime import datetime as dt


# 获取当前脚本所在的文件夹路径
文件路径 = os.path.dirname(os.path.abspath(__file__))

# 构建HTML文件的绝对路径
index_html = os.path.join(文件路径, 'interdoction/index.html')
# 构建 report.html 文件的绝对路径
report = os.path.join(文件路径, f'interdoction/report.html')
# 构建 日报生成.py 文件的绝对路径
日报生成 = os.path.join(文件路径, '日报生成.py')
# 构建 data/datas.reward 文件的绝对路径
数据文件 = os.path.join(文件路径, f'data/data.reward')
# 构建 tasks_file.txt 文件的绝对路径
tasks_file = os.path.join(文件路径, 'data/tasks.txt')


def 检验变量(变量):
    if 变量 != None and 变量 != "":
        return True
    else:
        return False

def 保存():
    with open(数据文件,mode="w",encoding="utf-8") as d:
        数据 = {}
        数据["努力项"] = 努力项
        数据["奖励项"] = 奖励项
        数据["努力项实现次数"] = 努力项实现次数
        数据["奖励项兑换次数"] = 奖励项兑换次数
        数据["积分"] = 积分
        数据["努力心得"] = 努力心得
        数据["奖励心得"] = 奖励心得
        数据["努力优先级列表"] = 努力优先级列表
        数据["努力重复列表"] = 努力重复列表
        d.write(str(数据))
        
def 重置():
    if ms.askyesno("是否重置？", "是否重置？该操作不可撤销！", icon=ms.WARNING):
        os.remove(数据文件)
        os.remove(report)

        #清除密码
        # 构建data_file.txt文件的绝对路径
        data_file = os.path.join(文件路径, 'data/passwd_file.txt')
        with open(data_file,mode="r",encoding="utf-8") as d:
            username_passwd_data = d.read()
            username_passwd_data = eval(username_passwd_data)
        with open(data_file,mode="w",encoding="utf-8") as d:
            del username_passwd_data[username]
            d.write(str(username_passwd_data))


        print(username_passwd_data)
        d.write(str(username_passwd_data))
        ms.showinfo("重置成功","重置成功，请重启程序")
        sys.exit()
    else:
        ms.showinfo("重置取消","已取消")


def 展示介绍():
    # 使用默认浏览器打开HTML文件
    webbrowser.open('file://' + index_html)


def 刷新表格():
    for i in 奖励表格.get_children():
        奖励表格.delete(i)
    
    for key,value in 奖励项.items():
        奖励表格.insert("", "end", values=(key, value))

    for i in 努力表格.get_children():
        努力表格.delete(i)

    a = 0
    for key,value in 努力项.items():
        if 努力重复列表[key]:
            循环 = "是"
        else:
            循环 = "否"

        if 努力优先级列表[key] >= a:
            努力表格.insert("", 0, values=(key, value ,努力优先级列表[key] ,循环))
        else:
            努力表格.insert("", "end", values=(key, value ,努力优先级列表[key] ,循环))
        a = 努力优先级列表[key]
def 添加奖励():
    奖励 = sim.askstring("添加奖励","奖励名称",parent=root)
    分值 = sim.askinteger("添加奖励","奖励分值",parent=root)
    if 检验变量(奖励) and 检验变量(分值):
        奖励项[奖励] = 分值
        奖励项兑换次数[奖励] = 0
        奖励心得[奖励] = []
        刷新表格()
        ms.showinfo("添加奖励","添加完成")
    保存()

def 删除奖励():
    奖励 = sim.askstring("删除奖励","奖励名称",parent=root)
    try:
        del 奖励项[奖励]
        刷新表格()
        ms.showinfo("删除奖励","删除成功")
        保存()
    except KeyError:
        if 检验变量(奖励):
            ms.showwarning("删除奖励",f"{奖励}不存在！")

def 兑换奖励():
    global 积分
    ms.showinfo("兑换奖励",f"你目前的积分是{积分}")
    奖励 = sim.askstring("兑换奖励","奖励名称",parent=root)
    try:
        兑换所需积分 = 奖励项[奖励]
    except KeyError:
        if 检验变量(奖励):
            ms.showwarning("兑换奖励",f"{奖励}不存在！")
    else:
        if 积分 >= 兑换所需积分:
            积分 -= 兑换所需积分
            奖励项兑换次数[奖励] += 1
            ms.showinfo("兑换奖励",f"兑换{奖励}成功！你目前的积分是{积分}")
            奖励心得[奖励].append(sim.askstring("奖励心得","在此输入你要记录的信息\n(可以是心得、兑换时间等，也可以什么都不填)",parent=root))
            保存()
        else:
            ms.showwarning("兑换奖励",f"兑换{奖励}失败！兑换{奖励}需要{兑换所需积分}，你目前的积分是{积分}")

def 添加努力():
    努力 = sim.askstring("添加努力","努力名称",parent=root)
    分值 = sim.askinteger("添加努力","努力分值",parent=root)

    global 优先级
    优先级 = 0
    def button_action(num):
        global 优先级
        优先级 = num
        print(优先级)
        dialog.destroy()

    for key, value in tasks.items():
        if key in 努力:
            优先级 = value["优先级"]
            重复 = value["重复"]
            if ms.askyesno("智能匹配",f"已经智能匹配到以下信息：\n优先级：{优先级}\n重复：{重复}\n请问是否采用该配置"):
                break
            else:
                continue
    else:
        dialog = tk.Toplevel(root)
        dialog.title("选择优先级")
        dialog.geometry("300x50")
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        高优先级按钮 = tk.ttk.Button(dialog,text="高优先级",command= lambda: button_action(3))
        高优先级按钮.place(x=0,y=0)
        中优先级按钮 = tk.ttk.Button(dialog,text="中优先级",command= lambda: button_action(2))
        中优先级按钮.place(x=100,y=0)
        低优先级按钮 = tk.ttk.Button(dialog,text="低优先级",command= lambda: button_action(1))
        低优先级按钮.place(x=200,y=0)
        root.wait_window(dialog)
        重复 = ms.askyesno("是否重复", "是否重复\n（如果该任务只需要执行一次，那么请选择否，否则选择是）") 

    if 检验变量(努力) and 检验变量(分值):
        努力项[努力] = 分值
        努力项实现次数[努力] = 0
        努力心得[努力] = []
        努力优先级列表[努力] = 优先级
        努力重复列表[努力] = 重复
        刷新表格()
        ms.showinfo("添加努力","添加完成")
    保存()

def 删除努力():
    努力 = sim.askstring("删除努力","努力名称",parent=root)
    try:
        del 努力项[努力]
        del 努力优先级列表[努力]
        del 努力重复列表[努力]
        刷新表格()
        ms.showinfo("删除努力","删除成功")
        保存()
    except KeyError:
        if 检验变量(努力):
            ms.showwarning("删除努力",f"{努力}不存在！")

def 兑换努力():
    global 积分
    ms.showinfo("兑换努力",f"你目前的积分是{积分}")
    努力 = sim.askstring("兑换努力","努力名称",parent=root)
    try:
        加分 = 努力项[努力]
    except KeyError:
        if 检验变量(努力):
            ms.showwarning("兑换努力",f"{努力}不存在！")
    else:
        积分 += 加分
        努力项实现次数[努力] += 1
        ms.showinfo("兑换努力",f"兑换{努力}成功！你目前的积分是{积分}")
        努力心得[努力].append(sim.askstring("努力心得","在此输入你要记录的信息\n(可以是心得、兑换时间等，也可以什么都不填)",parent=root))

        if not 努力重复列表[努力]:
            del 努力项[努力]
            del 努力优先级列表[努力]
            del 努力重复列表[努力]
            刷新表格()
            ms.showinfo("删除努力","由于该任务没有设置重复，现已被删除")

        保存()

def 生成努力日报():

    with open(日报生成, "r", encoding="utf-8") as file:
        exec(file.read())
    #重置数据
    for i in 奖励项兑换次数:
        奖励项兑换次数[i] = 0
    for i in 努力项实现次数:
        努力项实现次数[i] = 0
    保存()
    # 使用默认浏览器打开HTML文件
    webbrowser.open('file://' + report)



root = tk.Tk()
root.title("智能任务管理系统 星空2.8")
root.geometry("800x600")
root.maxsize(width=800,height=600)

#读取文件，如果文件不存在则初始化
try:

    with open(数据文件,mode="r",encoding="utf-8") as d:
        数据 = d.read()
        数据 = eval(数据)
        努力项 = 数据["努力项"]
        奖励项 = 数据["奖励项"]
        努力项实现次数 = 数据["努力项实现次数"]
        奖励项兑换次数 = 数据["奖励项兑换次数"]
        积分 = 数据["积分"]
        努力心得 = 数据["努力心得"]
        奖励心得 = 数据["奖励心得"]
        努力优先级列表 = 数据["努力优先级列表"]
        努力重复列表 = 数据["努力重复列表"]

        
except:

    努力项 = {'阅读': 5}
    奖励项 = {'喝奶茶': 1}
    努力项实现次数 = {'阅读': 0}
    奖励项兑换次数 = {'喝奶茶': 0}
    积分 = 0
    努力心得 = {'阅读':[]}
    奖励心得 = {'喝奶茶':[]}
    努力优先级列表 = {"阅读" : 2}
    努力重复列表 = {"阅读" : True}
    保存()

    with open(report,mode="w",encoding="utf-8") as report:
        report.write("")


    ms.showinfo("初始化成功","初始化成功，请重启程序")
    sys.exit()
else:

    with open(tasks_file,encoding="utf-8") as d:
        tasks =  d.read()
        tasks = eval(tasks)

    

奖励表格 = ttk.Treeview(root, columns=("key", "value"), show="headings")
奖励表格.heading("key", text="奖励项")
奖励表格.heading("value", text="分值")
奖励表格.column("key", width=200, minwidth=200, anchor='center')
奖励表格.column("value", width=200, minwidth=200, anchor='center')
奖励表格.place(x=0,y=0,width=400,height=400)

努力表格 = ttk.Treeview(root, columns=("key", "value", "priority", "repetition"), show="headings")
努力表格.heading("key", text="努力项")
努力表格.heading("value", text="分值")
努力表格.heading("priority", text="优先级")
努力表格.heading("repetition", text="重复")
努力表格.column("key", width=100, minwidth=100, anchor='center')
努力表格.column("value", width=100,anchor='center')
努力表格.column("priority", width=100,anchor='center')
努力表格.column("repetition", width=100, anchor='center')
努力表格.place(x=400,y=0,width=400,height=400)

刷新表格()

添加奖励按钮 = tk.ttk.Button(root,text="添加奖励",command=添加奖励)
添加奖励按钮.place(x=0,y=400,width=400)

删除奖励按钮 = tk.ttk.Button(root,text="删除奖励",command=删除奖励)
删除奖励按钮.place(x=0,y=430,width=400)

兑换奖励按钮 = tk.ttk.Button(root,text="兑换奖励",command=兑换奖励)
兑换奖励按钮.place(x=0,y=460,width=400)

添加努力按钮 = tk.ttk.Button(root,text="添加努力",command=添加努力)
添加努力按钮.place(x=400,y=400,width=400)

删除努力按钮 = tk.ttk.Button(root,text="删除努力",command=删除努力)
删除努力按钮.place(x=400,y=430,width=400)

兑换努力按钮 = tk.ttk.Button(root,text="兑换努力",command=兑换努力)
兑换努力按钮.place(x=400,y=460,width=400)

重置按钮 = tk.ttk.Button(root,text="重置",command=重置)
重置按钮.place(x=0,y=500)

介绍按钮 = tk.ttk.Button(root,text="查看介绍",command=展示介绍)
介绍按钮.place(x=700,y=550)

日报按钮 = tk.ttk.Button(root,text="生成日报",command=生成努力日报)
日报按钮.place(x=700,y=500)

root.mainloop()