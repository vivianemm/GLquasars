#!/bin/bash

yourfilenames=`ls /home/viviane/GravLens/Scraping/masterlens`
for eachfile in $yourfilenames
do
   python3 scraping_ml.py "/home/viviane/GravLens/Scraping/masterlens/$eachfile" "/home/viviane/GravLens/Scraping/masterlens/$eachfile"
done


# `/home/viviane/GravLens/Scraping/masterlens`
# "/home/viviane/GravLens/Scraping/masterlens/$eachfile" "/home/vivianemm/PycharmProjects/GravLens/Scraping/results/$eachfile"
