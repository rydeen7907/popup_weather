import tkinter as tk
from tkinter import messagebox
import requests
import time
# from urllib.parse import quote # quote関数をインポート (非推奨)

# def get_weather(api_key, city):
#     """OpenWeatherMap APIを使って天気情報を取得する"""
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"
#     complete_url = f"{base_url}appid={api_key}&q={city}"
#     response = requests.get(complete_url)
#     return response.json()

def get_weather(api_key, city):
    """OpenWeatherMap APIを使って天気情報を取得する"""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&lang=ja" #日本語で取得
    response = requests.get(complete_url)
    return response.json()

# 都市名を日本語で入力するとAPIが認識せず起動しなくなるので参考まで…
# def get_weather(api_key, city):
#     """OpenWeatherMap APIを使って天気情報を取得する"""
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"
#     encoded_city = quote(city) # cityをURLエンコード
#     complete_url = f"{base_url}appid={api_key}&q={encoded_city}&lang=ja"
#     response = requests.get(complete_url)
#     return response.json()

def check_bad_weather(weather_data):
    """悪天候条件をチェックする"""
    if weather_data["cod"] != 200:
        return False
    weather_id = weather_data['weather'][0]['id']
    # 雷、雨、霧雨、雪、大気現象
    if 200 <= weather_id <= 804: 
        return True
    return False

def show_weather_notification(city, weather_description):
    """悪天候のポップアップ通知を表示する"""
    root = tk.Tk()
    root.withdraw()  # ポップアップウィンドウを非表示
    messagebox.showwarning("悪天候の警告", 
                           f"{city}で{weather_description}が予想されます。ご注意ください。")

# def show_weather_notification(city, weather_description):
#     """悪天候のポップアップ通知を表示する"""
#     root = tk.Tk()
#     root.withdraw()  # ポップアップウィンドウを非表示

#     # アイコンを設定 (icon.icoは実際のアイコンファイル名に変更)
#     # ここで変更できるのはタイトル部分のアイコン
#     root.iconbitmap(".ico") 

#     messagebox.showwarning("悪天候の警告", 
#                            f"{city}で{weather_description}が予想されます。ご注意ください。")

def main(api_key, city, check_interval=3600): # 起動後60分ごとにチェックする
    # チェックする間隔を短くしすぎるとAPI無料枠を超過するので注意
    """定期的に天気をチェックし、悪天候の場合は通知する"""
    while True:
        weather_data = get_weather(api_key, city)
        if check_bad_weather(weather_data):
            weather_description = weather_data['weather'][0]['description']
            show_weather_notification(city, weather_description)
        time.sleep(check_interval)

if __name__ == "__main__":
    # OpenWeatherMap APIキーを入力 
    api_key = " YOUR API KEY " 
    # 都市名を入力 ※英字で入力
    city = " CITY "
    main(api_key, city)