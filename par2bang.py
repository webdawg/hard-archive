#!/usr/bin/env python
__author__ = "WebDawg"
__copyright__ = "What is that, does not exist."
__credits__ = ["Aliens", "Stardust", "Dogs",
                    "The Internet"]
__license__ = "GPL"
__version__ = "0.0001"
__maintainer__ = "WebDawg"
__email__ = "webdawg@hackspherelabs.com"
__status__ = "Yes Please"

#depends on par2 and xargs

import math
import os
import os.path
import subprocess
#from subprocess import check_output

# current working dir of script
currentworkingdir = os.getcwd()
# size of BDR dual layer media
bd_dl_targetSize_bytes = 50050629632
# size of BDR dual layer RW media (This is a guess)
bd_dl_rw_targetSize_bytes = 50050629632
#size of CDR media
cd_targetSize_bytes = 736966656
#size of DVD-R dual layer media
dvd_dl_targetSize_bytes = 8547991552
#size of DVD-R media
dvd_targetSize_bytes = 4706074624
#size of DVD-RW media
dvd_rw_targetSize_bytes = 4700372992

batch_mode = 1
currentDiskMode = bd_dl_targetSize_bytes


#https://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def calculate():
    global currentworkingdir
    print ("CWD: %s" % ( currentworkingdir ))
    print ("Calculating Folder Size...")
    global currentFolderSize
    currentFolderSize = getFolderSize( currentworkingdir )
    print ("SIZE: %s bytes" % ( currentFolderSize ))
    print ("DSK_SIZE: %s bytes" % ( currentDiskMode ))
    percentFull = (currentFolderSize / currentDiskMode)
    global percentFree
    percentFree = ( 1 - percentFull )
    print ("PF: %s" % ( percentFree ))
    prepar2Percent = ( percentFree * 100 )
    global par2Percent
    par2Percent = int(prepar2Percent)
    global wastedSpace
    global wastedSpaceMebibyte
    wastedSpace = int( ( prepar2Percent - par2Percent ) / 100 * currentDiskMode )
    wastedSpaceMebibyte = (wastedSpace /1024 /1024)
    print ("par2PF: %s" % ( par2Percent ))
    print ("WS: %s bytes or %.2f Mebibytes" % ( wastedSpace, wastedSpaceMebibyte ))
    global par2sizeBytes
    global par2sizeMebibyte
    par2sizeBytes = int( currentDiskMode * (par2Percent / 100))
    par2sizeMebibyte = (par2sizeBytes /1024 /1024)
    print ("par2FS: %s bytes or %.2f Mebibytes" % ( par2sizeBytes, par2sizeMebibyte ))
    print ("WARNING:  These calculations do not take in account\nthe ./recoveryFiles/command_run file")

def do_walk(the_dir):
    global filelist
    filelist = []
    for root, dirs, files in os.walk(the_dir):
        for f in files:
            fname = os.path.join(root, f)
            if os.path.isfile(fname):
                rel_fname = os.path.relpath(fname, the_dir)
                formatted_fname = ("\"./%s\"" % ( rel_fname) )
                filelist.append(formatted_fname)

def savecommand(commandSavePath):
    global par2Percent
    with open (commandSavePath, mode='a', encoding='utf-8') as commandFile:
        commandFile.write(" ".join(["par2", "c", "-m2048", "-r" +str(par2Percent), "-q" , "recoveryFiles/recoveryFiles"]))
        commandFile.write(" ")
        commandFile.write(" ".join(filelist))
        commandFile.write("\n\npar2 output:\n\n")

def runpar2():
    global par2Percent
    proc = subprocess.Popen(["xargs", "par2", "c", "-m2048", "-r" +str(par2Percent), "-q" , "recoveryFiles/recoveryFiles"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    joinedFilelist = (" ".join(filelist))
    encodedFilelist = joinedFilelist.encode('utf-8')
    
    #print(encodedFilelist)
    print ("par2 running, blocked until completion! \nFull output will be written to: ./recoveryFiles/command_run\n")
    par2output = proc.communicate(encodedFilelist)
    with open("./recoveryFiles/command_run", mode='ab') as commandFile:
        #commandFile.write("\n")
        for line in par2output:
            commandFile.write(line)
            
if not os.path.exists("recoveryFiles"):
    os.makedirs("recoveryFiles")
calculate()
do_walk(currentworkingdir)
with open("./recoveryFiles/command_run", mode='a', encoding='utf-8') as commandFile:
    commandFile.write("parbang v" + __version__)
    commandFile.write("\n\n")
    commandFile.write("------------------------------")
    commandFile.write("\n")
    commandFile.write("|   A DIAMOND IN THE ROUGH   |")
    commandFile.write("\n")
    commandFile.write("------------------------------")
    commandFile.write("\n\n")
    commandFile.write("Calculation Information:")
    commandFile.write("CWD: %s" % ( currentworkingdir ))
    commandFile.write("\n")
    commandFile.write("SIZE: %s bytes" % ( currentFolderSize ))
    commandFile.write("\n")
    commandFile.write("DSK_SIZE: %s bytes" % ( currentDiskMode ))
    commandFile.write("\n")
    commandFile.write("PF: %s" % ( percentFree ))
    commandFile.write("\n")
    commandFile.write("par2PF: %s" % ( par2Percent ))
    commandFile.write("\n")
    commandFile.write("WS: %s bytes or %.2f Mebibytes" % ( wastedSpace, wastedSpaceMebibyte ))
    commandFile.write("\n")
    commandFile.write("par2FS: %s bytes or %.2f Mebibytes" % ( par2sizeBytes, par2sizeMebibyte ))
    commandFile.write("\n")
    commandFile.write("WARNING:  These calculations do not take in account\nthe ./recoveryFiles/command_run file")
    commandFile.write("\n\n")
    commandFile.write("COMMAND RUN:")
    commandFile.write("\n")

savecommand("./recoveryFiles/command_run")

runpar2()