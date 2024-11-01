from datetime import datetime
import os

# 获取当前脚本所在的文件夹路径
文件路径 = os.path.dirname(os.path.abspath(__file__))
# 构建 日报生成模板.html 文件的绝对路径
日报生成模板 = os.path.join(文件路径, '日报生成模板.html')
# 构建 data/datas.reward 文件的绝对路径
数据文件 = os.path.join(文件路径, 'data/datas.reward')
# 构建 report.html 文件的绝对路径
日报内容 = os.path.join(文件路径, f'interdoction/{username}_report.html')

body = ""

with open(数据文件,encoding="utf-8") as d:
    数据 = d.read()
    数据 = eval(数据)
    努力项 = 数据["努力项"]
    奖励项 = 数据["奖励项"]
    努力项实现次数 = 数据["努力项实现次数"]
    奖励项兑换次数 = 数据["奖励项兑换次数"]
    积分 = 数据["积分"]
    夸夸助手 = 数据["夸夸助手"]
    努力心得 = 数据["努力心得"]
    奖励心得 = 数据["奖励心得"]

body = body + f"<h2>当前积分为{积分}</h2>"

body = body + "<h2>努力项实现次数</h2><table><tr><td>努力项</td><td>实现次数</td></tr>"
for key,value in 努力项实现次数.items():
    body = body + f"<tr><td>{key}</td><td>{value}</td></tr>"
body = body + "</table>"
    
body = body + "<h2>奖励项兑换次数</h2><table><tr><td>奖励项</td><td>兑换次数</td></tr>"
for key,value in 奖励项兑换次数.items():
    body = body + f"<tr><td>{key}</td><td>{value}</td></tr>"
body = body + "</table>"

print(努力心得)

内容 = ""
body = body + "<h2>努力心得</h2><table><tr><td>努力项</td><td>心得</td></tr>"
for key,value in 努力心得.items():
    print(value)
    for i in value:
        if i != "":
            内容 = 内容 + f"{i}<br>"
        body = body + f"<tr><td>{key}</td><td>{内容}</td></tr>"
body = body + "</table>"


内容 = ""
body = body + "<h2>奖励心得</h2><table><tr><td>奖励项</td><td>心得</td></tr>"
for key,value in 奖励心得.items():
    print(value)
    for i in value:
        内容 = 内容 + f"{i}<br>"
        print(内容)
    body = body + f"<tr><td>{key}</td><td>{内容}</td></tr>"
body = body + "</table>"

now = datetime.now()
# 格式化日期和时间，精确到分钟
formatted_time = now.strftime("%Y-%m-%d %H:%M")

with open(日报生成模板,encoding="utf-8") as r:
    d = r.read()
    d = d.format(time=formatted_time,body=body)
    with open(日报内容,mode="w",encoding="utf-8") as report:
        report.write(d)

print(body)