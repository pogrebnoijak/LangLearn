import secrets as rand
from random import randint
import string
from tkinter import *
import re
import PIL.ImageTk
import PIL.Image
import os, sys
import shutil
import time
from threading import Thread
import heapq


class MyThread(Thread):
    def run(self):
        global time_
        time_+=1
        time.sleep(time_)
        timer()
        if (time_pass == time_):
            stop()

def create_threads():
    for i in range(all_time):
        thread = MyThread()
        thread.start()

def stop():
    global is_stop
    text_input.configure(state='disabled')
    statistics()
    is_stop = True

def exit():
    if close_settings():
        return
    global stat_i
    stat_i = 999
    statistics()
    stat_i+=1
    root.destroy()

def show_new_word():
    if is_stop:
        restart()
        return
    text.configure(state='normal', background = "white")
    text.delete(1.0, END)
    text.insert(END, generate_word(), "center")
    text.configure(state='disabled')

def restart():
    global is_stop; global stat_i; global time_; global time_pass; global chance
    is_stop = False
    text_input.configure(state='normal', background = "white")
    text_input.delete(1.0, END)
    stat_i = 1; time_ = 0; time_pass = 0; chance+=1
    zerroing()
    show_new_word()
    kol_word(len(words))
    create_threads()

def zerroing():
    global incorrect; global attempt
    incorrect = [0 for x in range(len(words)+1)]
    attempt = [0 for x in range(len(words)+1)]

def fill(file):
    f = open(file, 'r')
    #f = open('data/words.txt', 'r')
    line = f.readline()
    while line:
        words.append(line)
        line = f.readline()
    f.close()
    words.sort()
    i = 1
    for word in words:
        res = re.split(r'\W+', word.lower())
        w1 = res[0]
        w2 = res[1]
        dict_words[i] = w2
        dict_words[-i] = w1
        i+=1
    training()
    for_start()

def for_start():
    text_time.insert(END, "time", "center")
    text_time.configure(state='disabled')

    text_input.configure(state='normal', background = "yellow")
    text_input.insert(END, "Start new game!", "center")
    text_input.configure(state='disabled')
    text_correct.configure(state='normal', background = "red")
    text_correct.insert(END, "Start new game!", "center")
    text_correct.configure(state='disabled')
    text.configure(state='normal', background = "green")
    text.insert(END, "Start new game!", "center")
    text.configure(state='disabled')
    global is_stop
    is_stop = True
    zerroing()

def kol_word(len):
    text_correct.configure(state='normal', background = "yellow")
    text_correct.delete(1.0, END)
    text_correct.insert(END, str(len) + " words", "center")
    text_correct.configure(state='disabled')

def timer():
    global time_pass
    min, sec = divmod(time_ - time_pass - 1, 60)
    time_pass+=1
    time_str = "%02d:%02d" % (min, sec)
    text_time.configure(state='normal')
    text_time.delete(1.0, END)
    text_time.insert(END, time_str, "center")
    text_time.configure(state='disabled')

def generate_word():
    global correct_word
    correct_word = rand.randbelow(len(words)) + 1
    #correct_word = randint(1, len(words))
    if ((mode == "both" and rand.randbelow(2) == 0) or mode == "rus"):
        correct_word *= -1
    return dict_words[-correct_word]

def keypress(key): #in linux
    #print(key.keycode) #change for other sistem
    if key.keycode == 36: #enter
        input()
    elif key.keycode == 9: #esc
        exit()
    elif key.keycode > 66 and key.keycode < 70: #f1 f2 f3
        statistics()
    elif key.keycode == 70: #f4
        settings()
    elif key.keycode == 51: #\
        new_game()

def input():
    global new_game_
    if not is_stop or new_game_:
        new_game_ = False
        if close_settings():
            return
        s = re.split(r'\s+', text_input.get(1.0, END))
        if s[0] == '':
            s[0] = s[1]
        text_input.delete(1.0, END)
        
        if correct_word != 0:
            attempt[abs(correct_word)]+=1
            if dict_words[correct_word] == s[0]:
                answer(True)
            else:
                incorrect[abs(correct_word)]+=1
                answer(False)
        show_new_word()

def new_game():
    if is_stop:
        close_settings()
        global new_game_
        new_game_ = True
        input()

def answer(is_correct):
    if is_correct:
        text_correct.configure(state='normal', background = "green")
        text_correct.delete(1.0, END)
        text_correct.insert(END, "Correct!", "center")
    else:
        text_correct.configure(state='normal', background = "red")
        text_correct.delete(1.0, END)
        text_correct.insert(END, dict_words[correct_word], "center")
    text_correct.configure(state='disabled')

def probability(answer, correct_answer):
    if answer != 0:
        text_correct.configure(state='normal', background = "blue")
        text_correct.delete(1.0, END)
        text_correct.insert(END, str(100 * correct_answer//answer) + "%", "center")
        text_correct.configure(state='disabled')

def statistics():
    close_settings()
    do_dir()
    global stat_i; global chance
    file_ = "statistics/statistics" + str(chance) + "_" + str(stat_i) + ".txt"
    stat_i+=1; answer = 0; wrong_answer = 0
    
    sort_answers = []
    for i in range(1, len(words)+1):
        str_ans = '{:>20} <-> {:<20} |  Всего: {} |  Неверно: {}\n'.format(str(dict_words[i]), str(dict_words[-i]), str(attempt[i]), str(incorrect[i]))
        heapq.heappush(sort_answers, (-incorrect[i], str_ans))
        answer+=attempt[i]; wrong_answer+=incorrect[i]
    f = open(file_, 'w')
    for i in range(1, len(words)+1):
        f.write(heapq.heappop(sort_answers)[1])
    f.close()
    probability(answer, answer - wrong_answer)

def do_dir():
    path = "statistics/"
    if not os.access(path, os.F_OK):
        os.mkdir(path)

def training():
    path = "statistics/"
    if os.access(path, os.F_OK):
        shutil.rmtree(path)

######################################################### Settings

def change_mode():
    global mode
    if check_1.get() == 0:
        mode = "eng"
    elif check_1.get() == 1:
        mode = "rus"        
    else:
        mode = "both"
        
def close_settings():
    global open_sett
    if open_sett:
        change_mode()
        open_sett = False
        global all_time
        s = re.split(r'\D+', text_change_time.get(1.0, END))
        if s[0] != "":
            all_time = int(s[0])
        text_settings.place_forget()
        eng.place_forget()
        rus.place_forget()
        both.place_forget()
        text_change_time.place_forget()
        return True
    return False

def settings():
    if close_settings(): 
        return
    global open_sett
    text_change_time.delete(1.0, END)
    text_change_time.insert(1.0, all_time)
    text_settings.pack();eng.pack(); rus.pack(); both.pack(); text_change_time.pack()
    text_settings.place(x = 50, y = 10, width = 600, height = 270)
    eng.place(x = 60, y = 60, width = 100)
    rus.place(x = 60, y = 85, width = 100)
    both.place(x = 60, y = 110, width = 100)
    text_change_time.place(x = 8, y = 90, width = 60, height = 20)
    open_sett = True
    
def show_txt():
    os.system('gedit ' + file)  
    
def show_stat():
    global stat_i; global chance
    if stat_i != 1:
        file_ = "statistics/statistics" + str(chance) + "_" + str(stat_i-1) + ".txt"
        os.system('gedit ' + file_)


######################################################### Main

dict_words = {}; words = []; incorrect = []; attempt = []
correct_word = 0; stat_i = 1; mode = "eng"; open_sett = False; all_time = 10; time_ = 0; time_pass = 0; is_stop = False; chance = 0; new_game_ = False
file = "data/lesson.txt"
#file = "data/words.txt"

root = Tk()
root.title("Learning")

panelFrame = Frame(root, width = 700, height = 40, bg = 'gray')
panelFrame.pack(side = 'top')

panel = Frame(root, width = 700, height = 300, bg='#aaffff')
panel.pack(side = 'top')
root.resizable(False, False)

text = Text(panel)
text.tag_configure("center", justify='center')
text.tag_add("center", 1.0, "end")
text.configure(state='disabled', font=("Verdana", 25), background="bisque", cursor="arrow")
text.pack()
text.place(x = 100, y = 40, width = 500, height = 45)

text_input = Text(panel)
text_input.tag_configure("center", justify='center')
text_input.tag_add("center", 1.0, "end")
text_input.configure(state='disabled', font=("Verdana", 25), background="white")
text_input.pack()
text_input.place(x = 100, y = 120, width = 500, height = 45)

text_correct = Text(panel)
text_correct.tag_configure("center", justify='center')
text_correct.tag_add("center", 1.0, "end")
text_correct.configure(state='disabled', font=("Verdana", 25), background="white", cursor="arrow")
text_correct.pack()
text_correct.place(x = 100, y = 200, width = 500, height = 45)

text_time = Text(panelFrame)
text_time.tag_configure("center", justify='center')
text_time.tag_add("center", 1.0, "end")
text_time.configure(state='normal', font=("Verdana", 20), background="white", cursor="arrow")
text_time.pack()
text_time.place(x = 0, y = 0, width = 100, height = 40)


but_next = Button(panelFrame, text = 'New game', command = new_game)
but_next.bind("<Button-1>")
but_next.pack()
but_next.place(x = 310, y = 0, width = 80, height = 40)

but_exit = Button(panelFrame, text = 'Exit', command = exit)
but_exit.bind("<Button-1>")
but_exit.pack()
but_exit.place(x = 200, y = 0, width = 80, height = 40)

but_stat = Button(panelFrame, text = 'Statistics', command = statistics)
but_stat.bind("<Button-1>")
but_stat.pack()
but_stat.place(x = 420, y = 0, width = 80, height = 40)

load1 = PIL.Image.open("images/settings.png")
load2 = PIL.Image.open("images/list.png")
load3 = PIL.Image.open("images/stat.png")

render1 = PIL.ImageTk.PhotoImage(load1)
but_settings = Button(panelFrame, image=render1, command = settings)
but_settings.image = render1
but_settings.bind("<Button-1>")
but_settings.pack()
but_settings.place(x = 660, y = 0, width = 40, height = 40)

render2 = PIL.ImageTk.PhotoImage(load2)
but_settings = Button(panelFrame, image=render2, command = show_txt)
but_settings.image = render2
but_settings.bind("<Button-1>")
but_settings.pack()
but_settings.place(x = 610, y = 0, width = 40, height = 40)

render3 = PIL.ImageTk.PhotoImage(load3)
but_settings = Button(panelFrame, image=render3, command = show_stat)
but_settings.image = render3
but_settings.bind("<Button-1>")
but_settings.pack()
but_settings.place(x = 560, y = 0, width = 40, height = 40)

########

text_settings = Text(panel)
text_settings.configure(state='disable')

check_1 = IntVar(text_settings)
check_1.set(0)
eng = Radiobutton(text="English    ", variable=check_1, value=0)
rus = Radiobutton(text="Russian   ", variable=check_1, value=1)
both = Radiobutton(text="Both        ", variable=check_1, value=2) #o yes

text_change_time = Text(text_settings)
text_change_time.configure(state='normal', font=("Verdana", 10), background="white")

########

fill(file)
root.bind('<Key>', keypress)
root.mainloop()