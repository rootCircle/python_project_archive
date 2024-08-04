# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 18:17:14 2021
Requirements:
    libraries,
    local image files,
    service-account-file
pyrebase:login
firebase_admin:db,registration
firebase storage:All Images are saved and retrieved as .png file
@author: Praveen Jaiswal
Scrolling through mousewheel is supported for Windows,Linux only
Email must always be in lower case
"""

"""
TODO : Add support for '#.$[]\' in firebase
TODO : Local Session Expiry Support by threading
TODO : Login Waiting Sync -Bugs
TODO : Page4_SellerRecentTransactions,Page4_BuyerRecentlyBrought
TODO : Transaction log every cash/wallet cash transaction made through Kans
TODO : Check for http connection instead of https to decrease false positives
TODO : Multi-threading to increase server response time and decrease waiting time(also by optimising queries)
TODO : GIF Transparency
TODO : Add new encoding tech to avoid key duplication in temp bank using timestamp
TODO : LoadingPage bug removal for time synchronisation
"""

LOG_FILE_FOLDER = "res"
LOG_FILE = ""
try:
    from datetime import datetime, timedelta
    import os
    import errno

    try:
        os.makedirs(LOG_FILE_FOLDER)
    except OSError as er:
        if er.errno != errno.EEXIST:
            print(er)

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    LOG_FILE = os.path.join(LOG_FILE_FOLDER, "log.log")  # Log File init

    print(formatted_date, "============PROGRAM STARTS============", file=open(LOG_FILE, 'a'))
except Exception as e:
    print("ERROR", e)
    import sys

    sys.exit()

try:
    import jiosaavnapi
    import tkinter as tk
    from tkinter import messagebox, Radiobutton, PhotoImage, StringVar, filedialog, ttk, simpledialog
    import tkinter.font as tkFont
    from PIL import Image, ImageTk
    import requests
    from io import BytesIO
    import random
    import time
    import pyrebase
    import urllib.request
    import json
    import pickle
    import requests.exceptions
    from multiprocessing.pool import ThreadPool
    import re
    import threading
except Exception as ex:
    try:
        os.makedirs(LOG_FILE_FOLDER)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print(e)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_date, "Import Error\t", ex, file=open(LOG_FILE, 'a'))
    import sys

    sys.exit()

"""
Some Custom Variable(Not to be modified)
"""
ITEMTYPE = -1
CHOOSEDITEMDETAILS = []

"""
Image Files Directories
"""
LOGOImgDir = os.path.join("data", "logonew.png")
DEFAULTIMAGEDir = os.path.join("data", "Additem.png")
HOMEPAGEImgDir = os.path.join("data", "logo.png")
SIGNUPPAGEImgDir = [os.path.join("data", "Part1.png"), os.path.join("data", "Part2.png")]
DASHBOARDImgDir = os.path.join("data", "Lighthouse.jpg")

CACHE_FOLDER = "cache"
DEFAULT_DOWNLOAD_LOCATION="Download"
LOADING_SCREENS = []
LOADING_GIF = os.path.join("data", "Loading.gif")
RESULTOUT=[]
CHOOSENSONG=[]

LeastWaitTime = 0.5  # in second(min time for loading)


# Application assume gif size to be 300*300

class LoadingPage(tk.Label):
    """
    Doesn't support non-void function as its return is not synchronised
    """

    def __init__(self, master, filename):
        try:
            im = Image.open(filename)
            seq = []
            try:
                while 1:
                    seq.append(im.copy())
                    im.seek(len(seq))  # skip to next frame
            except EOFError:
                pass  # we're done

            try:
                self.delay = im.info['duration']
            except KeyError:
                self.delay = 100

            first = seq[0].convert('RGBA')
            self.frames = [ImageTk.PhotoImage(first)]

            tk.Label.__init__(self, master, image=self.frames[0])

            temp = seq[0]
            for image in seq[1:]:
                temp.paste(image)
                frame = temp.convert('RGBA')
                self.frames.append(ImageTk.PhotoImage(frame))

            self.idx = 0

            self.cancel = self.after(self.delay, self.play)
        except FileNotFoundError as e:
            Apptools.writeLog("File not found\nQuit Module Use" + str(e))
            os._exit(0)

    def play(self):
        try:
            self.config(image=self.frames[self.idx])
            self.idx += 1
            if self.idx == len(self.frames):
                self.idx = 0
            self.cancel = self.after(self.delay, self.play)
        except Exception as e:
            Apptools.writeLog(e)

    def start(self, grab=True):
        """
        grab will set toplevel active and root window inactive
        """
        try:
            if not LOADING_SCREENS:
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                gifhalfdimension = [50, 50]
                LOADING_SCREENS.append(tk.Toplevel(self))
                screen = LOADING_SCREENS[-1]
                try:
                    screen.wm_overrideredirect(True)
                except:
                    screen.overrideredirect(True)

                # Eval is threading Unsafe
                # self.eval(f'tk::PlaceWindow {str(screen)} center')

                # x = self.winfo_x()
                # y = self.winfo_y()

                screen.geometry(
                    "+%d+%d" % (screen_width // 2 - gifhalfdimension[0], screen_height - 3 * gifhalfdimension[1]))
                screen.lift()
                screen.resizable(0, 0)
                if grab:
                    screen.grab_set()
                LoadingPage.anim = LoadingPage(screen, LOADING_GIF)
                LoadingPage.anim.pack()
            else:
                time.sleep(0.1)
                LoadingPage.start(self, grab)
        except RecursionError as e:
            Apptools.writeLog(e)

    def stop_it(self):
        try:
            if LOADING_SCREENS:
                try:
                    screen = LOADING_SCREENS[-1]
                    LoadingPage.anim.after_cancel(LoadingPage.anim.cancel)
                    screen.destroy()
                    del LOADING_SCREENS[-1]
                except IndexError as er:
                    Apptools.writeLog(er)
                    globals()['LOADING_SCREENS'] = []
            else:
                time.sleep(0.1)  # To avoid collission with other function calls
                LoadingPage.stop_it(self)
        except RecursionError as e:
            Apptools.writeLog(e)

    def perform(self, args):
        """
        args should include destination function
        order of args(root ,function,arguments)
        """
        t1 = threading.Thread(target=LoadingPage.start, args=(self,))
        t1.start()
        t2 = threading.Thread(target=LoadingPage.fxn, args=args)
        t2.start()

    def fxn(self, *args):
        t1 = time.time()
        function = args[0]
        arguments = args[1:]
        function(*arguments)
        t2 = time.time()

        diff = round(t2 - t1, 1)
        if diff < LeastWaitTime:
            time.sleep(LeastWaitTime - diff)
        LoadingPage.stop_it(self)


class Apptools:
    def download(url):
        path, url = url
        r = requests.get(url, stream = True)
        with open(path, 'wb') as f:
            for ch in r:
                f.write(ch)
            
    def image_Show(self,imgdir="", xrow=0, ycolumn=0, width=200, height=200, mode="grid", rspan=1, cspan=1, px=0, py=0, url=""):
        try:
            if url:
                response = requests.get(url)
                Photo = Image.open(BytesIO(response.content))
            elif imgdir:
                Photo = Image.open(imgdir)
            else:
                raise
        except Exception as e:
            Apptools.writeLog(e)
            Photo = Image.open(DEFAULTIMAGEDir)
        Photo = Photo.resize((width, height))
        render = ImageTk.PhotoImage(Photo)
        img = tk.Label(self, image=render)
        img.image = render
        if mode == 'grid':
            img.grid(row=xrow, column=ycolumn, rowspan=rspan, columnspan=cspan, padx=px, pady=py, sticky="ns")
        else:
            img.place(x=xrow, y=ycolumn, relx=0, rely=0)

    @staticmethod
    def openfilename():
        filetype = [('Image files', '*.jpg;*.jpeg;*.png;*.bmp'), ('All files', '*')]
        filename = filedialog.askopenfilename(title='Open', initialdir=os.getcwd(), filetypes=filetype)
        if filename:
            return filename

    @staticmethod
    def open_img():
        filename = Apptools.openfilename()
        if filename:
            try:
                img = Image.open(filename)
                img = img.resize((300, 300), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(img)
                img2 = img.resize((100, 100), Image.ANTIALIAS)
                renderCompressed = ImageTk.PhotoImage(img2)
                return render, renderCompressed, filename
            except Exception as e:
                Apptools.writeLog(e)

    def imgbutton(self, diry, width, height, irow, icolumn):
        try:
            Photo = Image.open(diry)
            Photo = Photo.resize((width, height))
            render = ImageTk.PhotoImage(Photo)

            imgbtn = tk.Button(self, image=render)
            imgbtn.config(command=lambda: Apptools.imgbutton_event(self, imgbtn))
            imgbtn.image = render
            imgbtn.grid(row=irow, column=icolumn, padx=10, pady=10)
        except Exception as e:
            Apptools.writeLog(e)
            self.imgbutton(DEFAULTIMAGEDir, width, height, irow, icolumn)

    def imgbutton_event(self, imgbtn):
        x = Apptools.open_img()
        if x:
            img, compImg, self.imageAddress = x
            imgbtn.config(image=compImg)
            imgbtn.image = compImg

    def is_not_null(*text):
        if len(text) != 0:
            for msg in text:
                if msg == "" or (isinstance(msg, str) and msg.strip() == ""):
                    return False
            return True
        else:
            return False

    def check_digit(*text):
        try:
            for i in text:
                x = float(i)
            return True
        except Exception as e:
            return False

    def in_limit(lower, upper, *text):
        if len(text) != 0:
            for msg in text:
                if Apptools.check_digit(msg):
                    val = float(msg)
                    if val > upper or val < lower:
                        return False
                else:
                    return False
            return True
        else:
            return False

    def generate_id(child, sp="id"):
        ref = FirebaseDB.getdataOrder(child, sp)
        if ref:
            out = list(ref.values())
            k = 1
            list_id = []
            for i in range(len(out)):
                list_id.append(out[i][sp])
            while k in list_id:
                k += 1
            return k
        elif ref is not None:
            return 1

    def randomtxt(length):
        txt = ""
        for i in range(length):
            n = random.randint(1, 62)
            if n <= 26:
                txt += chr(64 + n)
            elif n <= 52:
                txt += chr(70 + n)
            else:
                txt += chr(n - 5)
        return txt

    def generateuniquecode(child, idty):
        """"
        User need to precheck for internet connection.
        """
        out = FirebaseDB.getdataOrder(child, idty)
        if out is not None:
            list_wal = []
            for i in out:
                list_wal.append(out[i][idty])

            txt = Apptools.randomtxt(8)

            while txt in list_wal:
                txt = Apptools.randomtxt(8)

            return txt

    @staticmethod
    def clearImgCache():
        try:
            os.makedirs(CACHE_FOLDER)
        except OSError as e:
            if e.errno != errno.EEXIST:
                Apptools.writeLog(e)

        onlyfiles = [os.path.join(CACHE_FOLDER, f) for f in os.listdir(CACHE_FOLDER) if
                     os.path.isfile(os.path.join(CACHE_FOLDER, f))]
        for l in onlyfiles:
            if os.path.exists(l):
                os.remove(l)

    def writeLog(msg):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            os.makedirs(LOG_FILE_FOLDER)
        except OSError as e:
            if e.errno != errno.EEXIST:
                Apptools.writeLog(e)
        f = open(LOG_FILE, 'a')
        print(formatted_date, msg, file=f)
        f.flush()
        f.close()


class Apptoolsv2:

    
    def Treeoutput(self, column, out, label=None, srow=0, scolumn=0, scolumnspan=1, singleLineFilter=True,
                   InScrollableframe=True, lbrow=1, lbcolumn=0, fheight=250, fwidth=750):
        """
        out must be in form of list
        srow,scolumn,scolumnspan if InScrollableframe is true for scrollable frame
        lbrow,lbcolumn if InScrollableframe is False
        give one extra space for lbrow if label has some Value
        """
        if InScrollableframe:
            frame = ScrollableFrame(self, ch=fheight, cw=fwidth, showscrlbar=False)
            sframe = frame.scrollable_frame
        else:
            sframe = self
        if label:
            lbl = tk.Label(sframe, text=label)
            lbl.config(font=('Segoe UI', 20), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=lbrow - 1, column=lbcolumn, padx=30, pady=10)

        Apptoolsv2.listBox = ttk.Treeview(sframe)

        verscrlbar = ttk.Scrollbar(sframe, orient="vertical", command=Apptoolsv2.listBox.yview)
        verscrlbar.grid(row=lbrow, column=lbcolumn + 1, sticky="nsw", rowspan=2)

        hscrollbar = ttk.Scrollbar(sframe, orient="horizontal", command=Apptoolsv2.listBox.xview)
        hscrollbar.grid(row=lbrow + 1, column=lbcolumn, sticky="new")
        Apptoolsv2.listBox.configure(yscrollcommand=verscrlbar.set)
        Apptoolsv2.listBox.configure(xscrollcommand=hscrollbar.set)

        Apptoolsv2.listBox.config(selectmode="extended", columns=column, show="headings")

        for i in range(0, len(column)):
            Apptoolsv2.listBox.heading(column[i], text=column[i],
                                       command=lambda c=column[i]: Apptoolsv2.sortby(self, Apptoolsv2.listBox, c, 0))
            Apptoolsv2.listBox.column(column[i], minwidth=0)

        for col in column:
            Apptoolsv2.listBox.heading(col, text=col)
            Apptoolsv2.listBox.column(col, width=tkFont.Font().measure(col.title()))
        Apptoolsv2.listBox.grid(row=lbrow, column=lbcolumn, sticky="nsew")

        for i in out:
            if singleLineFilter:
                i = Apptoolsv2.singleline(self, i)
            Apptoolsv2.listBox.insert("", "end", values=i[:len(column)])

            for indx, val in enumerate(i[:len(column)]):
                ilen = tkFont.Font().measure(val)
                if Apptoolsv2.listBox.column(column[indx], width=None) < ilen:
                    Apptoolsv2.listBox.column(column[indx], width=ilen)
        if InScrollableframe:
            frame.grid(row=srow, column=scolumn, columnspan=scolumnspan)

        Apptoolsv2.listBox.bind('<Enter>', Apptoolsv2._bound_to_mousewheel)
        Apptoolsv2.listBox.bind('<Leave>', Apptoolsv2._unbound_to_mousewheel)

    def _bound_to_mousewheel(event):
        Apptoolsv2.listBox.bind_all("<MouseWheel>", Apptoolsv2._on_mousewheel)

    def _unbound_to_mousewheel(event):
        Apptoolsv2.listBox.unbind_all("<MouseWheel>")

    def _on_mousewheel(event):
        Apptoolsv2.listBox.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def singleline(self, txtlines):
        l = []
        if isinstance(txtlines, (list, tuple)):
            for i in txtlines:
                if isinstance(i, str):
                    l.append(i.replace("\n", " "))
                else:
                    l.append(i)
            return l
        else:
            return txtlines

    def sortby(self, tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        x = True

        for a, b in data:
            x = x and Apptools.check_digit(a)
        if x:
            for i in range(len(data)):
                data[i] = list(data[i])
                data[i][0] = float(data[i][0])
        data.sort(reverse=descending)

        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        tree.heading(col, command=lambda col=col: Apptoolsv2.sortby(self, tree, col, int(not descending)))


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Homepage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, cw=775, ch=500, showscrlbar=True, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg="#333333", highlightthickness=0)
        self.canvas.config(scrollregion=(0, 0, 900, 1000))
        if showscrlbar:
            vscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            hscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        s = ttk.Style()
        s.configure('TFrame', background='#333333')

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self._canvasWidth = cw
        self._canvasHeight = ch
        self.canvas.config(width=self._canvasWidth, height=self._canvasHeight,
                           scrollregion=(0, 0, self._canvasWidth, self._canvasHeight))
        if showscrlbar:
            self.canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

        self.canvas.grid(row=0, column=0)
        if showscrlbar:
            vscrollbar.grid(row=0, column=1, rowspan=2, sticky='nse')
            hscrollbar.grid(row=1, column=0, sticky='wse')

            self.canvas.bind('<Enter>', self._bound_to_mousewheel)
            self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        return None

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception as e:
            Apptools.writeLog(e)


class Homepage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):

        Apptools.image_Show(self, HOMEPAGEImgDir, 0, 0, 300, 450, rspan=10)

        lbl = tk.Label(self, text="Welcome to Kans")
        lbl.config(font=("Segoe UI", 20), fg="#E8E8E8", bg="#333333")
        lbl.grid(row=1, column=1, columnspan=3)

        lbl = tk.Label(self, text="Search Song")
        lbl.config(font=("Segoe UI", 18), fg="#E8E8E8", bg="#333333")
        lbl.grid(row=2, column=1, columnspan=3, pady=20)

        lbl = tk.Label(self, text="Link/ Search Term")
        lbl.config(font=("Segoe UI", 12), fg="#E8E8E8", bg="#333333")
        lbl.grid(row=3, column=1, padx=5)

        query = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        query.grid(row=3, column=2)

        btn = tk.Button(self, text="Search", command=lambda: self.Processing(master, query.get()))
        btn.config(bg="#1F8EE7", padx=7, pady=3, fg="#E8E8E8", bd=0, activebackground="#3297E9")
        btn.grid(row=5, column=3, padx=5)

    def Processing(self, *args):
        LoadingPage.perform(self, (self, self.search, *args))

    def search(self, master, query):
        if Apptools.is_not_null(query):
            result = jiosaavnapi.fancy_result(query)
            globals()['RESULTOUT'] = result
            master.switch_frame(Search_Results)
        else:
            messagebox.showwarning("Empty fields!", "Fill all the fields correctly to proceed.")

class Search_Results(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):

        lbl = tk.Label(self, text="Search Results")
        lbl.config(font=("Segoe UI", 20), fg="#E8E8E8", bg="#333333")
        lbl.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.output(master,RESULTOUT)

    def output(self, master, out):
        sep = ttk.Separator(self, orient='horizontal')
        sep.grid(row=1, column=0, columnspan=3, sticky="ew")
        frame = ScrollableFrame(self, cw=500, ch=300)

        if out:
            r = 0
            for data in out:
                minimalkeys=['id', 'song', 'album', 'year', 'primary_artists',
                 'featured_artists', 'singers', 'starring', 'language',
                 '320kbps', 'duration', 'image', 'media_url']

                req_keys = ['song', 'album', 'year', 'primary_artists',
                            'language','duration']


                imgdir = data[-2]
                if not imgdir:
                    imgdir = DEFAULTIMAGEDir
                txt=""
                for keys in req_keys:
                    txt+=keys.title()+" : "+data[minimalkeys.index(keys)]+"\n"
                txt.strip()
                try:
                    response = requests.get(imgdir)
                    Photo = Image.open(BytesIO(response.content))
                    Photo = Photo.resize((200, 200))
                    render = ImageTk.PhotoImage(Photo)

                except Exception as e:
                    Apptools.writeLog(e)

                    Photo = Image.open(DEFAULTIMAGEDir)
                    Photo = Photo.resize((250, 150))
                    render = ImageTk.PhotoImage(Photo)

                imgbtnfs = tk.Button(frame.scrollable_frame, text=txt, image=render, compound=tk.LEFT)
                imgbtnfs.image = render
                imgbtnfs.config(bg="#1F8EE7", padx=3, fg="#E8E8E8", bd=0, justify=tk.LEFT)
                imgbtnfs.config(activebackground="#3297E9", font=("Segoe Print", 15))
                imgbtnfs.grid(row=r, column=0, padx=10, pady=10, sticky="w")

                imgbtnfs.config(command=lambda x=data: self.framechange(master, x))
                r += 1

        else:
            lbl = tk.Label(frame.scrollable_frame, text="No Result Found :-(")
            lbl.config(font=("Segoe Print", 30), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=0, column=2, columnspan=4, padx=100, pady=100)


        frame.grid(row=1, column=0, columnspan=3)

    def framechange(self, master, x):
        globals()['CHOOSENSONG'] = x
        master.switch_frame(SongPlayer)

class SongPlayer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        
        lbl = tk.Label(self, text="Song Player")
        lbl.config(font=("Segoe UI", 30), fg="#E8E8E8", bg="#333333")
        lbl.grid(row=0, column=0, columnspan=3, sticky="ew")

        sep = ttk.Separator(self, orient='horizontal')
        sep.grid(row=1, column=0, columnspan=3, sticky="ew",pady=5)

        minimalkeys=['id', 'song', 'album', 'year', 'primary_artists',
                 'featured_artists', 'singers', 'starring', 'language',
                 '320kbps', 'duration', 'image', 'media_url']

        if len(CHOOSENSONG) == len(minimalkeys):

            imgurl=CHOOSENSONG[-2]
            Dir=None
            Apptools.image_Show(self, Dir, 2, 0, 200, 200, cspan=3,url=imgurl)
            
            lbl = tk.Label(self, text=CHOOSENSONG[minimalkeys.index('song')])
            lbl.config(font=("Segoe UI", 15), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=3, column=0, columnspan=3, sticky="ew")
            
            lbl = tk.Label(self, text=CHOOSENSONG[minimalkeys.index('album')])
            lbl.config(font=("Segoe UI", 8), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=4, column=0, sticky="w")
            
            lbl = tk.Label(self, text="By "+CHOOSENSONG[minimalkeys.index('primary_artists')])
            lbl.config(font=("Segoe UI", 8), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=5, column=2, sticky="e")
            
            lbl = tk.Label(self, text="ID : "+CHOOSENSONG[minimalkeys.index('id')])
            lbl.config(font=("Segoe UI", 15), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=6, column=0, columnspan=3, sticky="ew")

            btn = tk.Button(self, text="Play")
            btn.config(bg="#1F8EE7", padx=7, pady=3, fg="#E8E8E8", bd=0, activebackground="#3297E9")
            btn.grid(row=7, column=0 , sticky="ew")

            btn = tk.Button(self, text="Download", command=lambda: self.download())
            btn.config(bg="#1F8EE7", padx=7, pady=3, fg="#E8E8E8", bd=0, activebackground="#3297E9")
            btn.grid(row=7, column=2, sticky="ew")
        else:
            lbl = tk.Label(self, text="No song choosen! :-(")
            lbl.config(font=("Segoe UI", 32), fg="#E8E8E8", bg="#333333")
            lbl.grid(row=2, column=0, columnspan=3, sticky="ew")

    def download(self):
        minimalkeys=['id', 'song', 'album', 'year', 'primary_artists',
                 'featured_artists', 'singers', 'starring', 'language',
                 '320kbps', 'duration', 'image', 'media_url']
        path = os.path.join(DEFAULT_DOWNLOAD_LOCATION,CHOOSENSONG[minimalkeys.index('song')])
        print(CHOOSENSONG[minimalkeys.index('media_url')])
        urls=[(CHOOSENSONG[minimalkeys.index('song')],CHOOSENSONG[minimalkeys.index('media_url')])]
        ThreadPool(2).imap_unordered(Apptools.download, urls)
    

# Main Program
if __name__ == "__main__":
    app = App()
    app.title("Kans:Your Shopping Partner")
    app.resizable(0, 0)
    app.update_idletasks()
    x_Left = int(app.winfo_screenwidth() / 4)
    app.geometry("+{}+{}".format(x_Left, 100))
    try:
        Icon = PhotoImage(file=LOGOImgDir)
        app.iconphoto(False, Icon)
    except Exception as e:
        Apptools.writeLog(e)
        Icon = PhotoImage(file=DEFAULTIMAGEDir)
        app.iconphoto(False, Icon)
    app.mainloop()
