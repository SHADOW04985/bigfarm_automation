import pyautogui
from wonderwords import RandomWord
import tkinter as tk
from tkinter import ttk, messagebox
import gc

def stop():
    root.destroy()

    gc.collect()

    main()

    # root.mainloop()

def searchfunc(times):
    try:
        def clear():
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            gc.collect()
            root.after(0,mainfunc)

        def backspace():
            def bckspcloop():
                nonlocal count2
                if count2>0:
                    pyautogui.press("backspace")
                    # print(f'backspace {count2}')
                    count2 -= 1
                    gc.collect()
                    root.after(0,bckspcloop)
                else:
                    gc.collect()
                    root.after(0,mainfunc)
            # print('click for erasing')
            pyautogui.click()
            gc.collect()
            root.after(0,bckspcloop)

        def worditerate():
            nonlocal count2
            if count2 < lenwrd:
                pyautogui.write((xword[count2]))
                # print(xword[count2])
                count2 += 1
                gc.collect()
                root.after(0,worditerate)
            else:
                pyautogui.press('enter')
                # print('Pressed enter!')
                gc.collect()
                root.after(3000,backspace)

        def mainfunc():
            nonlocal count
            nonlocal lenwrd
            nonlocal xword
            nonlocal count2
            # print(count)
            if count<times.get():
                count += 1
                count2 = 0
                xword = list(RandomWord().word())
                lenwrd = len(xword)
                pyautogui.click()
                # print('click for writing')
                gc.collect()
                root.after(0,worditerate)

        lenwrd = 0
        xword = ""
        count = 0
        count2 = 0
        gc.collect()
        root.after(5000,clear)
    except Exception:
        messagebox.showinfo("Error","Unknown error has occured\nInsert only numbers")
    
def main():
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

    ttk.Label(root, text = "Number of searches: ").pack(pady=10)
    str(ttk.Entry(root, width=10,textvariable=srvar).pack(pady=5))

    start = ttk.Button(root,text="START",command=lambda: searchfunc(srvar))
    start.pack()

    reset_button = ttk.Button(root, text="STOP", command=lambda: stop())
    reset_button.pack()

    close = ttk.Button(root,text="CLOSE",command=root.destroy)
    close.pack()

    gc.collect()
    root.mainloop()

main()