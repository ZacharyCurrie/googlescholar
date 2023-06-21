#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 23:10:38 2023

@author: zach
"""
import csv
import requests
from bs4 import BeautifulSoup
import sys
import http.client
import time

urls = ['/citations?view_op=search_authors&hl=en&mauthors=label:digital_humanities',
        '/citations?view_op=search_authors&hl=en&mauthors=label:network_science',
        '/citations?view_op=search_authors&hl=en&mauthors=label:computational_social_science',
        '/citations?view_op=search_authors&hl=en&mauthors=label:social_networks',
        '/citations?view_op=search_authors&hl=en&mauthors=label:modeling_and_simulation']

CData = ['name', 'id', 'exp1', 'exp2', 'exp3', 'exp4', 'exp5'] + [str(year) for year in range(1991, 2014)]
output_file = 'researchers.csv'
data = []

for url in urls:
    time.sleep(5) # Sleep for 5 seconds
    conn = http.client.HTTPSConnection("scholar.google.com")
    conn.request("GET", url)
    r1 = conn.getresponse()
    text = r1.read()
    soup = BeautifulSoup(text, 'html.parser')
    # Select the researchers from the page
    researchers = soup.select('div.gs_ai')

    for researcher in researchers:
        time.sleep(5) # Sleep for 5 seconds
        name = researcher.select_one('h3.gs_ai_name a').text
        user_id = researcher.select_one('h3.gs_ai_name a')['href']
        user_id = user_id[user_id.index('=')+1:]

        exp1, exp2, exp3, exp4, exp5 = [''] * 5  

        exps = researcher.select('.gs_ai_int') 

        for i, exp in enumerate(exps):
            if i == 0:
                exp1 = exp.text.strip()
            elif i == 1:
                exp2 = exp.text.strip()
            elif i == 2:
                exp3 = exp.text.strip()
            elif i == 3:
                exp4 = exp.text.strip()
            elif i == 4:
                exp5 = exp.text.strip()

        citations = [cite.text for cite in researcher.select('.gs_ai_cby')]

        data.append([name, user_id, exp1, exp2, exp3, exp4, exp5] + citations)

# Save data to CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(CData)
    writer.writerows(data)

print(f"Data saved to {output_file}")

