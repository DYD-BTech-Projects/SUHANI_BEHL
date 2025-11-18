This project is a complete simulation of the Producer–Consumer Problem using Python, demonstrating how multiple producers and consumers work together using threads, semaphores, mutex locks, and a shared buffer.

It includes both:

A Backend Program (terminal-based simulation)

A Tkinter GUI Application (visual & interactive simulation)

🧩 Project Description

The Producer–Consumer Problem is a classic Operating System synchronization problem.
This project helps you understand:

How producers create items

How consumers remove items

How a fixed-size buffer works

Why mutex locks are required

What causes overflow (buffer full) & underflow (buffer empty)

How semaphores synchronize the system

The GUI provides a visual, easy-to-understand version of the concept, while the backend shows a real multithreading simulation.

🚀 Features
✔ Frontend (GUI)

Beautiful splash screen

Modern UI with dark theme

Real-time buffer visualization

Mutex lock–unlock indicator

Overflow & underflow alerts

Pause / Resume / Reset controls

Display of consumer order

Detailed Results Page

Easy input for number of producers & consumers

✔ Backend (Terminal)

Uses threading, semaphores, and Queue

Fixed buffer size

Random production & consumption timing

Logs:

Items produced

Items consumed

Overflow count

Underflow count

Auto-generated Gantt chart timeline

Automatic simulation runtime

📁 Files Included
File	Description
frontend.py	Tkinter-based GUI simulation
backend.py	Multithreading + semaphore backend logic
README.md	Project documentation
🔧 How to Run
1️⃣ Run the GUI Version
python frontend.py

2️⃣ Run the Terminal Backend
python backend.py


No external libraries needed — everything uses Python's built-in modules.

🎨 What You Will See in GUI

Visual buffer with 5 slots

Producers adding items

Consumers removing items

Mutex status:

🔒 Locked

🔓 Unlocked

Overflow warnings (Buffer Full)

Underflow warnings (Buffer Empty)

Consumption order timeline

Final results summary

📊 Learning Outcomes

This project helps you understand:

Multithreading

Semaphores (empty, full, mutex)

Critical section management

FIFO buffer working

Real-time synchronization

Producer–Consumer OS concept

Perfect for OS Lab, Python project submission, and academic presentations.

👩‍💻 Developer

Suhani
A Python enthusiast exploring GUI development & operating system concepts.
