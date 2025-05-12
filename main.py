import tkinter
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter import FLAT
from tkinter import font
import os
import sys
import random
import webbrowser
from datetime import datetime
import json
from filehandler import FileHandler
import xinghuoai
import get_api
import sparkAPI
import hitokoto

report = FileHandler("interdoction/report.html")
datafile = FileHandler("data/data.json")

def askstring(title, prompt, allow_empty=False):
    root.withdraw()
    while True:
        answer = simpledialog.askstring(title, prompt)
        if answer is None or answer == "" and not allow_empty:
            messagebox.showerror("错误", "输入不能为空")
        else:
            break
    root.deiconify()     
    return answer

def askinteger(title, prompt,max=float('inf'), min=0):
    root.withdraw()
    while True:
        answer = simpledialog.askinteger(title, prompt)
        if answer is None:
            messagebox.showerror("错误", "输入不能为空")
        elif answer > max or answer < min:
            messagebox.showerror("错误", f"输入必须在{min}和{max}之间")
        else:
            break
    root.deiconify() 
    return answer

def create_subwindow(items=None,dictionary=None,name="子窗口",allow_cancel=True):
    # 创建子窗口
    subwindow = tkinter.Toplevel(root)
    subwindow.title(name)
    subwindow.attributes('-topmost', 'true')
    if not allow_cancel:
        subwindow.protocol("WM_DELETE_WINDOW", lambda: None)

    if items == None:
        items = list(dictionary.keys())

    
    # 创建StringVar对象来存储选中的值
    selected_value = tkinter.StringVar()
    
    # 创建单选按钮
    for i, item in enumerate(items):
        radiobutton = ttk.Radiobutton(subwindow, text=item, variable=selected_value, value=item)
        radiobutton.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    
    # 提交按钮
    def submit():
        if selected_value.get() == "" and not allow_cancel:
            messagebox.showerror("错误", "请选择一个选项",parent=subwindow)
            return
        global value
        value = selected_value.get()
        subwindow.destroy()
    def cancel():
        global value
        value = ""
        subwindow.destroy()
    
    submit_button = ttk.Button(subwindow, text="提交", command=submit)
    submit_button.grid(row=len(items), column=0, columnspan=2, pady=10)
    if allow_cancel:
        cancel_button = ttk.Button(subwindow, text="取消", command=cancel)
        cancel_button.grid(row=len(items), column=3, columnspan=2, pady=10)
    subwindow.wait_window()
    if dictionary is None:
        return value
    else:
        return dictionary[value]

def create_multiple_subwindow(items=None,dictionary=None,name="子窗口",allow_cancel=True):
    global value
    value = []
    subwindow = tkinter.Toplevel(root)
    subwindow.title(name)
    subwindow.attributes('-topmost', 'true')
    if not allow_cancel:
        subwindow.protocol("WM_DELETE_WINDOW", lambda: None)

    values = {}

    if items is None:
        items = list(dictionary.keys())

    for i, item in enumerate(items):
        values[item] = tkinter.IntVar()
    for i, item in enumerate(items):
        checkbox = tkinter.Checkbutton(subwindow, text=item,variable=values[item], onvalue=1, offvalue=0)
        checkbox.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    def submit():
        global value
        value = []
        for i in values.keys():
            if values[i].get() == 1:
                value.append(i)
                
        # 修改判断逻辑
        if len(value) == 0:
            if not allow_cancel:
                messagebox.showerror("错误", "请选择一个选项",parent=subwindow)
                return  # 保持窗口打开
            else:
                value = []  # 显式设置为空列表
                
        subwindow.destroy()  # 仅在有效时关闭窗口
    def cancel():
        global value
        value = None
        subwindow.destroy()

    submit_button = ttk.Button(subwindow, text="提交", command=submit)
    submit_button.grid(row=len(items), column=0, columnspan=2, pady=10)
    if allow_cancel:
        cancel_button = ttk.Button(subwindow, text="取消", command=cancel)
        cancel_button.grid(row=len(items), column=3, columnspan=2, pady=10)
    subwindow.wait_window()
    # 修改最终返回逻辑
    if dictionary is None:
        return value  # 直接返回列表
    else:
        return [dictionary[i] for i in value]


def fresh_and_save():

    displayer.update()
    rewards_table.update()
    tasks_table.update()

    data = {
        'tasks': task.tasks,
        'rewards': reward.rewards,
        'point': point,
        'priority_list_of_tasks': task.priority_list_of_tasks,
        'repetition_list_of_tasks': task.repetition_list_of_tasks,
        'reward_count' : reward.reward_count,
        'tasks_effort_count' : task.tasks_effort_count,
        'effort_experience' : task.effort_experience,
        "tasks_time" : task.tasks_time,
        'reward_experience' : reward.reward_experience,
        'hitokoto_url' : hitokoto_url,
        'enable_ai' : enable_ai
    }
    datafile.write_as_json(data)
    
def reset(showinfo = True):
    if showinfo:
        condition = messagebox.askyesno("是否重置？", "是否重置？该操作不可撤销！", icon=messagebox.WARNING)
    else:
        condition = True

    if condition:
        data = {
            'tasks': {'阅读': 5},
            'rewards': {'喝奶茶': 1},
            'point': 0,
            'priority_list_of_tasks': {'阅读': 25},
            'repetition_list_of_tasks': {'阅读': True},
            'tasks_effort_count' : {"阅读":0},
            'reward_count' : {"喝奶茶":0},
            'effort_experience' : {"阅读":[]},
            'reward_experience' : {"喝奶茶":[]},
            'tasks_time' : {"阅读":60},
            'hitokoto_url' : "https://v1.hitokoto.cn/?c=d&c=i&c=k&encode=text",
            'enable_ai' : False
        }
        datafile.write_as_json(data)
        messagebox.showinfo("重置成功","重置成功，请重启程序")
        sys.exit()
    else:
        messagebox.showinfo("重置取消","已取消")

def change_hitokoto_url():
    global hitokoto_url
    c = {"动画": "c=a&","漫画": "c=b&","游戏": "c=c&","文学": "c=d&","原创": "c=e&","来自网络": "c=f&","其他": "c=g&","影视": "c=h&","诗词": "c=i&","网易云": "c=j&","哲学": "c=k&","抖机灵": "c=l&"}
    answer = create_multiple_subwindow(c.keys(),name="更改名言喜好",allow_cancel=False)

    global hitokoto_url
    hitokoto_url = "https://v1.hitokoto.cn/?"
    if not answer is None:
        for value in answer:
            hitokoto_url += c[value]
    hitokoto_url += "encode=text"
    fresh_and_save()

def change_optional_features():
    global enable_ai
    optionals = create_multiple_subwindow(["启用AI"],name="更改功能",allow_cancel=True)
    print(optionals)
    if optionals is not None:
        if "启用AI" in optionals:
            enable_ai = True
<<<<<<< HEAD
        else:
            enable_ai = False
=======
            print("启用AI")
        else:
            enable_ai = False
            print("禁用AI")
>>>>>>> 6816cf3273b22acbe9503404a43ff52a11bc0a6f
    fresh_and_save()
def ai():
    if enable_ai:
        xinghuoai.make_report()
    else:
        messagebox.showinfo("提示","AI功能未启用，请前往“可选功能”启用")
        
class Tasks():
    def __init__(self):
        self.tasks = data["tasks"]
        self.priority_list_of_tasks = data["priority_list_of_tasks"]
        self.repetition_list_of_tasks = data["repetition_list_of_tasks"]
        self.tasks_effort_count = data["tasks_effort_count"]
        self.effort_experience = data["effort_experience"]
        self.tasks_time = data["tasks_time"]
    def get_keys(self):
        return self.tasks.keys()
    def get_value(self,key):
        return self.tasks[key]
    def get_priority(self,key):
        return self.priority_list_of_tasks[key]
    def get_repetition(self,key):
        return self.repetition_list_of_tasks[key]
    def get_task_time(self,key):
        return self.tasks_time[key]
    def add(self):
        key = askstring("添加任务","请输入任务名称")
        value = askinteger("添加任务","请输入任务分数")
        if key in self.tasks:
            messagebox.showwarning("添加任务",f"{key}已存在")
        else:
            repetition = messagebox.askyesno("添加任务","是否为重复任务")

            importance_dictionary = {"不重要":1,"较重要":2,"重要":3,"很重要":4,"非常重要":float("inf")}
            importance = create_subwindow(dictionary=importance_dictionary,name="添加任务重要性",allow_cancel=False)

            urgency_dictionary = {"不紧急":1,"一般紧急":2,"紧急":3}
            urgency = create_subwindow(dictionary=urgency_dictionary,name="添加任务紧急度",allow_cancel=False)

            value_dictionary = {"低价值":1,"中价值":2,"高价值":3}
            value = create_subwindow(dictionary=value_dictionary,name="添加任务价值",allow_cancel=False)

            time = askinteger("添加任务","请输入任务时间")
            priority = 4*importance + 2*urgency + 3*value - time/10
            if priority == float("inf"):
                priority = "inf"
            else:
                priority = round(priority)
            self.tasks[key] = value
            self.priority_list_of_tasks[key] = priority
            self.tasks_time[key] = time
            self.repetition_list_of_tasks[key] = repetition
            self.tasks_effort_count[key] = 0
            self.effort_experience[key] = []
            fresh_and_save()

    def complete(self):
        global point
        key = create_subwindow(self.get_keys(),name="完成任务")
        if key == "":
            return
        self.tasks_effort_count[key] += 1
        self.effort_experience[key].append(askstring("完成任务","请输入心得体会",allow_empty=True))
        point += self.tasks[key]
        if not self.repetition_list_of_tasks[key]:
            self.delete(key, showinfo=False)
            messagebox.showinfo("完成任务",f"{key}没有重复，已删除")
        messagebox.showinfo("完成任务",f"完成{key}成功")
        fresh_and_save()
    def delete(self, key ="", showinfo = True):
        if key == "":
            key = create_subwindow(self.get_keys(),name="删除任务")
            if key == "":
                return
        if key in self.tasks:
            del self.tasks[key]
            del self.priority_list_of_tasks[key]
            del self.repetition_list_of_tasks[key]
            del self.tasks_time[key]
            if showinfo:
                messagebox.showinfo("删除任务",f"删除{key}成功")
            fresh_and_save()
        else:
            messagebox.showwarning("删除任务",f"{key}不存在")

class Rewards():
    def __init__(self):
        self.rewards = data["rewards"]
        self.reward_count = data["reward_count"]
        self.reward_experience = data["reward_experience"]
    def get_keys(self):
        return self.rewards.keys()
    def get_value(self,key):
        return self.rewards[key]
    def add(self):
        key = askstring("添加奖励","请输入奖励名称")
        value = askinteger("添加奖励","请输入奖励分数")
        if key in self.rewards:
            messagebox.showwarning("添加奖励",f"{key}已存在")
        else:
            self.rewards[key] = value
            self.reward_count[key] = 0
            self.reward_experience[key] = []
            fresh_and_save()
    def complete(self):
        global point
        key = create_subwindow(self.get_keys(),name="兑换奖励")
        if key == "":
            return
        if point >= self.rewards[key]:
            point -= self.rewards[key]
            messagebox.showinfo("兑换奖励",f"兑换{key}成功")
            self.reward_count[key] += 1
            self.reward_experience[key].append(askstring("兑换奖励","请输入心得体会",allow_empty=True))
            fresh_and_save()
        else:
            messagebox.showwarning("兑换奖励",f"兑换{key}失败，积分不足")
    def delete(self):
        key = create_subwindow(self.get_keys(),name="删除奖励")
        if key == "":
            return
        del self.rewards[key]
        messagebox.showinfo("删除奖励",f"删除{key}成功")
        fresh_and_save()

class PointDisplayer():
    def __init__(self, root):
        self.text_widget = tkinter.Text(root, relief=FLAT)
        self.text_widget.place(x=0,y=0,width=800)
        self.text_widget.insert("insert", "hello, world")
        self.my_font = font.Font(size=16)
        self.text_widget.tag_configure("center", justify='center', font=self.my_font)
        self.text_widget.tag_add("center", "1.0", "end")
    def update(self):
        global point
        self.text_widget.config(state=tkinter.NORMAL)
        self.text_widget.delete("1.0", tkinter.END)
        self.text_widget.insert("insert", f"当前分数为{point}\n{hitokoto.get_hitokoto(hitokoto_url)}")
        self.text_widget.tag_configure("center", justify='center',font=self.my_font)
        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tkinter.DISABLED)
class Table():
    def __init__(self,root,columns,place,data):
        self.data = data
        self.columns = columns
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for column in columns:
            self.tree.heading(column, text=column, anchor='center')
            self.tree.column(column, width=400//len(columns), anchor='center')
        self.tree.place(x=place[0],y=place[1],width=400,height=350)
    def update(self):
        self.tree.delete(*self.tree.get_children())
        count = 0
        if len(self.columns) == 2:
            for key in self.data.get_keys():
                self.tree.insert("", "end", values=(key,self.data.get_value(key)))
        else:
            dictionary = {}
            for i in self.data.get_keys():
                priority = self.data.get_priority(i)
                dictionary[i] = float("inf") if priority == "inf" else priority
            sorted_items = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
            lst = [item[0] for item in sorted_items]
            for i in lst:
                self.tree.insert("", "end", values=(i,self.data.get_value(i),self.data.get_priority(i),self.data.get_task_time(i),self.data.get_repetition(i)))

            


root = tkinter.Tk()
root.title("奖励自己")
root.geometry("800x650")
root.resizable(False, False)

root.protocol("WM_DELETE_WINDOW", sys.exit)

try:
    data = datafile.load()
    point = data["point"]
    enable_ai = data["enable_ai"]

except FileNotFoundError:
    reset(showinfo=False)
    sys.exit()

hitokoto_url = data["hitokoto_url"]


reward = Rewards()
task = Tasks()

displayer = PointDisplayer(root)
rewards_table = Table(root,("奖励项","分值"),(0,50),reward)
tasks_table = Table(root,("努力项","分值","优先级","时间","重复"),(400,50),task)
fresh_and_save()

add_reward_button = tkinter.ttk.Button(root, text="添加奖励", command=reward.add)
add_reward_button.place(x=0,y=400,width=400)
remove_reward_button = tkinter.ttk.Button(root, text="删除奖励", command=reward.delete)
remove_reward_button.place(x=0,y=450,width=400)
complete_reward_button = tkinter.ttk.Button(root, text="兑换奖励", command=reward.complete)
complete_reward_button.place(x=0,y=500,width=400)

add_task_button = tkinter.ttk.Button(root, text="添加任务", command=task.add)
add_task_button.place(x=400,y=400,width=400)
remove_task_button = tkinter.ttk.Button(root, text="删除任务", command=task.delete)
remove_task_button.place(x=400,y=450,width=400)
complete_task_button = tkinter.ttk.Button(root, text="完成任务", command=task.complete)
complete_task_button.place(x=400,y=500,width=400)

reset_button = tkinter.ttk.Button(root, text="重置", command=reset)
reset_button.place(x=0,y=550)

view_introduction_button = tkinter.ttk.Button(root, text="查看说明", command=lambda: webbrowser.open("https://gitee.com/chen-shuhan-1/reward-oneself/blob/master/README.md"))
view_introduction_button.place(x=710,y=550)

change_hitokoto_url_button = tkinter.ttk.Button(root, text="更改名言喜好", command=change_hitokoto_url)
change_hitokoto_url_button.place(x=0,y=600)

optional_features = tkinter.ttk.Button(root, text="可选功能", command=change_optional_features)
optional_features.place(x=355,y=600)  # 原位置x=0,y=500

report_button = tkinter.ttk.Button(root, text="生成报告", command=ai)
report_button.place(x=710,y=600)  # 保持原y坐标不变

root.mainloop()