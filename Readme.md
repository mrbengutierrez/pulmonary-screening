

# Pulmonary Voice Project #

This project was for the MIT Mobile attempting to make a Pulmonary Screening device. 
The device used the google voice kit.

## Clone Code ##
git clone https://github.com/mrbengutierrez/pulmonary_screening.git

## Step 1: Raspberry Pi Setup (Automatic) ##
* sudo bash /home/pi/pulmonary-voice/initialization.sh

## Step 1: Raspberry Pi Setup (Manual) ##

** Upgrade pi **

* sudo apt-get update

* sudo apt-get dist upgrade

* sudo pip3 install --upgrade 

** Update time **

* sudo apt-get install ntp

** Install python libraries **

* sudo pip3 install scikit-learn

* sudo pip3 install bcrypt

* sudo pip3 install -U numpy

* sudo pip3 install scipy 

* sudo apt-get install libatlas-base-dev

## Step 2: Raspberry Pi Setup (Manual)

** Download google api json files **

* rename to assistant.json and cloud_speech.json

* move to /home/pi folder

* copy json files also to /root

## Example Report

Date and Time: 2018-10-06 11:57 EDT
Patient's Name: Bob
Patient's Sex: male
Age: 27 years old
Weight (kg): 170 lb
Cough: yes I do
Nasal Symptoms: yes I do
Fever: I have
Experiences Breathlessness: I am yeah
Breathlessness Level (1=Light, 5=Severe): 3
Experiences Chest Pain: yeah
Personal History of Allergies: no
Family History of Allergies: no I do not
History of Smoking: yes
Number of Cigarettes per Day: 3
History of Tobacco: yes
History of Alcohol Consumption: yes
Cooks with Biomass: yes
Maximum Peak Flow Meter Reading (liters/min): 432
