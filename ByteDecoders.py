#!python3
"""
Project:      Voltcraft Data Analyzer
Author:       Valer Bocan, PhD <valer@bocan.ro>
Last updated: June 26th, 2014

Module
description:  The VoltcraftDataFile module processes data files containing history of voltage, current and power factor,
              as generated by the Voltcraft Energy-Logger 4000.
              
License:      This project is placed in the public domain, hoping that it will be useful to people tinkering with Voltcraft products.
              
Reference:    Voltcraft File Format: http://www2.produktinfo.conrad.com/datenblaetter/125000-149999/125323-da-01-en-Datenprotokoll_SD_card_file_Formatv1_2.pdf
"""

def DecodeHex(hexinput):
    """
    Converts to hexa each byte in the input tuple, concatenates the result and converts
    the resulting hexadecimal into decimal.    
    """
    return int(''.join('{:02x}'.format(x) for x in hexinput), 16)    

def DecodeDecimal(hexinput):
    """
    Converts to decimal each byte in the input tuple, concatenates the result and converts
    the resulting string into decimal.    
    """    
    return int(''.join('{0}'.format(x) for x in hexinput), 10)
