import threading
def print_thread_names():
    print("Current thread name:", threading.current_thread().name)
# Create multiple threads
threads = []
for i in range(7):
    thread = threading.Thread(target=print_thread_names)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()