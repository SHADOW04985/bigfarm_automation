import pyautogui
from wonderwords import RandomWord
import tkinter as tk
from tkinter import ttk, messagebox
import gc
import sys
import os
import csv
import requests
import pytesseract

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def stop():
    root.destroy()
    if pricewin.winfo_exists():
        pricewin.destroy()
        pricegui()
    gc.collect()
    guiwin()

def searchfunc(times):
    try:   

        def clear():
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            gc.collect()
            root.after(0,wordgen)

        def backspace():
            def bckspcloop():
                nonlocal count2
                if count2>0:
                    pyautogui.press("backspace")
                    count2 -= 1
                    gc.collect()
                    root.after(0,bckspcloop)
                else:
                    gc.collect()
                    root.after(0,wordgen)
            pyautogui.click()
            gc.collect()
            root.after(0,bckspcloop)

        def worditerate():
            nonlocal count2
            if count2 < lenwrd:
                pyautogui.write((xword[count2]))
                count2 += 1
                gc.collect()
                root.after(0,worditerate)
            else:
                pyautogui.press('enter')
                gc.collect()
                root.after(3000,backspace)

        def wordgen():
            nonlocal count
            nonlocal lenwrd
            nonlocal xword
            nonlocal count2
            if count<times.get():
                count += 1
                count2 = 0
                xword = list(RandomWord().word())
                lenwrd = len(xword)
                pyautogui.click()
                gc.collect()
                root.after(0,worditerate)

        lenwrd = 0
        xword = ""
        count = 0
        count2 = 0
        gc.collect()
        try:
            if count<times.get():
                root.after(5000,clear)
        except tk.TclError as e:
            messagebox.showerror("Data type error",f"Only integer input allowed.\n{e}")
    except Exception as e:
        messagebox.showerror("Error",e)

def sheetdownload():
    if not os.path.exists(resource_path("price.csv")):
        sheet_url = "https://docs.google.com/spreadsheets/d/1LbWDKR4hLwIE7qcIozdueSqP1GeA6hgLD2vw2vnHNpo"
        sheet_name = "PRIMARY SHEET (ADMIN)"
        output_file = "price.csv"
        export_url = f"{sheet_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        try:
            response = requests.get(export_url)
            if response.status_code == 200:
                csvpath = resource_path(output_file)
                with open(csvpath, 'w', newline='',encoding = 'utf-8') as csvfile:
                    csv_text = response.text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                    csvfile.write(csv_text)
            else:
                messagebox.showerror("CSV Download Error",f"Unable to pull csv")
        except Exception as e:
                messagebox.showerror("CSV Download Error",e)
                pricewin.destroy()
    else:
        pass

def colname():
    try:
        with open(resource_path("price.csv"), 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = next(csv_reader)
            hdr = headers[1]
        return hdr
    except Exception as e:
        messagebox.showerror("CSV Error",e)        

def namescan():
    try:
        pytesseract.pytesseract.tesseract_cmd = resource_path('Tesseract-OCR\\tesseract.exe')
        x, y = pyautogui.position()
        screenshot = pyautogui.screenshot(region=(x+3, y-5, 208, 30))
        text = pytesseract.image_to_string(screenshot)
        text = text[:-4]
        return text
    except Exception as e:
        messagebox.showerror("Scanner Error",e)

def vacantspace():
    row = 0
    while True:
        widgets = pricedata.grid_slaves(row, 0)
        if widgets:
            row += 1
        else:
            return row

def pricemap(flagparams):
    def itemiteration():
        nonlocal outcount
        freerow = vacantspace()
        rownum = freerow
        if outcount<len(matching_rows):
            pricedat = ttk.Label(pricedata, text = (f"{matching_rows[outcount][hdrname]}"),wraplength=490,anchor='center',justify='center')
            pricedat.grid(column=0,row=(rownum),pady=(5,0))
            itemprice = ttk.Label(pricedata, text = (f": {matching_rows[outcount][price]}"))
            itemprice.grid(column=1,row=(rownum))
            outcount+=1
            pricewin.after(0,itemiteration)
    try:
        gc.collect()
        outcount = 0
        hdrname = colname()
        if (flagparams==0):
            search_value = namescan()
        elif(flagparams==1):
            search_value = str(itemvar.get())
        search_value = search_value.strip()
        entry.delete(0,tk.END)
        entry.insert(0,search_value)
        price = 'Price\n(USD)'
        with open(resource_path("price.csv"), 'r', newline='', errors='replace') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            matching_rows = [row for row in csv_reader if search_value.lower() in row[hdrname].lower()]
        if len(matching_rows)==0:
            messagebox.showerror("No Result",f"No matching value found for '{search_value}'")
        elif len(matching_rows)>20:
            messagebox.showerror("Too Many Items",f"Too many results generated for '{search_value}'\nPlease adjust your pointer or provide better text input and try again.")
        else:
            pricewin.after(0,itemiteration)
    except Exception as e:
        messagebox.showerror("Price Map Error",e)
        
def destroy(win):
    for widgets in win.winfo_children():
        widgets.destroy()
    gc.collect()

def winprotocols():
    root.deiconify()
    pricewin.destroy()
    os.remove(resource_path("price.csv"))
    
def pricegui():
    root.iconify()
    sheetdownload()
    global pricewin
    global pricedata
    global itemvar
    global entry
    if pricewin is None or not pricewin.winfo_exists():
        pricewin = tk.Toplevel(root,bg="#FCEDDA")
        window_width = 580
        window_height = 330
        screen_width = pricewin.winfo_screenwidth()
        screen_height = pricewin.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        pricewin.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        pricewin.resizable(False, False)
        pricewin.title("Price Mapper")
        pricewin.attributes('-topmost', True)
        itemvar = tk.StringVar()
        canvas = tk.Canvas(pricewin)
        canvas.pack(pady=(80,0),side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(pricewin, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        pricedata = tk.Frame(canvas)
        canvas.create_window((0, 0), window=pricedata, anchor="nw")

        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        pricedata.bind("<Configure>", update_scroll_region)
        pricewin.protocol("WM_DELETE_WINDOW", winprotocols)
        scan = ttk.Button(pricewin,text="SCAN",command = lambda: pricewin.after(1800,pricemap,0))
        scan.place(x = 143, y = 5)
        custom = ttk.Button(pricewin,text="SEARCH",command = lambda: pricemap(1))
        custom.place(x = 235, y = 5)
        clr = ttk.Button(pricewin,text="CLEAR",command = lambda: destroy(pricedata))
        clr.place(x = 331, y = 5)

        def on_entry_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg='black')

        def on_entry_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder_text)
                entry.config(fg='#999999')

        entry = tk.Entry(pricewin, width=49,textvariable=itemvar,fg='#999999')
        placeholder_text = "Provide your custom search here and hit the search button"
        entry.insert(0, placeholder_text)
        entry.bind('<FocusIn>', on_entry_focus_in)
        entry.bind('<FocusOut>', on_entry_focus_out)
        entry.bind("<Return>", lambda event: custom.invoke())
        entry.place(x = 89, y = 50)
        pricewin.mainloop()
    else:
        pricewin.lift()
    
def guiwin():
    global root
    root=tk.Tk()
    window_width = 280
    window_height = 230
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)
    root.title("Bing farm")
    root.attributes('-topmost', True)
    srvar=tk.IntVar()
    ttk.Label(root, text = "Number of searches: ").pack(pady=5)
    ttk.Entry(root, width=10,textvariable=srvar).pack(pady=(5,25))
    start = ttk.Button(root,text="START",command=lambda: searchfunc(srvar))
    start.pack()
    msn = ttk.Button(root,text="PRICE",command=lambda: pricegui())
    msn.pack()
    reset_button = ttk.Button(root, text="STOP", command=lambda: stop())
    reset_button.pack()
    close = ttk.Button(root,text="CLOSE",command=root.destroy)
    close.pack()
    gc.collect()
    root.mainloop()

if __name__ == "__main__":
    pricewin = None
    guiwin()