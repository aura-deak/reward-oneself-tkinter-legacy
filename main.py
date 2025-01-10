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

index_html = FileHandler("interdoction/index.html")
report = FileHandler("interdoction/report.html")
daily_report = FileHandler("日报生成.py")
datafile = FileHandler("data/data.reward")
tasks_file = FileHandler("data/tasks.txt")
one = FileHandler("data/一言.txt")

def askstring(title, prompt):
    while True:
        answer = simpledialog.askstring(title, prompt)
        if answer is None or answer == "":
            messagebox.showerror("错误", "输入不能为空")
        else:
            break     
    return answer

def askinteger(title, prompt,max=float('inf'), min=0):
    while True:
        answer = simpledialog.askinteger(title, prompt)
        if answer is None:
            messagebox.showerror("错误", "输入不能为空")
        elif answer > max or answer < min:
            messagebox.showerror("错误", f"输入必须在{min}和{max}之间")
        else:
            break
    return answer

def fresh_and_save():

    displayer.update()
    rewards_table.update()
    tasks_table.update()

    data = {
        'tasks': task.tasks,
        'rewards': reward.rewards,
        'point': point,
        'priority_list_of_tasks': task.priority_list_of_tasks,
        'repetition_list_of_tasks': task.repetition_list_of_tasks
    }
    datafile.overwrite(str(data))
    
def reset():
    if messagebox.askyesno("是否重置？", "是否重置？该操作不可撤销！", icon=messagebox.WARNING):
        data = {
            'tasks': {'阅读': 5},
            'rewards': {'喝奶茶': 1},
            'point': 0,
            'priority_list_of_tasks': {'阅读': 2},
            'repetition_list_of_tasks': {'阅读': True}
        }
        datafile.overwrite(str(data))
        messagebox.showinfo("重置成功","重置成功，请重启程序")
        sys.exit()
    else:
        messagebox.showinfo("重置取消","已取消")

class Tasks():
    def __init__(self):
        self.tasks = eval(datafile.read())["tasks"]
        self.priority_list_of_tasks = eval(datafile.read())["priority_list_of_tasks"]
        self.repetition_list_of_tasks = eval(datafile.read())["repetition_list_of_tasks"]
        self.predefined_tasks = eval(tasks_file.read())
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
        elif key in self.predefined_tasks:
            print(self.predefined_tasks[key])
            property = eval(str(self.predefined_tasks[key]))["property"]
            repetition = eval(str(self.predefined_tasks[key]))["repetition"]
            if messagebox.askyesno("添加任务",f"智能匹配到任务{key}，是否采用？\n优先级为{property}，是否重复为{repetition}"):
                self.tasks[key] = value
                self.priority_list_of_tasks[key] = property
                self.repetition_list_of_tasks[key] = repetition
                fresh_and_save()
            else:
                property = askinteger("添加任务","请输入任务优先级（1-3）",max=3,min=1)
                repetition = messagebox.askyesno("添加任务","是否为重复任务")
                self.tasks[key] = value
                self.priority_list_of_tasks[key] = property
                self.repetition_list_of_tasks[key] = repetition
                fresh_and_save()
        else:
            property = askinteger("添加任务","请输入任务优先级（1-3）",max=3,min=1)
            repetition = messagebox.askyesno("添加任务","是否为重复任务")
            self.tasks[key] = value
            self.priority_list_of_tasks[key] = property
            self.repetition_list_of_tasks[key] = repetition
            fresh_and_save()
    def complete(self):
        global point
        key = askstring("完成任务","请输入任务名称")
        if key in self.tasks:
            if self.repetition_list_of_tasks[key]:
                point += self.tasks[key]
            else:
                self.delete(key)
                print("完成任务",f"{key}没有重复，已删除")
            messagebox.showinfo("完成任务",f"完成{key}成功")
            fresh_and_save()
        else:
            messagebox.showwarning("完成任务",f"{key}不存在")
    def delete(self, key =""):
        if key == "":
            key = askstring("删除任务","请输入任务名称")
        if key in self.tasks:
            del self.tasks[key]
            del self.priority_list_of_tasks[key]
            del self.repetition_list_of_tasks[key]
            messagebox.showinfo("删除任务",f"删除{key}成功")
            fresh_and_save()
        else:
            messagebox.showwarning("删除任务",f"{key}不存在")

class Rewards():
    def __init__(self):
        self.rewards = eval(datafile.read())["rewards"]
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
            fresh_and_save()
    def complete(self):
        global point
        key = askstring("兑换奖励","请输入奖励名称")
        if key in self.rewards:
            if point >= self.rewards[key]:
                point -= self.rewards[key]
                messagebox.showinfo("兑换奖励",f"兑换{key}成功")
                fresh_and_save()
            else:
                messagebox.showwarning("兑换奖励",f"兑换{key}失败，积分不足")
        else:
            messagebox.showwarning("兑换奖励",f"{key}不存在")
    def delete(self):
        key = askstring("删除奖励","请输入奖励名称")
        if key in self.rewards:
            del self.rewards[key]
            messagebox.showinfo("删除奖励",f"删除{key}成功")
            fresh_and_save()
        else:
            messagebox.showwarning("删除奖励",f"{key}不存在")
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
        self.text_widget.insert("insert", f"当前分数为{point}\n{random.choice(one.read().splitlines())}")
        self.text_widget.tag_configure("center", justify='center',font=self.my_font)
        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tkinter.DISABLED)
        print(f"当前分数为{point} \n {random.choice(one.read().splitlines())}")
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
root.geometry("800x600")
root.resizable(False, False)

try:
    data = eval(datafile.read())
    point = data["point"]
except FileNotFoundError:
    data = {
        'tasks': {'阅读': 5},
        'rewards': {'喝奶茶': 1},
        'point': 0,
        'priority_list_of_tasks': {'阅读': 2},
        'repetition_list_of_tasks': {'阅读': True}
    }
    datafile.overwrite(str(data))
    messagebox.showinfo("提示","数据文件不存在，已创建新的数据文件。请重新运行程序。")
    sys.exit()

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

view_introduction_button = tkinter.ttk.Button(root, text="查看说明", command=lambda: webbrowser.open("https://gitee.com/chen-shuhan-1/Intelligent-task-management-system/blob/master/README.md"))
view_introduction_button.place(x=710,y=550)


root.mainloop()