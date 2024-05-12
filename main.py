import time
import threading
import tkinter as tk
from pynput import keyboard
from PIL import ImageTk, Image

kill: bool = False
current_thread: None | threading.Thread = None


def macro_loop():
    global kill
    kill = False
    kb = keyboard.Controller()
    while kill is False:
        kb.press(keyboard.Key.ctrl)
        kb.release(keyboard.Key.ctrl)
        time.sleep(0.5)


def end_loop():
    global current_thread, kill
    if current_thread:
        current_thread.join(1)
        kill = True
    label.configure(text="Press F1 to start")
    control.configure(text='Start', command=lambda: start_loop())


def start_loop():
    global current_thread
    current_thread = threading.Thread(target=macro_loop)
    current_thread.start()
    label.configure(text="Press F1 to kill")
    control.configure(text="Stop", command=lambda: end_loop())


def on_press(key):
    if key == keyboard.Key.f1:
        if current_thread is None:
            start_loop()
        elif current_thread.is_alive():
            end_loop()
        else:
            start_loop()


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    root = tk.Tk()
    root.title('')
    root.iconbitmap("icons/icon16.ico")
    root.minsize(175, 150)
    root.maxsize(250, 200)
    img = Image.open("icons/icon64.ico")
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    panel = tk.Label(root, image=img, width=128)
    panel.pack(fill="both", expand=1)
    label = tk.Label(root, text="Press F1 to start")
    label.pack()
    control = tk.Button(root, width=10, text='Start', command=lambda: start_loop())
    control.pack()
    ext = tk.Button(root, width=10, text='Exit', command=root.destroy)
    ext.pack()
    root.mainloop()

