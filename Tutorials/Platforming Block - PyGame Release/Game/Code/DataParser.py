#DataParser.py
#Parses data from the TileSheet Data file
import os

def parse(path):
    fs = open(path)
    dta = fs.readlines()
    fs.close()
    return dta