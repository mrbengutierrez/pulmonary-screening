#!/usr/bin/env python3


"""A demo of the Pulmonary Screen Voice Box"""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

import smtplib

def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print('successfully sent email')
        time.sleep(random.randrange(30,350))
    except Exception as e:
        print(e)



def screener():
    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    
    button.wait_for_press()
    recognizer = aiy.cloudspeech.get_recognizer()
    answers = {}

    aiy.audio.say('May I help you?')
    led.set_state(aiy.voicehat.LED.BLINK)
    recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
            
    aiy.audio.say('May I ask you a couple of questions?')   
    led.set_state(aiy.voicehat.LED.BLINK)
    recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('What is the patients weight in kilograms?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['weight']  =  recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient have a cough?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['cough'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient have nasal symptoms?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['nasal'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Has the patient had a fever?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['fever'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient experience breathlessness?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['breathless'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('On a scale of one to five, what is the degree of the patients breathlessness?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['breathless_level'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient experience chest pain?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['chest_pain']= recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient have a personal history of allergies?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['allergies_personal'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient have family history of allergies')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['allergies_family'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Has the patient been a smoker?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['smoker'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Has the patient been a tobacco chewer?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['tobacco'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('How many cigarettes does the patent smoke or consume per day?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['cigarettes_num'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Does the patient drink alcohol?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['alcohol'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('Has the patient regularly cooked with biomass?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['biomass'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    aiy.audio.say('What was the patients maximum peak flow meter reading in three trials in liters per min?')
    led.set_state(aiy.voicehat.LED.BLINK)
    answers['pfm'] = recognizer.recognize()
    led.set_state(aiy.voicehat.LED.OFF)
    
    for answer in answers:
            print(answer + ': '+ str(answers[answer]))

    for answer in answers:
        sub = ''
        sub += answer + ': ' + str(answers[answer]) + '\n'
    user = 'mitmobilelab'
    password = 'pwd'
    recipient = 'mitmobilelab@gmail.com'
    subject = 'TEST'
    body = 'sub'
    send_email(user,pwd,recipient,subject,body)




def main():
    screener()




if __name__ == '__main__':
    main()

