#!/usr/bin/env python
# Created 01/26/15 by Jason Albert
# Program to create VPD images from input template files

############################################################
# Imports - Imports - Imports - Imports - Imports - Imports
############################################################
import sys
sys.path.insert(0,"pymod");
import cmdline
import os
import xml.etree.ElementTree as ET
import glob

############################################################
# Function - Functions - Functions - Functions - Functions
############################################################
def help():
    print("createVpd.py")
    print("Required Args")
    print("Optional Args")
    print("-h|--help              This help text")

def merge(files):
    first = None
    for filename in files:
        data = ET.parse(filename).getroot()
        if first is None:
            first = data
        else:
            first.extend(data)
    if first is not None:
        return ET.tostring(first)

############################################################
# Main - Main - Main - Main - Main - Main - Main - Main
############################################################
rc = 0
# Get the path the script is being called from
cwd = os.path.dirname(os.path.abspath(__file__))

################################################
# Command line options
clError = 0

# Help text
if (cmdline.parseOption("-h","--help")):
    help()
    exit(0)

# Look for input files - the option can be repeated multiple times
clInputFiles = list()
while True:
    clInputFile = cmdline.parseOptionWithArg("-i")
    if (clInputFile == None):
        break
    else:
      clInputFiles.append(clInputFile)

# Error check we got input files
if (len(clInputFiles) == 0):
    print("ERROR: At least 1 -i arg is required")
    clError+=1

# Error check the command line
if (clError):
    print("ERROR: Missing required cmdline args!  Please review the output above to determine which ones!")
    exit(clError)

# All cmdline args should be processed, so if any left throw an error
if (len(sys.argv) != 1):
    print("ERROR: Extra cmdline args detected - %s" % (sys.argv[1:])) # [1:] don't inclue script name in the list
    exit(len(sys.argv))

files = list()
for file in clInputFiles:
    files.extend(glob.glob(file))

#xml_files = glob.glob("tvpd/opfr.tvpd")

print(files)

m = merge(files)

print "++++++++++++++++"
print m
print "++++++++++++++++"

root = ET.fromstring(m)
root.tag
root.attrib
for child in root:
    print child.tag, child.attrib

print "|||||||||||||||||||||||||||"

for desc in root.iter('kwdesc'):
    print(desc.tag, desc.attrib, desc.text)

exit(0)

xml_element_tree = None
for xml_file in xml_files:
    print xml_file
    data = ET.parse(xml_file).getroot()
    print ET.tostring(data)
    for result in data.iter('recordname'):
        print "here"
        if xml_element_tree is None:
            xml_element_tree = data 
            insertion_point = xml_element_tree.findall("./results")[0]
        else:
            insertion_point.extend(result) 

print("########################")
if xml_element_tree is not None:
    print ET.tostring(xml_element_tree)
