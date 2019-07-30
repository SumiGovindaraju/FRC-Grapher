#!/usr/bin/env python3

"""
Websocket that forwards relevant Network Tables data to the webpage and also caches data for that instance of the page for later use.
"""

import argparse
import datetime
import json
import logging
import os
import signal
import sys
from threading import Thread

from networktables import NetworkTables
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

__author__ = "SumiGovindaraju"
__copyright__ = "Copyright (c) 2018-2019 Sumi Govindaraju"
__credits__ = ["SumiGovindaraju"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "SumiGovindarajut"

parser = argparse.ArgumentParser(
    description="FRC-Grapher, " + __copyright__)
parser.add_argument("-c", "--config", help="Path to saved configuration file", metavar="")
parser.add_argument("-i", "--ip", default="localhost",
                    help="IP address of NetworkTables server", metavar="", type=str)
parser.add_argument("-r", "--replay-match", default=False,
                    help="path to JSON cache file for match replay", metavar="", type=str)
args = parser.parse_args()


def loadConfig():
    ret_val = set()
    if args.config:
        try:
            with open(args.config, 'r') as infile:
                data = json.loads(infile.read())
                for i in data:
                    ret_val.add(i)
        except FileNotFoundError:
            print("Configuration file not found. Using empty set instead.")
    else:
        print("Configuration file not specified. Using empty set instead.")

    return ret_val


keys = loadConfig()
connections = set()


class GrapherWebSocket(WebSocket):
    def handleMessage(self):
        if (self.data.startswith("Add Dataset: ")):
            keys.add(self.data[13:])
        elif (self.data == "Save Config"):
            filename = "config.json"
            if args.config != None:
                filename = args.config
            with open(filename, 'w') as outfile:
                outfile.write(json.dumps(list(keys)))

    def handleConnected(self):
        connections.add(self)
        if args.replay_match:
            try:
                with open(args.replay_match, 'r') as infile:
                    for connection in connections:
                        connection.sendMessage("Replay")
                        connection.sendMessage(infile.read())
            except FileNotFoundError:
                print("JSON cache file not found. Exiting...")
                sys.exit()

    def handleClose(self):
        connections.remove(self)


server = SimpleWebSocketServer('localhost', 8254, GrapherWebSocket)

global currentTimestamp
currentTimestamp = 0
datasets = {}
colors = [
    'rgb(255, 99, 132)',
    'rgb(201, 203, 207)',
    'rgb(255, 159, 64)',
    'rgb(153, 102, 255)',
    'rgb(255, 205, 86)',
    'rgb(54, 162, 235)',
    'rgb(75, 192, 192)'
]

if not os.path.isdir("cache/"):
    print("not a dir")
    os.makedirs("cache/")
cacheFileName = "cache/FRC Grapher JSON Cache " + \
    datetime.datetime.now().strftime("%Y-%m-%d %I.%M.%S %p") + ".json"


def valueChanged(table, key, value, isNew):
    global currentTimestamp
    if key == 'frc-grapher-timestamp':
        currentTimestamp = value
        for connection in connections:
            connection.sendMessage(
                u"" + json.dumps({'key': str(key), 'value': str(value)}))
    if key in keys:
        for connection in connections:
            connection.sendMessage(
                u"" + json.dumps({'key': str(key), 'value': str(value)}))
        if not key in datasets:
            color = len(datasets) % len(colors)
            datasets[key] = {
                "label": key,
                "fill": False,
                "backgroundColor": colors[color],
                "borderColor": colors[color],
                "data": [{
                    "x": currentTimestamp,
                    "y": value
                }]
            }
        else:
            if (datasets[key]["data"][len(datasets[key]["data"]) - 1]["x"] == currentTimestamp):
                datasets[key]["data"][len(
                    datasets[key]["data"]) - 1]["y"] = value
            else:
                datasets[key]["data"].append({
                    "x": currentTimestamp,
                    "y": value
                })

        with open(cacheFileName, "w") as outfile:
            json.dump(datasets, outfile)


def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)


if not args.replay_match:
    logging.basicConfig(level=logging.DEBUG)

    NetworkTables.initialize(server=args.ip)
    NetworkTables.addConnectionListener(
        connectionListener, immediateNotify=True)

    sd = NetworkTables.getTable("SmartDashboard")
    sd.addEntryListener(valueChanged)


def close_sig_handler(signal, frame):
    server.close()
    sys.exit()


signal.signal(signal.SIGINT, close_sig_handler)
server.serveforever()
