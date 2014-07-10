#!python3
"""
Project:      Voltcraft Data Analyzer
Author:       Valer Bocan, PhD <valer@bocan.ro>
Last updated: July 8th, 2014

Module
description:  The VoltcraftDataFile module processes data files containing history of voltage, current and power factor,
              as generated by the Voltcraft Energy-Logger 4000.
              
License:      This project is placed in the public domain, hoping that it will be useful to people tinkering with Voltcraft products.
              
Reference:    Voltcraft File Format: http://www2.produktinfo.conrad.com/datenblaetter/125000-149999/125323-da-01-en-Datenprotokoll_SD_card_file_Formatv1_2.pdf
"""

from itertools import tee
from datetime import datetime
from datetime import timedelta
from ByteDecoders import DecodeHex

def Process(filename):
    """
    Description: Process a Voltcraft data file. Data files contain minute-by-minute history of voltage, current and power factor.
    Input:       File name.
    Output:      Dictionary containing values for "Timestamp", "Voltage", "Current", "PowerFactor", "Power", (via generator function)
    """
    try:
        with open(filename, "rb") as fin:
            x = tuple(fin.read())
    except IOError:
        raise Exception('The specified file does not exist.')
    
    i = 0
    MinuteOffset = 0
    StartTime = datetime.now().replace(second=0, microsecond=0)
        
    while True:
        if DecodeHex(x[i:i+3]) == 14730730:            
            # Encountered the beginning of a new data block
            i += 3 # Advance magic number of the new data block            

            # Decode date and time that follows
            Month = DecodeHex(x[i:i+1])
            Day = DecodeHex(x[i+1:i+2])
            Year = DecodeHex(x[i+2:i+3]) + 2000
            Hour = DecodeHex(x[i+3:i+4])
            Minute = DecodeHex(x[i+4:i+5])
            StartTime = datetime(Year, Month, Day, Hour, Minute, 0, 0)            
            MinuteOffset = 0
            i += 5 # Advance date and time
            continue
            
        if DecodeHex(x[i:i+4]) == 4294967295:            
            # Encountered the end block
            break
        
        # Read voltage (2 bytes), current (2 bytes) and power factor (1 byte)
        Voltage = DecodeHex(x[i:i+2]) / 10 # Volts
        Current = DecodeHex(x[i+2:i+4]) / 1000 # Amperes
        PowerFactor = DecodeHex(x[i+4:i+5]) / 100 # CosPHI
        TimeStamp = StartTime + timedelta(minutes = MinuteOffset)
        Power = Voltage * Current * PowerFactor / 1000 # kW
        ApparentPower = Voltage * Current / 1000 # kVA
        MinuteOffset += 1
        i += 5        
        res = {"Timestamp":TimeStamp, "Voltage":Voltage, "Current":Current, "PowerFactor":PowerFactor, "Power":Power, "ApparentPower":ApparentPower}
        yield res

def DetectBlackouts(VoltcraftData):
    pw = pairwise(VoltcraftData)
    for x,y in pw:
        diff = y["Timestamp"] - x["Timestamp"]
        if  diff > timedelta(minutes = 1):
            res = {"Timestamp":x["Timestamp"], "Duration": diff}
            yield res

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
