#!/usr/bin/env python

import json
import socket
import time
import subprocess

vantage_file="../vantage_points.json"
parameter_file="../monitor_parameters.json"
output_path="../data/"

def get_monitor_ip(ip_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    with open(vantage_file, "r") as vantage_file_f:
        vantage_points=json.load(vantage_file_f)
        for point in vantage_points:
            if vantage_points[point] != local_ip:
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
    while True:
        for ip in ip_list:
            cmd="sudo ping -c "+str(packet_num)+" -s "+str(packet_size)+" "+ip
            p=subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='gbk')
            output=p.communicate()[0]
            print(output)
        time.sleep(interval)





if __name__ == '__main__':
    main()