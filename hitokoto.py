# 该程序由通义灵码生成，用于获取一言（hitokoto）的数据

import requests

def get_hitokoto():
    url = "https://v1.hitokoto.cn/?c=d&c=i&c=k&encode=text"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"请求失败，状态码: {response.status_code}"

if __name__ == "__main__":
    # 调用函数并打印结果
    hitokoto_text = get_hitokoto()