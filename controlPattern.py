import asyncServo
import getch
from datetime import datetime
import os
import movements as m
import json

def control(servo):
    s = ""
    delta = 3
    startServo = int(servo / 4) * 4
    servos = "["
    for i in range(startServo, startServo + 3):
        servos += str(i) + ","
    speed = .1
    print("Control servos %s by arrow keys and page up / down" % (servos[:-1]+ "]"))
    print("Increase delta hit + redcue delta hit - To exit hit q")
    print(". makes a point in pattern, w will write pattern, digit will add a delay to pattern")
    pattern = "["   
    while True:
        c = getch.getch()
        if len(c) == 0:
            continue
        key = ord(c)
        if c == "q":  # q to exit
            print("exit")
            break
        if c == "+":
            delta += 1
            print("increase delta new delta:", delta)
        if c == "-":
            delta -= 1
            if delta <= 0: delta = 0
            print("decrease delta new delta:", delta)
        if c == ".":
            p = "[%d,%.1f],[%d,%.1f],[%d,%.1f]," % (startServo, round(m.legs.getAngle(startServo),1),
                                         startServo+1,round(m.legs.getAngle(startServo+1),1),
                                         startServo+2,round(m.legs.getAngle(startServo+2),1))
            print("Pattern:", p)
            pattern += p
        if c >= "0" and c <= "9":
            p = "[." + c + "]," 
            print("Pattern:", p)
            pattern += p
        if c == "w":
            s = input("Control type >")
            #fn =  os.getcwd() + "/patterns/" + s + " " + datetime.now().strftime("%m-%d %H:%M:%S.pat")
            fn =  os.getcwd() + "/patterns/" + s + ".pat"
            pattern = pattern[:-1] + "]"
            print("Write pattern %s to file %s" % (pattern, fn))
            with open(fn, "w") as text_file:
                 text_file.write(pattern)
            pattern = "["
        elif key == 10:  # Enter
            print("Enter:", s)
            s = ""
        elif key == 27:  # Special keys (arrows, f keys, ins, del, etc.)
            c1 = getch.getche()
            key1 = ord(c1)
            key = ord(getch.getche())
            #print(c1, "|", key1, ":", key)
            if key == 66:  # Down arrow
                asyncServo.asyncMove([[startServo, m.legs.getAngle(startServo) + delta]], speed)
                #print("down arrow")
            elif key == 65:  # Up arrow
                asyncServo.asyncMove( [[startServo, m.legs.getAngle(startServo) - delta]], speed )
                #print("up arrow")
            elif key == 67:  # right arrow
                asyncServo.asyncMove([[startServo+1, m.legs.getAngle(startServo+1) - delta]],speed)
                #print("right arrow")
            elif key == 68:  # left arrow
                #print("left arrow")
                asyncServo.asyncMove([[startServo+1, m.legs.getAngle(startServo+1) + delta]], speed)
            elif key == 53:  # page up
                #print("page up")
                asyncServo.asyncMove([[startServo+2, m.legs.getAngle(startServo+2) + delta]], speed)
            elif key == 54:  # page down
                #print("page down")
                asyncServo.asyncMove([[startServo+2, m.legs.getAngle(startServo+2) - delta]], speed)

        else:
            s += chr(key)


def runFile(fn):
  try:
    fn =  os.getcwd() + "/patterns/" + fn + ".pat"
    f = open(fn, 'r')
    s = f.read()
    f.close()
    print("s:", s)
    ar = json.loads(s)
    print("ar:", ar)
    asyncServo.asyncMove(ar, .5)
  except FileNotFoundError:
    print('File %s does not exist' % (fn))
    return
  #except:
   #   print("Error processing file")

 