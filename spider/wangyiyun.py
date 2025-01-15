# 网易云榜单的抓取
import os
import re

import requests

# 常量定义
MUSIC_DIR = "music"
BASE_URL = "https://music.163.com/discover/toplist?id=3778678"
MUSIC_DOWNLOAD_URL = "http://music.163.com/song/media/outer/url?id={}.mp3"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# 创建音乐目录
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)


def fetch_song_list():
    """获取歌曲列表"""
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch song list, status code: {response.status_code}")
    return re.findall(r'<li><a href="/song\?id=(\d+)">(.*?)</a>', response.text)


def download_song(song_id, song_title):
    """下载歌曲"""
    song_url = MUSIC_DOWNLOAD_URL.format(song_id)
    song_path = os.path.join(MUSIC_DIR, f"{song_title}.mp3")

    # 如果歌曲已存在，跳过下载
    if os.path.exists(song_path):
        print(f"歌曲已存在，跳过: {song_title}")
        return

    # 下载歌曲
    try:
        response = requests.get(song_url, headers=HEADERS, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        with open(song_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"下载成功: {song_title}")
    except Exception as e:
        print(f"下载失败: {song_title}, 错误: {e}")


def main():
    """主函数"""
    try:
        song_list = fetch_song_list()
        if not song_list:
            print("未找到歌曲列表")
            return

        print(f"共找到 {len(song_list)} 首歌曲")
        for index, (song_id, song_title) in enumerate(song_list, start=1):
            print(f"{index}. 开始抓取歌曲: {song_title}")
            download_song(song_id, song_title)
    except Exception as e:
        print(f"程序运行出错: {e}")


if __name__ == "__main__":
    main()
