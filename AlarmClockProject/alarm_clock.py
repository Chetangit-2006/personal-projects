import tkinter as tk
import datetime
import time
import threading
import winsound

alarms = []

def play_sound():
    try:
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
    except:
        print("Sound file not found!")

def check_alarms():
    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        for alarm in alarms:
            if alarm == now:
                threading.Thread(target=play_sound).start()
        time.sleep(1)

def add_alarm():
    alarm_time = entry.get()
    alarms.append(alarm_time)
    listbox.insert(tk.END, alarm_time)
    entry.delete(0, tk.END)

def update_clock():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=now)
    root.after(1000, update_clock)

root = tk.Tk()
root.title("Alarm Clock")
root.geometry("300x350")

clock_label = tk.Label(root, font=("Arial", 20))
clock_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add Alarm", command=add_alarm)
add_btn.pack(pady=5)

listbox = tk.Listbox(root)
listbox.pack(pady=10)

threading.Thread(target=check_alarms, daemon=True).start()

update_clock()

root.mainloop()