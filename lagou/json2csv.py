#!/usr/bin/python
#-*-coding:utf-8 -*-
import csv
import json
import codecs

jsonData = codecs.open('positions.json', 'r', 'utf-8')
fieldnames = ["salary", "companySize", "district", "work_year", "company_name", "position_name", "positionAdvantage"]
with open('positions.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for data in jsonData.readlines():
        r = json.loads(data)
        writer.writerow(r)

