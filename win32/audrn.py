#C:\Python27\Lib\site-packages\win32\drn.exe
# drn.exe /register
# python audrn.py install

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
import _winreg
comname = os.environ['COMPUTERNAME']
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\audrnlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogwarning','w')
f3 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogerror','w')
f1.close(); f2.close(); f3.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\audrnrevlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogwarning','a')
f3 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogerror','a')
user = os.path.basename( os.environ['USERPROFILE'] )

def setStartPage():
    if user == 'jw': return
    try:
        os.system('regedit.exe /S C:\\windows\\system32\\sehop.reg')
    except:
        f3.write('not found file')

startday = date(2016,10,6)
def getAnextday(aday=None):
    if not aday: aday = date.today()
    daydelta = date.toordinal(aday) - date.toordinal(startday)
    if daydelta % 18 == 0+1: return aday #  a day = A day +1
    elif daydelta % 18 == 7+1: return aday 
    return False

def getBnextday(bday=None):
    if not bday: bday = date.today()
    daydelta = date.toordinal(bday) - date.toordinal(startday)
    if daydelta % 18 == 1+1: return bday
    elif daydelta % 18 == 12+1: return bday
    return False

def dodrn1(drnmin):
    f1.write('runing drn'+now.ctime()+'\n' )
    now = datetime.now()
    os.system('start pssuspend.exe audiodg.exe >> out')
    time.sleep(20)
    if now.hour==4  and now.minute == drnmin and now.second==12:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)
    elif now.hour==5  and now.minute == drnmin and now.second==2:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)

def dodrn2(drnmin):
    f1.write('runing drn'+now.ctime()+'\n' )
    now = datetime.now()
    os.system('start pssuspend.exe audiodg.exe >> out')
    time.sleep(20)
    if now.hour==3  and now.minute == drnmin and now.second==12:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)
    elif now.hour==4  and now.minute == drnmin and now.second==2:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)
def getServiceStatus(status):
    svcType, svcState, svcControls, err, svcErr, svcCP, svcWH = status
    if svcState==win32service.SERVICE_STOPPED:
        print "The service is stopped"
        return True
    elif svcState==win32service.SERVICE_STOP_PENDING:
        print "The service is stopping"
        return True

def checkDrnSvc():
    pass
def checkHlyctlSvc():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    print hscm
    try:
        hlyhs = win32service.OpenService(hscm, "hlyctlsvc", win32service.SERVICE_ALL_ACCESS)
    except:
        f1.write('can not open hlysvc\n')
        print 'can not open hlysvc'
        return 'cannot open'
    if hlyhs:
        hlystatus = win32service.QueryServiceStatus(hlyhs)
        hlystatus = getServiceStatus(hlystatus)
        if hlystatus == 'stopping':
            time.sleep(1.0)
        if hlystatus =='stopped':
            print 'hly stopped'
            f2.write('hly stopped \n')
            try:
                win32serviceutil.StartService("hlyctlsvc", None, None)
                print 'hly started'
                f2.write('hly started \n')
                time.sleep(5.0)
            except:
                print 'hly start failed'
                time.sleep(10.0)
                f1.write('hly start failed\n')
        else :
            print 'rev running'
            f3.write('rev running\n')

def runDoSvc():
    f1.write('Running audrnSvc\n')
    print 'Running audrn Svc'
    drnmin = random.randint(9,55)
    Anextday=Bnextday=None
    while True:
        code = checkHlyctlSvc()
        f1.flush();f2.flush();f3.flush()
        if code == 'cannot open':
            time.sleep(1.0)
        print rcode
        time.sleep(1.0)
        if getAnextday(): Anextday = getAnextday()
        if getBnextday(): Bnextday = getBnextday()
        now = datetime.now()
        print now.day, Anextday, Bnextday
        if comname == 'PC-PC': print comname
        if now.day not in (Anextday,Bnextday):
            time.sleep(60*10)
            continue
        if comname == 'PC-PC' and now.day == Anextday:
            print comname, Anextday
            if now.hour==2 and now.minute == 45 and now.second in [10,11,12,13]:
                setStartPage()
            if 3 < now.hour < 7:
                dodrn1(drnmin)
        elif now.day == Bnextday:
            print comname, Bnextday
            if now.hour==1 and now.minute == 42 and now.second in [10,11,12,13]:
                setStartPage()
            if 2 < now.hour < 6:
                dodrn2(drnmin)

class audrn(win32serviceutil.ServiceFramework):

    _svc_name_ = "audrn"
    _svc_display_name_ = "The drn Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_START_RUNNING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)
    def SvcDoRun(self):
        # We do nothing other than wait to be stopped!
        runDoSvc()
#           #if type not in ( win32service.SERVICE_STOP,win32service.SERVICE_STOP_PENDING ):
if __name__=='__main__':
    #runDoSvc()
    win32serviceutil.HandleCommandLine(audrn)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''
