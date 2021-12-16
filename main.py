import pyfirmata
import playsound
from gtts import gTTS
import os
import speech_recognition as sr
from datetime import datetime
import random

time = datetime.now()

arduino = pyfirmata.Arduino("COM8")

light = arduino.get_pin("d:8:o")
robotHead = arduino.get_pin("d:9:s")
rightElbow = arduino.get_pin("d:10:s")
leftElbow = arduino.get_pin("d:11:s")
lm35pin = arduino.get_pin('a:0:i')

'''
3*SG90 micro servo motor for head and hands
LM35 temperature sensor
you can use any arduino board
light pin connected to a SSR relay
upload standard firmata sketch on arduino board
file->example->(examples for any board) firmata->standard firmata

'''

it = pyfirmata.util.Iterator(arduino)
it.start()

robotHead.write(90)
rightElbow.write(0)
leftElbow.write(0)

#define some response message for input command

ResponseMessageList = ["hey","hi master","hello there","hello","hello master","hello, how do you do","hey, what'sapp"]
ResponseMessageList2 = ["i'm fine master","i'm good, how are you","every thing is good","i am very good, thanks"]
ResponseMessageList3 = ["i am at your srvice master","tell me your command master","tell your order master","i am under your command"]

num = 1

def assistantVoice(output):
    global num
    num += 1
    print("Robot: ",output)

    tospeak = gTTS(text = output , lang="en",slow=False)

    file = str(num)+".mp3"
    tospeak.save(file)

    playsound.playsound(file,True)
    os.remove(file)

def audioRecognizer():
    speech = sr.Recognizer()
    #audio = ''

    with sr.Microphone() as source:
        print("say your command: ")
        audio = speech.listen(source)#phrase_time_limit=15
        text = ''
        #print("stop.")

        try:
            text = speech.recognize_google(audio,language="en-US")
            print("your command: ",text)
            #return text

        except:
            #assistantVoice("i can't hear your, try again")
            print("i'm waiting for your command.")
    return text


def action(input_command):
    try:
        if "turn off" in input_command or "off" in input_command:
            light.write(0)
            assistantVoice("ligh is off.")

        elif "turn on" in input_command or "on" in input_command:
            light.write(1)
            assistantVoice("light is on")

        elif "left" in input_command or "left side" in input_command:
            robotHead.write(180)

        elif "right" in input_command or "right side" in input_command:
            robotHead.write(0)

        elif "who is" in input_command or "master" in input_command:
            assistantVoice("my master is mohammadreza sharifi.")

        elif "what time" in input_command:
            assistantVoice(str(time))

        elif "thank you" in input_command:
            assistantVoice("you're welcome master.")

        elif "how are you" in input_command or "how do you do" in input_command:
            responsemessage2 = random.choices(ResponseMessageList2)
            assistantVoice(str(responsemessage2))

        elif "give me" in input_command or "five" in input_command:
            assistantVoice("ok master.")
            rightElbow.write(110)

        elif "look" in input_command or "at me" in input_command:
            robotHead.write(90)
            responsemessage3 = random.choices(ResponseMessageList3)
            assistantVoice(str(responsemessage3))

        elif "hands" in input_command or "up" in input_command:
            rightElbow(120)
            leftElbow(120)

        elif "hands" in input_command or "down" in input_command:
            rightElbow(10)
            leftElbow(10)

        elif "what is" in input_command or "temperature" in input_command:
            temperature = str(temp)
            assistantVoice(f"The temperature is {temperature} degrees Celsius ")

        elif "hello" in input_command or "hi" in input_command:
            responsemessage = random.choices(ResponseMessageList)
            assistantVoice(str(responsemessage))

        else:
            pass

    except:
        assistantVoice("i can't handle your command!, do not have another order?")
        answer = audioRecognizer()
        if "yes" in str(answer):
            assistantVoice("i am at your service.")

#if __name__ == "__main__":
#    assistantVoice("Hi there, i am robotic assistant. can i help you?")

while True:
    #assistantVoice("Hi there, i am robotic assistant. can i help you?")
    text = audioRecognizer().lower()

    analogValue = lm35pin.read()
    temp = (analogValue/1024.0)*500000

    if text == 0 :
        continue

    if "bye" in str(text) or "see you later" in str(text):
        assistantVoice("ok master, see you later.")
        break

    action(text)

robotHead.write(90)
rightElbow.write(0)
leftElbow.write(0)
