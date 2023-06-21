import pyautogui
from wonderwords import RandomWord
import tkinter as tk
from tkinter import ttk, messagebox
import gc

def searchfunc(times):
    try:
        def clear():
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            root.after(0,mainfunc)

        def backspace():
            def bckspcloop():
                nonlocal count2
                if count2>0:
                    pyautogui.press("backspace")
                    # print(f'backspace {count2}')
                    count2 -= 1
                    root.after(0,bckspcloop)
                else:
                    root.after(0,mainfunc)
            # print('click for erasing')
            pyautogui.click()
            root.after(0,bckspcloop)

        def worditerate():
            nonlocal count2
            if count2 < lenwrd:
                pyautogui.write((xword[count2]))
                # print(xword[count2])
                count2 += 1  
                root.after(0,worditerate)
            else:
                pyautogui.press('enter')
                # print('Pressed enter!')
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
                root.after(0,worditerate)

        lenwrd = 0
        xword = ""
        count = 0
        count2 = 0
        gc.collect()
        root.after(5000,clear)
    except Exception:
        messagebox.showinfo("Error","Unknown error has occured\nInsert only numbers")


def msn_shopping_game():

    # def link():
    #     pyautogui.write("https://www.msn.com/en-us/shopping?game-first-position=1")
    #     pyautogui.press('enter')
    #     root.after(5000,scrolldwn)
    
    def scrolldwn():
        scroll = ('javascript:document.querySelector("shopping-page-base")'
            '?.shadowRoot.querySelector("shopping-homepage")'
            '?.shadowRoot.querySelector("msft-feed-layout")'
            '?.shadowRoot.querySelector("msn-shopping-game-pane").scrollIntoView();')

        pyautogui.click()
        pyautogui.write(scroll)
        pyautogui.press('enter')
        root.after(3000,corrans)

    def corrans():
        corr = ('javascript:var msnShoppingGamePane = document.querySelector("shopping-page-base")'
                '?.shadowRoot.querySelector("shopping-homepage")'
                '?.shadowRoot.querySelector("msft-feed-layout")'
                '?.shadowRoot.querySelector("msn-shopping-game-pane");'
                'if(msnShoppingGamePane != null){'
                'msnShoppingGamePane.cardsPerGame = 1;'
                'msnShoppingGamePane.resetGame();}')
        
        pyautogui.click()
        pyautogui.write(corr)
        pyautogui.press('enter')
        # root.after(3000,click)

    # def click():
    #     nonlocal shopcount
    #     clickeez = ("javascript:var parentElement = document.querySelector('#root > div > div > fluent-design-system-provider"
    #             "> div > div:nth-child(4) > div > shopping-page-base').shadowRoot.querySelector('div > div.shopping-page-content"
    #             "> shopping-homepage').shadowRoot.querySelector('div > msft-feed-layout')"
    #             ".shadowRoot.querySelector('msn-shopping-game-pane').shadowRoot;"
    #             "var element = parentElement.querySelector('div > div > button.shopping-select-overlay-button');"
    #             "if (element) {"
    #             "element.click();}")
        
    #     if loopcount<shopcount.get():
    #         pyautogui.click()
    #         pyautogui.write(clickeez)
    #         pyautogui.press('enter')
    #         root.after(3000,playagain)
    
    # def playagain():
    #     nonlocal loopcount
    #     again = ('javascript:document.querySelector'
    #             '("#root > div > div > fluent-design-system-provider > div > div:nth-child(4)'
    #             ' > div > shopping-page-base").shadowRoot.querySelector("div > div.shopping-page-content '
    #             '> shopping-homepage").shadowRoot.querySelector("div > msft-feed-layout").shadowRoot'
    #             '.querySelector("msn-shopping-game-pane").shadowRoot.querySelector'
    #             '("div.shopping-game-pane-container > div > div.game-panel-header-2 > button.game-panel-button").click();')
        
    #     if loopcount<shopcount.get():   
    #         gc.collect()
    #         loopcount += 1
    #         pyautogui.click()
    #         pyautogui.write(again)
    #         pyautogui.press('enter')
    #         root.after(3000,click)

    # loopcount=0
    root.after(5000,scrolldwn)
    
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

shop = ttk.Button(root,text="SHOP",command=lambda: msn_shopping_game())
shop.pack()

close = ttk.Button(root,text="CLOSE",command=root.destroy)
close.pack()

root.mainloop()