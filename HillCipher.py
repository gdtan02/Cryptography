import math
import random
import numpy as np

class HillCipher(object):

    def __init__(self, block_size):
        self.block_size = block_size
        self.key_matrix = np.zeros((block_size, block_size))
        self.generate_key_matrix()
        
    def generate_key_matrix(self):
        """
        This method is called to prompt user to enter the value for the key 
        and initialize the key matrix.
        
        Limitation:
        The key matrix should not be the singular matrix (without inverse), and the modular
        multiplicative inverse of its determinant under modulo 26 need to be existed.
        
        """
        for i in range(self.block_size):
            for j in range(self.block_size):
                self.key_matrix[i][j] = int(input("Enter the key matrix for [" + str(i) + "][" + str(j) + "]: "))

    
    def get_modular_inverse(self, a, b):
        """
        This method takes two integers as parameters, a and b, and is used to find the
        modular multiplicative inverse of a under modulo b. The modular multiplicative
        inverse is an integer, i, which will be returned as result.
        
        The multiplicative inverse of "a modulo b" exists if and only if a and ba are
        relatively prime. (gcd(a,b) == 1). If the modular multiplicative inverse does
        not exist, a ValueError will be raised.
        
        Args:
            a (_int_): an integer which its modular multiplicative inverse under modulo b to be find.
            b (_int_): modulo

        Raises:
            ValueError: The modular multiplicative inverse of a under modulo b does not exist.

        Returns:
            _int_: the modular multiplicative inverse of a under modulo b, i.
        """
        for i in range(b):
            if (((i % b) * (a % b)) % b == 1):
                return i
        else:
            raise ValueError(a, " has no inverse mod ", b)
    

    def inverse(self, key_matrix):
        """This method is used to compute the inverse matrix.

        Args:
            key_matrix (_np_matrix_): a square matrix which is used as the key

        Returns:
            _np_matrix_: the inverse of the key matrix
        """
        det_key = np.linalg.det(key_matrix).round().astype(int)
        print(np.linalg.inv(key_matrix))
        adj = np.round(np.linalg.inv(key_matrix) * np.linalg.det(key_matrix)).astype(int) % 26
        
        det_mi = self.get_modular_inverse(int(det_key), 26)

        inverse_matrix = (det_mi * adj).round().astype(int)

        return inverse_matrix
        
    
    
    
    def encrypt(self, message):  
        """
        The method used to encrypt the message into ciphertext. 
        
        Pseudocode:
        1) Takes the message to be encrypted as argument, clean the message by removing the padding.
        2) Convert the characters of the message into numerical value and store them into vectors 
            with size [1, m], where m = the block size.
        3) Multiply the message vectors with key matrix generated to compute the cipher vectors. 
            The size of key matrix is [m, m], and the cipher vector has the size of [1, m], where
            m = block size. Formula as below:
            C (P, K) = P * K mod 26,
            where C = cipher vector, P = message vector, K = key matrix
        4) Convert the value of the cipher vectors into characters and form the ciphertext.
        

        Args:
            message (_str_): the message to be encrypted

        Returns:
            _str_: the encrypted message
        """

        ciphertext = "" 
        print(self.key_matrix)
        
        # Remove the padding
        message = message.upper().replace(" ", "")
        message = message.upper().replace("_", "")
        msg_length = len(message)        
        
        message_list = list(message)

        # Construct n message vectors with size (1 * block_size), where n is the number of rows.
        cols = self.block_size
        rows = math.ceil(msg_length/self.block_size)
        message_vector = np.zeros((rows, cols))
        

        # Convert the message into numerical format and store into message vector
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
        
        # Compute the cipher vector by multiplying the message vector with key generated.
        # C(P, K) = P * K mod 26, where C = cipher vector, P = message vector, K = key matrix
        cipher_vector = np.dot(message_vector, self.key_matrix) % 26
        cipher_vector = cipher_vector.astype(np.int64)
        
        print("Cipher vector:\n", cipher_vector)
        
        # Convert the value of the cipher vector back to their respective 
        # characters and form the ciphertext.
        cipher_list = []
        for r in range(rows):
            row = []
            for c in range(cols):
                    row.append(chr(cipher_vector[r][c] + 65)) 
            cipher_list.append(row)
        
        print("Cipher list:", cipher_list)
        for r in range(rows):
            ciphertext += ''.join(cipher_list[r])
            
        # Add the padding back to the end of ciphertext
        if(padding_count > 0):
            ciphertext = ciphertext[:-padding_count]
            ciphertext += ('_' * padding_count)
            
        return ciphertext
    
    
    # TODO: Still got bug
    def decrypt(self, cipher):
        """This method is used to decrypt the ciphertext into plaintext message. 
        
        Pseudocode:
        1) Compute the inverse of the key matrix. The inverse matrix has a size of [m, m], where
            m = the block size.
        2) Convert the characters of the ciphertext into numerical value and store them into cipher
            vectors with size [1, m], where m = the block size.
        3) Multiply the cipher vectors with the inverse of key matrix to get the plaintext vectors.
            The plaintext vectors should have a size of [1, m]. The formula as below:
            P (C, K) = C * K^ mod 26
            where P = plaintext vector, C = cipher vector, K^ = inverse of key matrix, K
        4) Convert the values of plaintext vector back to characters to form the plaintext mesage.

        Args:
            cipher (_str_): the ciphertext to be decrypted

        Returns:
            _str_: the decrypted message
        """
        
        # Compute the inverse of key matrix
        inverse_key = self.inverse(self.key_matrix)
        
        plaintext = ""
        
        cipher_length = len(cipher)
        cipher_list = list(cipher.upper())
        
        # Convert the message into numerical format and store it into cipher vector
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
        
        # Decrypt the message by multiplying the cipher vector with the inverse of key matrix
        plaintext_vector = np.dot(cipher_vector, inverse_key)
        plaintext_vector = np.round(plaintext_vector) % 26
        plaintext_vector = plaintext_vector.astype(np.int64)
        
        print("Plaintext vector:\n", plaintext_vector)
    
    
        # Convert the value of plaintext vector back into characters to form the plaintext.
        plaintext_list = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(chr(plaintext_vector[r][c] + 65)) 
            plaintext_list.append(row)
        
        # Remove the padding of the character
        print("Plaintext list:, ", plaintext_list)
        for r in range(rows):
            plaintext += ''.join(plaintext_list[r])
        
        if(padding_count > 0):
            plaintext = plaintext[:-padding_count]
            
        return plaintext
        
        
        
    

        
message = "I love Computing Math!!!"
r = HillCipher(int(input("Enter the block size of the key: ")))

print("Original message:", message)
ciphertext = r.encrypt(message)
print("Encrypted message:", ciphertext)

plaintext = r.decrypt(ciphertext)
print("Decrypted message:", plaintext)



