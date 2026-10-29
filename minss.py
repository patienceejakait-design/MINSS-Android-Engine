import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os, shutil, subprocess, threading, time, json

APP='MINSS Android Engine V5.1 Debug'
BG='#080b09'; PANEL='#111713'; GREEN='#39ff88'; TXT='#eef7f0'; MUTED='#9aa79e'; RED='#ff6b6b'
BASE=Path(__file__).resolve().parent
CONFIG=BASE/'minss_config.json'; LOGFILE=BASE/'minss_debug.log'

def sdk_candidates():
    home=Path.home(); paths=[]
    for k in ('ANDROID_SDK_ROOT','ANDROID_HOME'):
        if os.environ.get(k): paths.append(Path(os.environ[k]))
    paths += [home/'AppData/Local/Android/Sdk', Path('C:/Android/Sdk'), Path('C:/Android'), home/'Android/Sdk']
    out=[]
    for p in paths:
        try:
            if p.exists() and p not in out: out.append(p)
        except Exception: pass
    return out

def find_tool(name):
    for candidate in (shutil.which(name), shutil.which(name+'.exe')):
        if candidate: return str(Path(candidate))
    for sdk in sdk_candidates():
        for p in (sdk/'emulator'/f'{name}.exe', sdk/'platform-tools'/f'{name}.exe', sdk/'emulator'/name, sdk/'platform-tools'/name):
            if p.exists(): return str(p)
    return ''

class App:
    def __init__(self, root):
        self.root=root; root.title(APP); root.geometry('940x700'); root.minsize(780,580); root.configure(bg=BG)
        self.config=self.load_config(); self.emu=self.config.get('emulator') or find_tool('emulator'); self.adb=self.config.get('adb') or find_tool('adb'); self.avds=[]
        top=tk.Frame(root,bg='#050706'); top.pack(fill='x')
        tk.Label(top,text='MINSS',font=('Segoe UI',22,'bold'),fg=GREEN,bg='#050706').pack(side='left',padx=22,pady=14)
        tk.Label(top,text='ANDROID ENGINE • V5.1 DEBUG',font=('Segoe UI',11,'bold'),fg=TXT,bg='#050706').pack(side='left')
        self.status=tk.Label(root,text='Checking tools…',bg=BG,fg=MUTED,font=('Segoe UI',10)); self.status.pack(anchor='w',padx=22,pady=(12,5))
        body=tk.Frame(root,bg=BG); body.pack(fill='both',expand=True,padx=18,pady=8)
        left=tk.Frame(body,bg=PANEL,width=250); left.pack(side='left',fill='y',padx=(0,12)); left.pack_propagate(False)
        right=tk.Frame(body,bg=PANEL); right.pack(side='left',fill='both',expand=True)
        tk.Label(left,text='ENGINE TOOLS',bg=PANEL,fg=GREEN,font=('Segoe UI',12,'bold')).pack(anchor='w',padx=15,pady=(14,8))
        self.button(left,'Detect tools',self.detect); self.button(left,'Browse for emulator.exe',self.pick_emu); self.button(left,'Browse for adb.exe',self.pick_adb)
        self.button(left,'List virtual devices',self.list_avds); self.button(left,'Boot selected (Lite)',self.boot); self.button(left,'Refresh ADB devices',self.devices); self.button(left,'Install APK',self.install); self.button(left,'Open debug log',self.open_log)
        tk.Label(right,text='Virtual devices (select one)',bg=PANEL,fg=TXT,font=('Segoe UI',12,'bold')).pack(anchor='w',padx=14,pady=(12,6))
        self.listbox=tk.Listbox(right,bg='#070a08',fg=TXT,selectbackground='#176c3d',font=('Consolas',10),height=6,relief='flat'); self.listbox.pack(fill='x',padx=14)
        tk.Label(right,text='Activity log',bg=PANEL,fg=TXT,font=('Segoe UI',12,'bold')).pack(anchor='w',padx=14,pady=(12,6))
        self.logbox=tk.Text(right,bg='#070a08',fg=TXT,insertbackground=GREEN,font=('Consolas',9),wrap='word',relief='flat'); self.logbox.pack(fill='both',expand=True,padx=14,pady=(0,14))
        self.log('V5.1 diagnostic build started.')
        self.log('Important: MINSS is a launcher/bridge, not an Android runtime by itself.')
        self.detect()
    def load_config(self):
        try: return json.loads(CONFIG.read_text(encoding='utf-8'))
        except Exception: return {}
    def save_config(self):
        CONFIG.write_text(json.dumps({'emulator':self.emu,'adb':self.adb},indent=2),encoding='utf-8')
    def button(self, parent, label, fn):
        tk.Button(parent,text=label,command=fn,bg='#17221b',fg=TXT,activebackground='#245b38',activeforeground=TXT,relief='flat',font=('Segoe UI',10),padx=7,pady=8).pack(fill='x',padx=12,pady=4)
    def log(self,msg):
        line=f'[{time.strftime("%H:%M:%S")}] {msg}'
        try:
            with LOGFILE.open('a',encoding='utf-8') as f: f.write(line+'\n')
        except Exception: pass
        self.logbox.insert('end',line+'\n'); self.logbox.see('end')
    def run(self,args,timeout=25):
        try:
            p=subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=timeout,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            return p.returncode, (p.stdout+'\n'+p.stderr).strip()
        except subprocess.TimeoutExpired: return 124, 'Command timed out after '+str(timeout)+' seconds.'
        except Exception as e: return 1, repr(e)
    def detect(self):
        if not self.emu: self.emu=find_tool('emulator')
        if not self.adb: self.adb=find_tool('adb')
        self.log('Emulator path: '+(self.emu or 'NOT FOUND'))
        self.log('ADB path: '+(self.adb or 'NOT FOUND'))
        self.log('SDK candidates: '+('; '.join(map(str,sdk_candidates())) if sdk_candidates() else 'none found in standard locations'))
        self.status.config(text=('Emulator and ADB detected' if self.emu and self.adb else 'Missing tool(s) — use Browse buttons to locate them'),fg=(GREEN if self.emu and self.adb else RED))
        if self.emu: self.list_avds()
    def pick_emu(self):
        f=filedialog.askopenfilename(title='Select emulator.exe',filetypes=[('Windows executable','emulator.exe'),('Executable files','*.exe'),('All files','*.*')])
        if f: self.emu=f; self.save_config(); self.log('Manually selected emulator: '+f); self.detect()
    def pick_adb(self):
        f=filedialog.askopenfilename(title='Select adb.exe',filetypes=[('Windows executable','adb.exe'),('Executable files','*.exe'),('All files','*.*')])
        if f: self.adb=f; self.save_config(); self.log('Manually selected ADB: '+f); self.detect()
    def list_avds(self):
        if not self.emu: self.log('Cannot list AVDs: emulator.exe not found. Use Browse for emulator.exe.'); return
        c,o=self.run([self.emu,'-list-avds'])
        self.listbox.delete(0,'end'); self.avds=[x.strip() for x in o.splitlines() if x.strip() and not x.lower().startswith(('emulator:','info:'))]
        for a in self.avds: self.listbox.insert('end',a)
        self.log('List AVDs exit code: '+str(c)+'; output: '+(o or '(empty)'))
        if not self.avds: self.log('No AVD listed. This is not a boot failure yet: there may be no configured virtual device for this SDK.')
    def boot(self):
        if not self.emu: messagebox.showerror('Emulator not found','Use Browse for emulator.exe and select it from your Android SDK emulator folder.'); return
        sel=self.listbox.curselection()
        if not sel: messagebox.showinfo('Select a device','Click a device name in the list first. If the list is empty, click List virtual devices and inspect the log.'); return
        name=self.avds[sel[0]]
        args=[self.emu,'-avd',name,'-no-snapshot','-no-boot-anim','-gpu','swiftshader_indirect','-memory','768','-cores','2','-noaudio']
        self.log('Boot command: '+' '.join(args))
        self.log('Trying a lightweight test configuration: 768 MB guest RAM. May still be too heavy for 4 GB total system RAM.')
        def worker():
            try:
                with LOGFILE.open('a',encoding='utf-8') as f:
                    p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                    self.root.after(0,lambda:self.log('Emulator process started, PID '+str(p.pid)))
                    for line in p.stdout:
                        self.root.after(0,lambda s=line.rstrip():self.log(s))
                    rc=p.wait(); self.root.after(0,lambda:self.log('Emulator exited with code '+str(rc)))
            except Exception as e: self.root.after(0,lambda:self.log('BOOT ERROR: '+repr(e)))
        threading.Thread(target=worker,daemon=True).start()
    def devices(self):
        if not self.adb: self.log('ADB not found. Use Browse for adb.exe.'); return
        c,o=self.run([self.adb,'devices','-l']); self.log('ADB devices exit code '+str(c)+':\n'+(o or '(empty)'))
    def install(self):
        if not self.adb: messagebox.showerror('ADB not found','Use Browse for adb.exe and select platform-tools\\adb.exe.'); return
        f=filedialog.askopenfilename(title='Choose APK',filetypes=[('Android APK','*.apk')])
        if not f:return
        c,o=self.run([self.adb,'install','-r',f],timeout=180); self.log('APK install exit code '+str(c)+':\n'+o)
        messagebox.showinfo('APK install','Check Activity log for details.')
    def open_log(self):
        try:
            if not LOGFILE.exists(): LOGFILE.write_text('MINSS log created.\n',encoding='utf-8')
            os.startfile(str(LOGFILE))
        except Exception as e: messagebox.showerror('Could not open log',str(e))

if __name__=='__main__':
    try:
        root=tk.Tk(); App(root); root.mainloop()
    except Exception as e:
        try: (Path(__file__).resolve().parent/'minss_startup_error.txt').write_text(repr(e),encoding='utf-8')
        except Exception: pass
        raise
