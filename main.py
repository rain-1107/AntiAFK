import time
import threading
import tkinter as tk
from pynput import keyboard

kill = False
current_thread: bool | threading.Thread = False


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
    label2.configure(text="Press F1 to start")
    control.configure(text='Start', command=lambda: start_loop())


def start_loop():
    global current_thread
    current_thread = threading.Thread(target=macro_loop)
    current_thread.start()
    label2.configure(text="Press F1 to kill")
    control.configure(text="Stop", command=lambda: end_loop())


def on_press(key):
    if key == keyboard.Key.f1:
        if current_thread is False:
            start_loop()
        elif current_thread.is_alive():
            end_loop()
        else:
            start_loop()


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    root = tk.Tk()
    root.title('AntiAFK')
    root.minsize(200, 100)
    label1 = tk.Label(root, text="AntiAFK macro")
    label1.pack()
    label2 = tk.Label(root, text="Press F1 to start")
    label2.pack()
    control = tk.Button(root, width=10, text='Start', command=lambda: start_loop())
    control.pack()
    ext = tk.Button(root, width=10, text='Exit', command=root.destroy)
    ext.pack()
    root.mainloop()

