#!/usr/bin/python

import sys,re,datetime
from datetime import *
parameter = sys.argv

def time2str(dt):
    return "%s%s%sT%s%s%s"%(dt.date.year,dt.date.month,dt.date.day,dt.time.hour,dt.time.minute,dt.time.second)

def str2time(st):
    #print "%s %s %s %s %s %s\n"%(st[0:4],st[4:6],st[6:8],st[9:11],st[11:13],st[13:16]);
    dt = datetime(int(st[0:4]),int(st[4:6]),int(st[6:8]),int(st[9:11]),int(st[11:13]),int(st[13:16]));
    return dt

inputFile = "stdCourseTable.action.html"
outputFile = ""
CALSCALE = "GREGORIAN"
CALNAME = "Curriculum"
TIMEZONE = "Asia/Shanghai"
TZOFFSETFROM = "+0800"
TZOFFSETTO = "+0800"
TZNAME = "CST"
DTSTART = "19700101T000000"

TIMEFORMAT = "%Y%m%dT%H%M%S"

startTime = datetime(2012,9,10,0,0,0);

timeList = [
         [timedelta(hours=8 ,minutes=0) ,timedelta(hours=8 ,minutes=45)]
        ,[timedelta(hours=8 ,minutes=55),timedelta(hours=9 ,minutes=40)]
        ,[timedelta(hours=9 ,minutes=55),timedelta(hours=10,minutes=40)]
        ,[timedelta(hours=10,minutes=50),timedelta(hours=11,minutes=35)]
        ,[timedelta(hours=11,minutes=45),timedelta(hours=12,minutes=30)]
        ,[timedelta(hours=13,minutes=30),timedelta(hours=14,minutes=15)]
        ,[timedelta(hours=14,minutes=25),timedelta(hours=15,minutes=10)]
        ,[timedelta(hours=15,minutes=20),timedelta(hours=16,minutes=05)]
        ,[timedelta(hours=16,minutes=15),timedelta(hours=17,minutes=0)]
        ,[timedelta(hours=17,minutes=10),timedelta(hours=17,minutes=55)]
        ,[timedelta(hours=18,minutes=30),timedelta(hours=19,minutes=15)]
        ,[timedelta(hours=19,minutes=25),timedelta(hours=20,minutes=10)]
        ,[timedelta(hours=20,minutes=20),timedelta(hours=21,minutes=05)]
        ,[timedelta(hours=21,minutes=15),timedelta(hours=22,minutes=0)]]

weekList = ["MO"
        ,"TU"
        ,"WE"
        ,"TH"
        ,"FR"
        ,"SA"
        ,"SU"
        ]

weekInSemester = 19;

argv = sys.argv
for i in range(len(argv)):
    if (argv[i]=='-i') | (argv[i]=='--input-file'):
        if i<len(argv) - 1:
            inputFile = argv[i + 1]
            i += 1
        else:
            print "Please type a file name after %s\n"%argv[i]
    if (argv[i]=='-o') | (argv[i]=='--outoput-file'):
        if i<len(argv) - 1:
            outputFile = argv[i + 1]
            i += 1
        else:
            print "Please type a file name after %s\n"%argv[i]

if outputFile=="":
    pos = inputFile.rfind('.')
    if (pos>=0):
        outputFile = inputFile[:pos + 1] + 'ics';
    else:
        outputFile = inputFile + '.ics';

print "Please input the date when the semester start."
print "Format Example : 20120910"
print "It means the semester starts at 10th Sept,2012"
print "Now is your turn : "

startTime = str2time(raw_input() + "T000000");

print "How many weeks are there in a semester ?"

weekInSemester = int(raw_input())

fin = open(inputFile,"r")
fout = open(outputFile,"w")

print "Input File : %s"%inputFile
print "Output File : %s"%outputFile
fout.write("BEGIN:VCALENDAR\n\
PRODID:-//Google Inc//Google Calendar 70.9054//EN\n\
VERSION:2.0\n\
CALSCALE:%s\n\
METHOD:PUBLISH\n\
X-WR-CALNAME:%s\n\
X-WR-TIMEZONE:%s\n\
X-WR-CALDESC:\n\
BEGIN:VTIMEZONE\n\
TZID:%s\n\
X-LIC-LOCATION:%s\n\
BEGIN:STANDARD\n\
TZOFFSETFROM:%s\n\
TZOFFSETTO:%s\n\
TZNAME:%s\n\
DTSTART:%s\n\
END:STANDARD\n\
END:VTIMEZONE\n\
"%(CALSCALE,CALNAME,TIMEZONE,TIMEZONE,TIMEZONE,TZOFFSETFROM,TZOFFSETTO,TZNAME,DTSTART))

#print datetime.now()
#today = time2str(datetime.now())
today = datetime.now().strftime(TIMEFORMAT)
cur = fin.readline();
while cur.find("var index=0")==-1:
    cur = fin.readline();

cur = fin.readline();
while cur!="":
    if cur.find("index=")!=-1 and fin.readline().find("arranges[index]=new TimeUnit();")!=-1:
        cur = fin.readline();
        week = int(cur[cur.find("week=") + 5:-3])
        cur = fin.readline();
        startUnit = int(cur[cur.find("Unit=") + 5:-3])
        cur = fin.readline();
        units = int(cur[cur.find("nits=") + 5:-3])
        cur = fin.readline();
        content = cur[cur.find("ent='") + 5:-3]

        weekDelta = timedelta(days=week - 1)

        fout.write("BEGIN:VEVENT\n")
        fout.write("DTSTART;TZID=%s:%s\n"%(TIMEZONE,(startTime + weekDelta + timeList[startUnit - 1][0]).strftime(TIMEFORMAT)))
        fout.write("DTEND;TZID=%s:%s\n"%(TIMEZONE,(startTime + weekDelta + timeList[startUnit + units - 2][1]).strftime(TIMEFORMAT)))
        fout.write("RRULE:FREQ=WEEKLY;COUNT=%d;BYDAY=%s\n"%(weekInSemester,weekList[week - 1]))
        fout.write("DTSTAMP%sZ\n"%(today))
        #fout,write("UID")
        fout.write("CREATED:%sZ\n"%(today))
        fout.write("DESCRIPTION:%s\n"%(content[:content.find("<br/>")].replace("<br>"," ")))
        fout.write("LAST-MODIFIED:%sZ\n"%(today))
        fout.write("LOCATION:%s\n"%(content[content.find("<br/>"):].replace("<br>","").replace("<br/>"," ")))
        fout.write("SEQUENCE:%d\n"%(0))
        fout.write("STATUS:CONFIRMED\n")
        fout.write("SUMMARY:%s\n"%(content[content.find("<br>") + 4:content.find("<br/>")]))
        fout.write("TRANSP:OPAQUE\n")
        fout.write("END:VEVENT\n")
    cur=fin.readline();

fout.write("END:VCALENDAR\n")
fout.close()
