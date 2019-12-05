#!/bin/bash

yourfilenames=`ls /home/vivianemm/PycharmProjects/GravLens/Scraping/masterlens`
for eachfile in $yourfilenames
do
   python APP.py "/home/vivianemm/PycharmProjects/GravLens/Scraping/masterlens/$eachfile" "/home/vivianemm/PycharmProjects/GravLens/Scraping/masterlens/result/$eachfile"
done

