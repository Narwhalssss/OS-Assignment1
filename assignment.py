import threading
import random
import queue

# Constants
LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = queue.Queue(maxsize=BUFFER_SIZE)

counter_condition = threading.Condition()
counter = 0

def producer():
    global counter
    with open("all.txt", "w") as f_all:
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            buffer.put(num)  
            with counter_condition:
                counter += 1
                counter_condition.notify_all()  
            f_all.write(f"{num}\n")

def consumer(odd):
    file_name = "odd.txt" if odd else "even.txt"
    with open(file_name, "w") as f_out:
        while True:
            with counter_condition:
                counter_condition.wait_for(lambda: counter == MAX_COUNT or not buffer.empty())
                if counter == MAX_COUNT and buffer.empty():
                    break
            try:
                num = buffer.get_nowait()  
                if odd and num % 2 == 1 or not odd and num % 2 == 0:
                    f_out.write(f"{num}\n")
                else:
                    buffer.put(num)
            except queue.Empty:
                continue

producer_thread = threading.Thread(target=producer)
consumer_thread_odd = threading.Thread(target=consumer, args=(True,))
consumer_thread_even = threading.Thread(target=consumer, args=(False,))

producer_thread.start()
consumer_thread_odd.start()
consumer_thread_even.start()

producer_thread.join()
consumer_thread_odd.join()
consumer_thread_even.join()

print("YES")


