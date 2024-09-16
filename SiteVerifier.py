#!/usr/bin/env python
# encoding: utf-8
# @author: Mast1n
# @file: SiteVerifier.py
# @desc: A tool designed to verify the accessibility and status of a list of URLs.


import os.path
import signal
import threading
import argparse
import requests
import random
import time
from termcolor import cprint
from bs4 import BeautifulSoup
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed


exit_flag = threading.Event()
alive_count = 0


class Status(Enum):
    REFUSE = 0
    ALIVE = 1
    ERROR = -1


def print_logo():
    logo = r"""

       _________.__  __                          

      /   _____/|__|/  |_  ____                  

      \_____  \ |  \   __\/ __ \                 
      /        \|  ||  | \  ___/                 
     /_______  /|__||__|  \___  >                
             \/               \/             V1.0   
____   ____           .__  _____.__              
\   \ /   /___________|__|/ ____\__| ___________ 
 \   Y   // __ \_  __ \  \   __\|  |/ __ \_  __ \
  \     /\  ___/|  | \/  ||  |  |  \  ___/|  | \/
   \___/  \___  >__|  |__||__|  |__|\___  >__|   
              \/                        \/         
                                      
            𝑃𝑜𝑤𝑒𝑟𝑒𝑑 𝑏𝑦 𝑀𝑎𝑠𝑡1𝑛       
   """
    cprint(logo, "blue", attrs=["bold"])


def format_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    return url


def output_console(result: tuple):
    try:
        status, url, status_code, title, packet_size = result
        COLOR_MAP = {
            "200": "green",
            "302": "blue",
            "403": "yellow"
        }
        color = COLOR_MAP.get(status_code, "white")
        if status == Status.ALIVE:
            out_file(result)
            cprint(f"[{status_code}]", color, attrs=["bold"], end=" ")
            cprint(f"{url}  {title.strip()}", "white")
        elif status == Status.REFUSE:
            cprint(f"[{status_code}]", "grey", attrs=["bold"], end=" ")
            cprint(f"{url}  {title.strip()}", "white")
        elif status == Status.ERROR:
            cprint(f"ERROR {url}  Unable to access.", "red")
    except Exception as e:
        cprint(f"ERROR: {e}", "red")


def load_file(filepath):
    urls = set()
    with open(filepath, 'r') as f:
        for line in f:
            if line is not None:  # 确保 line 不是 None
                url = line.strip()
                if url:  # 确保 url 不是空字符串
                    url = format_url(url)
                    urls.add(url)
    return list(urls)


def dir_init():
    basedir = "./result/"
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    for filename in os.listdir(basedir):
        file_path = os.path.join(basedir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def out_file(result: tuple):
    basedir = "./result/"
    status, url, status_code, title, packet_size = result
    FILE_MAP = {
        "200": "result_200.txt",
        "302": "result_302.txt",
        "403": "result_403.txt"
    }

    with open(basedir + "result.txt", "a+", encoding="utf-8") as f:
        f.write(f"{status_code} {url}  {title.strip()}\n")
        filename = FILE_MAP.get(status_code)
        with open(basedir + filename, "a+", encoding="utf-8") as file:
            file.write(url + "\n")


def verify(url: str):
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    header = {"User-Agent": random.choice(user_agents)}

    def request(url: str):
        global alive_count
        try:
            requests.packages.urllib3.disable_warnings()
            resp = requests.get(url=url, headers=header, verify=False, timeout=3)
            resp.encoding = 'utf-8'
            status_code = str(resp.status_code)
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            packet_size = len(resp.content)
            if status_code in ["200", "302", "403"]:
                alive_count += 1
                return Status.ALIVE, url, status_code, title, packet_size
            else:
                return Status.REFUSE, url, status_code, title, packet_size
        except Exception as e:
            return Status.ERROR, url, "", "Connection Error", 0

    result = request(url)
    if result[0] == Status.ERROR and url.startswith("https://"):
        surl = url.replace("https://", "http://")
        result = request(surl)

    return result


def signal_handler(signum, frame):
    cprint("Program interrupted by user. Stopping...", "yellow")
    exit_flag.set()
    exit(0)


def thread_work(urls, threads):
    global exit_flag
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(verify, url): url for url in urls}
        for future in as_completed(futures, timeout=None):
            if exit_flag.is_set():
                for f in futures:
                    if not f.done():
                        f.cancel()
                break
            result = future.result()
            output_console(result)
    executor.shutdown(wait=False)


def main():
    global exit_flag
    dir_init()
    signal.signal(signal.SIGINT, signal_handler)
    print_logo()
    cprint("[*] Start working...", "magenta")
    time.sleep(0.6)

    try:
        parser = argparse.ArgumentParser()
        parser.usage = "SiteVerifier.py -f <file> [-t <threads> -h <help message>]"
        parser.add_argument("-f", "--file", help="Input file path for loading URLs", required=True)
        parser.add_argument("-t", "--threads", help="Maximum number of threads to use. default 25", default=25, type=int)
        args = parser.parse_args()

        urls = load_file(args.file)
        thread_work(urls, args.threads)
        cprint("[*] All tasks completed. Program finished.", "magenta")
        print(f"Total accessible sites: {alive_count}")
        print(f"Please check the result file in './result'")
    except TypeError:
        pass
    except Exception as e:
        cprint(e, "red")


if __name__ == '__main__':
    main()
