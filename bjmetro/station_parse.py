#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("stations.xml")
stations = DOMTree.documentElement
stations = stations.getElementsByTagName("s")


class Station:
    def __init__(self, name, line_name, first_end):
        self.name = name
        self.line_name = line_name
        self.first_end = first_end


station_array = []
for station in stations:
    station_array.append(
        Station(station.getAttribute("name"), station.getAttribute("linename"), station.getAttribute("firstend")))

for station in station_array:
    print("%s %s %s" % (station.name, station.line_name, station.first_end))
