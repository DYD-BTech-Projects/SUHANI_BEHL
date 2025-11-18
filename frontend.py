import tkinter as tk
import time
import string
import random
import threading
from tkinter import ttk

# GLOBAL VARIABLES
BUFFER_SIZE = 5
buffer = []
item_names = list(string.ascii_uppercase)
produced_list = []
consumption_order = []
running = False
paused = False
overflow_count = 0
underflow_count = 0

# Helper (thread-safe small pause)
def wait_or_pause(duration):
    steps = int(duration * 10)
    for _ in range(steps):
        time.sleep(0.1)
        if not running:
            return False
        while paused:
            time.sleep(0.1)
            if not running:
                return False
    return True

# SPLASH SCREEN
def show_splash_then_start(root):
    root.withdraw()
    splash = tk.Toplevel()
    splash.title("🚀 Loading Producer–Consumer Simulator")
    splash.geometry("700x400")
    splash.configure(bg="#101820")
    splash.resizable(False, False)

    tk.Label(splash, text="🎯 Producer–Consumer Simulator",
             fg="white", bg="#101820", font=("Arial", 20, "bold")).pack(pady=30)
    tk.Label(splash, text="Developed ❤️ by Suhani",
             fg="#00ffcc", bg="#101820", font=("Arial", 14, "italic")).pack(pady=10)
    tk.Label(splash, text="Initializing System Components...",
             fg="skyblue", bg="#101820", font=("Arial", 12)).pack(pady=20)

    progress = ttk.Progressbar(splash, orient="horizontal", length=420, mode="determinate")
    progress.pack(pady=30)
    progress["maximum"] = 100

    def loader():
        for i in range(101):
            progress["value"] = i
            splash.update_idletasks()
            time.sleep(0.03)
        splash.destroy()
        root.deiconify()
        home_page(root)

    threading.Thread(target=loader, daemon=True).start()

# HOME PAGE
def home_page(root):
    for w in root.winfo_children():
        w.destroy()

    frame = tk.Frame(root, bg="#141414")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🎯 Producer–Consumer Problem Simulator",
             font=("Arial", 24, "bold"), fg="#00ffcc", bg="#141414").pack(pady=24)

    info_text = (
        "👋 Welcome!\n\n"
        "This interactive simulation shows producers producing items\n"
        "and consumers taking them from a fixed-size buffer (FIFO).\n\n"
        "• Buffer limited to 5 slots\n"
        "• Producers wait if buffer full (overflow)\n"
        "• Consumers wait if buffer empty (underflow)\n"
        "• Mutex (visual) shows who has exclusive access and when it’s unlocked\n"
    )
    tk.Label(frame, text=info_text, fg="white", bg="#141414",
             font=("Arial", 13), justify="left", wraplength=820).pack(pady=10)

    tk.Label(frame, text="💡 Developed by: Suhani", fg="#00ff99",
             bg="#141414", font=("Arial", 12, "italic")).pack(pady=6)

    btn = tk.Button(frame, text="▶ Start Simulation", width=20, bg="#00cc66", fg="white",
                    font=("Arial", 14, "bold"), command=lambda: (frame.destroy(), visualization_page(root)))
    btn.pack(pady=28)

# VISUALIZATION PAGE
def visualization_page(root):
    global buffer, item_names, produced_list, consumption_order, running, paused, overflow_count, underflow_count

    buffer = []
    item_names = list(string.ascii_uppercase)
    produced_list = []
    consumption_order = []
    overflow_count = 0
    underflow_count = 0
    running = False
    paused = False

    for w in root.winfo_children():
        w.destroy()

    page = tk.Frame(root, bg="#1e1e1e")
    page.pack(fill="both", expand=True)

    tk.Label(page, text="Producer–Consumer Visualization (Mutex Lock–Unlock)",
             font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white").pack(pady=8)

    canvas = tk.Canvas(page, width=850, height=250, bg="#2e2e2e", highlightthickness=0)
    canvas.pack(pady=10)

    buffer_slots = []
    slot_texts = []
    start_x, slot_w = 200, 80
    for i in range(BUFFER_SIZE):
        x1 = start_x + i * (slot_w + 2)
        rect = canvas.create_rectangle(x1, 100, x1 + slot_w, 180, fill="black", outline="white", width=2)
        txt = canvas.create_text(x1 + slot_w // 2, 140, text="", font=("Arial", 14, "bold"), fill="white")
        buffer_slots.append(rect)
        slot_texts.append(txt)

    status = tk.Label(page, text="Status: Waiting for input...", font=("Arial", 13), bg="#1e1e1e", fg="white")
    status.pack(pady=6)
    lock_label = tk.Label(page, text="🔓 Mutex Unlocked", font=("Arial", 14, "bold"),
                          bg="#1e1e1e", fg="lightgreen")
    lock_label.pack(pady=4)
    order_label = tk.Label(page, text="Consumption Order: —", font=("Arial", 13, "bold"),
                           bg="#1e1e1e", fg="skyblue")
    order_label.pack(pady=6)

    input_frame = tk.Frame(page, bg="#1e1e1e")
    input_frame.pack(pady=8)
    tk.Label(input_frame, text="Producers:", bg="#1e1e1e", fg="white").grid(row=0, column=0, padx=6)
    producers_entry = tk.Entry(input_frame, width=6)
    producers_entry.grid(row=0, column=1, padx=6)
    tk.Label(input_frame, text="Consumers:", bg="#1e1e1e", fg="white").grid(row=0, column=2, padx=6)
    consumers_entry = tk.Entry(input_frame, width=6)
    consumers_entry.grid(row=0, column=3, padx=6)

    btn_row = tk.Frame(page, bg="#1e1e1e")
    btn_row.pack(pady=14)

    start_btn = tk.Button(btn_row, text="▶ Start", width=12, bg="green", fg="white", font=("Arial", 12, "bold"))
    pause_btn = tk.Button(btn_row, text="⏸ Pause", width=12, bg="#007acc", fg="white", font=("Arial", 12, "bold"))
    reset_btn = tk.Button(btn_row, text="🔄 Reset", width=12, bg="#444", fg="white", font=("Arial", 12, "bold"))
    results_btn = tk.Button(btn_row, text="📄 Results", width=12, bg="purple", fg="white", font=("Arial", 12, "bold"))

    start_btn.grid(row=0, column=0, padx=10)
    pause_btn.grid(row=0, column=1, padx=10)
    reset_btn.grid(row=0, column=2, padx=10)
    results_btn.grid(row=0, column=3, padx=10)

    def update_buffer_ui(highlight=None):
        for i in range(BUFFER_SIZE):
            if i < len(buffer):
                canvas.itemconfig(buffer_slots[i], fill="lime")
                canvas.itemconfig(slot_texts[i], text=buffer[i], fill="black")
            else:
                canvas.itemconfig(buffer_slots[i], fill="black")
                canvas.itemconfig(slot_texts[i], text="")
        if highlight == "overflow":
            canvas.config(highlightbackground="red", highlightthickness=3)
        elif highlight == "underflow":
            canvas.config(highlightbackground="yellow", highlightthickness=3)
        else:
            canvas.config(highlightthickness=0)
        root.update_idletasks()

    # PRODUCER
    def produce_item(pid):
        global buffer, produced_list, overflow_count
        if len(buffer) >= BUFFER_SIZE:
            status.config(text=f"Producer {pid} waiting — Buffer Full ❌")
            overflow_count += 1
            update_buffer_ui("overflow")
            wait_or_pause(1.0)
            lock_label.config(text="🔓 Mutex Unlocked — Producer can now access buffer", fg="lightgreen")
            update_buffer_ui(None)
            return
        lock_label.config(text=f"🔒 Mutex Locked by Producer {pid}", fg="red")
        wait_or_pause(0.6)
        if not item_names:
            item_names.extend(list(string.ascii_uppercase))
        item = item_names.pop(0)
        buffer.append(item)
        produced_list.append(item)
        update_buffer_ui()
        status.config(text=f"Producer {pid} produced {item}. Buffer size: {len(buffer)}")
        wait_or_pause(0.8)
        lock_label.config(text="🔓 Mutex Unlocked", fg="lightgreen")

    # CONSUMER
    def consume_item(cid):
        global buffer, consumption_order, underflow_count
        if len(buffer) == 0:
            status.config(text=f"Consumer {cid} waiting — Buffer Empty ⚠️")
            underflow_count += 1
            update_buffer_ui("underflow")
            wait_or_pause(1.0)
            lock_label.config(text="🔓 Mutex Unlocked — Consumer can now access buffer", fg="lightgreen")
            update_buffer_ui(None)
            return
        lock_label.config(text=f"🔒 Mutex Locked by Consumer {cid}", fg="orange")
        wait_or_pause(0.6)
        item = buffer.pop(0)
        consumption_order.append(item)
        update_buffer_ui()
        status.config(text=f"Consumer {cid} consumed {item}. Buffer size: {len(buffer)}")
        order_label.config(text="Consumption Order: " + " → ".join(consumption_order))
        wait_or_pause(0.8)
        lock_label.config(text="🔓 Mutex Unlocked", fg="lightgreen")

    def simulation_loop(num_producers, num_consumers, steps=20):
        global running
        running = True
        status.config(text="Simulation started...")
        for _ in range(steps):
            if not running:
                break
            if random.choice(["P", "C"]) == "P":
                pid = random.randint(1, max(1, num_producers))
                produce_item(pid)
            else:
                cid = random.randint(1, max(1, num_consumers))
                consume_item(cid)
        status.config(text="✅ Simulation finished.")
        running = False

    def start_clicked():
        global running, paused
        if running:
            return
        try:
            np = int(producers_entry.get())
            nc = int(consumers_entry.get())
            if np <= 0 or nc <= 0:
                status.config(text="⚠️ Enter positive integers for producers & consumers.")
                return
        except Exception:
            status.config(text="⚠️ Please enter valid integers.")
            return
        paused = False
        t = threading.Thread(target=simulation_loop, args=(np, nc, 20), daemon=True)
        t.start()

    def pause_clicked():
        global paused
        paused = not paused
        pause_btn.config(text="▶ Resume" if paused else "⏸ Pause",
                         bg="#ffcc00" if paused else "#007acc")

    def reset_clicked():
        global running, paused, buffer, item_names, produced_list, consumption_order, overflow_count, underflow_count
        running = False
        paused = False
        buffer = []
        item_names = list(string.ascii_uppercase)
        produced_list = []
        consumption_order = []
        overflow_count = 0
        underflow_count = 0
        status.config(text="🔄 Reset done.")
        lock_label.config(text="🔓 Mutex Unlocked", fg="lightgreen")
        order_label.config(text="Consumption Order: —")
        update_buffer_ui()

    def show_results():
        result_page(root)

    start_btn.config(command=start_clicked)
    pause_btn.config(command=pause_clicked)
    reset_btn.config(command=reset_clicked)
    results_btn.config(command=show_results)

# RESULTS PAGE
def result_page(root):
    global produced_list, consumption_order, overflow_count, underflow_count
    for w in root.winfo_children():
        w.destroy()

    frame = tk.Frame(root, bg="#121212")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📊 Simulation Results", font=("Arial", 22, "bold"),
             fg="white", bg="#121212").pack(pady=20)

    produced_count = len(produced_list)
    consumed_count = len(consumption_order)
    produced_items = " → ".join(produced_list) if produced_list else "(none)"
    consumed_items = " → ".join(consumption_order) if consumption_order else "(none)"

    summary = (
        f"🧩 Total Items Produced: {produced_count}\n\n"
        f"📦 Produced items: {produced_items}\n\n"
        f"🧾 Items Consumed: {consumed_items}\n\n"
        f"🚫 Overflow (Full Buffer): {overflow_count}\n"
        f"⚠️ Underflow (Empty Buffer): {underflow_count}\n\n"
        "✅ Learning Points:\n"
        "- Mutex Locked = critical section access\n"
        "- Unlocked = buffer free to access again\n"
        "- FIFO ensures order: first produced → first consumed\n"
        "- Producers wait when full; consumers wait when empty\n"
    )

    tk.Label(frame, text=summary, bg="#121212", fg="lightgreen",
             font=("Arial", 13), justify="left", wraplength=950).pack(pady=12)

    tk.Button(frame, text="🏠 Back to Home", width=18, bg="#00b894", fg="white",
              font=("Arial", 12, "bold"),
              command=lambda: (frame.destroy(), home_page(root))).pack(pady=18)

# ENTRY POINT
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Producer–Consumer Project Simulator by Suhani")
    root.geometry("1100x700")
    root.configure(bg="#000")
    show_splash_then_start(root)
    root.mainloop()
