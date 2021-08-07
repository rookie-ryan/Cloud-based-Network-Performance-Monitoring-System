#!/usr/bin/env python

import json
import time
import subprocess
import sys
import traceback
from datetime import datetime
import os
from multiprocessing.dummy import Pool as ThreadPool

# input and output path
vantage_file= "vantage_points.json"
parameter_file="monitor_parameters.json"
output_path="data/"

def get_monitor_ip(ip_list):
    with open(vantage_file, "r") as vantage_file_f:
        vantage_points=json.load(vantage_file_f)
        for point in vantage_points:
                ip_list.append(vantage_points[point])

def main():
    ip_list=[]
    get_monitor_ip(ip_list)
    # get parameter
    with open(parameter_file, "r") as parameter_file_f:
        parameters=json.load(parameter_file_f)
        interval=parameters['interval']
        packet_size=parameters['size']
        packet_num=parameters['number']
    t_p=ThreadPool()
    while True:
        for ip in ip_list:
            ping_cmd="sudo ping -c "+str(packet_num)+" -s "+str(packet_size)+" "+ip
            # ping command will return 2 lines of summary results after "ping statistics"
            grep_cmd = " | grep -A 2 statistics"
            try:
                current_month=datetime.now().strftime("%Y-%m")
                current_day=datetime.now().strftime("%d")
                current_time=datetime.now().strftime("%H:%M:%S")
                output = subprocess.check_output(ping_cmd+grep_cmd,shell=True)
                output=output.decode("utf-8")
                loss_rate = output.split(",")[2]
                rtt = output.split("rtt")[1]
            except IndexError: # when split, as ping failed
                # write fail infomation
                a=1
            except:
                sys.stderr.write(traceback.format_exc())
            else:
                dir=output_path+current_month
                if not os.path.exists(dir):
                    os.makedirs(dir)
                write_data={}
                write_data[current_time]={
                    "loss rate":loss_rate,
                    "rtt":rtt
                }
                output_file=dir+"/"+current_day+".json"
                with open(output_file, "a+") as write_f:
                    write_f.write(json.dumps(write_data) + "\n")
        time.sleep(interval)

if __name__ == '__main__':
    main()