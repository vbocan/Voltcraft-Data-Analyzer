"""
Project:      Voltcraft Data Analyzer
Author:       Valer Bocan, PhD <valer@bocan.ro>
Last updated: June 25rd, 2014

Module
description:  The VoltcraftDataFile module processes data files containing history of voltage, current and power factor,
              as generated by the Voltcraft Energy-Logger 4000.
              
License:      This project is placed in the public domain, hoping that it will be useful to people tinkering with Voltcraft products.
              
Reference:    Voltcraft File Format: http://www2.produktinfo.conrad.com/datenblaetter/125000-149999/125323-da-01-en-Datenprotokoll_SD_card_file_Formatv1_2.pdf
"""

from datetime import datetime
from datetime import timedelta
from ByteDecoders import DecodeHex

def Process(filename):
    """
    Description: Process a Voltcraft data file. Data files contain minute-by-minute history of voltage, current and power factor.
    Input:       File name.
    Output:      Dictionary containing values for "Timestamp", "Voltage", "Current", "PowerFactor", "Power", "BlackoutCount", "BlackoutDuration" (via generator function)
    """
    try:
        with open(filename, "rb") as fin:
            x = tuple(fin.read())
    except IOError:
        raise Exception('The specified file does not exist.')
    
    i = 0
    MinuteOffset = 0
    StartTime = datetime.now()
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
            CurrentTimeStamp = datetime(Year, Month, Day, Hour, Minute, 0, 0)

            if MinuteOffset != 0:
                # This means we've encountered a new data block without a corresponding end block
                # i.e. there has been a blackout (with start time in 'TimeStamp' and end time in 'CurrentTimeStamp'.
                BlackoutStart = TimeStamp
                BlackoutDuration = CurrentTimeStamp - TimeStamp
                if BlackoutDuration.total_seconds() < 0:
                    raise Exception("Possibly a corrupted file as the historic data seems invalid")
                yield {"Status":"Blackout", "Timestamp":BlackoutStart, "Duration":BlackoutDuration}
                
            StartTime = CurrentTimeStamp
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
        yield {"Status":"Live", "Timestamp":TimeStamp, "Voltage":Voltage, "Current":Current, "PowerFactor":PowerFactor, "Power":Power}
        MinuteOffset += 1
        i += 5
    
