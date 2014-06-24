"""
Project:      Voltcraft Data Analyzer
Author:       Valer Bocan, PhD <valer@bocan.ro>
Last updated: June 24rd, 2014

Module
description:  The VoltcraftDataFile module processes data files containing history of voltage, current and power factor,
              as generated by the Voltcraft Energy-Logger 4000.
              
License:      This project is placed in the public domain, hoping that it will be useful to people tinkering with Voltcraft products.
              Derivative works are permitted with or without mentioning the author.
              
Reference:    Voltcraft File Format: http://www2.produktinfo.conrad.com/datenblaetter/125000-149999/125323-da-01-en-Datenprotokoll_SD_card_file_Formatv1_2.pdf
"""

import csv
from datetime import timedelta
from datetime import datetime

def WriteInfoData(filename, info, data):
    """
    Write informational data to a text file
    """
    try:
        with open(filename, "wt") as fout:
            fout.write("Voltcraft Data Analyzer v1.0 (June 24th, 2014)\n")
            fout.write("Valer Bocan, PhD <valer@bocan.ro>\n")
            fout.write("\n")
            fout.write("Initial time on device: {0}\n".format(info["InitialDateTime"]))
            fout.write("Unit number: {0}\n".format(info["UnitNumber"]))
            fout.write("\n")
            fout.write("Total power consumed: {0:.3f} kWh\n".format(info["TotalPowerConsumed"]))
            fout.write("History:\n")
            fout.write("          Today: {0:.3f} kWh\n".format(info["ConsumptionHistory"][0]))
            fout.write("      Yesterday: {0:.3f} kWh\n".format(info["ConsumptionHistory"][1]))
            fout.write("     2 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][2]))
            fout.write("     3 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][3]))
            fout.write("     4 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][4]))
            fout.write("     5 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][5]))
            fout.write("     6 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][6]))
            fout.write("     7 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][7]))
            fout.write("     8 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][8]))
            fout.write("     9 days ago: {0:.3f} kWh\n".format(info["ConsumptionHistory"][9]))
            fout.write("\n")
            fout.write("Total recorded time: {0}\n".format(GetDurationStringFromMinutes(info["TotalRecordedTime"])))
            fout.write("History:\n")
            fout.write("          Today: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][0])))
            fout.write("      Yesterday: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][1])))
            fout.write("     2 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][2])))
            fout.write("     3 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][3])))
            fout.write("     4 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][4])))
            fout.write("     5 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][5])))
            fout.write("     6 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][6])))
            fout.write("     7 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][7])))
            fout.write("     8 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][8])))
            fout.write("     9 days ago: {0}\n".format(GetDurationStringFromHours(info["RecordedTimeHistory"][9])))
            fout.write("\n")
            fout.write("Total time with power consumption: {0}\n".format(GetDurationStringFromMinutes(info["TotalOnTime"])))
            fout.write("History:\n")
            fout.write("          Today: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][0])))
            fout.write("      Yesterday: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][1])))
            fout.write("     2 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][2])))
            fout.write("     3 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][3])))
            fout.write("     4 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][4])))
            fout.write("     5 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][5])))
            fout.write("     6 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][6])))
            fout.write("     7 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][7])))
            fout.write("     8 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][8])))
            fout.write("     9 days ago: {0}\n".format(GetDurationStringFromHours(info["OnTimeHistory"][9])))
            fout.write("\n")
            fout.write("Tariff 1: {0}\n".format(info["Tariff1"]))
            fout.write("Tariff 2: {0}\n".format(info["Tariff2"]))
            fout.write("\n")
            fout.write("Parameter history:\n")
            for d in data:
                fout.write("[{0}] U={1:02}V I={2:.2f}A cosPHI={3:.2f} P={4:.3f}kW\n".format(d["Timestamp"].strftime("%Y-%m-%d %H:%M"), d["Voltage"], d["Current"], d["PowerFactor"], d["Power"]))
            stats = GetDataStatistics(data)
            fout.write("\n")
            fout.write("Statistics:\n")            
            fout.write("Minimum voltage: {0}V\n".format(stats["MinVoltage"]))
            fout.write("Maximum voltage: {0}V\n".format(stats["MaxVoltage"]))
            fout.write("Maximum power: {0:.3f}kW\n".format(stats["MaxPower"]))
            fout.write("\n")
            fout.write("File generated on: {0}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    except IOError:
        raise Exception('Could not write out information file.')

def WriteHistoricData(filename, data):
    """
    Write historic data to a CSV file
    """
    with open(filename, 'w', newline='') as fp:
        wr = csv.writer(fp, delimiter=';')
        header = [['Timestamp', 'Voltage (V)', 'Current (A)', 'Power (kW)']]
        wr.writerows(header)  # Write header
        for d in data:
            str = [[d["Timestamp"], d["Voltage"], d["Current"], d["Power"]]]
            wr.writerows(str)

def GetDurationStringFromHours(duration):
    """
    Convert a number of hours in a hour:min:sec string representation
    """
    offset = timedelta(hours=duration)
    d = datetime(1,1,1) + offset
    return "{0:02}h {1:02}m".format(d.hour, d.minute)

def GetDurationStringFromMinutes(duration):
    """
    Convert a number of minutes in a hour:min:sec string representation
    """
    offset = timedelta(minutes=duration)
    d = datetime(1,1,1) + offset
    return "{0:02}d {1:02}h {2:02}m".format(d.day-1, d.hour, d.minute)

def GetDataStatistics(data):
    MinVoltage = min(item['Voltage'] for item in data)
    MaxVoltage = max(item['Voltage'] for item in data)
    MaxPower = max(item['Power'] for item in data)
    return {"MinVoltage":MinVoltage, "MaxVoltage":MaxVoltage, "MaxPower":MaxPower}
