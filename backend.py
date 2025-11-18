import threading   # For creating threads (producers and consumers run in parallel)
import time        # For adding delays (simulate production/consumption time)
import random      # For random choices and timing
import string      # to produce as items
from queue import Queue  # Thread-safe queue for the buffer
#BUFFER CONFIGURATION
BUFFER_SIZE = 5             # Maximum number of items buffer can hold
buffer = Queue(BUFFER_SIZE) # Queue acts as the buffer
mutex = threading.Semaphore(1)        # Mutex for exclusive access to buffer
empty = threading.Semaphore(BUFFER_SIZE)  # Tracks empty slots in buffer
full = threading.Semaphore(0)         # Tracks filled slots in buffer
#GLOBAL STATE
produced_items = []         # Keep track of all produced items
consumed_items = []         # Keep track of all consumed items
gantt_chart = []            # Timeline of production and consumption for visualization
overflow_count = 0          # Number of times producers had to wait (buffer full)
underflow_count = 0         # Number of times consumers had to wait (buffer empty)
running = True              # Flag to control when threads should stop
#PRODUCER FUNCTION
def produce(pid):
    global overflow_count
    while running:  # Keep producing while simulation is running
        item = random.choice(string.ascii_uppercase)  # Pick a random letter to produce
        empty.acquire()  # Wait if buffer has no empty slots (decrement empty semaphore)

        mutex.acquire()  # Lock the buffer to safely add an item
        if buffer.full():  # Check if buffer is actually full
            print(f"[Producer {pid}] ❌ Buffer Full — Waiting (wait signal)")
            overflow_count += 1  # Count overflow events
        else:
            buffer.put(item)           # Add item to buffer
            produced_items.append(item) # Track produced item
            gantt_chart.append(f"P{pid}:{item}")  # Add event to Gantt chart
            print(f"[Producer {pid}] 🔒 Mutex Locked")
            print(f"[Producer {pid}] Produced Item → {item}")
            print(f"Buffer State: {list(buffer.queue)}")  # Show current buffer contents
        time.sleep(random.uniform(0.5, 1.1))  # Simulate production time
        print(f"[Producer {pid}] 🔓 Mutex Unlocked (signal)\n")
        mutex.release()  # Unlock buffer
        full.release()   # Signal consumer that buffer has items
        time.sleep(random.uniform(0.6, 1.2))  # Delay before producing next item
#CONSUMER FUNCTION
def consume(cid):
    global underflow_count
    while running:  # Keep consuming while simulation is running
        full.acquire()  # Wait if buffer is empty (decrement full semaphore)

        mutex.acquire()  # Lock buffer to safely remove an item
        if buffer.empty():  # Check if buffer is actually empty
            print(f"[Consumer {cid}] ⚠️ Buffer Empty — Waiting (wait signal)")
            underflow_count += 1  # Count underflow events
        else:
            item = buffer.get()       # Remove item from buffer
            consumed_items.append(item) # Track consumed item
            gantt_chart.append(f"C{cid}:{item}")  # Add event to Gantt chart
            print(f"[Consumer {cid}] 🔒 Mutex Locked")
            print(f"[Consumer {cid}] Consumed Item → {item}")
            print(f"Buffer State: {list(buffer.queue)}")  # Show current buffer contents
        time.sleep(random.uniform(0.5, 1.1))  # Simulate consumption time
        print(f"[Consumer {cid}] 🔓 Mutex Unlocked (signal)\n")
        mutex.release()  # Unlock buffer
        empty.release()  # Signal producer that buffer has empty slots
        time.sleep(random.uniform(0.6, 1.2))  # Delay before consuming next item
# MAIN FUNCTION
def main():
    global running

    print("\n PRODUCER–CONSUMER SIMULATOR \n")
    np = int(input("Enter number of Producers: "))  # Get number of producers
    nc = int(input("Enter number of Consumers: "))  # Get number of consumers
    # Create threads for producers and consumers
    producers = [threading.Thread(target=produce, args=(i+1,)) for i in range(np)]
    consumers = [threading.Thread(target=consume, args=(i+1,)) for i in range(nc)]
    # Start all threads
    for t in producers + consumers:
        t.daemon = True  # Set threads as daemon (end automatically with main program)
        t.start()
    # Run simulation for random duration automatically
    runtime = random.randint(12, 20)  # Duration in seconds
    print(f"\n🕒 Simulation running automatically for {runtime} seconds...\n")
    time.sleep(runtime)
    # Stop all threads
    running = False
    time.sleep(2)  # Give threads time to finish
    # RESULTS SUMMARY 
    print("\n Simulation Complete!\n")
    print("--- RESULTS SUMMARY ---")
    print(f"Total Items Produced: {len(produced_items)}")
    print(f"Total Items Consumed: {len(consumed_items)}")
    print(f"Overflow (Buffer Full Waits): {overflow_count}")
    print(f"⚠️ Underflow (Buffer Empty Waits): {underflow_count}")
    print("\nProduced Order:", " → ".join(produced_items) if produced_items else "None")
    print("Consumed Order:", " → ".join(consumed_items) if consumed_items else "None")

    print("\n --- GANTT CHART (Execution Timeline) ---")
    if gantt_chart:
        print(" → ".join(gantt_chart))
    else:
        print("(No events recorded)")

    print("\nPress 'q' to exit...")
    # Wait for user to quit
    while True:
        key = input()
        if key.lower() == 'q':
            print("👋 Exiting simulation. Goodbye!")
            break
#ENTRY POINT
if __name__ == "__main__":
    main()
