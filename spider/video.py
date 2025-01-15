import re
import tkinter as tk
import webbrowser
from tkinter import messagebox

import requests

# 常量定义
API_URLS = {
    1: 'http://jiexi.pengdouw.com/jiexi1/?url=',
    2: 'http://jiexi.pengdouw.com/jiexi2/?url=',
    3: 'http://jiexi.pengdouw.com/jiexi3/?url='
}

# 创建主窗口
root = tk.Tk()
root.geometry('500x200+200+200')
root.title('在线观看电影 - 自用版')


def parse_video_url(api_url, video_url):
    """解析视频 URL"""
    try:
        response = requests.get(api_url + video_url)
        response.raise_for_status()  # 检查请求是否成功
        video_url = re.findall('<iframe id="baiyug" scrolling="no" src="(.*?)"', response.text)[0]
        webbrowser.open(video_url)
    except requests.RequestException as e:
        messagebox.showerror("错误", f"网络请求失败: {e}")
    except IndexError:
        messagebox.showerror("错误", "解析视频 URL 失败，请检查输入链接是否正确")


def show():
    """处理播放按钮点击事件"""
    api_num = api_num_var.get()
    video_url = video_url_var.get().strip()

    if not video_url:
        messagebox.showwarning("提示", "请输入播放地址")
        return

    if api_num not in API_URLS:
        messagebox.showerror("错误", "无效的接口选择")
        return

    parse_video_url(API_URLS[api_num], video_url)


# 接口选择部分
api_frame = tk.LabelFrame(root, text="选择接口", padx=10, pady=10)
api_frame.pack(pady=10, fill="x")

api_num_var = tk.IntVar(value=1)  # 默认选择一号线路
for num, text in [(1, "一号线路"), (2, "二号线路"), (3, "三号线路")]:
    tk.Radiobutton(api_frame, text=text, variable=api_num_var, value=num).pack(side="left")

# 播放地址输入部分
input_frame = tk.LabelFrame(root, text="播放地址", padx=10, pady=10)
input_frame.pack(pady=10, fill="x")

video_url_var = tk.StringVar()
tk.Entry(input_frame, textvariable=video_url_var, width=50).pack(fill="x")

# 解析播放按钮
tk.Button(root, text="在线解析播放", bg="green", fg="white", font=("宋体", 14), command=show).pack(fill="x", pady=10)

# 运行主循环
root.mainloop()
