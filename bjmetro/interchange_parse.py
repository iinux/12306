#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("interchange.xml")
exchanges = DOMTree.documentElement
exchanges = exchanges.getElementsByTagName("ex")


class Exchange:
    def __init__(self, node):
        self.name = node.getAttribute("s")
        line_map = {
            '1号线': '0',
            '2号线': '1',
            '4号线大兴线': '2',
            '5号线': '3',
            '6号线': '4',
            '8号线': '5',
            '9号线': '6',
            '10号线': '7',
            '13号线': '8',
            '14号线': '9',
            '15号线': '10',
            '八通线': '11',
            '昌平线': '12',
            '亦庄线': '13',
            '房山线': '14',
            '机场线': '15',
            '7号线': '16',
            '14号线(东)': '17',
            '16号线': '18',
        }
        new_line_map = {}
        for key, value in line_map.items():
            new_line_map[value] = key.decode("utf8")
        self.from_line = new_line_map[node.getAttribute("fl")]
        self.to_line = new_line_map[node.getAttribute("tl")]

exchange_array = []
for exchange in exchanges:
    exchange_array.append(Exchange(exchange))

for exchange in exchange_array:
    print("%s %s %s" % (exchange.name, exchange.from_line, exchange.to_line))
