from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from urllib import request
from tkinter import filedialog
from threading import Thread
from bs4 import BeautifulSoup
import requests, subprocess, socket, time


def isvalid(url):
	return requests.head(url).status_code < 400

def late_ver():
    global ver
    down_latest.config(state=DISABLED, relief='groove', cursor='arrow', bg='white')
    down.config(state=DISABLED, relief='groove', cursor='arrow', bg='white')
    down.bind('<Motion>', lambda _:down_latest.config(bg='white', relief='groove'))
    down.update_idletasks()
    down_latest.bind('<Motion>', lambda _:down_latest.config(bg='white', relief='groove'))
    down_latest.update_idletasks()
    status.config(state=NORMAL, text='Finding latest version of python \navailable on the server...', justify=CENTER)
    status.place_configure(x=25, y=325)
    status.update_idletasks()
    
    find_latestversion()

    if ver and messagebox.askyesno(f'Download python {ver}', f'The latest version of python is {ver}.\n Do you want to download it?'):
        status.config(state=NORMAL, text=f'Downloading python {ver}...')
        status.place_configure(x=41, y=350)
        status.update_idletasks()
        downfun(ver)

    down_latest.config(state=NORMAL, relief='ridge', cursor='hand2')
    down.config(state=NORMAL, relief='ridge', cursor='hand2')
    down.bind('<Motion>', lambda _:down.config(bg='#aefffb', relief='groove'))
    down_latest.bind('<Motion>', lambda _:down_latest.config(bg='#aefffb', relief='groove'))
    status.config(text='Download not yet initialized...', state=DISABLED)
    status.place_configure(x=41, y=350)
    status.update_idletasks()
    return


def find_latestversion():
    global ver

    IPaddress=socket.gethostbyname(socket.gethostname())
    if IPaddress=="127.0.0.1":
        messagebox.showerror('No internet connection', 'Check your internet connection and try again.')
        ver=None
        return

    try:
        url = 'https://www.python.org/downloads/'

        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = [chunk for chunk in chunks if chunk]


        ver=text[(text.index('Download the latest version of Python'))+1].split(' ')[2]
        return

    except:
        messagebox.showerror('Error', 'There was some error while finding\n latest version of python.')
        ver=None
        return

def show_progress(block_num, block_size, total_size):
    global start_time

    downloaded = block_num * block_size
    percent=int((downloaded/total_size)*100)
    duration = time.time() - start_time
    speed = round(downloaded / (1024 * 1024 * duration), 2)
    conv_time=time.strftime('%H:%M:%S', time.gmtime(duration))
    prog_bar.config(value=percent)
    percent_label.config(text=f'Percentage: {percent}%')
    if speed<1:
        speed_label.config(text=f'Speed: {speed*1024} KB/s')
    else:
        speed_label.config(text=f'Speed: {speed} MB/s')

    time_label.config(text=f'Elapsed time-{conv_time}')
    return

def downfun(vers=None):
    global version,status,ver,start_time

    IPaddress=socket.gethostbyname(socket.gethostname())
    if IPaddress=="127.0.0.1":
        messagebox.showerror('No internet connection', 'Check your internet connection and try again.')
        return

    else:
        down_latest.config(state=DISABLED, relief='groove', cursor='arrow')
        down.config(state=DISABLED, relief='groove', cursor='arrow')
        down.bind('<Motion>', lambda _:down_latest.config(bg='white', relief='groove'))
        down.update_idletasks()
        down_latest.bind('<Motion>', lambda _:down_latest.config(bg='white', relief='groove'))
        down_latest.update_idletasks()
        percent_label.config(state=NORMAL, text='Percentage: 0%')
        time_label.config(state=NORMAL, text='Elapsed time-00:00:00')
        speed_label.config(state=NORMAL, text='Speed: 0 MB/s')

        ver=version.get() if version.get() else vers
        down_url=f'https://www.python.org/ftp/python/{ver}/python-{ver}-amd64.exe'

        if isvalid(down_url) and ver:

            filedir=filedialog.askdirectory(title='Choose directory to download', initialdir=r'\Downloads')
            direc=(filedir+f'/python-{ver}-amd64.exe').replace('/', '\\')
            if filedir:
                status.config(state=NORMAL, text=f'Downloading python {ver}...')
                status.place_configure(x=41, y=350)
                status.update_idletasks()

                start_time = time.time()
                print(start_time)
                request.urlretrieve(down_url, direc, show_progress)

                subprocess.Popen(rf'explorer /select,"{direc}"')

                status.config(text='Download not yet initialized...', state=DISABLED)
                status.place_configure(x=41, y=350)
                status.update_idletasks()
                prog_bar.config(value=0)
                prog_bar.update_idletasks()

        elif not ver:
            messagebox.showerror('No version entered', 'Enter a version to download.')
        
        else:
            messagebox.showerror('Python version not found', 'Requested python version not found on server.')

        down_latest.config(state=NORMAL, relief='ridge', cursor='hand2')
        down.config(state=NORMAL, relief='ridge', cursor='hand2')
        down.bind('<Motion>', lambda _:down.config(bg='#aefffb', relief='groove'))
        down.update_idletasks()
        down_latest.bind('<Motion>', lambda _:down_latest.config(bg='#aefffb', relief='groove'))
        down_latest.update_idletasks()
        percent_label.config(state=DISABLED, text='Percentage: --%')
        time_label.config(state=DISABLED, text='Elapsed time-00:00:00')
        speed_label.config(state=DISABLED, text='Speed: -- MB/s')
        return

root=Tk()
root.title('Python download client')
root.geometry('400x450+450+150')
root.resizable(0, 0)
#root.iconbitmap('icon.ico')

Label(text='The python download client', font='Arial 20 bold').pack(side=TOP)

Label(text='Enter the version to be downloaded here:', font='Arial 16').place(x=5, y=80)

version=ttk.Entry(width=20, font='Arial 18')
version.place(x=65, y=130)
version.focus()

def dwn_th():
    dwn_th=Thread(target=downfun, daemon=True)
    dwn_th.start()

def lt_th():
    lt_th=Thread(target=late_ver, daemon=True)
    lt_th.start()

down=Button(cursor='hand2', font='Arial 20', relief='ridge', text='Download this version', bg='white', command=dwn_th)
down.place(x=53, y=185)
down.bind('<Motion>', lambda _:down.config(bg='#aefffb', relief='groove'))
down.bind('<Leave>', lambda _:down.config(bg='white', relief='groove'))

down_latest=Button(cursor='hand2', font='Arial 20', relief='ridge', text='Download latest version', bg='white', command=lt_th)
down_latest.place(x=42, y=260)
down_latest.bind('<Motion>', lambda _:down_latest.config(bg='#aefffb', relief='groove'))
down_latest.bind('<Leave>', lambda _:down_latest.config(bg='white', relief='groove'))

status=Label(text='Download not yet initialized...', font='Arial 18', state=DISABLED, justify=CENTER)
status.place(x=41, y=350)

prog_bar=ttk.Progressbar(root, mode='determinate', orient=HORIZONTAL, length=350)
prog_bar.place(x=25, y=400)

speed_label=Label(text='Speed: -- MB/s', state=DISABLED)
speed_label.place(x=25, y=425)

percent_label=Label(text='Percentage: --%', state=DISABLED)
percent_label.place(x=140, y=425)

time_label=Label(text='Elapsed time-00:00:00', state=DISABLED)
time_label.place(x=255, y=425)

root.mainloop()
