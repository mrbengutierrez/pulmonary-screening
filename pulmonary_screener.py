#!/usr/bin/env python3
import secret_saver as decoder

"""A demo of the Pulmonary Screen Voice Box"""

import aiy.audio # for google voicebox
import aiy.cloudspeech # for google voicebox
import aiy.voicehat # for google voicebox
#import bcrypt # pip install bcrypt, for salting passwords
import smtplib # for sending emails
import time # for emails (maybe not necessary)
import datetime # for keeping track of the date
import os, sys # wifi

def storePassword(filename):
    """Saves password into filename"""
    # Not implemented
    pass

def extractPassword(filenames):
    """Extracts password from filename"""
    # Not implemented
    pass
    
    
    
    
def wordsInString(word_list,string):
    """Checks if any words in word_list are in string"""
    for word in word_list:
        if word in string:
            return True
        return False
        
def boolToInt(boolean): 
    """Returns 1 if boolean is True, else returns 0"""
    if boolean == True:
        return 1
    return 0
    
def getIntsInString(string):
    """Returns a list of integers in string"""
    int_list = []
    int_flag = False
    curr = ''
    for i,char in enumerate(string):
        try:
            curr += str(int(char))
            if i == len(string) - 1:
                int_list.append(int(curr))
        except ValueError:
            if curr != '':
                int_list.append(int(curr))
                curr = ''
    return int_list

def isOneIntInString(string):
    "Returns True if only one integer in string"""
    if len(getIntsInString(string)) == 1:
        return True
    return False

def isIntInString(string):
    """Returns True if integer in string"""
    if len(getIntsInString(string)) > 0:
        return True
    return False
        
def getIntInString(string):
    """Returns first int in string"""
    return getIntsInString(string)[0]    

def isValidRange(string,lower_bound,upper_bound):
    """Returns True if first integer in string is inbetween lower_bound and upper_bound"""
    if not isIntInString(string):
        return False
    integer = getIntInString(string)
    if integer >= lower_bound and integer <= upper_bound:
        return True
    return False
    
def sendEmail(user, pwd, recipient, subject, body):
    """Sends an email to user. Return True if email """
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    attempts = 3
    for _ in range(attempts):
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
            time.sleep(1) # Maybe not necessary
            print('Successfully sent email')
            return True
        except Exception as e:
            print(e)
    return False        
    
def getDate():
    """Returns a string of the current date"""
    tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M") + ' ' + str(tz_string)
    
    
def connectWifi():
    pass
    
class Screener():
    def __init__(self):
        self.button = aiy.voicehat.get_button()
        self.led = aiy.voicehat.get_led()
        aiy.audio.get_recorder().start()
        self.recognizer = aiy.cloudspeech.get_recognizer()
        self.affirmative = ['yes','absolutely','yea','ok','affirmative','aye','yup','yep','yip','sure','totally','right','roger','amen']
        self.negative = ['no','nix','nay','nah','negative','veto']
        self.say = aiy.audio.say
        # First time initialization
        self.say('Hi, I am your personal health assistant. Press the button if you are ever feeling sick.')

        return
    
    def waiting(self):
        """Continously waits for user to press button, asks user questions when pressed"""
        while(True):
            self.button.wait_for_press()
            if self.askInitialQuestions() == True:
                report = self.askRespiratoryQuestions()
                #report = self.askTestQuestions() # TESTING
                self.printReport(report,processed=False)
                self.printReport(report,processed=False)
                self.sendReport(report)

           
    def askInitialQuestions(self):
        """Asks patient intial screening questions, returns True if patient has respiratory symptoms"""
        answer = self.askQuestion('Hi, may I help you? Are you feeling sick today?')
        if self.isAffirmative(answer):
            answer = self.askQuestion('Are you experiencing any respiratory symptoms?')
            if self.isAffirmative(answer):
                return True
            else:
                self.say('Sorry at this time I am only able to help with respiratory problems. Please consult your primary care doctor')
        elif 'setting' in answer or 'config' in answer: # change settings if user says 'settings' or 'configuration'
            print('answer = ' + str(answer))
            self.setConfiguration()
        else: 
            self.say('Ok, no problem. Feel free to let me know if you are feeling sick')
        return False
            
    def setConfiguration(self):
        """Sets configuration settings for screen"""
        answer = self.askQuestion('Would you like to set the wifi settings?')
        if self.isAffirmative(answer):
            self.say('Sorry, cannot change the wifi settings.')
        self.say('Done changing the wifi settings.')
        return            
        
    def askQuestion(self,question,conditions=[]):
        """Asks question over speaker, returns answer as string.
            question (string): Question to be asked
            conditions (list of functions): Conditions to be put on answer.
        """
        attempts = 5 # Number of times to attempt asking the question, before restarting the program?
        for _ in range(attempts):
            self.say(question)
            self.led.set_state(aiy.voicehat.LED.BLINK)
            answer  =  self.recognizer.recognize()
            self.led.set_state(aiy.voicehat.LED.OFF)
            print('answer = ' + str(answer))
            if answer != None:
                conditions_met = True
                for condition_tuple in conditions:
                    condition = condition_tuple[0]
                    args = condition_tuple[1]
                    if condition(answer,*args) == False:
                        conditions_met = False
                if conditions_met == True:
                    return answer
                self.say('Could you try answering again? If you do not know the answer to the question, give your best estimate')
            else:
                self.say('Sorry, I did not understand you correctly.')
        # restart from the beginning
        self.say('Sorry, I am having trouble understanding you. Lets start from the beginning.')
        self.askInitialQuestions()
    
    def isAffirmative(self,answer):
        """Checks if answer is affirmative"""
        return wordsInString(self.affirmative,answer)      
                    
            
    def askTestQuestions(self):
        """ To test faster"""
        questions = {} # format questions[var] = question
        unprocessed_answers = {} # format answers[var] = unprocessed answer
        processed_answers = {} # format answers[var] = processed answer
        labels = {} # format labels[var] = label
        order = [] # formating order[i] = var

        key = 'name'
        questions[key] = 'What is your name?'
        labels[key] = "Patient's Name"
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = answer
        
        key = 'weight'
        questions[key] = 'What is your weight in kilograms?'
        labels[key] = 'Weight (kg)'
        order.append(key)
        answer = self.askQuestion(questions[key],conditions=[isIntInString])
        unprocessed_answers[key] = answer
        processed_answers[key] = getIntInString(answer) 
        
        key = 'breathless'
        questions[key] = 'Are you experiencing breathlessness?'
        labels[key] = 'Experiences Breathlessness'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
        
        return [questions,unprocessed_answers,processed_answers,labels,order]

    def askRespiratoryQuestions(self):
        """Asks patient a list of respiratory questions. Returns tuple(questions,answers,labels,order)
            
            OUTPUT:
            tuple( 
                questions (dict): questions asked to patient
                answers (dict): patient answers
                labels (dict): label for questions
                order (dict): order questions were asked
                )
        """
            
        questions = {} # format questions[var] = question
        unprocessed_answers = {} # format answers[var] = unprocessed answer
        processed_answers = {} # format answers[var] = processed answer
        labels = {} # format labels[var] = label
        order = [] # formating order[i] = var

        key = 'name'
        questions[key] = 'What is your name?'
        labels[key] = "Patient's Name"
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = answer
        
        key = 'sex'
        questions[key] = 'Are you male or female?'
        labels[key] = "Patient's Sex"
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer 
        if wordsInString(['female','woman','girl','lady'],answer):
            processed_answers[key] = 0
        else:
            processed_answers[key] = 1 
        
        key = 'age'
        questions[key] = 'How old are you?'
        labels[key] = 'Age'
        order.append(key)
        answer = self.askQuestion(questions[key],conditions=[(isIntInString,[])])
        unprocessed_answers[key] = answer
        processed_answers[key] = getIntInString(answer)      
        
        key = 'weight'
        questions[key] = 'What is your weight in kilograms?'
        labels[key] = 'Weight (kg)'
        order.append(key)
        answer = self.askQuestion(questions[key],conditions=[(isIntInString,[])])
        unprocessed_answers[key] = answer
        processed_answers[key] = getIntInString(answer) 
        
        key = 'cough'
        questions[key] = 'Do you have a cough?'
        labels[key] = 'Cough'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'nasal'
        questions[key] = 'Do you have any nasal symptoms?'
        labels[key] = 'Nasal Symptoms'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'fever'
        questions[key] = 'Do you have a fever?'
        labels[key] = 'Fever'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'breathless'
        questions[key] = 'Are you experiencing breathlessness?'
        labels[key] = 'Experiences Breathlessness'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'breathless_level'
        questions[key] = 'On a scale of one to five from light to severe, what is the degree of the of your breathlessness?'
        labels[key] = 'Breathlessness Level (1=Light, 5=Severe)'
        order.append(key)
        if self.isAffirmative(unprocessed_answers['breathless']):
            answer = self.askQuestion(questions[key],conditions=[(isValidRange,[0,5])])
            unprocessed_answers[key] = answer
            processed_answers[key] = getIntInString(answer)
        else:
            unprocessed_answers[key] = 'Question Not Asked'
            processed_answers[key] = 1
                        
        key = 'chest_pain'
        questions[key] = 'Do you experience chest pain?'
        labels[key] = 'Experiences Chest Pain'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'allergies_personal'
        questions[key] ='Do you have a personal history of allergies?'
        labels[key] = 'Personal History of Allergies'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'allergies_family'
        questions[key] ='Do you have a family history of allergies'
        labels[key] = 'Family History of Allergies'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'smoker'
        questions[key] = 'Have you been a smoker?'
        labels[key] = 'History of Smoking'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                
        key = 'cigarettes'
        questions[key] = 'How many cigarettes do you smoke or consume per day?'
        labels[key] = 'Number of Cigarettes per Day'
        order.append(key)
        if self.isAffirmative(unprocessed_answers['smoker']):
            answer =  self.askQuestion(questions[key],conditions=[(isIntInString,[])])
            unprocessed_answers[key] = answer
            processed_answers[key] = getIntInString(answer)
        else:
            unprocessed_answers[key] = 'Question Not Asked'
            unprocessed_answers[key] = 0
                        
        key = 'tobacco'
        questions[key] = 'Do you ever chew tobacco?'
        labels[key] = 'History of Tobacco'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'alcohol'
        questions[key] = 'Do you drink alcohol?'
        labels[key] = 'History of Alcohol Consumption'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                        
        key = 'biomass'
        questions[key] ='Do you use a fire stove to cook food?'
        labels[key] = 'Cooks with Biomass'
        order.append(key)
        answer = self.askQuestion(questions[key])
        unprocessed_answers[key] = answer
        processed_answers[key] = boolToInt(self.isAffirmative(answer))
                                
        key = 'pfm'
        questions[key] ='What is your maximum peak flow meter reading in three trials in liters per min?'
        labels[key] = 'Maximum Peak Flow Meter Reading (liters/min)'
        order.append(key)
        answer = self.askQuestion('Do you have a peak flow meter available?')
        if self.isAffirmative(answer):
            self.say('Please take three peak flow meter readings now.')
            time.sleep(20)
            answer = self.askQuestion(questions[key],conditions=[(isIntInString,[])])
            unprocessed_answers[key] = answer
            processed_answers[key] = getIntInString(answer)
        else:
            unprocessed_answers[key] = 'No peak flow meter available.'
            processed_answers[key] = 450 # Average pfm?
        
        self.say('Thank you. I will send off this information to be reviewed.')
        return [questions,unprocessed_answers,processed_answers,labels,order]
        
    def printReport(self,report,processed=False):
        """Prints the patients report to the terminal"""
        #questions = report[0]
        unprocessed_answers = report[1]
        processed_answers = report[2]
        labels = report[3]
        order = report[4]
        if processed == True:
            answers = processed_answers
        else:
            answers = unprocessed_answers
        
        print()
        if processed:
            print('--- Patient Report (Processed Answers) ---')
        else:
            print('--- Patient Report (Raw Answers) ---')
        print('Date and Time: ' + getDate())
        for i,key in enumerate(order):
            print( str(labels[key]) + ': ' + str(answers[key]))
        print('--- End Patient Report ---')
        print()
        return
    
    def sendReport(self,report,processed=False):
        """Sends the patients report by email. Returns True if email sent successfully, False otherwise"""
        #questions = report[0]
        unprocessed_answers = report[1]
        processed_answers = report[2]
        labels = report[3]
        order = report[4]
        if processed == True:
            answers = processed_answers
        else:
            answers = unprocessed_answers
        
        body_list = []
        body_list.append('Date and Time: ' + getDate() + '\n')
        for i,key in enumerate(order):
            body_list.append( str(labels[key]) + ': ' + str(answers[key]) +'\n' )
        body = ''.join(body_list) # O(chars in body_list) time

        user = 'mitmobilelab@gmail.com'
        t1 = time.time()
        P = decoder.Protect()
        pwd = P.getSecret('mitmobilelab')
        print('Time to get password: ' + str(time.time() - t1)[0:6] + ' sec')
        recipient = 'mitmobilelab@gmail.com'
        subject = 'Patient Report for ' + str(answers['name']) 
        #body = body
        if sendEmail(user,pwd,recipient,subject,body) == True:
            print('Report sent successfully')
            return True
        print('Report failed to send')
        return False
        #return sendEmail(user,pwd,recipient,subject,body)

def main():
    time.sleep(10) # Wait 10 secs for wifi to connect
    S = Screener()
    S.waiting()




if __name__ == '__main__':
    main()


