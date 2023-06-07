import math
import random
import numpy as np

class HillCipher(object):

    def __init__(self, block_size):
        self.block_size = block_size
        self.key_matrix = np.zeros((block_size, block_size))
        self.generate_key_matrix()
        
    def generate_key_matrix(self):
        for i in range(self.block_size):
            for j in range(self.block_size):
                self.key_matrix[i][j] = int(input("Enter the key matrix for [" + str(i) + "][" + str(j) + "]: "))

    
    def get_modular_inverse(self, a, b):
        for i in range(b):
            if (i * a) % b == 1:
                return i
        else:
            raise ValueError(a, " has no inverse mod ", b)
    
    def inverse(self, key_matrix):
        det_key = np.linalg.det(key_matrix).round().astype(int)
        print(np.linalg.inv(key_matrix))
        adj = np.round(np.linalg.inv(key_matrix) * np.linalg.det(key_matrix)).astype(int) % 26
        
        det_mi = self.get_modular_inverse(int(det_key), 26)

        inverse_matrix = (det_mi * adj).round().astype(int)

        return inverse_matrix
        
    
    
    
    def encrypt(self, message):  

        ciphertext = "" 
        print(self.key_matrix)
        
        message = message.upper().replace(" ", "")
        msg_length = len(message)        
        
        message_list = list(message)

        cols = self.block_size
        rows = math.ceil(msg_length/self.block_size)
        message_vector = np.zeros((rows, cols))
        


        index = 0
        padding_count = 0 
        for r in range(rows):
            for c in range(cols):
                if(index >= msg_length):
                    message_vector[r][c] = 26
                    padding_count += 1
                else:
                    message_vector[r][c] = ord(message_list[index]) % 65
                index += 1
        
                    
        print("message vector:", message_vector)
        
        cipher_vector = np.dot(message_vector, self.key_matrix) % 26
        cipher_vector = cipher_vector.astype(np.int64)
        
        print("Cipher vector:\n", cipher_vector)
        
        cipher_list = []
        for r in range(rows):
            row = []
            for c in range(cols):
                    row.append(chr(cipher_vector[r][c] + 65)) 
            cipher_list.append(row)
        
        print("Cipher list:", cipher_list)
        for r in range(rows):
            ciphertext += ''.join(cipher_list[r])
            
        if(padding_count > 0):
            ciphertext = ciphertext[:-padding_count]
            ciphertext += ('_' * padding_count)
            
        return ciphertext
    
    
    def decrypt(self, cipher):
        inverse_key = self.inverse(self.key_matrix)
        
        plaintext = ""
        
        cipher_length = len(cipher)
        cipher_list = list(cipher.upper())
        
        cols = self.block_size
        rows = math.ceil(cipher_length/self.block_size)
        cipher_vector = np.zeros((rows, cols))
        
        index = 0
        padding_count = 0
        for r in range(rows):
            for c in range(cols):
                if(index >= cipher_length or cipher_list[index] == '_'):
                    cipher_vector[r][c] = 26
                    padding_count += 1
                else:
                    cipher_vector[r][c] = ord(cipher_list[index]) % 65
                index += 1
        
        print("Cipher vector:\n", cipher_vector)
        
        plaintext_vector = np.dot(cipher_vector, inverse_key)
        plaintext_vector = np.round(plaintext_vector) % 26
        plaintext_vector = plaintext_vector.astype(np.int64)
        
        print("Plaintext vector:\n", plaintext_vector)
    
        
        plaintext_list = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(chr(plaintext_vector[r][c] + 65)) 
            plaintext_list.append(row)
        
        print("Plaintext list:, ", plaintext_list)
        for r in range(rows):
            plaintext += ''.join(plaintext_list[r])
        
        if(padding_count > 0):
            plaintext = plaintext[:-padding_count]
            
        return plaintext
        
        
        
    

        
message = "I love Computing Math"
r = HillCipher(int(input("Enter the block size of the key: ")))

print("Original message:", message)
ciphertext = r.encrypt(message)
print("Encrypted message:", ciphertext)

plaintext = r.decrypt(ciphertext)
print("Decrypted message:", plaintext)



