#!/usr/bin/env python3
import json
import requests
import socket
import os

def get_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        return "خطا در دریافت IP: " + str(e)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def user_exists(server, uuid):
    url = f"http://{server['host']}:{server['port']}/xui/inbound/list"
    headers = {"Authorization": server['token']}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            inbounds = response.json()
            for inbound in inbounds:
                for client in inbound.get("clientStats", []):
                    if client.get("id") == uuid:
                        return True
    except Exception as e:
        print(f"⛔ خطا در ارتباط با سرور {server['host']}: {e}")
    return False

def create_user(server, uuid, username):
    url = f"http://{server['host']}:{server['port']}/xui/inbound/addClient"
    headers = {"Authorization": server['token'], "Content-Type": "application/json"}
    data = {
        "inboundId": 1,
        "settings": {
            "clients": [
                {
                    "id": uuid,
                    "email": username
                }
            ]
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"⛔ خطا در افزودن کاربر به سرور {server['host']}: {e}")
        return False

def sync_all():
    config = load_config()
    uuid = config["uuid"]
    username = config["username"]
    server_list = config["servers"]

    print(f"🔍 IP سرور فعلی: {get_ip()}")
    for server in server_list:
        print(f"\n➤ بررسی سرور {server['host']}")
        if user_exists(server, uuid):
            print(f"✅ کاربر با UUID {uuid} در سرور موجود است.")
        else:
            print(f"⛔ کاربر یافت نشد. در حال ساخت...")
            if create_user(server, uuid, username):
                print("✅ کاربر با موفقیت اضافه شد.")
            else:
                print("❌ افزودن کاربر ناموفق بود.")

if __name__ == "__main__":
    sync_all()
