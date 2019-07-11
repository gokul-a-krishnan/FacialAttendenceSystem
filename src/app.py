import tkinter as tk
from glib import reco as gk
import webbrowser


def start_scan(name, input_window):
    name = str(name)
    if name:
        if name.isalpha():
            input_window.destroy()
            gk.gscan(name, 10)


def scan():
    print('Scanning...')
    root = tk.Tk()
    root.title('Add Student')
    root.resizable(0, 0)
    root.geometry('300x200+100+100')
    tk.Label(root, text='Name:').place(x=35, y=50, width=50, height=50)
    en = tk.Entry(root)
    en.place(x=90, y=65, width=100, height=20)
    tk.Button(root, text='  Scan  ', command=lambda: start_scan(en.get(), root)).place(x=100, y=100, width=75,
                                                                                       height=25)


def record():
    gk.gdetect()


def report():
    print(webbrowser.open('http://localhost/', new=0, autoraise=True))


def update():
    gk.gtrain()


def main():
    mw = tk.Tk()
    mw.option_add("*Button.Background", "white")
    mw.option_add("*Button.Foreground", "black")
    mw.title('Facial Attendance System')
    mw.geometry("500x500")
    mw.resizable(0, 0)
    back = tk.Frame(master=mw, bg='grey')
    back.pack_propagate(0)
    back.pack(fill=tk.BOTH, expand=1)
    bn_scan = tk.Button(master=back, text='Add Student', command=scan)
    bn_train = tk.Button(master=back, text='Start', command=record)
    bn_rec = tk.Button(master=back, text='Report', command=report)
    close = tk.Button(master=back, text='Update', command=update)
    bn_scan.place(x=50, y=150, width=120, height=45)
    bn_train.place(x=200, y=150, width=120, height=45)
    bn_rec.place(x=350, y=150, width=120, height=45)
    close.place(x=200, y=350, width=120, height=45)
    mw.mainloop()


if __name__ == '__main__':
    main()
