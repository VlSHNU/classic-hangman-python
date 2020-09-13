from tkinter import *
from tkinter import messagebox
import random,ast
from PIL import ImageTk, Image
import collections
import os

root=Tk()
w_width = 1100
w_height = 600
x = (root.winfo_screenwidth() // 2) - (w_width // 2)
y = (root.winfo_screenheight() // 2) - (w_height // 2)
root.geometry('{}x{}+{}+{}'.format(w_width, w_height, x, y))
root.title("Classic Hangman!")
root.config(bg="white")
root.minsize(1000,480)

levels_list=[os.path.splitext(x)[0] for x in [f for f in os.listdir("categories") if os.path.isfile(os.path.join("categories", f))]]

hidden_words=dict()
words_list=[]
word_labels_list=[]
alphabets_btn_list=[]
level_btn_list=[]
wrong_count=0
full_word=None
word=None
hint=None

def forget_base_frames():
    hangman_body.pack_forget()
    hangman_body_image.pack_forget()
    alphabets_frame.pack_forget()
    words_frame.pack_forget()

def reset():
    global word_labels_list,alphabets_btn_list,wrong_count,level_btn_list
    hangman_body_image.delete("all")
    
    for label in word_labels_list:
        label.pack_forget()
    hint_label.pack_forget()
    for btn in alphabets_btn_list:
        btn.pack_forget()
    word_labels_list.clear()
    hidden_words.clear()
    wrong_count=0
    for btns in level_btn_list:
        btns.pack_forget()
    game_title.pack_forget()
    category_label.pack_forget()
    

def select_level_btn(event):
    global words_list
    event.widget.cget("text")
    a_file=open(f"categories\{event.widget.cget('text')}.json", "r")
    words_list=ast.literal_eval(a_file.read())
    print(words_list)
    a_file.close()
    level_select_bg.pack_forget()
    hangman_body.pack(side=LEFT,fill=Y)
    hangman_body_image.pack(expand=True)
    alphabets_frame.pack(side=BOTTOM,fill=X,expand=True)
    words_frame.pack(side=BOTTOM,fill=X,expand=True)
    create_word()
    create_alphabet_btns()


def choose_level():
    global levels_list,level_btn_list
    reset()
    forget_base_frames()
    level_select_bg.pack(expand=True,fill=BOTH)
    game_title.pack(pady=20)
    category_label.pack(pady=(0,20))
    for level in levels_list:
        btn=Label(level_select_bg,text=level,cursor="hand2",font=('Corbel',15),relief="solid",bd=1)
        btn.pack(ipadx=5,ipady=5,pady=5)
        btn.bind("<Button>",select_level_btn)
        level_btn_list.append(btn)
    

def get_initial_blocked_letters():
    global word,full_word
    temp=[item for item, count in collections.Counter(word).items() if count > 1]
    result = [ e for e in full_word ] 
    for a in temp: 
        if a in full_word: 
            result.remove(a)
    return result


def create_word():
    global words_list,hidden_words,word_labels_list,full_word,word,hint
    if not words_list:
        forget_base_frames()
        messagebox.showinfo(message="all levels passed")
        
        sys.exit()
    word=random.choice(list(words_list.keys()))
    hint=words_list[word]
    print(word)
    print(hint)
    vanish_no_list=random.sample(range(0, len(word)),len(word)-2)
    print(vanish_no_list)
    
    for n in vanish_no_list:
        if word[n] in hidden_words:
            hidden_words[word[n]].append(n)
        else:
            hidden_words[word[n]] = [n]
    full_word=list(word)
    print(hidden_words)
    for x in word:
        if x in hidden_words.keys():
            for y in hidden_words[x]:
                full_word[y]=" "

    print(full_word)

    words_holder.pack(side=TOP,fill=Y,pady=10)
    for letter in full_word:
        l=Label(words_holder,text=letter,font=('Corbel',20),relief="solid",bd=1,width=2,bg="white")
        l.pack(side=LEFT,padx=2)
        word_labels_list.append(l)

    hint_label.config(text=f"Hint: {hint}",font=('Corbel',15))
    hint_label.pack(side=TOP,fill=Y,pady=10)

        
def create_hangman_img(wrong_count):
    image = Image.open(f"images/{wrong_count}.png")
    image = image.resize((340, 420), Image.BICUBIC)
    img = ImageTk.PhotoImage(image)
    hangman_body_image.create_image(20, 20, image=img, anchor=NW)
    hangman_body_image.image=img


def check_letter(event):
    global hidden_words,wrong_count,full_word,word,words_list
    print(event.widget.cget("state"))
    if event.widget.cget("state") !="disabled":
        clicked_letter=event.widget.cget("text")
        print(clicked_letter)
        if clicked_letter in hidden_words.keys():
            for index in hidden_words[clicked_letter]:
                word_labels_list[index].config(text=clicked_letter)
                full_word[index]=clicked_letter
                print(full_word)
                if full_word==list(word):
                    messagebox.showinfo(message="Win\nYAY")
                    del words_list[word]
                    print(f"new {words_list}")
                    reset()
                    create_word()
                    create_alphabet_btns()      
        else:
            print("absent")
            wrong_count+=1
            create_hangman_img(wrong_count)
            
            if wrong_count>=5:
                messagebox.showinfo(message=f"noob\nthe answer was {word}")
                print(f"new {words_list}")
                choose_level()       
        event.widget.config(bg="SystemButtonFace",state=DISABLED)

def create_alphabet_btns():
    global alphabets_btn_list,full_word
    alphabet='a'

    letter_strip1.pack(side=TOP,fill=Y,pady=10)
    letter_strip2.pack(side=TOP,fill=Y,pady=10)
    for x in range(26):
        if x<13:
            b=Label(letter_strip1,text=alphabet,width=2,bg="white",cursor="hand2",font=('Corbel',25)) 
        else:
            b=Label(letter_strip2,text=alphabet,width=2,bg="white",cursor="hand2",font=('Corbel',25)) 
        b.pack(side=LEFT,padx=2)
        b.bind("<Button>",check_letter)
        if b.cget('text') in get_initial_blocked_letters():
            b.config(bg="SystemButtonFace",state=DISABLED)
        alphabets_btn_list.append(b)
        alphabet = chr(ord(alphabet) + 1)


hangman_body=Canvas(root,bg="white")
hangman_body_image=Canvas(hangman_body,bg="white",height=450)
words_frame=Canvas(root,bg="white")
alphabets_frame=Canvas(root,bg="white")

words_holder=Canvas(words_frame,bg="white")
hint_label=Label(words_frame)
letter_strip1=Frame(alphabets_frame,bg="white")
letter_strip2=Frame(alphabets_frame,bg="white")

level_select_bg=Canvas(root,height=w_height-4,width=w_width,bg="white")
game_title=Label(level_select_bg,text="Classic Hangman!",font=('Corbel',45,'bold'),bg="white")
category_label=Label(level_select_bg,text="Choose a category",font=('Corbel',20,'bold','underline'),bg="white")

choose_level()
root.mainloop()