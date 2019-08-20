import tkinter as tk
import webbrowser

from FaceRecognizer import FaceRecognitionAPI as Fr, api_path


def start_scan(name, input_window):
    name = str(name)
    if name:
        if name.isalpha():
            input_window.destroy()
            Fr.scan(name, 10)


def scan_click():
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
    Fr.detect()


def report():
    webbrowser.open(api_path.url, new=0, autoraise=True)


def record_time():
    Fr.out_time()


def update():
    Fr.train()


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
    bn_scan = tk.Button(master=back, text='Add Student', command=scan_click)
    bn_train = tk.Button(master=back, text='Class In', command=record)
    bn_rec = tk.Button(master=back, text='Report', command=report)
    bn_out = tk.Button(master=back, text='Class Out', command=record_time)
    bn_update = tk.Button(master=back, text='Update', command=update)
    bn_scan.place(x=50, y=150, width=120, height=45)
    bn_train.place(x=200, y=150, width=120, height=45)
    bn_rec.place(x=350, y=150, width=120, height=45)
    bn_out.place(x=200, y=250, width=120, height=45)
    bn_update.place(x=200, y=350, width=120, height=45)
    mw.mainloop()


if __name__ == '__main__':
    main()
