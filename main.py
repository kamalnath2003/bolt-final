import subprocess
import webbrowser
import pyjokes
import speech_recognition as sr
import pyttsx3
import pywhatkit
from win32 import win32gui,win32console
import wolframalpha
import datetime
import wikipedia
from gtts import gTTS
import requests
import os
from googletrans import  Translator
import cv2 as cv
import pytesseract
import operator
from playsound import playsound
import  numpy as np
import sys
import pandas as pd
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
from sklearn.preprocessing import  MinMaxScaler
from keras.models import Sequential
from keras.layers import  Dense, Dropout, LSTM
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.config import Config

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
cap = None
ret = None
frame = None
key = None
cap = cv.VideoCapture(0)

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '768')


MASTER = "ADAM"
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
translator = Translator()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    print(hour)

    if hour>=0 and hour <12:
        talk("good morning" + MASTER)

    elif hour>=12 and hour<18:
        talk("good afternoon" + MASTER)

    else:
        talk("good Evening" + MASTER)

    talk("i am your assistant. How may I help you?")

def ting():
    playsound("ting.mp3")



def read():
    while True:
        ret, frame = cap.read()
        cv.imshow('Window', frame)
        text = pytesseract.image_to_string(frame)
        print(text)
        talk(text)
        key = cv.waitKey(2000)
        if key == (ord('q')):
            break

    cv.destroyAllWindows()
    cap.release()

class Root(BoxLayout):
    pass


class RecordButton(Button):


    # String Property to Hold output for publishing by Textinput
    output = StringProperty('')



    def record(self):
        ting()
        # GUI Blocking Audio Capture
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

        try:
            value = listener.recognize_google(voice)
            self.output = "You said \"{}\"".format(value)



            if 'bolt' or 'bold' or 'gold' or 'v' or 'bol' or 'board' or 'cold' in command:
                command = command.replace('bolt', '').replace('bold', '').replace('gold','').replace('v','').replace('bol','').replace('board','').replace('cold','')
                self.output = "You said \"{}\"".format(value)
                self.output = command
                print(command)

            else:
                print('my name is bolt tell you command after saying my name Sir')
                talk('my name is bolt tell you command after saying my name Sir')
            if 'play' in command:
                song = command.replace('play', '')
                value = listener.recognize_google(voice)
                talk('playing  ' + song)
                self.output = "You said \"{}\"".format(value)  + ':  Playing  ' + song
                pywhatkit.playonyt(song)

            elif 'hello' in command:
                print('hello how can i help you ??')
                talk('hello, how can i help you ??')
                self.output = "You said \"{}\"".format(value)

            elif 'how are you' in command:
                print('Im fine sir how are you ' )
                talk('Im fine sir how are you')
                self.output = "You said \"{}\"".format(value)

            elif 'translate ' in command:
                engine.setProperty('rate', 170)
                talk('ill ask my sister to translate wait sir')
                sentence = command.replace('translate', '')
                out = translator.translate(sentence, dest='ta')
                tts = gTTS(out.text, lang='ta')
                print(out.text)
                tts.save("audio.mp3")
                playsound("audio.mp3")
                self.output ="You said \"{}\"".format(value) +'ill ask my sister thrisha to translate wait sir'+ out.text



            elif 'take note' in command:
                talk('enter the things you want to write as handwriting sir')
                text = input('enter the text: ', )

                pywhatkit.text_to_handwriting(text, "demo1.png")
                os.startfile("demo1.png")

            elif 'stock' in command:
                talk('select the date and desired company to plot the graph')
                self.output = "You said \"{}\"".format(value) + 'select the date and desired company to plot the graph'
                os.startfile("stock_visualizer.pyw")



            elif 'in english' in command:
                engine.setProperty('rate', 170)
                talk('ill ask my sister thrisha to translate wait sir')
                command = listener.recognize_google(voice, language="ta-IN")
                sentence = command.replace('in english', '')
                out = translator.translate(sentence, dest='en')
                tts = gTTS(out.text, lang='en')
                tts.save("audio.mp3")
                playsound("audio.mp3")




            elif "send whatsapp message" in command:
                talk('On what number should I send the message sir? Please enter in the console: ')
                self.output = 'On what number should I send the message sir? Please enter in the console: '
                number = input("Enter the number: ")
                talk("What is the message sir?")
                self.output = 'What is the message sir?'
                message = takeCommand().lower()
                send_whatsapp_message(number, message)
                talk("I've sent the message sir.")


            elif 'time' in command:
                time = datetime.datetime.now().strftime('%H:%M:%p')
                print(time)
                self.output = "You said \"{}\"".format(value) + ' \n current time is :' + time
                talk('current time is ' + time)

            elif "weather" in command:
                api_key = "8ef61edcf1c576d65d836254e11ea420"
                base_url = "https://api.openweathermap.org/data/2.5/weather?"
                city_name = command.replace('weather in','')
                talk("finding sir.....")
                self.output = "finding sir"
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    talk(" Temperature in kelvin unit is " +
                          str(current_temperature) +
                          "\n humidity in percentage is " +
                          str(current_humidiy) +
                          "\n description  " +
                          str(weather_description))
                    print(" Temperature in kelvin unit = " +
                          str(current_temperature) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))
                    self.output = (" Temperature in kelvin unit = " +
                          str(current_temperature) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))

                else:
                    talk(" City Not Found ")
                    self.output = ("City Not found try again")



            elif 'who is' in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 1, auto_suggest=False)
                print(info)
                self.output = "You said \"{}\"".format(value) + '\n' + info
                talk(info)

            elif 'alarm' in command:
                hide  = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hide , win32console.SW_SHOW)
                talk('tell the time to set alarm')
                time = input(": Enter The Time:",)
                self.output = "You said \"{}\"".format(value) + '\n' + 'enter the time in the console only'

                while True:
                    Time_Ac = datetime.datetime.now()
                    now = Time_Ac.strftime("%H:%M:%S")

                    if now == time:
                        talk("Time to wake up")
                        playsound('C:/Users/kamal/Downloads/larm-sound-21949.mp3')
                        talk("Alarm closed!")

                    elif now>time:
                        break

            elif 'are you' in command:
                info = 'Im bolt im from your computer i was born in 2022 and made by few fellow so called engineers in a college called jeppiar institute of technology you should call me bolt or else i wont anwer your question'
                self.output = "You said \"{}\"".format(value) + '\n' + info
                print(info)
                talk(info)

            elif 'open' in command:
                app = command.replace('open', '')
                if 'chrome' in app:
                    subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

                if 'whatsapp' in app:
                    subprocess.Popen("C:\\Users\\kamal\\AppData\\Local\\WhatsApp\\WhatsApp.exe")
                if 'edge' in app:
                    subprocess.Popen("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")

            elif 'go to youtube' in command:
                webbrowser.open("https://www.youtube.com/", new=2)
                self.output = "You said \"{}\"".format(value) + '\n' + 'opening youtube sir '
                talk("opening youtube sir")

            elif 'go to google' in command:
                webbrowser.open("https://www.google.com/", new=2)
                self.output = "You said \"{}\"".format(value) + '\n' + 'opening google sir '
                talk("opening google sir")

            elif 'go to facebook' in command:
                webbrowser.open("https://www.facebook.com/", new=2)
                self.output = "You said \"{}\"".format(value) + '\n' + 'opening dacebook sir '
                talk("opening facebook sir")


            elif 'close' in command:
                if 'browser' in command:
                    os.system("taskkill/im msedge.exe")
                elif 'you' in command:
                    os.system("taskkill/im python.exe")
                elif 'chrome' in command:
                    os.system("taskkill/im chrome.exe")
                elif 'whatsapp' in command:
                    os.system("taskkill/im whatsapp.exe")
                elif 'discord' in command:
                    os.system("taskkill/im discord.exe")

            elif 'can you' in command:
                engine.setProperty('rate', 200)
                info = 'SINCE IM JUST A PROTOTYPE I CAN ONLY TAKE FEW COMMANDS SUCH AS: \n ' \
                       'PLAY SOMETHING ON YOUTUBE \n' \
                       'ASK ME ABOUT SOMETHING \n' \
                       'ASK ME ABOUT SOMEONE  \n' \
                       'TELL THE TIME \n' \
                       'WRITE IN HANDWRITING FONT' \
                       'SHOW STOCK PRICES' \
                       'TRANSLATE FROM TAMIL TO ENGLISH' \
                       'TRANSLATE FROM ENGLISH TO TAMIL' \
                       'SET ALARM \n' \
                       'GOOGLE SOMETHING \n' \
                       'CALCULATE NUMBERS \n' \
                       'TELL PYTHON RELATED  JOKES  \n' \
                       'SEND MESSAGE IN WHATSAPP \n' \
                       'OPEN WEBSITES LIKE GOOGLE,FACEBOOK,YOUTUBE \n' \
                       'OPEN AND KILL APPS LIKE CHROME,EDGE\n' \
                        'TRANSLATE FROM ENGLISH TO TAMIL\n' \
                       'FIND LOCATION OF A PLACE' \
                        'AND MUCH MORE...'
                self.output = "You said \"{}\"".format(value) + '\n' + info
                print(info)
                talk(info)

            elif 'google' in command:
                import wikipedia as googleScrap
                search = command.replace('google', '')
                talk('this is what i found in web sir')
                pywhatkit.search(search)
                result = googleScrap.summary(search,2)
                self.output = "You said \"{}\"".format(value) + '\n' + result
                print(result)
                talk(result)

            elif 'guess' in command:
                talk('Enter the ticker of company:')
                company = input('Enter the ticker of company:')
                # ai predict

                start = dt.datetime(2012, 1, 1)
                end = dt.datetime(2020, 1, 1)

                data = web.DataReader(company, 'yahoo', start, end)

                # Prepare Data
                scaler = MinMaxScaler(feature_range=(0, 1))
                scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

                prediction_days = 60

                x_train = []
                y_train = []

                for x in range(prediction_days, len(scaled_data)):
                    x_train.append(scaled_data[x - prediction_days:x, 0])
                    y_train.append(scaled_data[x, 0])

                x_train, y_train = np.array(x_train), np.array(y_train)
                x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

                # Built the model
                model = Sequential()

                model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
                model.add(Dropout(0.2))
                model.add(LSTM(units=50, return_sequences=True))
                model.add(Dropout(0.2))
                model.add(LSTM(units=50))
                model.add(Dropout(0.2))
                model.add(Dense(units=1))
                model.compile(optimizer='adam', loss='mean_squared_error')
                model.fit(x_train, y_train, epochs=25, batch_size=32)

                # load text data
                test_start = dt.datetime(2020, 1, 1)
                test_end = dt.datetime.now()

                test_data = web.DataReader(company, 'yahoo', test_start, test_end)
                actual_prices = test_data['Close'].values

                total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

                model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
                model_inputs = model_inputs.reshape(-1, 1)
                model_inputs = scaler.transform(model_inputs)

                x_test = []

                for x in range(prediction_days, len(model_inputs)):
                    x_test.append(model_inputs[x - prediction_days:x, 0])

                x_test = np.array(x_test)
                x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

                prediction_prices = model.predict(x_test)
                prediction_prices = scaler.inverse_transform(prediction_prices)

                plt.plot(actual_prices, color="black", label=f"actual {company} Price")
                plt.plot(prediction_prices, color="green", label=f"predicted {company} Price")
                plt.title(f"{company} Share Price")
                plt.xlabel('Time')
                plt.ylabel(f"{company} Share price")
                plt.legend()
                plt.show()



            elif 'calculate' in command:
                print("calculating sir")
                talk("calculating sir")
                command = command.replace('calculate' , '')


                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        'plus': operator.add,
                        '-': operator.sub,
                        'minus': operator.sub,
                        'x': operator.mul,
                        'into': operator.mul,
                        'divided': operator.__truediv__,
                        'by': operator.__truediv__,
                        'Mod': operator.mod,
                        'mod': operator.mod,
                        '^': operator.xor,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                print('the answer is')
                talk('the answer is ')
                print(eval_binary_expr(*(command.split())))
                talk(eval_binary_expr(*(command.split())))


            elif 'joke' in command:
                joke = pyjokes.get_joke()
                self.output = "You said \"{}\"".format(value) + '\n' + joke
                print(joke)
                talk(joke)

            elif 'bye' in command:
                print('good bye, have a nice day !!')
                talk('good bye, have a nice day !!')
                sys.exit()

            elif 'thank you' in command:
                print("your welcome")
                talk('your welcome')

            elif 'stop' in command:
                print('good bye, have a nice day !!')
                talk('good bye, have a nice day !!')
                sys.exit()
            elif 'tata' in command:
                print('good bye, have a nice day !!')
                talk('good bye, have a nice day !!')
                sys.exit()
            elif 'locate ' in command:
                talk('locating ...')
                loc = command.replace('locate', '')
                if 'on map' in loc:
                    loc = loc.replace('on map', ' ')
                url = 'https://google.nl/maps/place/' + loc + '/&amp;'
                webbrowser.get().open(url)
                print('Here is the location of ' + loc)
                talk('Here is the location of ' + loc)

            elif 'on map' in command:
                talk('locating ...')
                loc = command.split(" ")
                print(loc[1])
                url = 'https://google.nl/maps/place/' + loc[1] + '/&amp;'
                webbrowser.get().open(url)
                print('Here is the location of ' + loc[1])
                talk('Here is the location of ' + loc[1])

            elif 'location of' in command:
                talk('locating ...')
                loc = command.replace('find location of', '')
                url = 'https://google.nl/maps/place/' + loc + '/&amp;'
                webbrowser.get().open(url)
                print('Here is the location of ' + loc)
                talk('Here is the location of ' + loc)


            elif 'geography' in command:
                talk('I can answer to computational and geographical questions and what question do you want to ask now')
                question = takeCommand()
                app_id = "R2K75H-7ELALHR35X"
                client = wolframalpha.Client('R2K75H-7ELALHR35X')
                res = client.query(question)
                answer = next(res.results).text
                talk(answer)
                print(answer)

            elif 'gmail' in command:
                print('opening gmail ...')
                talk('opening gmail..')
                webbrowser.open_new('https://mail.google.com/')

            elif "advice" in command or 'adice' in command:
                talk(f"Here's an advice for you, sir")
                advice = get_random_advice()
                talk(advice)
                talk("For your convenience, I am printing it on the screen sir.")
                print(advice)
                self.output = "For your convenience, I am printing it on the screen sir." + advice

            elif "read" in command:
                read()

            else:

                self.output = "You said \"{}\"".format(value) + '\n' + 'sorry sir i dont know the answer '
                talk('sorry sir i dont know the answer')
                print(' Here is what i found on the internet..')
                talk('Here is what i found on the internet..')
                search = 'https://www.google.com/search?q=' + command
                webbrowser.open(search)


        except sr.UnknownValueError:
            self.output = talk("Oops! Didn't catch that")
            takeCommand()

        except sr.RequestError as e:
            self.output = talk("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            takeCommand()




def talk(text):
    engine.say(text)
    engine.runAndWait()

def send_whatsapp_message(number, message):
    pywhatkit.sendwhatmsg_instantly(f"+91{number}", message)

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']




def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            talk("Pardon me, please say that again")
            return "None"
        return statement



class SpeechApp(App):
    def build(self):
        wishMe()

       # Calibrate the Microphone to Silent Levels
        print("A moment of silence, please...")
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(listener.energy_threshold))
        # Create a root widget object and return as root
        return Root()





if __name__ == '__main__':
    SpeechApp().run()

