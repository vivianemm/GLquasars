#!/bin/bash

yourfilenames=`ls /home/vivianemm/PycharmProjects/GravLens/Scraping/masterlens`
for eachfile in $yourfilenames
do
   python3 scraping_ml.py "/home/vivianemm/PycharmProjects/GravLens/Scraping/masterlens/$eachfile" "/home/vivianemm/PycharmProjects/GravLens/Scraping/masterlens/results/$eachfile"
done


# `ls /home/viviane/GravLens/Scraping/masterlens`
# "/home/viviane/GravLens/Scraping/masterlens/$eachfile" "/home/vivianemm/PycharmProjects/GravLens/Scraping/results/$eachfile"