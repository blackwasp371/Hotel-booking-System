import socket
import os

host = '127.0.0.1'
port = 5566

key = 13
characters = [' ', '.', '-', '(', ')', '!', '_', '>', '<', '/', '\\', '|', '+', '=', '[', ']', ':', ';', '`', '~', '"']

def encryption(message):
    encrypted = ""
    for character in message:
        if character.isupper():
            character_index = ord(character) - ord('A')
            character_shift = (character_index + key) % 26 + ord('A')
            character_new = chr(character_shift)
            encrypted += character_new
        elif character.islower():
            character_index = ord(character) - ord('a')
            character_shift = (character_index + key) % 26 + ord('a')
            character_new = chr(character_shift)
            encrypted += character_new
        elif character.isdigit():
            character_new = (int(character) + key) % 10
            encrypted += str(character_new)
        elif character in characters:
            character_index = characters.index(character)
            character_shift = (character_index + key) % len(characters)
            character_new = characters[character_shift]
            encrypted += character_new
        else:
            encrypted += character
    return encrypted

def decryption(message):
    dencrypted = ""
    for character in message:
        if character.isupper():
            character_index = ord(character) - ord('A')
            character_shift = (character_index - key) % 26 + ord('A')
            character_new = chr(character_shift)
            dencrypted += character_new
        elif character.islower():
            character_index = ord(character) - ord('a')
            character_shift = (character_index - key) % 26 + ord('a')
            character_new = chr(character_shift)
            dencrypted += character_new
        elif character.isdigit():
            character_new = (int(character) - key) % 10
            dencrypted += str(character_new)
        elif character in characters:
            character_index = characters.index(character)
            character_shift = (character_index - key) % len(characters)
            character_new = characters[character_shift]
            dencrypted += character_new
        else:
            dencrypted += character
    return dencrypted

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

def read_files():
    result1 = ""
    with open('hotel.csv', "r") as f:
        reader = f.read().split('\n')
        for rows in reader:
            if rows != '':
                row = rows.split(', ')
                result1 += f"->{row[0]}-|-{row[1]}-|-{row[2]}-|-{row[3]}-|-{row[4]}-|-{row[5]}"
    f.close()
    result = f"DataInfo{result1}"
    return result

while True:
    # Establish a connection with a client
    c, addr = s.accept()
    print("Connection from: " + str(addr))

    data = decryption(c.recv(2048).decode())

    if data.startswith('AddUser'):
        user_info = data.split('-|-')
        with open("hotel.csv", 'a') as csvfile:  # file handling1
                    csvfile.write('{0}, {1}, {2}, {3}, {4}, {5}\n'.format(
                        str(user_info[1]), user_info[2], user_info[3], str(user_info[4]), str(user_info[5]), user_info[6]))

        csvfile.close()
        
        c.send(encryption("Details has been added!").encode('utf-8'))
    
    elif data.startswith('Update'):
        user_info = data.split('-|-')
        with open("hotel.csv", "r") as f1, open("hotels_tmp.csv", "w") as working:
            for line in f1:
                if user_info[1] not in line:
                    working.write(line)
                else:
                    working.write('{0}, {1}, {2}, {3}, {4}, {5}\n'.format(
                        user_info[1], user_info[2], user_info[3], user_info[4], user_info[5], user_info[6]))
        os.remove("hotel.csv")
        os.rename("hotels_tmp.csv", "hotel.csv")

        c.send(encryption("Data Updated!").encode('utf-8'))
    
    elif data.startswith('Delete'):
        user_info = data.split('-|-')
        with open("hotel.csv", 'r') as f, open("hotels_tmp.csv", "w") as w1:  # file handling2
            for line in f:
                if user_info[1] not in line:
                    w1.write(line)
        os.remove("hotel.csv")
        os.rename("hotels_tmp.csv", "hotel.csv")
        f.close()
        w1.close()
        c.send(encryption("Data Deleted!").encode('utf-8'))
    
    elif data.startswith('Get Data?'):
        c.send(encryption(read_files()).encode('utf-8'))
    
    c.send(encryption("ACK").encode('utf-8'))
    c.close()