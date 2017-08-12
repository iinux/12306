#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("beijing.xml")
sw = DOMTree.documentElement
lines = sw.getElementsByTagName("l")


class Station:
    def __init__(self, node):
        self.n = node.getAttribute("n")
        self.acc = node.getAttribute("acc")
        self.lb = node.getAttribute("lb")


class Line:
    def __init__(self, node, stations):
        self.lb = node.getAttribute("lb")
        self.stations = stations

line_array = []
for line in lines:
    station_array = []
    stations = line.getElementsByTagName("p")
    for station in stations:
        station = Station(station)
        if station.lb != "":
            station_array.append(station)

    line_array.append(Line(line, station_array))


for line in line_array:
    print line.lb
    for station in line.stations:
        print station.acc, station.lb
