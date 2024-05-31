import _thread
import time

args = None

# Define a function for the thread
def mythread(threadname):
   global args
   args = input("input anything: ")

# Create one threads as follows

start = time.time()
_thread.start_new_thread( mythread, ("UI",) )
while args==None:  # mimic your work loop
       # print("Start", time.time())
       if start  + 1 < time.time():
         print(start)
         start = time.time()

print("main loops end demo end")
