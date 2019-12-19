#!/bin/bash

yourfilenames=`ls /home/viviane/GravLens/Scraping/masterlens`
for eachfile in $yourfilenames
do
   python scraping_ml.py "/home/viviane/GravLens/Scraping/masterlens/$eachfile" "/home/vivianemm/PycharmProjects/GravLens/Scraping/results/$eachfile"
done
