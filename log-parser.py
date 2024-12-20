#!/usr/bin/env python3

import platform, subprocess, uuid, glob, sys, time, os
from datetime import datetime
ostest = platform.platform()    

###################################################################################################
###                                 Functions defined here:                                     ###
###################################################################################################

def clear():
    if ostest[0] == 'W': # Then Windows 
        os.system('cls')
    else: # Assume Linux / Mac
        os.system('clear')

def countfiles(logpath):
    log = glob.glob(logpath+'*.log')
    txt = glob.glob(logpath+'*.txt')    
    return (log, txt)

def readfile(inputpath):
    strlist = []
    with open(inputpath, 'r', encoding='utf-8', errors='ignore') as file:
        strlist += file.readlines()
    return strlist

def writefile(writepath, list, inputpath='', addlogname=0, WriteAppend='w', printoutputpath=0):
    with open(writepath, WriteAppend, encoding='utf-8', errors='ignore') as f:
        if addlogname == 1:
            f.write('\n****************************************' + inputpath + '****************************************\n\n')
        for item in list:
            f.write("%s" % item)
        if printoutputpath != 1:
            print('File output to : ' + writepath)

def renamefile(tfname):
    if os.path.exists(logpath+tfname):
        while True:
            clear()
            fname = input('Please provide a name for the file:\n(z. and .log will be added automatically)\n>')
            try:
                os.rename(logpath+tfname, logpath+'z.'+fname+'.log')
                print('File successfully saved as: '+logpath+'z.'+fname+'.log')
                break
            except:print('Failed to save, check that only valid filename characters are being entered and try again.')

def getfilelist(logpath):
    listofnames = []
    listofext = []
    nameandext = []
    finallist = []
    fullfilelist = []
    for file in os.listdir(logpath):
        fullfilelist += [file]
        tempstring = ''        
        for x in file:
            if x.isalpha() or x == '-' or x == '_' or tempstring == 'z':
                tempstring += x
            elif x == '.':
                if not tempstring == 'z':
                    if not tempstring in listofnames:
                        if tempstring[-1:] == '-':tempstring = tempstring[:-1]
                        if not tempstring in listofnames:
                            listofnames += [tempstring]
                            listofext += [file[-4:]]
                    break    

    for n in range (0, len(listofnames)):        
        nameandext += [listofnames[n]+'*'+listofext[n]]
    for names in nameandext:
        count = 0
        for file in os.listdir(logpath):
            if names[0:-5] == file[:len(names[0:-5])]:
                if file[len(names[:-5]):len(names[:-4])] == '.' or file[len(names[:-5]):len(names[:-4])] == '-':
                    count += 1
        finallist += [str(count)+'\tfiles of type: '+names]
    return (fullfilelist, nameandext, listofnames, finallist)
              
def displayresult(stringlist):
    fname = str(uuid.uuid4())
    winapps = ['C:\\Program Files\\Notepad++\\notepad++.exe', 'C:\\Program Files (x86)\\Notepad++\\notepad++.exe', 'C:\\Windows\\System32\\notepad.exe']  # From preferred to least preferred
    with open(logpath + 'z.' + fname + '.log', 'w', encoding='utf-8', errors='ignore') as f:
        for line in stringlist:
            f.write(line)
    v1 = ''
    if ostest[0] == 'W':  # Windows
        for app in winapps:
            if os.path.exists(app):
                v1 = app
                break
    else:  # Linux & Mac
        if os.path.isfile('/usr/bin/vim'):
            v1 = 'vim'
        elif os.path.isfile('/usr/bin/nano'):
            v1 = 'nano'

    v2 = logpath + 'z.' + fname + '.log'

    if os.path.exists(v2):
        if v1 != '':
            if ostest[0] == 'W':
                subprocess.call([v1, v2])
            else:
                if v1 == 'vim':
                    subprocess.call([v1, '-c', 'set nowrap', v2])
                else:
                    subprocess.call([v1, v2])
        os.remove(v2)

def readlog(path):    
    start = time.time()
    Linelist = []    
    print('Reading the log file into memory...')
    Linelist = readfile(path)
    end = time.time()            
    print('{} log lines read in {:.2f} seconds'.format(len(Linelist), end - start))
    return Linelist

def customsearch(searchw1,searchtype,list,cs,searchw2='',searchw3=''):
    start = time.time()  
    resultlist = []
    line1addition = ''
    dateinfo = ''
    if searchtype == 2:line1addition = '  AND NOT  Match: \''+searchw2+'\''
    elif searchtype == 3:line1addition = '  AND  Match: \''+searchw2+'\''
    elif searchtype == 4:line1addition = '  OR  Match: \''+searchw2+'\''
    elif searchtype == 5:line1addition = '  AND  Match: \''+searchw2+'\'  AND  Match: \''+searchw3+'\''
    elif searchtype == 6:line1addition = '  AND  Match: \''+searchw2+'\'  OR  Match: \''+searchw3+'\''
    elif searchtype == 7:line1addition = '  AND  Match: \''+searchw2+'\'  AND NOT  Match: \''+searchw3+'\''
    elif searchtype == 8:line1addition = '  OR  Match: \''+searchw2+'\'  OR  Match: \''+searchw3+'\''
    elif searchtype == 9:line1addition = '  OR  Match: \''+searchw2+'\'  AND NOT  Match: \''+searchw3+'\''
    elif searchtype == 10:line1addition = '  AND NOT  Match: \''+searchw2+'\'  AND NOT  Match: \''+searchw3+'\''    
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
                templine = str(line).lower()
                tempsearchw1 = str(searchw1).lower()
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
            elif searchtype == 5:
                if tempsearchw1 in templine and tempsearchw2 in templine and tempsearchw3 in templine:matchfound = 1
            elif searchtype == 6:
                if tempsearchw1 in templine and (tempsearchw2 in templine or tempsearchw3 in templine):matchfound = 1
            elif searchtype == 7:
                if tempsearchw1 in templine and tempsearchw2 in templine and not tempsearchw3 in templine:matchfound = 1
            elif searchtype == 8:
                if tempsearchw1 in templine or tempsearchw2 in templine or tempsearchw3 in templine:matchfound = 1
            elif searchtype == 9:
                if (tempsearchw1 in templine or tempsearchw2 in templine) and not tempsearchw3 in templine:matchfound = 1
            elif searchtype == 10:
                if tempsearchw1 in templine and not tempsearchw2 in templine and not tempsearchw3 in templine:matchfound = 1
            if matchfound == 1:
                resultlist+=[line]
                matchcount += 1
    end = time.time()
    clear()
    print('Search complete...\nOperation completed in '+str(end - start)[:4]+' seconds\nMatches found: '+str(matchcount)+'\n\n')

    if matchcount != 0:
        return resultlist
        
def summary(stype):
    start = time.time()
    print('Generating '+stype+' report')
    if stype == 'WARN':print('Depending on the time range selected, CPU and storage I/O this can take several minutes')
    errorwarnlist = []
    trimmedlist = []
    uniqueerrorlist = []
    inrange = 0
    startingminute = 0    
    errorwarnlist = customsearch(' '+stype+' ',1,Lines,1)

    print('searching for unique '+stype+'s...\n')

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
            if ecount < 1000:addtab = '\t'
            else:addtab=''
            uereport += [str(ecount)+addtab+'\t instances of : '+err]
    end = time.time()
    print('Operation completed in '+str(end - start)[:4]+' seconds\n\n')
    print('total unique '+stype+'s found : '+str(len(uereport)))
    return uereport

def geterrorstacks():
    start = time.time()
    print('Creating full Error stack list log')
    errfound = 0
    errorwarnlist = []
    for line in Lines:
        if line[:2] == '20':
            errfound = 0
            if ' ERROR ' in line:
                errfound = 1
                errorwarnlist+=['\n###########################################################################################################################################################################################\n###########################################################################################################################################################################################\\n###########################################################################################################################################################################################\\n\n'+line]
        elif errfound == 1:errorwarnlist+=[line]
    end = time.time()
    print('Operation completed in '+str(end - start)[:4]+' seconds\n\n')
    return errorwarnlist

def getlatency(latencystring,endtrim):
    ints = 0
    pingstring = ''
    for x in range ((3+endtrim), 12):
        try:
            if latencystring[-x].isdigit():
                ints +=1
                pingstring = latencystring[-x]+pingstring
        except:pass
    return pingstring

def latencyreport(list,limit,type):
    while True:
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
            dtfrom = datetime.strptime(fromdatetimestring, '%Y-%m-%d %H:%M:%S.%f')
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
        end = time.time()
        print('Operation completed in '+str(end - start)[:4]+' seconds\n')
        print('Found '+str(matchcount)+' latencies over '+str(limit)+'ms\n')
        return resultlist

def getmultiplelogs(logpath,mlogname):
    while True:
        with open(logpath+'z.combined.log', 'w') as f:f.write('')
        for file in os.listdir(logpath):

            if file[:len(mlogname)] == mlogname:
                if file[len(mlogname):len(mlogname)+1] == '.':
                    print(file)
        break
    q = input('Hit Enter to continue...\n>')

    '''listtowrite = readfile(logpath+file)
        writefile(logpath+logname,listtowrite,file,1,'a',1)'''
        #return List
    
def getmultiplesymphonylogs(logpath='', slogname=''):
    symphonylogtype = slogname[9:]
    with open(logpath + 'z.combined.log', 'w', encoding='utf-8', errors='ignore') as combined_file:
        logcount = 0
        teststring = ''
        for x in range(0, 101):
            teststring = logpath + 'symphony-' + symphonylogtype + '-' + str(x) + '.log'
            if os.path.exists(teststring):
                print('Reading : ' + teststring)
                listtowrite = readfile(teststring)
                writefile(logpath + 'z.combined.log', listtowrite, teststring, 1, 'a', 1)
                logcount += 1
        if os.path.exists(logpath + 'symphony-' + symphonylogtype + '.log'):
            print('Reading : ' + logpath + 'symphony-' + symphonylogtype + '.log')
            listtowrite = readfile(logpath + 'symphony-' + symphonylogtype + '.log')
            writefile(logpath + 'z.combined.log', listtowrite, logpath + 'symphony-' + symphonylogtype + '.log', 1, 'a', 1)
            logcount += 1
    clear()
    print('A single log file has been created with all the log files concatenated in order. It is located at \'{}z.combined.log\''.format(logpath))
    Lines = readlog(logpath + 'z.combined.log')
    return Lines

def specifylogs(logpath,firstrun=0,Lines=[]):
    logname = 'z.combined.log'    
    #Lines = []    
    while True:        
        combinedlog = 0
        logcount = 0
        for x in range (1, 101):
            slp = logpath+'symphony-commproxy-'+str(x)+'.log'
            if os.path.exists(slp):logcount += 1
        if os.path.exists(logpath+'symphony-commproxy.log'):logcount += 1
        if os.path.exists(logpath+logname):combinedlog += 1
        print('\nThe directory \''+logpath+'\' contains:\n')

        print(str(len([entry for entry in os.listdir(logpath)]))+'\tfiles in total\n')
        # return (fullfilelist, nameandext, listofnames, finallist)
        fullfilelist, nameandext, listofnames, finallist = getfilelist(logpath)
        for names in finallist:
            print(names)
        print('\nPick an option from the choices below\n(Options 5 and higher will overwrite or create a new z.combined.log file)\n')
        if firstrun == 0:print('1:  Back to previous menu')
        else:print('1:  Quit')
        print('2:  Change working directory')
        print('3:  Specify a single file to work with')

        if combinedlog > 0:
            print('4:  Work with the most recently created z.combined.log file')
        else:
            print('4:  There is no pre-existing z.combined.log file in the directory (this option is disabled)')
        menuoptionpos = 5
        for names in nameandext: # generate options from 6 onwards
            if names[0:2] == 'z.':pass
            elif menuoptionpos < 10:print(str(menuoptionpos)+':  All files of type: '+names)
            else: print(str(menuoptionpos)+': All files of type: '+names)
            menuoptionpos += 1
        logtypeq = input('\nEnter the corresponding number :\n> ')
        clear()
        if logtypeq == '1':
            if firstrun == 0:   
                if Lines != []:break # back
            else:sys.exit() # quit
        if logtypeq == '2': # change directory
            Lines = []
            specifylogpath()
        elif logtypeq == '3': # specify a single log
            while True:
                logname = input('\nEnter the file name of the log file:\n> ')
                if logname[-1] == ' ':logname = logname[:-1]
                if os.path.exists(logpath+logname):
                    Lines = readlog(logpath+logname)
                    break
                else:print('\n\''+logpath+logname+'\' not found...')
            break
        elif logtypeq == '4': # work with pre-existing z.combined.log file
            logname = 'z.combined.log'
            if os.path.exists(logpath+logname):
                if os.path.exists(logpath+logname):
                    print('Reading : '+logpath+logname)
                    Lines = readlog(logpath+logname)
                break
            else:
                clear()
                print('\n********** \''+logpath+logname+'\' not found... **********')            
        else:
            try:
                if int(logtypeq) > 4: # deal with the dynamically created options from 4 onwards
                    menuoptionpos = 5
                    for names in listofnames:
                        if menuoptionpos == int(logtypeq):
                            if names.lower()[:9] == 'symphony-': # read symphony-*.log files in order
                                Lines = getmultiplesymphonylogs(logpath,names)
                            else: # read specified files in order
                                Lines = getmultiplelogs(logpath,names)
                        menuoptionpos += 1
            except:pass
        if Lines != []:break         
    return (logname, logpath, Lines)

def resultmenu(rlist, q4v=0):
    while True:
        print('Pick from the options below\n')
        print('1: Back to previous menu')
        print('2: Save the results to a file')
        print('3: View the results in a text editor  (you will still have the option to save it after)')
        if q4v == 1:print('4: Refine Search')
        q = input('>')
        if q == '1':
            clear()
            break            
        if q == '2':
            writefile(logpath+'z.temp.log',rlist)
            renamefile('z.temp.log')                
        if q == '3':
            displayresult(rlist)
        if q4v == 1:
            if q == '4':
                clear()                  
                return 'refine'
        clear()

def specifylogpath():
    while True:
        logpath = input('\nEnter the absolute path to the directory which contains the log file(s):\nLinux example /symphony/cpx/customer/logs\nWindows example c:\\users\\user\\desktop\\logs\n> ')
        if logpath[-1] == ' ':
            logpath = logpath[:-1]
        logpath = logpath+'/'
        logpath = logpath.replace('\\', '/')    
        if os.path.exists(logpath):
            clear()
            return logpath
        else:
            clear()
            print('\nThe path \''+logpath+'\'\ndoes not appear to be valid, please try again\n')

###################################################################################################
###                                     Main() starts here:                                     ###
###################################################################################################

clear()
print('Make sure you have run this script with a user that has rights to read the log files')
fdt = datetime
tdt = datetime
fromdatetimestring = ''
todatetimestring = ''
casesetting = 'Insensitive'
caseselected = 0
Lines = []
logpath = specifylogpath()
logname, logpath, Lines = specifylogs(logpath,1)
retry = 0
while True:
    if retry == 0:
        print('\nPick an option from the choices below\n')
        print('1: Quit')
        if fromdatetimestring != '':
            print('2: Date/time   (change/clear settings) \n   Currently configured search window:\n   From : '+str(fdt))
            if todatetimestring != '':print('   To   : '+str(tdt))
            else:print('   To   : End of log')
        else:print('2: Date/time   (Specify a time range to search in (optional))')
        print('3: Log select  (Open the file/directory selection menu)')
        print('4: Err & Warn  (Preconfigured reports for Errors and Warnings in CPX logs)')
        print('5: Latency     (Latency over provided threshold report (for: \'duration =\') in CPX logs)')
        print('6: Latency     (Latency over provided threshold report (for: \'Delivery cycle process time:\') in CPX logs)')
        print('7: Custom      (Display the 1, 2 or 3 string AND/OR/NOT search menu)')
        mainmenuq = input('\nEnter the corresponding number :\n> ')
    else: retry = 0
    clear()
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
                dtq = input('\nEnter the corresponding number :\n> ')
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
        logname, logpath, Lines = specifylogs(logpath, 0, Lines)
    elif mainmenuq == '4':
        retry = 0
        while True:
            if retry == 0:
                print('\nPick an option from the choices below (applied per log line)\n')
                print('1: Back to main search menu')
                print('2: Warnings  (Warning lines only)')
                print('3: Warnings  (Unique Warnings report)')
                print('4: Errors    (Error lines only)')
                print('5: Errors    (Unique Errors report)')
                print('6: Errors    (Full Error stacks (ignores date/time settings))')
                errorwarnmenuq = input('\nEnter the corresponding number :\n> ')
            else: retry = 0                
            clear()
            if errorwarnmenuq == '1':
                clear()
                break
            elif errorwarnmenuq == '2':
                print('Creating Warning list log')
                resultmenu(customsearch(' WARN ',1,Lines,1))
            elif errorwarnmenuq == '3':resultmenu(summary('WARN'))
            elif errorwarnmenuq == '4':
                print('Creating short Error list log')
                resultmenu(customsearch(' ERROR ',1,Lines,1))
            elif errorwarnmenuq == '5':resultmenu(summary('ERROR'))
            elif errorwarnmenuq == '6':resultmenu(geterrorstacks())
        clear()
    elif mainmenuq == '5':
        while True:
            print('Enter the minimum latency for the report (ms)')
            ping = getlatency(input('>')+'ms',0)        
            if ping.isdigit():break
        if resultmenu(latencyreport(Lines,ping,'duration = '), 1) == 'refine':retry = 1
        clear()
    elif mainmenuq == '6':
        while True:
            print('Enter the minimum latency for the report (ms)')
            ping = getlatency(input('>')+' ms',1)        
            if ping.isdigit():break
        if resultmenu(latencyreport(Lines,ping,'Delivery cycle process time: '), 1) == 'refine':retry = 1
        clear()
    elif mainmenuq == '7':
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
            custommenuq = input('\nEnter the corresponding number :\n> ')
            clear()
            if custommenuq == '1':
                break
            if custommenuq == '2':
                if caseselected == 1:caseselected = 0
                else: caseselected = 1                
            elif custommenuq == '3':
                searchterm = input('Enter the string to search for :\n> ')
                resultmenu(customsearch(searchterm,1,Lines,caseselected))
            elif custommenuq == '4':
                retry = 0
                while True:
                    if retry == 0:                 
                        print('\nPick an option from the choices below (logic applied per log line)\n')
                        print('1: Back to the previous menu')
                        print('2: Match string-x AND string-y')
                        print('3: Match string-x OR string-y')
                        print('4: Match string-x AND NOT string-y')
                        siicustommenuq = input('\nEnter the corresponding number :\n> ')
                    else: retry = 0
                    clear()
                    if siicustommenuq == '1':
                        break
                    elif siicustommenuq == '2':
                        print('Search type : x AND y')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        if resultmenu(customsearch(x,3,Lines,caseselected,y), 1) == 'refine':retry = 1
                    elif siicustommenuq == '3':
                        print('Search type : x OR y')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        if resultmenu(customsearch(x,4,Lines,caseselected,y), 1) == 'refine':retry = 1
                    elif siicustommenuq == '4':
                        print('Search type : x AND NOT y')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        if resultmenu(customsearch(x,2,Lines,caseselected,y), 1) == 'refine':retry = 1
                    clear()
            elif custommenuq == '5':
                clear()
                retry = 0
                while True:
                    if retry == 0:
                        print('\nPick an option from the choices below (logic applied per log line)\n')
                        print('1: Back to the previous menu')
                        print('2: Match string-x AND string-y AND string-z')
                        print('3: Match string-x AND string-y OR string-z')
                        print('4: Match string-x AND string-y AND NOT string-z')
                        print('5: Match string-x OR string-y OR string-z')
                        print('6: Match string-x OR string-y AND NOT string-z')
                        print('7: Match string-x AND NOT string-y AND NOT string-z')                    
                        siiicustommenuq = input('\nEnter the corresponding number :\n> ')
                    else:retry = 0
                    clear()                    
                    if siiicustommenuq == '1':
                        clear()
                        break                  
                    if siiicustommenuq == '2':
                        print('Search type : x AND y AND z')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        z = input('Enter the \'z\' string value :\n> ')
                        if resultmenu(customsearch(x,5,Lines,caseselected,y,z), 1) == 'refine':retry = 1
                    elif siiicustommenuq == '3':
                        print('Search type : x AND (y OR z)')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        z = input('Enter the \'z\' string value :\n> ')
                        if resultmenu(customsearch(x,6,Lines,caseselected,y,z), 1) == 'refine':retry = 1
                    elif siiicustommenuq == '4':
                        print('Search type : x AND y AND NOT z')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        z = input('Enter the \'z\' string value :\n> ')
                        if resultmenu(customsearch(x,7,Lines,caseselected,y,z), 1) == 'refine':retry = 1
                    elif siiicustommenuq == '5':
                        print('Search type : x OR y OR z')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        z = input('Enter the \'z\' string value :\n> ')
                        if resultmenu(customsearch(x,8,Lines,caseselected,y,z), 1) == 'refine':retry = 1
                    elif siiicustommenuq == '6':
                        print('Search type : (x OR y) AND NOT z')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        z = input('Enter the \'z\' string value :\n> ')
                        if resultmenu(customsearch(x,9,Lines,caseselected,y,z), 1) == 'refine':retry = 1
                    elif siiicustommenuq == '7':
                        print('Search type : x AND NOT y AND NOT z')
                        x = input('Enter the \'x\' string value :\n> ')
                        y = input('Enter the \'y\' string value :\n> ')
                        z = input('Enter the \'z\' string value :\n> ')
                        if resultmenu(customsearch(x,10,Lines,caseselected,y,z), 1) == 'refine':retry = 1
                    clear()
                clear()
        clear()
