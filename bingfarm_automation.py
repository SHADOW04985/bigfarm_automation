import pyautogui
from wonderwords import RandomWord
from time import sleep
import tkinter as tk
from tkinter import ttk, messagebox
import gc
import keyboard

def searchfunc(times):
    sleep(5)
    count = 0
    pyautogui.click() 
    keyboard.press_and_release("ctrl+a","\b")
    try:
        while count<times.get():
            
            # pyautogui.click() 
            xword = list(RandomWord().word())
            for i in range(len(xword)):
                pyautogui.write(xword[i])

            # counter = len(str(xword)) 
            # keyboard.press_and_release("ctrl+\b")
            
            # pyautogui.write(str(xword))
            pyautogui.press('enter')

            count+=1
            sleep(2)
            pyautogui.click()
            for i in range(len(xword)):
                keyboard.press_and_release("\b")
                sleep(0.1)
            # while backc<len(xword):
            #     keyboard.press_and_release("\b")
            #     backc+=1
            # backc=0
        gc.collect()
    except Exception:
        messagebox.showinfo("Error","Unknown error has occured\nInsert only numbers")
    count = 0

root=tk.Tk()
window_width = 280
window_height = 180
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.title("Bing farm")

srvar=tk.IntVar()

ttk.Label(root, text = "Number of searches: ").pack(pady=10)
str(ttk.Entry(root, width=10,textvariable=srvar).pack())

start = ttk.Button(root,text="START",command=lambda: searchfunc(srvar))
start.pack(pady=10)

close = ttk.Button(root,text="CLOSE",command=root.destroy)
close.pack()

root.mainloop()