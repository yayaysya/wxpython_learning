#!/usr/bin/env python
# coding=gbk

'''
    this is a python file about how to use xml in python
    pyhton prase the xml with the ElementTree Way
'''

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import  xml.etree.ElementTree as ET

def xml_prase(xml_file):
    tree = ET.ElementTree(file=xml_file)  # 导入xml文件
    root = tree.getroot()
    print root.tag, root.attrib, root.text
    print len(root.tag), len(root.text), root.text
    for RootChrildren in root:
        print len(RootChrildren.tag), RootChrildren.tag, RootChrildren.attrib,\
            len(RootChrildren.text)
        for RootChrildrenChrildren in RootChrildren:
            print RootChrildrenChrildren.tag,\
                  RootChrildrenChrildren.attrib,\
                  RootChrildrenChrildren.text

def main():
    xml_prase('bookstore.xml')

if __name__ == '__main__':
    main()
