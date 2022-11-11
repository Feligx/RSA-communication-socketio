#RSA implementation
import math
import random

'''
  ------- RSA - Implementation -------
'''
def RSA(p, q):  #Step 1 of RSA Select p,q given at input
  #Step 2 RSA
  n = p * q
  #Step 3 RSA
  phi_n = (p - 1) * (q - 1)
  #Step 4 RSA
  a = 0
  while a != 1:
    e = random.randint(1, phi_n - 1)
    if math.gcd(e, n) == 1:
      try:
        d = pow(e, -1, phi_n)
        a = 1
      except:
        continue
  K_pub = [str(n), str(e)]
  K_priv = d
  return K_pub, K_priv


def encrypt(x, K_pub):
  return pow(x, K_pub[1], K_pub[0])


def decrypt(y, K_priv, K_pub):
  return pow(y, K_priv, K_pub[0])
    

'''
  ------- RSA - Signature -------
'''
def digital_signature(K_priv, x):
  s = pow(int(x, 2), K_priv, p*q)
  return s

def verify_signature(x, s, K_pub):
    if pow(s, K_pub[1], K_pub[0]) == x%K_pub[0]:
        return 1
    else:
        return 0

'''
  ------- Slicer & Txt2Bin & Bin2Txt -------
'''

# Particionar un texto y formar bloques de 128 de long
def slicer(text):
  blocks = []
  count = 0
  str = ''
  print('slicing', text)
  for i in range(len(text)):
    if count <= 255:
      str = str + text[i]
      count += 1
    else:
      blocks.append(str)
      str = text[i]
      count = 1
  if len(str) != 0:
    blocks.append(str)
  return blocks
  
def slicer_inv(text):
  counter = 0
  blocks = []
  temp_string = ""
  for c in range(len(text)):
    if counter <= 2047:
      temp_string = temp_string + text[c]
      counter += 1
    else:
      blocks.append(temp_string)
      temp_string = text[c]
      counter = 1
  if len(temp_string) != 0:
    blocks.append(temp_string)
  return blocks

# Pasar de texto a binario con ascii en utf08
def text2bin(txt: str):
  return ''.join([format(ord(i), '08b') for i in txt])

# Pasar de binario a texto con utf08
  
def bin2text(bin_num: str):
  return ''.join(chr(int(bin_num[c*8: (c+1)*8], 2)) for c in range(0, len(bin_num)//8))

'''
  ------- ECB wrappers -------
'''

def ecb_encrypt(text, K_pub):
    #Slice the text in blocks
    sliced = slicer(text)

    #Transform blocks from characters to binary
    blocks = [text2bin(text) for text in sliced]

    #Encryption of the blocks
    ciphered = [bin(encrypt(int(b,2), K_pub)).replace('0b', '').zfill(2048) for b in blocks]

    return ciphered

def ecb_signature(ciphered, K_priv):
    #Sign each blocks
    signatures = [bin(digital_signature(K_priv, s)).replace('0b', '').zfill(2048) for s in ciphered]
    
    return signatures
  
def ecb(text, K_pub_own, K_pub_receiver, K_priv):
    K_pub_receiver = [int(K_pub_receiver[0]), int(K_pub_receiver[1])]
    K_pub_own = [int(K_pub_own[0]), int(K_pub_own[1])]
    ciphered_blocks = ecb_encrypt(text, K_pub_receiver)

    signed_blocks = ecb_signature(ciphered_blocks, K_priv)

    #Concatenation of the ciphertext
    message = "".join(ciphered_blocks)

    #Concatenation of the signature
    signature = "".join(signed_blocks)

    return message, signature

def ecb_signature_validation(sliced_message, sliced_signature, K_pub):
  
    print('Validando!')
    K_pub = [int(K_pub[0]), int(K_pub[1])]

    #Compute validation
    is_valid = [verify_signature(int(sliced_message[s], 2) ,int(sliced_signature[s], 2), K_pub) for s in range(len(sliced_signature))]
    return 0 not in is_valid
  
def ecb_decryption(sliced, K_pub, K_priv):
    K_pub = [int(K_pub[0]), int(K_pub[1])]
    clear = [bin(decrypt(int(c, 2), K_priv, K_pub)).replace('0b', '').zfill(2048) for c in sliced]

    #Concatenating the final message
    clear_text = "".join(bin2text(c) for c in clear)

    return clear_text
  
'''
  ------- Main function -------
'''

p = 2 ** 1024 - 105 

q = 2 ** 1023 + 1155

message = ""
signature = ""
K_pub, K_priv = RSA(p, q)

def main():
  global K_pub, K_priv, message, signature
  if input('Desea Cifrar(1) o Descifrar(2)?') == '1':
    text = input('Ingrese el texto a cifrar:\n> ')

    message, signature = ecb(text)
    
    if input("Want to continue? (Y/n): ") == 'Y':
      main()
      
  else:
    #Recover encrypted blocks
    sliced = slicer_inv(message)
    signature_prime = ecb_signature_validation(sliced)
    
    #Check the integrity of the message s.t: s = s'
    if signature == signature_prime:
      print('El mensaje es válido!')
      print('Descifrando!')
      #Dectypt the obtained blocks
      clear_text = ecb_decryption(sliced)
      print("Obtained Message:\n", clear_text, '\n')
    else:
      print('Ocurrió algo con el mensaje...')
