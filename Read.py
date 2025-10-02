###########################################################
#    Text scrolling, vowel detection and counting program       # 
#                       Written By: August C.                                       #
###########################################################

# Imports
from time import sleep
import sys
from SimpleMFRC522 import SimpleMFRC522
import LCD
import re
import math
import tm1637

# Variable initalization
reader = SimpleMFRC522()
tm = tm1637.TM1637(clk=20, dio=21)
clear = [0, 0, 0, 0]
LCD.init(0x27, 1)
LCD.clear()
tm.write(clear)
amt = 0
dis = 0

# Check if a word contains a vowel
def vowelOrConsonant(x):

    if (re.search(".+[aeiou]", x)):
        return True
    elif re.search("^[aeiou]", x):
        return True
    else:
        return False


# update vowel counter for a word
def updateVowelCounterWord(val, amt):
    for i in val:
        if vowelOrConsonant(i):
            amt = amt + 1
            tm.write(clear)
            if amt > 99:
                tm.numbers(amt - amt + 1, amt, color= False)
            else:
                tm.number(amt)

def writeToCard():
    LCD.clear()
    LCD.write(0,0, "What do you-")
    LCD.write(1,1, "want to write?")
    userInput = input("")
    LCD.clear()
    LCD.write(0,0, "Hold to reader")
    reader.write(userInput)
    LCD.clear()
    LCD.write(0,0, "Data written")
    sleep(2)
    

# Infinite Loop, to print text value of an RFID compatible device, and count the vowels
try:
    print("Check LCD screen for output")
    while True:
        val = "NaN"
        LCD.write(0,0, "hold card to-")
        LCD.write(1,1, "reader") 
        id, text = reader.read()
        LCD.clear()
        if vowelOrConsonant(text):
            LCD.write(2, 0, "Contains vowel")
            sleep(1)
            LCD.clear()
            val = text
            valEnd = re.search("\S(?=\s*$)",text)
            newVal = val[:valEnd.end()+1]
            dis = len(newVal) -1
            if dis > 30:
                # Write and clear the screen after displaying new character to imitate scrolling effect
                for i in range(0, dis):
                    LCD.write(0, 0, newVal[i:16+i])
                    if vowelOrConsonant(newVal[i]):
                         amt = amt + 1
                         tm.write(clear)
                         tm.number(amt)
                    sleep(0.8)
                    LCD.clear()
            else:
                if dis < 16:
                    LCD.write(0,0, newVal)
                    updateVowelCounterWord(newVal, amt)
                    sleep(3)
                    LCD.clear()
                else:
                    LCD.write(0, 0, newVal[0:15] + "-")
                    LCD.write(1, 1, newVal[15:])
                    updateVowelCounterWord(newVal, amt)
                    sleep(3)
                    LCD.clear()
        else:
            LCD.write(2, 0, "No vowels here")
            sleep(1)
            LCD.clear()
        
        LCD.clear()
        LCD.write(0,0, "Write new data-")
        LCD.write(1,1, "to card? y/n")
        choice = input("")
        if choice == "y":
            writeToCard()
        elif choice == "n":
            LCD.clear()
            LCD.write(0,0, "ok, continuing")
            sleep(1)
        else:
            LCD.clear()
            LCD.write(0,0, "invalid input")

except KeyboardInterrupt:
    GPIO.cleanup()
    raise
  
