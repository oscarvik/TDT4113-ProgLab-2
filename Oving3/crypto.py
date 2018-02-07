import random
import math
import re
from Oving3.crypto_utils import generate_random_prime, modular_inverse, blocks_from_text, text_from_blocks


#SUPERKLASSE PERSON
class Person:

    def __init__(self, cipher):
        self.cipher = cipher

    def set_key(self,key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cipher(self):
        return


#SUBKLASSE AV PERSON
class Sender(Person):

    def operate_cipher(self,text):
        self.decoded_text = text
        self.encoded_text = self.cipher.encode(text,self.key)
        return self.encoded_text


#SUBKLASSE AV PERSON
class Receiver(Person):

    def operate_cipher(self,text):
        self.encoded_text = text
        self.decoded_text = self.cipher.decode(text,self.key)
        return self.decoded_text

    # Genererer den private og offentlige nøkkelen i tupler, i henhold til RSAs oppførsel i oppgavebeskrivelsen
    def generate_key(self,bit):
        p1 = 0
        p2 = 0
        while p1 == p2:
            p1 = generate_random_prime(bit)
            p2 = generate_random_prime(bit)

        phi = (p1 - 1) * (p2 - 1)
        e = random.randint(3, phi-1)
        while modular_inverse(e,phi) == None:
            e = random.randint(3, phi-1)

        d = modular_inverse(e,phi)
        n = p1 * p2
        self.public_key = (n, e)
        #print("N: "+str(n)+" E: "+str(e))
        self.key = (n, d)
        #print("N: "+str(n)+" D: "+str(d))


#SUBKLASSE AV PERSON
class Hacker(Person):

    def __init__(self, dictionary,cipher):
        self.words = [line.rstrip('\n') for line in open(dictionary)]
        super().__init__(cipher)


    def brute_force(self, message):
        print("hacker 'fanger' opp meldingen: " + message)
        cipher = self.cipher
        possible_keys = cipher.possible_keys()
        for key in possible_keys:
            decoded = cipher.decode(message, key)
            decoded_lst = decoded.split(" ")
            decoded_stripped_lst = []
            for word in decoded_lst:
                stripped_word = word.strip(',') #fjerner det meste av 'not alphanumeric'
                decoded_stripped_lst.append(stripped_word)
            if self.search(decoded_stripped_lst):
                possible_answers = decoded_stripped_lst
                answer = ""
                for word in possible_answers:
                    answer += word+" "
                return answer
        return "No Match"

    def search(self, message):
        for word in message:
            if word.lower() not in self.words:
                return False
        return True


#SUPERKLASSE CIPHER
class Cipher:

    def __init__(self):
        self.alphabet = [chr(x) for x in range(32,127)]

    def encode(self, message, key):
        return

    def decode(self, message, key):
        return

    #verifiserer at input er lik output, mao. at krypteringen og dekryptering fungerer som det skal
    def verify(self,message,key):
        encoded = self.encode(message, key)
        decoded = self.decode(encoded,key)
        return message == decoded


#SUBKLASSE AV CIPHER
class Caesar(Cipher):

    def encode(self, message,key):
        kryptert = ""
        for element in message:
            new_key = (self.alphabet.index(element) + key) % 95
            kryptert += self.alphabet[new_key]
        return kryptert

    def decode(self, message,key):
        dekrypt = ""
        for element in message:
            new_key = (self.alphabet.index(element) - key) % 95
            dekrypt += self.alphabet[new_key]
        return dekrypt

    def possible_keys(self):
        return [x for x in range(0,95)]


#SUBKLASSE AV CIPHER
class Multi(Cipher):

    def encode(self, message, key):
        kryptert = ""
        for element in message:
            new_index = (self.alphabet.index(element) * key) % 95
            kryptert += self.alphabet[new_index]
        return kryptert

    def decode(self, message, key):
        dekrypt = "ugyldig nøkkel"
        new_index = modular_inverse(key,95)
        if new_index !=None:
            dekrypt = self.encode(message,new_index)
        return dekrypt

    def possible_keys(self):
        return [x for x in range(0,95)]


#SUBKLASSE AV CIPHER
class Affine(Cipher):

    def encode(self, message, key):
        multi = Multi()
        encoded_multi = multi.encode(message,key[0])

        caesar = Caesar()
        encoded_txt = caesar.encode(encoded_multi,key[1])
        return encoded_txt

    def decode(self, message, key):
        caesar = Caesar()
        decoded_txt_c = caesar.decode(message,key[1])

        multi = Multi()
        decoded_txt = multi.decode(decoded_txt_c,key[0])
        return decoded_txt

    def possible_keys(self):
        keys =[ x for x in range(0,95) if math.gcd(x,95) == 1]

        return [(x,y) for x in keys for y in range(0,95)]


#SUBKLASSE AV CIPHER
class Unbreakable(Cipher):

    def encode(self, message, key):
        index = 0
        kryptert = ""
        for element in message:
            new_index = (self.alphabet.index(element) + self.alphabet.index(key[index])) % 95
            kryptert += self.alphabet[new_index]
            if index < len(key)-1:
                index += 1
            else:
                index = 0
        return kryptert

    def possible_keys(self):
        return [line.rstrip('\n') for line in open('english_dict.txt')]

    def decode(self, message, key):
        new_key = ""
        for element in key:
            new_key += self.alphabet[(95 - self.alphabet.index(element)) % 95]
        index = 0
        dekrypt = ""
        for element in message:
            new_index = (self.alphabet.index(element) + self.alphabet.index(new_key[index])) % 95
            dekrypt += self.alphabet[new_index]
            if index < len(new_key)-1:
                index += 1
            else:
                index = 0
        return dekrypt


#SUBKLASSE AV CIPHER
class RSA(Cipher):

    def encode(self, message, key):
        binString = blocks_from_text(message,1)
        encoded = self.encode_nr(binString,key)
        return encoded

    def encode_nr(self,list,key):
        encoded_list = []
        for block in list:
            encoded_list.append(pow(block,key[1],key[0]))
        return encoded_list

    def decode(self, message, key):
        de_message = self.decode_nr(message,key)
        text = ""
        text += text_from_blocks(de_message,8)
        return text

    def decode_nr(self,list,key):
        decoded_list = []
        for block in list:
            decoded_list.append(pow(block, key[1], key[0]))
        return decoded_list

def main():
#Setter opp instanser av de forskjellige cipher-klassene
    caesar = Caesar()
    multi = Multi()
    affine = Affine()
    un = Unbreakable()
    rsa_krypt = RSA()

    message = "~HEI PYTHON"

#Caesar-cipher uten bruk av sender og reciever
    print("Caesar-kryptering:")
    print("Melding: "+message)
    x = caesar.encode(message,5)
    print("kryptert: "+x)
    y = caesar.decode(x,5)
    print("dekryptert: "+y)

#Multiplikasjons-cipher uten bruk av sender og reciever
    print("\nMultiplikator-kryptering:")
    print("Melding: "+message)
    b = multi.encode(message,3)
    print("kryptert: "+b)
    c = multi.decode(b,3)
    print("dekryptert: "+c)

#Affine cipher uten bruk av sender og reciever
    print("\nAffine-kryptering:")
    print("melding: "+message)
    w = affine.encode(message,(3,5))
    print("kryptert: "+w)
    e = affine.decode(w,(3,5))
    print("dekryptert: "+e)

#“Ubrytelige” cipher uten bruk av sender og reciever
    print("\n'Ubrytelig'-kryptering:")
    print("melding: "+message)
    y = un.encode(message, "PIZZA")
    print("kryptert: "+y)
    z = un.decode(y, "PIZZA")
    print("dekryptert: "+z+"\n")


#RSA kryptering med bruk av sender og reciever
    print("RSA-kryptering:")
    sender = Sender(rsa_krypt)
    reciever = Receiver(rsa_krypt)
    #reciever generer public og private key
    reciever.generate_key(8)
    #sender tilegnes recievers public key
    sender.set_key(reciever.public_key)
    print("melding: "+message)
    krypt = sender.operate_cipher(message)
    print("kryptert: " +str(krypt))
    dekrypt = reciever.operate_cipher(krypt)
    print("dekrypt: "+dekrypt)

#generell bruk av sender og reciever
    print("\nSender-Reciever test:")
    sender2 =  Sender(affine)
    sender2.set_key((3,5))
    reciever2 = Receiver(affine)
    reciever2.set_key((3,5))
    print("melding: "+message)
    krypt2 = sender2.operate_cipher(message)
    print("kryptert: "+krypt2)
    dekrypt2 = reciever2.operate_cipher(krypt2)
    print("dekryptert: "+dekrypt2)
    print("verify: "+str(affine.verify(message,(3,5))))

#test av hacker klassen
    print("\nHacker-test:")
    message2 = "This is a, test"
    ordbok = "english_dict.txt"
    hacker = Hacker(ordbok, un)
    krypt_txt = un.encode(message2,"hello")
    dekrypt_txt = hacker.brute_force(krypt_txt)
    print("klartekst: " + dekrypt_txt)


main()
#Sender- og Receiever-klasse er ikke ferdig implementert
