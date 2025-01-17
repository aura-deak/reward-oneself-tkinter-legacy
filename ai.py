import sparkAPI
from filehandler import FileHandler
import get_api
from datetime import datetime
import sys
import tkinter as tk
from tkinter import messagebox
import webbrowser
import markdown

def ai(query):
    api_file = FileHandler("data/api.txt")
    if not api_file.check():
        get_api.get_api_credentials()

    api = api_file.read()
    appid, api_secret, api_key, domain, Spark_url = api.split('\n')
    return sparkAPI.main(appid, api_secret, api_key, Spark_url, domain, query)

def make_report():
    report_template = FileHandler("static_resources/template.html")
    report_file = FileHandler("data/report.html")

    data_file = FileHandler("data/data.reward")
    if data_file.check():
        data = eval(data_file.read())
        query = f"""
你是报告生成助手，请帮助用户生成《奖励自己 阶段总结》，对用户进行鼓励、建议和规划。
注意：平台本身不提供、兑换、奖励任何物质和虚拟产品，奖励由用户自己兑换，该工具只是帮助你统计和记录信息。请在报告中指明这一点。
以markdown格式生成报告。
给出具体的报告，而不是报告模板。
完成任务可以增加积分，兑换奖励需要扣除积分，本软件单人使用，请不要跳出规则框架进行回答。
以下是该阶段用户的数据：
tasks为《完成任务能够得到的积分》，rewards为《兑换奖励所需的积分》，point为用户当前的积分,priority_list_of_tasks为任务优先级列表（最高为3）,repetition_of_tasks为任务是否可以重复，tasks_effort_count为任务的实现次数，reward_count为奖励的兑换次数，effort_experience为任务的努力心得列表，reward_experience为奖励的奖励心得列表。
用户当前的积分：{data['point']}，任务的实现次数：{data['tasks_effort_count']}，奖励的兑换次数：{data['reward_count']}，任务的努力心得列表：{data['effort_experience']}，奖励的奖励心得列表：{data['reward_experience']}
""" 
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("提示", "当前没有应用的使用数据")
        sys.exit()

    while True:
        answer = ai(query)
        if not "[" in answer and "#" in answer:
            break
    answer = markdown.markdown(answer)
    report = report_template.read().format(content=answer, time=datetime.now().strftime("%Y-%m-%d %H:%M"))
    report_file.overwrite(report)
    messagebox.showinfo("提示", "阶段报告生成成功")
    webbrowser.open(report_file.path())

if __name__ == "__main__":
    make_report()
    

