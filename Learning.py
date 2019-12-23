import secrets as rand
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
    root.destroy()

def show_new_word():
    if is_stop:
        restart()
    text.configure(state='normal')
    text.delete(1.0, END)
    text.insert(END, generate_word(), "center")
    text.configure(state='disabled')

def restart():
    #training()
    global is_stop; global stat_i; global time_; global time_pass; global chance
    is_stop = False
    text_input.configure(state='normal')
    stat_i = 1; time_ = 0; time_pass = 0; chance+=1
    zerroing()
    show_new_word()
    kol_word(len(words))
    create_threads()

def zerroing():
    global incorrect; global attempt
    incorrect = [0 for x in range(len(words)+1)]
    attempt = [0 for x in range(len(words)+1)]

def fill():
    f = open('data/words.txt', 'r')
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
    training() #
    restart()

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
    if ((mode == "both" and rand.randbelow(2) == 0) or mode == "rus"):
        correct_word *= -1
    return dict_words[-correct_word]

def keypress(key): #in linux
    if key.keycode == 36: #enter
        input()
    elif key.keycode == 9: #esc
        exit()
    elif key.keycode > 66 and key.keycode < 70: #f1 f2 f3
        statistics()
    elif key.keycode == 70: #f4
        settings()

def input():
    if close_settings():
        return
    s = re.split(r'\s+', text_input.get(1.0, END))
    if s[0] == '':
        s[0] = s[1]
    text_input.delete(1.0, END)
    
    if correct_word != 0:
        attempt[correct_word]+=1
        if dict_words[correct_word] == s[0]:
            answer(True)
        else:
            incorrect[abs(correct_word)]+=1
            answer(False)
    show_new_word()

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
    

######################################################### Main

dict_words = {}; words = []; incorrect = []; attempt = []
correct_word = 0; stat_i = 1; mode = "eng"; open_sett = False; all_time = 10; time_ = 0; time_pass = 0; is_stop = False; chance = 0

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
text.place(x = 200, y = 40, width = 300, height = 45)

text_input = Text(panel)
text_input.configure(state='normal', font=("Verdana", 25), background="white")
text_input.pack()
text_input.place(x = 200, y = 120, width = 300, height = 45)

text_correct = Text(panel)
text_correct.tag_configure("center", justify='center')
text_correct.tag_add("center", 1.0, "end")
text_correct.configure(state='disabled', font=("Verdana", 25), background="white", cursor="arrow")
text_correct.pack()
text_correct.place(x = 200, y = 200, width = 300, height = 45)

text_time = Text(panelFrame)
text_time.tag_configure("center", justify='center')
text_time.tag_add("center", 1.0, "end")
text_time.configure(state='disabled', font=("Verdana", 20), background="white", cursor="arrow")
text_time.pack()
text_time.place(x = 0, y = 0, width = 100, height = 40)


but_next = Button(panelFrame, text = 'Next', command = input)
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

load = PIL.Image.open("images/settings.png")
render = PIL.ImageTk.PhotoImage(load)
but_settings = Button(panelFrame, image=render, command = settings)
but_settings.image = render
but_settings.bind("<Button-1>")
but_settings.pack()
but_settings.place(x = 660, y = 0, width = 40, height = 40)

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

fill()
root.bind('<Key>', keypress)
root.mainloop()