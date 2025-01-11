# 该脚本使用copilot生成

import tkinter as tk
from tkinter import simpledialog, messagebox
from filehandler import FileHandler

api = FileHandler("data/api.txt")

def askstring(title, prompt):
    while True:
        answer = simpledialog.askstring(title, prompt)
        if answer is None or answer == "":
            messagebox.showerror("错误", "输入不能为空")
        else:
            break     
    return answer

def select_version(root):
        versions = {
            "Lite版本": "lite",
            "Pro版本": "generalv3",
            "Pro-128K版本": "pro-128k",
            "Max版本": "generalv3.5",
            "Max-32K版本": "max-32k",
            "4.0 Ultra版本": "4.0Ultra"
        }

        version = tk.StringVar()
        version.set("lite")  # Set default value

        def get_selected_version():
            return version.get()

        version_window = tk.Toplevel(root)
        version_window.title("选择版本")

        tk.Label(version_window, text="请选择版本:").pack()

        for text, value in versions.items():
            tk.Radiobutton(version_window, text=text, variable=version, value=value).pack(anchor=tk.W)

        tk.Button(version_window, text="确定", command=version_window.destroy).pack()

        root.wait_window(version_window)
        #return versions[get_selected_version()]
        return get_selected_version()


def get_api_credentials():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    app_id = askstring("输入", "请输入您的APPID:")
    api_secret = askstring("输入", "请输入您的APISecret:")
    api_key = askstring("输入", "请输入您的APIKey:")
    api.overwrite(f"{app_id}\n{api_secret}\n{api_key}\n{select_version(root)}")
    messagebox.showinfo("提示", "API凭据已保存")

if __name__ == "__main__":
    value = get_api_credentials()
    print(value)