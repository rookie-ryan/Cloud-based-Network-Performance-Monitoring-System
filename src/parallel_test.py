#!/usr/bin/env python

import json
import time
import subprocess
import sys
import traceback
from datetime import datetime
import os
from multiprocessing import Pool

# input and output path
vantage_file = "vantage_points.json"
parameter_file = "monitor_parameters.json"
output_path = "data/"

# get parameter
with open(parameter_file, "r") as parameter_file_f:
    parameters = json.load(parameter_file_f)
    interval = parameters['interval']-3  # ping command takes about 3 seconds
    packet_size = parameters['size']
    packet_num = parameters['number']

# get ip list
ip_list = []
with open(vantage_file, "r") as vantage_file_f:
    vantage_points = json.load(vantage_file_f)
    for point in vantage_points:
        ip_list.append(vantage_points[point])


def work(ip):
    return_data={}
    current_time = datetime.now().strftime("%H:%M:%S")
    ping_cmd = "sudo ping -c " + str(packet_num) + " -s " + str(packet_size) + " " + ip
    # ping command will return 2 lines of summary results after "ping statistics"
    grep_cmd = " | grep -A 2 statistics"
    try:
        output = subprocess.check_output(ping_cmd + grep_cmd, shell=True)
        output = output.decode("utf-8")
        loss_rate = output.split(",")[2].strip()
        rtt = output.split("rtt")[1].strip()
    except IndexError:  # when split, as ping failed
        # write fail infomation
        return_data = {
            "ip":ip,
            "time":current_time,
            "loss rate": -1,
            "rtt": -1
        }
        return return_data
    except:
        sys.stderr.write(traceback.format_exc())
    else:
        return_data = {
            "ip": ip,
            "time": current_time,
            "loss rate": loss_rate,
            "rtt": rtt
        }
        return return_data


def main():
    while True:
        # storage result by time
        current_month = datetime.now().strftime("%Y-%m")
        current_day = datetime.now().strftime("%d")
        dir = output_path + current_month
        if not os.path.exists(dir):
            os.makedirs(dir)

        # create thread pool
        t_p = Pool(len(ip_list))
        ping_data=t_p.map(work, ip_list)

        write_data = {}
        for item in ping_data:
            if item["time"] not in write_data.keys():
                write_data[item["time"]]={}
            write_data[item["time"]][item["ip"]]={
                "loss rate": item["loss rate"],
                "rtt": item["rtt"]
            }
        output_file = dir + "/" + current_day + ".json"
        with open(output_file, "a+") as write_f:
            write_f.write(json.dumps(write_data) + "\n")
        t_p.close()
        time.sleep(interval-3)


if __name__ == '__main__':
    main()
