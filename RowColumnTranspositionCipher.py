import numpy as np
import math

class RowColumnTranspositionCipher(object):
    
    def __init__ (self, key):
        """Intialize the key of the cipher.

        Args:
            key (_str_): The keyword which consists of uppercase letters (A-Z) only
        """
        self.key = key.upper()
        
    # Helper function
    # def swap_operation(self, matrix, row_a, row_b):
    #     temp = matrix[row_a]
    #     matrix[row_a] = matrix[row_b]
    #     matrix[row_b] = temp   
        
    def encrypt(self, message):
        """ The method is used to encrypt the message.
        
        Pseudocode: 
        1) Construct an empty matrix with size [m, n], where m = number of rows, n = number of columns.
            The number of columns is determined by the length of the keyword.
        2) Compute the key order and swapping list. 
           The swapping list contains the index of rows that need to be swapped.
        3) Write the message and padding characters into the matrix row-wise.
        4) Perform ERO where two rows are swapped according to the swapping list. The row with the index of
           i th element in the swapping list is swapped with the row with the index of (i+1)th element in the
           swapping list, starting from the first to the (key.length-1)th element.
        5) Read the ciphertext column-wise based on the key order.

        Args:
            message (_str_): the message to be encrypted

        Returns:
            _str_: the encrypted message
        """
        cipher = ""
        
        msg_length = len(message)
        key_length = len(self.key)
        
        # Construct the matrix
        column_size = key_length
        row_size = math.ceil(msg_length / key_length)
        matrix = []
        
        # Compute key order and swapping list
        key_list = list((ord(self.key[i]) % 65) for i in range(key_length))
        key_order = [0 for i in range(key_length)]
        key_dict = {}
        for i in range(key_length):
            # key_order[i] =key_order = list(sorted(list(key)).index(key[i]) for i in range(key_length))
            if key_list[i] in key_dict:
                order = list(sorted(key_list)).index(key_list[i]) + key_dict[key_list[i]]
                key_dict[key_list[i]] += 1
            else:
                order = list(sorted(key_list)).index(key_list[i])
                key_dict[key_list[i]] = 1
            key_order[i] = order

        swapping = np.array(list([key_list[i] , key_list[i+1]]  for i in range(key_length-1))) % row_size
        
        # Write the message and padding characters into the matrix row-wise.
        index = 0
        for r in range(row_size):
            row = []
            for c in range(column_size):
                if(index >= msg_length):
                    row.append("_")
                else:
                    row.append(message[index])
                index += 1
            matrix.append(row)
        
        # ERO - swapping two rows
        for i in range(len(swapping)):
            matrix[swapping[i][0]], matrix[swapping[i][1]] = matrix[swapping[i][1]], matrix[swapping[i][0]] 
            # self.swap_operation(matrix, swapping[i][0], swapping[i][1])
        
        # Read the matrix column-wise based on the key order
        # for c in range(column_size):
        #     current_index = key_order.index(c)
        #     for r in range(row_size):
        #         cipher += matrix[r][current_index]
        

        
        # Get the transpose of matrix to read it column-wise based on the key order
        matrix = np.array(matrix)
        transpose = matrix.transpose()
        for col in range(column_size):
            current = key_order.index(col)
            cipher += ''.join(transpose[current])
 
        return cipher
     
     
    def decrypt(self, cipher):
        """This method is used to decrypt the ciphertext into plaintext message. 
        
        Pseudocode:
        1) Construct the empty transpose matrix with size [n, m].
        2) Compute the key order and swapping list. 
        3) Write the ciphertext into the matrix constructed row-wise according to the key order. Then,
            transpose the matrix to get the decipher matrix.
        4) Perform ERO where two rows are swapped based on the swapping list in reverse order.
        5) Read the plaintext starting from the first to the last row of the matrix.

        Args:
            cipher (_str_): the ciphertext to be decrypted

        Returns:
            _str_: the decrypted message
        """
        message = ""
        
        key_length = len(self.key)
        msg_length = len(cipher)
        
        # Compute an empty transpose matrix
        column_size = key_length
        row_size = math.ceil(msg_length / key_length)
        
        transpose = []
        for col in range(column_size):
            transpose += [[None] * row_size]
        
        # Compute the key order and swapping list. The swapping list is in reverse order to the swapping
        # list in the encrypt method.
        key_list = list((ord(key[i]) % 65) for i in range(key_length))
        key_order = [0 for i in range(key_length)]
        key_dict = {}
        

        for i in range(key_length):
            if key_list[i] in key_dict:
                order = list(sorted(key_list)).index(key_list[i]) + key_dict[key_list[i]]
                key_dict[key_list[i]] += 1
            else:
                order = list(sorted(key_list)).index(key_list[i])
                key_dict[key_list[i]] = 1
            key_order[i] = order
        
        swapping = np.array(list([key_list[i], key_list[i-1]] for i in range(key_length-1, 0, -1))) % row_size
        
  
        # Write the ciphertext into the matrix constructed row-wise according to the key order
        index = 0
        for c in range(column_size):
           current = key_order.index(c)
           for r in range(row_size):
               transpose[current][r] = cipher[index]
               index += 1 
            
        # Transpose the matrix to get the decipher matrix
        transpose = np.array(transpose)
        decipher_matrix = transpose.transpose().tolist()
        
        # ERO - swapping two rows
        for i in range(len(swapping)):
            decipher_matrix[swapping[i][0]], decipher_matrix[swapping[i][1]] = decipher_matrix[swapping[i][1]], decipher_matrix[swapping[i][0]] 
        
        for r in range(row_size):
            message += ''.join(decipher_matrix[r])
        
        # Remove the padding in the message
        padding_count = message.count('_')
        message = message[:-padding_count]
        
        
        return message
    
    
        
message = "Kill corona virus at twelve am tomorrow"
key = "PATTERN"
r = RowColumnTranspositionCipher(key)
ciphertext = r.encrypt(message)

print(ciphertext)
ciphertext = 'owuirm va _oi  o_ortrKravetc_mneslo al lwt'

plaintext = r.decrypt(ciphertext)
print(plaintext)
        
