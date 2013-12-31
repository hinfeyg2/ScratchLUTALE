#!/usr/bin/env python

from xml.dom import minidom
import re
import os
import ntpath
from datetime import datetime

xmldoc = minidom.parse("cmd-0.xml")
constructLuts = xmldoc.getElementsByTagName("lut")


"""
sProject = os.getenv('SCRATCH_SHOT_FILENAME','NOT WORKING')
rollpath = sProject.split("\")
rollindex = rollpath.len() - 1
temp = rollpath(rollindex)

"""

def tc_to_frame(hh, mm, ss, ff):
    return ff + (ss + mm*60 + hh*3600) * 25

def frame_to_tc(fn):
    ff = fn % 25
    s = fn // 25
    return (s // 3600, s // 60 % 60, s % 60, ff)

report = open("scratchale.ale", "w")

report.write("Heading")
report.write("\n")
report.write("\n")
report.write("FIELD_DELIM	TABS")
report.write("\n")
report.write("\n")
report.write("VIDEO_FORMAT	1080")
report.write("\n")
report.write("\n")
report.write("AUDIO_FORMAT	48khz")
report.write("\n")
report.write("\n")
report.write("FPS	25")
report.write("\n")
report.write("\n")
report.write("\n")
report.write("\n")
report.write("Column")
report.write("\n")
report.write("\n")
report.write("End	Name	Creation Date	Source File	Duration	Drive	IN-OUT	Mark IN	Mark OUT	Audio SR	Tracks	Start	Tape	Video	TapeID	Comments	<LUT>")
report.write("\n")
report.write("\n")
report.write("\n")
report.write("\n")
report.write("\n")
report.write("Data")
report.write("\n")
report.write("\n")


shotindex = xmldoc.getElementsByTagName("shot")

for shotinstance in shotindex:
	
	name = shotinstance.getElementsByTagName("name")
	for items in name:
		clipname = str(items.firstChild.data)
	
	length = shotinstance.getElementsByTagName("length")
	for items in length:
		thisshotlength = str(items.firstChild.data)

	clipdatetime = str(shotinstance.parentNode.parentNode.getAttribute('datetime'))
	d = datetime.strptime(clipdatetime,'%Y-%m-%dT%H:%M:%S')
	d.strftime('%d/%m/$Y %H:%M:%S')
	clipstarttimecode = shotinstance.getElementsByTagName("timecode")
	
	
	for items in clipstarttimecode:
		clipcode = str(items.firstChild.data)

	endtimecodearray = []
	for items in clipstarttimecode:
		tempcode = items.firstChild.data.split(":")
		startcodeframes = tc_to_frame(int(tempcode[0]), int(tempcode[1]), int(tempcode[2]), int(tempcode[3]))
		endcodelength = startcodeframes + int(thisshotlength)
		tempendtimecode = frame_to_tc(endcodelength)
		
		def addleadingzero(number):
		
			if len(str(number)) == 1:
				return "0" + str(number)
			else:
				return str(number)
		
		
		clipendtimecode = addleadingzero(tempendtimecode[0]) + ":" + addleadingzero(tempendtimecode[1]) + ":" + addleadingzero(tempendtimecode[2]) + ":" + addleadingzero(tempendtimecode[3])
	
	
	
	tempdurationcode = frame_to_tc(int(thisshotlength))
	clipduration = addleadingzero(tempdurationcode[0]) + ":" + addleadingzero(tempdurationcode[1]) + ":" + addleadingzero(tempdurationcode[2]) + ":" + addleadingzero(tempdurationcode[3])
	
	fps = shotinstance.getElementsByTagName("fps")
	for items in fps:
		clipfps = items.firstChild.data
	
	lut = shotinstance.getElementsByTagName("lut")
	for items in lut:
		cliplut = ntpath.basename(items.firstChild.data)
		
	report.write(clipendtimecode)
	report.write("	")
	report.write(clipname)
	report.write("	")
	report.write(d.strftime('%d/%m/%Y %H:%M:%S '))
	report.write("		")	
	report.write(str(clipduration))
	report.write("						")
	report.write("V")
	report.write("	")
	report.write(clipcode)
	report.write("	")
	report.write("TestRoll2")
	report.write("	")
	report.write("DNxHD 120 (HD1080i)")
	report.write(" 			")
	report.write(cliplut)

	report.write("\n")
	report.write("\n")
	
"""	
	report.write(temp)
"""	

	
report.close()