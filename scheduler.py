import requests
import os,sys
import subprocess
import webbrowser
import shutil
import traceback,types
import urllib2

# this schedules the script to run every X minutes
def Set_Time(time):
    directory = 'C:\Windows\SystWOW64\config\systemprofile\Desktop'
    if not os.path.exists(directory):
        if not isUserAdmin():
            try:
                runAsAdmin()
                os.makedirs(directory)
            except:
                pass
    try:
        subprocess.check_output('schtasks /create /sc minute /mo ' + str(time) + ' /tn "test_process_to_run_every_'+str(time)+'_min" /tr //'+sys.argv[0],shell=True)
    except Exception as e:
        webbrowser.open_new('https://www.google.ca/search?source=hp&q=' + str(e))
# Checks if root
def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print "Admin check failed, assuming not an admin."
            return False
    elif os.name == 'posix':
        return os.getuid() == 0
    else:
        raise RuntimeError, "Unsupported operating system for this module: %s" % (os.name,)

# Asks for root
def runAsAdmin(cmdLine=None, wait=True):
    if os.name != 'nt':
        raise RuntimeError, "This function is only implemented on Windows."
    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon
    python_exe = sys.executable
    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
        raise ValueError, "cmdLine is not a sequence."
    cmd = '"%s"' % (cmdLine[0],)
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'
    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)
    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)        
    else:
        rc = None
    return rc

Set_Time(1)
