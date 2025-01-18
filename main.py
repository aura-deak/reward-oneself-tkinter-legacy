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
from filehandler import FileHandler
import ai
import get_api
import sparkAPI
import hitokoto

report = FileHandler("interdoction/report.html")
datafile = FileHandler("data/data.reward")

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

def create_subwindow(items,name="子窗口",allow_cancel=True):
    # 创建子窗口
    subwindow = tkinter.Toplevel(root)
    subwindow.title(name)
    subwindow.attributes('-topmost', 'true')
    # 计算窗口高度
    window_height = 50 + 30 * len(items)  # 每个项目占用30像素，加上标题栏的50像素
    subwindow.geometry(f"300x{window_height}")

    
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
    return value

def create_multiple_subwindow(items,name="子窗口",allow_cancel=True):
    subwindow = tkinter.Toplevel(root)
    subwindow.title(name)
    subwindow.attributes('-topmost', 'true')
    values = {}
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
        if len(value) == 0 and not allow_cancel:
            messagebox.showerror("错误", "请选择一个选项",parent=subwindow)
            return
        subwindow.destroy()
    def cancel():
        subwindow.destroy()
        return

    submit_button = ttk.Button(subwindow, text="提交", command=submit)
    submit_button.grid(row=len(items), column=0, columnspan=2, pady=10)
    if allow_cancel:
        cancel_button = ttk.Button(subwindow, text="取消", command=cancel)
        cancel_button.grid(row=len(items), column=3, columnspan=2, pady=10)
    subwindow.wait_window()
    return value
    

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
        'reward_experience' : reward.reward_experience,
        'hitokoto_url' : hitokoto_url
    }
    datafile.overwrite(str(data))
    
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
            'priority_list_of_tasks': {'阅读': 2},
            'repetition_list_of_tasks': {'阅读': True},
            'tasks_effort_count' : {"阅读":0},
            'reward_count' : {"喝奶茶":0},
            'effort_experience' : {"阅读":[]},
            'reward_experience' : {"喝奶茶":[]},
            'hitokoto_url' : "https://v1.hitokoto.cn/?c=d&c=i&c=k&encode=text"
        }
        datafile.overwrite(str(data))
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
    for value in answer:
        hitokoto_url += c[value]
    hitokoto_url += "encode=text"
    fresh_and_save()

class Tasks():
    def __init__(self):
        self.tasks = eval(datafile.read())["tasks"]
        self.priority_list_of_tasks = eval(datafile.read())["priority_list_of_tasks"]
        self.repetition_list_of_tasks = eval(datafile.read())["repetition_list_of_tasks"]
        self.tasks_effort_count = eval(datafile.read())["tasks_effort_count"]
        self.effort_experience = eval(datafile.read())["effort_experience"]
    def get_keys(self):
        return self.tasks.keys()
    def get_value(self,key):
        return self.tasks[key]
    def get_priority(self,key):
        return self.priority_list_of_tasks[key]
    def get_repetition(self,key):
        return self.repetition_list_of_tasks[key]
    def add(self):
        key = askstring("添加任务","请输入任务名称")
        value = askinteger("添加任务","请输入任务分数")
        if key in self.tasks:
            messagebox.showwarning("添加任务",f"{key}已存在")
        else:
            query = f"任务名：{key}，请为该任务添加优先级和是否重复，优先级从高到低为3,2,1。是否重复为True或False，True为长期性、重复性任务、False为短期、一次性任务。使用{{'priority':优先级,'repetition':是否重复}}格式回答"
            while True:
                answer = ai.ai(query)
                try:
                    answer = eval(answer)
                    priority = answer["priority"]
                    repetition = answer["repetition"]
                except:
                    continue
                else:
                    break
            if not messagebox.askyesno("是否使用智能匹配？", f"是否使用智能匹配？匹配到的优先级为{priority}，重复为{repetition}"):
                priority = create_subwindow([1,2,3],name="添加任务优先级",allow_cancel=False)
                repetition = messagebox.askyesno("添加任务","是否为重复任务")
            self.tasks[key] = value
            self.priority_list_of_tasks[key] = priority
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
            if showinfo:
                messagebox.showinfo("删除任务",f"删除{key}成功")
            fresh_and_save()
        else:
            messagebox.showwarning("删除任务",f"{key}不存在")

class Rewards():
    def __init__(self):
        self.rewards = eval(datafile.read())["rewards"]
        self.reward_count = eval(datafile.read())["reward_count"]
        self.reward_experience = eval(datafile.read())["reward_experience"]
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
        for key in self.data.get_keys():
            if len(self.columns) == 2:
                self.tree.insert("", "end", values=(key,self.data.get_value(key)))
            else:
                self.tree.insert("", "end", values=(key,self.data.get_value(key), self.data.get_priority(key), self.data.get_repetition(key)))





root = tkinter.Tk()
root.title("奖励自己")
root.geometry("800x650")
root.resizable(False, False)

try:
    data = eval(datafile.read())
    point = data["point"]
except FileNotFoundError:
    reset(showinfo=False)
    sys.exit()

hitokoto_url = data["hitokoto_url"]

api = FileHandler("data/api.txt")
if not api.check():
    get_api.get_api_credentials()


reward = Rewards()
task = Tasks()

displayer = PointDisplayer(root)
rewards_table = Table(root,("奖励项","分值"),(0,50),reward)
tasks_table = Table(root,("努力项","分值","优先级","重复"),(400,50),task)
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

report_button = tkinter.ttk.Button(root, text="生成报告", command=ai.make_report)
report_button.place(x=710,y=600)

root.mainloop()