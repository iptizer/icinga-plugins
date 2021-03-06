#!/bin/env python
'''plugin to check the cli command and gether some performance data'''

import sys
import argparse
import subprocess

# icinga returncode vars
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

def perfdata(outputList):
    '''perfdata output'''
    perfdata = "|"
    for element in outputList:
        perfdata = perfdata+str(element[2])+"_"+str(element[1])+"="+str(element[3])+str(element[4])+";"+str(args.warning)+";"+str(args.critical)+" "
    print perfdata

def message(outputList):
    '''output of the status for icinga'''
    for element in outputList:
        if "CRITICAL" in element:
            print '%s is %s because %s is %s%s' %(element[2], element[5], element[1], element[3], element[4])
        elif "WARNING" in element:
            print '%s is %s because %s is %s%s' %(element[2], element[5], element[1], element[3], element[4])
        else:
            pass

def parse_cellcli(output, warning, critical):
    outputList=output.splitlines()
    analyzedList=[]
    for line in outputList:
        lineList = line.split()
        if int(lineList[3]) > critical:
            lineList.append('CRITICAL')
        elif int(lineList[3]) > warning:
            lineList.append('WARNING')
        else:
            lineList.append('OK')
        analyzedList.append(lineList)
    if any('CRITICAL' in x for x in analyzedList):
        message(analyzedList)
        perfdata(analyzedList)
        critical_exit()
    elif any("WARNING" in x for x in analyzedList):
        message(analyzedList)
        perfdata(analyzedList)
        warning_exit()
    else:
        print "Everything is OK"
        perfdata(analyzedList)
        ok_exit()

def fetch_stats(dcliArgs):
    dcliOutput = subprocess.Popen(dcliArgs, stdout=subprocess.PIPE, shell=True).communicate()[0]
    if len(dcliOutput):
        return dcliOutput

# icinga returncode functions
def critical_exit():
    sys.exit(EXIT_CRITICAL)

def warning_exit():
    sys.exit(EXIT_WARNING)

def ok_exit():
    sys.exit(EXIT_OK)

def unknown_exit():
    sys.exit(EXIT_UNKNOWN)

if __name__ == '__main__':
    # request parameters for script
    #dcliArgs = str(args.dcli) +  ' -c ' + str(args.hostname) + ' -l ' + str(args.username) + ' "' + str(args.query) + '"'
    command = 'grep ' + 'NFS4ERR_STALE ' + '/var/adm/messages ' + '| ' + 'grep ' + '-v ' + '/preload/ '
    out = fetch_stats(command)
    parse_cellcli(cellstats, args.warning, args.critical)
