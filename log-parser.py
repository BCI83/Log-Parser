import platform
import time
from datetime import datetime
import os

###################################################################################################
###                                 Functions defined here:                                     ###
###################################################################################################

def clear():
    ostest = platform.platform()    
    if ostest[0] == 'W':
        os.system('cls')
    else: 
        os.system('clear')

def readfile(inputpath):
    strlist = []
    file = open(inputpath, 'r')
    strlist += file.readlines()
    file.close()
    return strlist

def writefile(writepath,list,inputpath='',addlogname=0,WriteAppend='w',printoutputpath=0):
    with open(writepath, WriteAppend) as f:
        if addlogname == 1:f.write('\n****************************************'+inputpath+'****************************************\n\n')
        for item in list:f.write("%s" % item)
        if printoutputpath != 1:print('File output to : '+writepath)

def readfulllog():    
    start = time.time()
    Linelist = []    
    print('Reading the full concatenated log file into memory...')
    Linelist = readfile(logpath+'/z.full-log.log')
    end = time.time()            
    print(str(len(Linelist))+' log lines read in '+str(end - start)[:4]+' seconds\n')
    return Linelist

def customsearch(searchw1,searchtype,list,cs,searchw2='',searchw3=''):
    start = time.time()  
    resultlist = []
    line1addition = ''
    dateinfo = ''
    if searchtype == 2:line1addition = '  +  Exclude: \''+searchw2+'\''
    if searchtype == 3:line1addition = '  +  Match: \''+searchw2+'\''
    if todatetimestring != '':dateinfo = '  +  Between: '+fromdatetimestring+'  &  '+todatetimestring
    elif fromdatetimestring != '':dateinfo = '  +  From '+fromdatetimestring+' to the end of the log'
    resultlist+='Search results for > Match: \''+searchw1+'\''+line1addition+dateinfo+'\n\n'
    inrange = 0
    matchcount = 0
    startingminute = 0
    if fromdatetimestring != '':dtfrom = datetime.strptime(fromdatetimestring, '%Y-%m-%d %H:%M:%S.%f')
    if todatetimestring != '':dtto = datetime.strptime(todatetimestring, '%Y-%m-%d %H:%M:%S.%f')
    for line in list:
        if fromdatetimestring != '':
            if startingminute == 0:                
                if line[:16] == fromdatetimestring[:16]:startingminute = 1
            else:
                try:
                    testline = line[:23]
                    test = datetime.strptime(testline, '%Y-%m-%d %H:%M:%S.%f')
                    if test >= dtfrom:inrange = 1
                    if todatetimestring != '':
                        if dtto <= test :inrange = 0
                except:
                    pass
        else:inrange = 1
        if inrange == 1:
            matchfound = 0
            if cs == 1:
                templine = line
                tempsearchw1 = searchw1
                if searchw2 != '':tempsearchw2 = searchw2
                if searchw3 != '':tempsearchw3 = searchw3
            elif cs == 0:
                templine = line.lower()
                tempsearchw1 = searchw1.lower()
            if searchw2 != '':tempsearchw2 = searchw2.lower()
            if searchw3 != '':tempsearchw3 = searchw3.lower()
            if searchtype == 1:
                if tempsearchw1 in templine:matchfound = 1
            elif searchtype == 2:
                if tempsearchw1 in templine and not tempsearchw2 in templine:matchfound = 1
            elif searchtype == 3:
                if tempsearchw1 in templine and tempsearchw2 in templine:matchfound = 1
            elif searchtype == 4:
                if tempsearchw1 in templine or tempsearchw2 in templine:matchfound = 1
            
            elif searchtype == 5:#AND AND
                if tempsearchw1 in templine and tempsearchw2 in templine and tempsearchw3 in templine:matchfound = 1
            elif searchtype == 6:#AND ( OR )
                if tempsearchw1 in templine and (tempsearchw2 in templine or tempsearchw3 in templine):matchfound = 1
            elif searchtype == 7:#AND AND-NOT
                if tempsearchw1 in templine and tempsearchw2 in templine and not tempsearchw3 in templine:matchfound = 1
            elif searchtype == 8:#OR OR
                if tempsearchw1 in templine or tempsearchw2 in templine or tempsearchw3 in templine:matchfound = 1
            elif searchtype == 9:#( OR ) AND-NOT
                if (tempsearchw1 in templine or tempsearchw2 in templine) and not tempsearchw3 in templine:matchfound = 1
            elif searchtype == 10:#AND-NOT AND-NOT
                if tempsearchw1 in templine and not tempsearchw2 in templine and not tempsearchw3 in templine:matchfound = 1

            if matchfound == 1:
                resultlist+=[line]
                matchcount += 1
    end = time.time()
    clear()
    print('Search complete... Matches found : '+str(matchcount)+'\nOperation completed in '+str(end - start)[:4]+' seconds\n\n')

    while True:
        if matchcount == 0:break
        if searchw1 == ' ERROR ':
            writefile(logpath+'/z.ERROR.log',resultlist)
            break
        elif searchw1 == ' WARN ':
            writefile(logpath+'/z.WARN.log',resultlist)
            break
        else:               
            fname = input('Please enter the filename you want the output file to have\nThe file name will be prefixed with \'z.\' and appended with \'.log\' automatically\n>')
            try:
                writefile(logpath+'/z.'+fname+'.log',resultlist)
                break
            except:print('\nBad filename, please try again\n')

def summary(type):
    start = time.time()
    print('Generating '+type+' report')
    if type == 'warning':print('Depending on the time range selected, CPU and storage I/O this can take several minutes')
    stype = ''
    if type == 'error':stype = 'ERROR'
    elif type == 'warning':stype = 'WARN'
    errorwarnlist = []
    trimmedlist = []
    uniqueerrorlist = []
    inrange = 0
    startingminute = 0
    customsearch(' '+stype+' ',1,Lines,1)
    errorwarnlist = readfile(logpath+'/z.'+stype+'.log')

    print('\nsearching for unique '+type+'s...\n')

    if fromdatetimestring != '':dtfrom = datetime.strptime(fromdatetimestring, '%Y-%m-%d %H:%M:%S.%f')
    if todatetimestring != '':dtto = datetime.strptime(todatetimestring, '%Y-%m-%d %H:%M:%S.%f')
    for line in errorwarnlist:
        if fromdatetimestring != '':
            if startingminute == 0:
                if line[:16] == fromdatetimestring[:16]:startingminute = 1
            else:
                try:                    
                    test = datetime.strptime(line[:23], '%Y-%m-%d %H:%M:%S.%f')
                    if test >= dtfrom:inrange = 1
                    if todatetimestring != '':
                        if dtto <= test :inrange = 0
                except:
                    pass
        else:inrange = 1

        if inrange == 1:
            templine = ''
            if line[41:42]==']':templine = line[41+2:]
            elif line[42:43]==']':templine = line[41+3:]
            elif line[40:41]==']':templine = line[41+1:]
            for x in range (0, 9):
                templine = templine.replace("#"+str(x), "#*")
            trimmedlist += [templine]
    
    for tline in trimmedlist:
        unique = 1
        for uline in uniqueerrorlist:
            if tline == uline:
                unique = 0
                break
        if unique == 1:uniqueerrorlist += [tline]

    uereport = []
    for err in uniqueerrorlist:
        if err != '':
            ecount = 0
            for tline in trimmedlist:
                if [err] == [tline]:ecount += 1
            uereport += [str(ecount)+'\t instances of : '+err]
    print('total unique '+type+'s found : '+str(len(uereport)))
    writefile(logpath+'/z.'+type+'Report.log',uereport)

    end = time.time()
    print('Operation completed in '+str(end - start)[:4]+' seconds\n\n')

def geterrorstacks():
    start = time.time()
    print('Creating full Error list log')
    errfound = 0
    errorwarnlist = []
    for line in Lines:
        if line[:2] == '20':
            errfound = 0
            if ' ERROR ' in line:
                errfound = 1
                errorwarnlist+=['\n############################################################################################################\n\n'+line]
        elif errfound == 1:errorwarnlist+=[line]
    writefile(logpath+'/z.error-stacks.log',errorwarnlist)
    end = time.time()
    print('Operation completed in '+str(end - start)[:4]+' seconds\n\n')

def case():
    while True:
        clear()
        print('\nDo you want this search to be case sensitive?\n')
        print('1: case sensitive')
        print('2: case insensitive')
        caseselectq = input('\nEnter the corresponding number :\n>')
        if caseselectq == '1' or caseselectq == '2':break
    clear()
    if caseselectq == '1':return 1
    else:return 0

def getlatency(latencystring,endtrim):
    ints = 0
    pingstring = ''
    for x in range ((3+endtrim), 10):
        try:
            if latencystring[-x].isdigit():
                ints +=1
                pingstring = latencystring[-x]+pingstring
        except:pass
    return pingstring

def latencyreport(list,limit,type):
    start = time.time()
    dateinfo = ''
    resultlist = []
    searchterm = type
    inrange = 0
    matchcount = 0
    startingminute = 0
    if todatetimestring != '':
        dateinfo = '  +  Between: '+fromdatetimestring+'  &  '+todatetimestring
        dtto = datetime.strptime(todatetimestring, '%Y-%m-%d %H:%M:%S.%f')
    elif fromdatetimestring != '':
        dateinfo = '  +  From '+fromdatetimestring+' to the end of the log'
        dtfrom = datetime.strptime(fromdatetimestring, '%Y-%m-%d %H:%M:%S.%f')
    resultlist+='Search results for > Match: \''+type+'\' with a response time over '+limit+'ms '+dateinfo+'\n\n'
    for line in list:
        if fromdatetimestring != '':
            if startingminute == 0:                
                if line[:16] == fromdatetimestring[:16]:startingminute = 1
            else:
                try:
                    testline = line[:23]
                    test = datetime.strptime(testline, '%Y-%m-%d %H:%M:%S.%f')
                    if test >= dtfrom:inrange = 1
                    if todatetimestring != '':
                        if dtto <= test :inrange = 0
                except:
                    pass
        else:inrange = 1
        if inrange == 1:
            if searchterm in line:
                if type == 'duration =':teststring = getlatency(line,0)
                else:teststring = getlatency(line,1)
                if int(teststring) > int(limit):
                    resultlist+=[line]
                    matchcount += 1
    print('Found '+str(matchcount)+' latencies over '+str(limit)+'ms')
    end = time.time()
    while True:
        fname = input('Please enter the filename you want the output file to have\nThe file name will be prefixed with \'z.\' and appended with \'.log\' automatically\n>')
        try:
            writefile(logpath+'/z.'+fname+'.log',resultlist)
            break
        except:print('\nBad filename, please try again\n')
    print('Operation completed in '+str(end - start)[:4]+' seconds\n\n')

###################################################################################################
###                                   Main() starts here:                                       ###
###################################################################################################

clear()
print('Make sure you have run this script with a user that has rights to read the log files')
fdt = datetime
tdt = datetime
fromdatetimestring = ''
todatetimestring = ''
casesetting = ''
firstrun = 1
caseselected = 0
Lines = []
while True:
    print('\nEnter the absolute path to the directory which')
    logpath = input('contains the symphony-commproxy*.log files \n> ')
    logpath = logpath.replace('\\', '/')
    filestowork = 0
    csymplogfileexists = 0
    if os.path.exists(logpath):
        print('The directory exists\nChecking for log files')
        symlogfilesfound = 0
        logcount = 0
        if os.path.exists(logpath+'/z.full-log.log'):symlogfilesfound += 1       
        for x in range (1, 101):
            slp = logpath+'/symphony-commproxy-'+str(x)+'.log'
            if os.path.exists(slp):logcount += 1
        if os.path.exists(logpath+'/symphony-commproxy.log'):logcount += 1
        if logcount > 0:symlogfilesfound += 2
        if symlogfilesfound == 0:print('No symphony-commproxy*.log or full-log.log files found')
        elif symlogfilesfound == 1:print('A pre-existing z.full-log.log file has been found')
        elif symlogfilesfound == 2:print(str(logcount)+' symphony-commproxy*.log files found')
        elif symlogfilesfound == 3:print(str(logcount)+' symphony-commproxy*.log files found\nA pre-existing z.full-log.log file has been found\n')
        while True:
            if symlogfilesfound == 3:
                print('\nPick an option from the choices below\n\n1: Work from the symphony-commproxy*.log files\n2: Work from the pre-existing z.full-log.log file')
                logquestion = input('\nEnter the corresponding number :\n>')
                if logquestion == '1' or logquestion == '2':break
            elif symlogfilesfound == 2:
                logquestion = '1'
                break
            elif symlogfilesfound == 1:
                logquestion = '2'
                break
        if logquestion == '1':
            with open(logpath+'/z.full-log.log', 'w') as f:f.write('')
            filestowork = 1
            logcount = 0
            teststring = ''
            for x in range (0, 101):
                teststring = logpath+'/symphony-commproxy-'+str(x)+'.log'
                if os.path.exists(teststring):
                    print('Reading : '+teststring)
                    listtowrite = readfile(teststring)
                    writefile(logpath+'/z.full-log.log',listtowrite,teststring,1,'a',1) 
                    logcount += 1
            if os.path.exists(logpath+'/symphony-commproxy.log'):
                print('Reading : '+logpath+'/symphony-commproxy.log')
                listtowrite = readfile(logpath+'/symphony-commproxy.log')
                writefile(logpath+'/z.full-log.log',listtowrite,logpath+'/symphony-commproxy.log',1,'a',1)            
                logcount += 1
                break
        elif logquestion == '2':
            filestowork = 2    
            if os.path.exists(logpath+'/z.full-log.log'):
                print('Reading : '+logpath+'/z.full-log.log')
                csymplogfileexists = 1
                logcount += 1
                break
    if logcount > 0:break           
    else:print('\''+logpath+'\' directory not found on this system\nPlease try again')
if csymplogfileexists == 0:print('A single log file has been created with all the log files concatenated in order\nIt is located at \''+logpath+'/z.full-log.log\'')

Lines = readfulllog()

while True:
    print('\nPick an option from the choices below\n')
    print('1: Quit')
    if fromdatetimestring != '':
        print('2: Date/time   (change/clear settings) \n   Currently configured search window:\n   From : '+str(fdt))
        if todatetimestring != '':print('   To   : '+str(tdt))
        else:print('   To   : End of log')
    else:print('2: Date/time   (Specify a time range to search in (optional))') 
    print('3: Err & Warn  (Preconfigured reports for Errors and Warnings)')   
    print('4: Latency     (Latency over threshold report (for: \'duration =\'))')
    print('5: Latency     (Latency over threshold report (for: \'Delivery cycle process time:\'))')
    print('6: Custom      (Display the custom search menu)')
    mainmenuq = input('\nEnter the corresponding number :\n>')
    clear()
    firstrun = 0
    start = time.time()
    if mainmenuq == '1':break    
    elif mainmenuq == '2':
        clearback = 0
        if fromdatetimestring != '':
            while True:
                print('\nThe time range below is currently configured\n')
                print('From : '+ str(fdt)+'\nTo : '+str(tdt)+'\n Which is : yyyy-mm-dd hh:mm:ss.mis\n'+str(tdt-fdt)+'\nDo you want to clear/change this?\n')
                print('1: Back')
                print('2: Clear the configured date/times')
                print('3: Change the date/times configured')
                dtq = input('\nEnter the corresponding number :\n>')
                clear()
                if dtq == '1': break
                if dtq == '2' or dtq == '3':
                    fromdatetimestring = todatetimestring = ''
                    if dtq == '2':
                        print('Date and time settings reverted back to the default (search all available dates and times)\nReading the full log file to memory...')
                        clearback = 1
                        break
                    elif dtq == '3':
                        break
            clear()
        while True:
            if clearback == 1:break
            while True:
                print('\nSetting up the date range to use for all sebsequent seraches\nEnter the \'From\' date/time in the log format (yyyy-mm-dd hh:mm:ss.mics)')
                fromdatetimestring = input('>')
                try:
                    if not '.' in fromdatetimestring:fromdatetimestring += '.0'
                    fdt = datetime.strptime(fromdatetimestring, '%Y-%m-%d %H:%M:%S.%f')
                    dtfset = 1
                    df = str(fdt)
                    break
                except:print('\nThe entered date and time string entered was not valid\nPlease try again (the format must match the CPX logs)')
            while True:
                print('\nEnter the \'To\' date/time in the log format (yyyy-mm-dd hh:mm:ss.mics)\n(leave blank to search to the end of the log file)')
                todatetimestring = ''
                todatetimestring = input('>')
                try:
                    if todatetimestring != '':
                        if not '.' in todatetimestring:todatetimestring += '.0'
                        tdt = datetime.strptime(todatetimestring, '%Y-%m-%d %H:%M:%S.%f')
                        dttset = 1
                        dt = str(dttset)
                        if fdt<tdt :break
                        else:print('\nInvalid \'To\' value, as it is before the \'From\' value..\nPlease enter a time/date later than \'From\' value: '+df[:23])
                except:print('\nThe entered date and time string entered was not valid\nPlease try again (the format must match the CPX logs)')
            clear()
            if todatetimestring != '':print('F : '+ str(fdt)+'\nT : '+str(tdt)+'\nWhich is a range of:\nh:mm:ss.mis\n'+str(tdt-fdt)+'\n')
            else:print('From : '+ str(fdt)+' to the end of the log file has been selected\n')
            break
        clear()    
    elif mainmenuq == '3':
        clear()
        while True:
            print('\nPick an option from the choices below (applied per log line)\n')
            print('1: Back to main search menu')
            print('2: Warnings  (Warning lines only)')
            print('3: Warnings  (Unique Warnings report)')
            print('4: Errors    (Error lines only)')
            print('5: Errors    (Unique Errors report)')
            print('6: Errors    (Full Error stacks (ignores date/time settings))')
            errorwarnmenuq = input('\nEnter the corresponding number :\n>')
            clear()
            if errorwarnmenuq == '1':
                clear()
                break
            elif errorwarnmenuq == '2':
                print('Creating Warning list log')
                customsearch(' WARN ',1,Lines,1)
            elif errorwarnmenuq == '3':summary('warning')
            elif errorwarnmenuq == '4':
                print('Creating short Error list log')
                customsearch(' ERROR ',1,Lines,1)
            elif errorwarnmenuq == '5':summary('error')
            elif errorwarnmenuq == '6':geterrorstacks()
    elif mainmenuq == '4':
        while True:
            print('Enter the minimum latency for the report (ms)')
            ping = getlatency(input('>')+'ms',0)        
            if ping.isdigit():break
        latencyreport(Lines,ping,'duration = ')
    elif mainmenuq == '5':
        while True:
            print('Enter the minimum latency for the report (ms)')
            ping = getlatency(input('>')+' ms',1)        
            if ping.isdigit():break
        latencyreport(Lines,ping,'Delivery cycle process time: ')
    elif mainmenuq == '6':
        clear()
        while True:
            print('\nPick an option from the choices below\n')
            print('1: Back to main search menu')
            if caseselected == 0:casesetting = 'Insensitive'
            elif caseselected == 1:casesetting = 'Sensitive'
            print('2: Change case sensitivity - Currently set to \'Case '+casesetting+'\'')
            print('3: Match one string')
            print('4: Two string AND/OR/NOT search menu')
            print('5: Three string AND/OR/NOT search menu')
            custommenuq = input('\nEnter the corresponding number :\n>')
            clear()
            if custommenuq == '1':
                clear()
                break
            if custommenuq == '2':
                caseselected = case()                
            elif custommenuq == '3':
                searchterm = input('Enter the string to search for : \n>')
                customsearch(searchterm,1,Lines,caseselected)
            elif custommenuq == '4': 
                clear()
                while True:                    
                    print('\nPick an option from the choices below (logic applied per log line)\n')
                    print('1: Back to the previous menu')
                    print('2: Match string-x AND string-y')
                    print('3: Match string-x OR string-y')
                    print('4: Match string-x AND NOT string-y')
                    siicustommenuq = input('\nEnter the corresponding number :\n>')
                    clear()
                    if siicustommenuq == '1':
                        clear()
                        break
                    elif siicustommenuq == '2':# x AND y
                        print('Search type : x AND y')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        customsearch(x,3,Lines,caseselected,y)
                    elif siicustommenuq == '3':# x OR y
                        print('Search type : x OR y')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        customsearch(x,4,Lines,caseselected,y)
                    elif siicustommenuq == '4':# x AND NOT y
                        print('Search type : x AND NOT y')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        customsearch(x,2,Lines,caseselected,y)
            elif custommenuq == '5':
                clear() 
                while True:
                    print('\nPick an option from the choices below (logic applied per log line)\n')
                    print('1: Back to the previous menu')
                    print('2: Match string-x AND string-y AND string-z')
                    print('3: Match string-x AND string-y OR string-z')
                    print('4: Match string-x AND string-y AND NOT string-z')
                    print('5: Match string-x OR string-y OR string-z')
                    print('6: Match string-x OR string-y AND NOT string-z')
                    print('7: Match string-x AND NOT string-y AND NOT string-z')                    
                    siiicustommenuq = input('\nEnter the corresponding number :\n>')
                    clear()                    
                    if siiicustommenuq == '1':
                        clear()
                        break                  
                    if siiicustommenuq == '2':# x AND y AND z
                        print('Search type : x AND y AND z')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        z = input('Enter the \'z\' string value : \n>')
                        customsearch(x,5,Lines,caseselected,y,z)
                    elif siiicustommenuq == '3':# x AND (y OR z)
                        print('Search type : x AND (y OR z)')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        z = input('Enter the \'z\' string value : \n>')
                        customsearch(x,6,Lines,caseselected,y,z)
                    elif siiicustommenuq == '4':# x AND y AND NOT z
                        print('Search type : x AND y AND NOT z')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        z = input('Enter the \'z\' string value : \n>')
                        customsearch(x,7,Lines,caseselected,y,z)
                    elif siiicustommenuq == '5':# x OR y OR z
                        print('Search type : x OR y OR z')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        z = input('Enter the \'z\' string value : \n>')
                        customsearch(x,8,Lines,caseselected,y,z)
                    elif siiicustommenuq == '6':# (x OR y) AND NOT z
                        print('Search type : (x OR y) AND NOT z')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        z = input('Enter the \'z\' string value : \n>')
                        customsearch(x,9,Lines,caseselected,y,z)
                    elif siiicustommenuq == '7':# x AND NOT y AND NOT z
                        print('Search type : x AND NOT y AND NOT z')
                        x = input('Enter the \'x\' string value : \n>')
                        y = input('Enter the \'y\' string value : \n>')
                        z = input('Enter the \'z\' string value : \n>')
                        customsearch(x,10,Lines,caseselected,y,z)
                clear()        
        clear()                