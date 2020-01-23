import random
import bcrypt
from Crypto.Cipher import AES
import shutil
import json
import os






class Protect:
    def __init__(self):
        self.n_max = 10
        self.encoding = 'utf8'
        self.asc = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        self.hex = '0123456789abcdef'

    def ascToDict(self,asc_string):
        asc_dict = {}
        for i,char in enumerate(asc_string):
            asc_dict[char] = i  
        return asc_dict

    def genRandomAscii(self,length):
        a = ''
        for _ in range(length):
            a += random.choice(self.asc)
        return a

    def genRandomHex(self,length):
        a = ''
        for _ in range(length):
            a += random.choice(self.hex)
        return a

    def encrypt(self,key,iv,text):
        E = AES.new(key,AES.MODE_CBC,iv)
        output_length = 256
        delta_length = output_length - len(text)
        padded_text = text + self.genRandomAscii(delta_length)
        encrypted_text = E.encrypt(padded_text)
        return encrypted_text

    def decrypt(self,key,iv,encrypted_text):
        D = AES.new(key,AES.MODE_CBC,iv)
        result = D.decrypt(encrypted_text).decode()
        return result

    def encode(self,secret):
        asc_scrambled = ''.join(random.sample(self.asc,len(self.asc)))
        asc_dict = self.ascToDict(asc_scrambled)
        
        n = random.randint(1,self.n_max)
        s = ''
        for char in secret:
            loc = asc_dict[char] + n
            if loc >= len(asc_scrambled):
                loc -= len(asc_scrambled)
            s += asc_scrambled[loc]
        
        double = asc_scrambled + s
        key = self.genRandomHex(32)
        iv = self.genRandomHex(16)
        encrypted_text = self.encrypt(key,iv,double)
        salt = bcrypt.gensalt(4)
        hashed = bcrypt.hashpw(secret.encode(self.encoding),salt)
        #hashed = self.hashSecret(s)
        return (encrypted_text,key,iv,hashed)
        
    def decode(self,encrypted_text,key,iv,hashed):
        text = self.decrypt(key,iv,encrypted_text)
        new_asc = text[:len(self.asc)]
        new_s = text[len(self.asc):]
        print('len(new_s) = ' + str(len(new_s)))
        asc_dict = self.ascToDict(new_asc)
        for n in range(1,self.n_max+1):
            temp_s = ''
            for char in new_s:
                loc = asc_dict[char] - n
                if loc < 0:
                    loc += len(new_asc)
                temp_s += new_asc[loc]
                if bcrypt.checkpw(temp_s.encode(self.encoding),hashed):
                    return temp_s
        return False
    

        
            
            
                    
                    
            
            
        
    

def main():
    P = Protect()
    pwd = 'CAT IN THE HAT'
    #P.storeSecret(pwd,'pwd folder',10)
    #print('len(pwd) = ' + str(len(pwd)))
    x,y,w,z = P.encode(pwd)
    #print('x = ' + str(x))
    #print('y = ' + str(y))
    #print('w = ' + str(w))
    #print('z = ' + str(z))
    #print('P.encode(pwd): ' + str(x))
    d = P.decode(x,y,w,z)
    #print('len(decoded) = ' + str(d))
    print('P.decode(c): ' + str(d))
    #key = P.genRandomHex(32)
    #iv = P.genRandomHex(16)
    #print('iv = ' + str(iv))
    #f = P.encrypt(key,iv,'cat')
    #print('encrypt: ' + str(f))
    #g = P.decrypt(key,iv,f)
    #print('decrypt: ' + str(g))
    
    

if __name__ == '__main__':
    main()
