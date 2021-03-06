""" monitor.py
Monitoring Application for Application's log file.
Log file is written to in append-only fashion. 
@author: Shreyas Moudgalya{shreyas@hawk.iit.edu}
"""

from argparse import ArgumentParser
from datetime import datetime
from send_email import *
import time
GLOBAL_TOTAL = 0

"""Consume the input log file
	Invoke parseLine() for each new line of log"""

def main():
	#p=ArgumentParser()
	#p.addArgument("log_file",help="file to write application logs to")
	#args = p.parse_args()

	try:
		logfile = open("logfile.txt", "r")
		#print ("Name of the file: ", logfile.name)
	except Exception as e:
		print(str(e))

	parseLine(logfile)
	
	

def parseFile(logfile):
    #logfile.seek(0,2) #Go to the end of the file
    while True:
        line = logfile.readline()
        #print(line)
        if not line:
            time.sleep(0.1)
            continue
        yield line


""" Parses a give line of the log
Calls send_email(msg) with all stats info when ERROR line has occurred """
def parseLine(logfile):
	parseFileGenerator = parseFile(logfile)
	
	for line in parseFileGenerator:
		item = line.replace('[',"")
		items = item.split("]")
		incidentTime = items[0]
		logName = items[1]
		levelName = items[2]
		errorMessage = items[3]
		
		if levelName == "ERROR":
			print(line.rstrip('\n'))
			global GLOBAL_TOTAL
			GLOBAL_TOTAL += 1
			message = """
	##SERVER ALERT
	##Received: {incidentdate}
	##Total Alerts: {total:7d}
	##Log Name: {log}
	##The Log Error is {m}""".format(incidentdate=incidentTime,total=GLOBAL_TOTAL,log=logName,m=errorMessage)
			send_email(message)

			
if __name__ == "__main__":
	main()
