#! /usr/bin/env python

import ue9
import LabJackPython
from time import time, sleep

list_of_registers = range(240,253,2)
list_of_registers += range(96,109,2)
list_of_registers += range(144,157,2)
list_of_registers += range(192,205,2)

def V2K(vi, number):
    return 100.*vi

def getJD():
    return (time() / 86400.) + 2440587.5

def ReadDat(dev, regNum):
    try:
        return V2K(dev.readRegister(regNum), regNum)
    except(IndexError):
        return -1.
    except(LabJackPython.LabJackException):
        dev.close()
        try:
            dev.open()
            return V2K(dev.readRegister(regNum), regNum)
        except(LabJackPython.LabJackException):
            return -2.

def readTemps(_d, _list_of_registers):
# Get the internal temperature as well.
    ret = [getJD()] + [_d.getTemperature()] + [ReadDat(_d,i) for i in _list_of_registers]
    return ret

def aggData(cumList, dev, _list_of_registers, n_per_int):
    if cumList is None:
        raise(TypeError)
    else:
        for i,tnew in enumerate(readTemps(dev, _list_of_registers)):
            if cumList[i] < 0:
                pass
            if tnew < 0:
                cumList[i] = tnew
            else:
                cumList[i] += tnew/n_per_int
        return cumList

# seconds per integration
sPerInt = 10.
# minutes per file
mPerFile = 60.
outDir = '/home/obs/TMON/Temperatures/'

d = ue9.UE9()

while True:
    fileName = '%stemp.%7.5f.txt'%(outDir, getJD())
    print 'Writing to %s'%fileName
    f = open(fileName, 'w')
    file_start_time = time()
    while(time() - file_start_time < mPerFile * 60.):
        Ts = None
        int_start_time = time()
        while(time()-int_start_time < sPerInt):
            try:
                try:
                    Ts = aggData(Ts, d, list_of_registers)
                except(TypeError):
                    Ts = readTemps(d, list_of_registers)
            except(KeyboardInterrupt):
                d.close()
        f.write("\t".join(["%7.5f"%t for t in Ts])+"\n")
        f.flush()
    f.close()
d.close()
