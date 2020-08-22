import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_before = []
    xml_now = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            filename = root.find('filename').text
        xml_before.append(filename.split(".")[0])    
        xml_now.append(xml_file.replace(".xml", "").split("\\")[1])

    for i in range(len(xml_before)):
        os.rename(r"images/train/"+xml_now[i]+".jpg", r"images/train/" + xml_before[i] + ".jpg")
        os.rename(r"images/xml_train/"+xml_now[i]+".xml", r"images/xml_train/" + xml_before[i] + ".xml")
    # print(xml_now)
    # print(xml_before)


def main():
    xml_df = xml_to_csv("images/xml_train")


if __name__ == '__main__':
    main()