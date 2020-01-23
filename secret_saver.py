import random
import bcrypt
from Crypto.Cipher import AES
import shutil
import pickle
import os






class Protect:
    def __init__(self):
        self.n_max = 3
        self.encoding = 'utf8'
        self.asc = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        self.hexs = '0123456789abcdef'
        self.subdir = 'security/'

    def ascToDict(self,asc_string):
        """Converts an ascii string to a dictionary"""
        asc_dict = {}
        for i,char in enumerate(asc_string):
            asc_dict[char] = i  
        return asc_dict

    def genRandomAscii(self,length):
        """Generates a random ascii string of a particular length"""
        a = ''
        for _ in range(length):
            a += random.choice(self.asc)
        return a

    def genRandomHex(self,length):
        """Generates a random hex number string of a particular length"""
        a = ''
        for _ in range(length):
            a += random.choice(self.hexs)
        return a

    def encrypt(self,key,iv,text):
        """Returns an ecryption of text"""
        E = AES.new(key,AES.MODE_CBC,iv)
        output_length = 256
        delta_length = output_length - len(text)
        padded_text = text + self.genRandomAscii(delta_length)
        encrypted_text = E.encrypt(padded_text)
        return encrypted_text

    def decrypt(self,key,iv,encrypted_text):
        """decrypts and encrypted text"""
        D = AES.new(key,AES.MODE_CBC,iv)
        result = D.decrypt(encrypted_text).decode()
        return result

    def encode(self,secret):
        """returns an encoded secret"""
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
        """Decodes an encoded text into a string"""
        text = self.decrypt(key,iv,encrypted_text)
        new_asc = text[:len(self.asc)]
        new_s = text[len(self.asc):]
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
    
    
    def storeSecret(self,secret,folder,num_files=2):
        """Stores secret in subdirectory folder, stores secret across number of files"""
        folder = self.subdir + folder
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
        encrypted_list = []
        key_list = []
        iv_list = []
        hashed_list = []
        with open(self.subdir + 'words.txt','r') as f:
            content = f.readlines()
        words = [x.strip() for x in content]
        for i in range(num_files):
            if i == 0:
                pwd1 = secret
            else:
                int_range = 1000;
                pwd1 = random.choice(words) + str( random.randint(0,int_range) )
                pwd2 = str( random.randint(0,int_range) ) + random.choice(words)
                x2,y2,w2,z2 = self.encode(pwd2)
            x1,y1,w1,z1 = self.encode(pwd1)
            encrypted_list.append(x1)
            key_list.append(y1)
            iv_list.append(w1)
            if i == 0:
                hashed_list.append(z1)
            else:
                hashed_list.append(z2)
        
        random.shuffle(encrypted_list)
        random.shuffle(key_list)
        random.shuffle(iv_list)
        random.shuffle(hashed_list)
        
        for i in range(num_files):
            x = encrypted_list[i]
            y = key_list[i]
            w = iv_list[i]
            z = hashed_list[i]
            output_list = [x,y,w,z]
            file_name = str(i) + str(self.genRandomHex(10)) + '.json'
            file_name = folder + '/' + file_name
            pickle.dump(output_list,open(file_name,'wb'))

    def getSecret(self,folder):
        """returns secret string located in subdirectory folder"""
        folder = self.subdir + folder
        encrypted_list = []
        key_list = []
        iv_list = []
        hashed_list = []
        file_list = []
        for f in os.listdir(folder):
            if f.endswith('.json'):
                file_list.append(folder + '/' + f)
        for f in file_list:
            x,y,w,z = pickle.load(open(f,'rb'))
            encrypted_list.append(x)
            key_list.append(y)
            iv_list.append(w)
            hashed_list.append(z)
        
        for encryption in encrypted_list:
            for key in key_list:
                for iv in iv_list:
                    for hashed in hashed_list:
                        try:
                            secret = self.decode(encryption,key,iv,hashed)
                            if secret != False:
                                return secret
                        except (UnicodeDecodeError,KeyError,ValueError):
                            pass
        return False
            
        
            
        
            
            
                    
                    
            
            
        
    

def main():
    P = Protect()
    pwd = input('Enter password you would like to store: ')
    folder = input('What folder would you like to store password: ' )
    P.storeSecret(pwd,folder,2)
    import time
    t1 = time.time()
    secret = P.getSecret(folder)
    print('Time to retrieve password: ' + str(time.time() - t1)[0:6] + ' sec')
    print('Secret stored as: ' + str(secret))
    
    
    

if __name__ == '__main__':
    main()
