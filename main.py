# ----------------------------- Importing Modules ----------------------------------- #
import tkinter
from tkinter.filedialog import askopenfilename
import cv2
import PIL.Image
import PIL.ImageTk
from functools import partial  # to give args to functions in 'command' of Buttons
import threading
import time
import imutils
# ----------------------------------------------------------------------------------- #

# ---------------------------------- Main Screen ------------------------------------- #
SET_WIDTH = 750
SET_HEIGHT = 400

root = tkinter.Tk()
root.wm_iconbitmap("icon1.ico")
root.resizable(width=False, height=False)
root.title("3rd Umpire Decision Review")
# ----------------------------------------------------------------------------------- #

# to get the video
stream = cv2.VideoCapture("1.mp4")

# -------------------------------------- Functions ------------------------------------ #


# Playing video in forward/backward mode
def play(speed):
    try:
        frame = stream.get(cv2.CAP_PROP_POS_FRAMES)
        stream.set(cv2.CAP_PROP_POS_FRAMES, frame + speed)

        grabbed, frame = stream.read()
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        ###
        i = canvas.create_text(120, 25, fill="yellow", font="Times 22 bold", text="Decision Pending")
        r = canvas.create_rectangle(canvas.bbox(i), fill="dark gray")
        canvas.tag_lower(r, i)
    except:
        print("Video Ended !!!")


# To show "Decision Pending", then "sponsor" and then "Out/Not-Out
def pending(decision):
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    ###
    time.sleep(2)  # for pausing the screen
    ###
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    ###
    time.sleep(1.7)
    ###
    if decision == 'out':
        decision_img = "out.png"
    else:
        decision_img = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


# If batsman is OUT
def out():
    thread = threading.Thread(target=pending, args=("out", ))
    thread.daemon = 1
    thread.start()


# If batsman is NOT-OUT
def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()


# For browsing different video clips (mp4 only)
def browse_function():
    global stream
    file_name = tkinter.filedialog.askopenfile(parent=root, initialdir='/home/',
                                               title='Select your video', filetypes=[('video files', '.mp4')])
    if file_name is not None:
        stream = cv2.VideoCapture(file_name.name)

# ----------------------------------------------------------------------------------------- #


# ---------------------------------------- Main Body -------------------------------------- #
if __name__ == "__main__":
    btn = tkinter.Button(root, text="Choose File", width=50, background="orange",
                         command=browse_function)
    btn.pack()

    cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
    canvas = tkinter.Canvas(root, width=SET_WIDTH, height=SET_HEIGHT)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
    img_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
    canvas.pack()

    btn = tkinter.Button(root, text="<< Previous (Fast)", width=50, command=partial(play, -25))
    btn.pack()
    btn = tkinter.Button(root, text="<< Previous (Slow)", width=50, command=partial(play, -2))
    btn.pack()
    btn = tkinter.Button(root, text=">> Next (Slow)", width=50, command=partial(play, 2))
    btn.pack()
    btn = tkinter.Button(root, text=">> Next (Fast)", width=50, command=partial(play, 25))
    btn.pack()
    btn = tkinter.Button(root, text="Give OUT", background="red", width=50, command=out)
    btn.pack()
    btn = tkinter.Button(root, text="Give NOT-OUT", background="green", width=50, command=not_out)
    btn.pack()

    root.mainloop()
# ------------------------------------------------------------------------------------------ #
