import pickle as pk
import time
import winsound
import pygame
import os

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FEEDBACK_DIR = os.path.join(BASE_DIR, "feedback")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FEEDBACK_DIR, exist_ok=True)

MUSIC_PATH = os.path.join(BASE_DIR, "music", "welcome.wav")

# ================= MUSIC =================
pygame.mixer.init()
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.play(fade_ms=2000)

# ================= WELCOME =================
print("WELCOME SIR!")
winsound.Beep(700, 200)
time.sleep(0.5)
winsound.Beep(500, 200)
time.sleep(0.5)

print("Let me introduce you to")
winsound.Beep(900, 150)
time.sleep(1)

print("=" * 44)
print(" " * 15, "ＸＣＲＹＰＴ")
print("=" * 44)

winsound.Beep(500, 400)
winsound.Beep(500, 400)

# ================= MAIN CHOICE =================
Choice = input("E for Encrypting, D for Decrypting: ")

# ================= ENCRYPT =================
if Choice.lower() == "e":
    NameInput = input("What is your name: ")
    PhoneNumber = input("What is your Phone Number: ")
    EmailID = input("What is your Email-ID: ")
    PasswordInput = input("What is your Email-ID Password: ")
    AadharNumber = input("What is your Aadhar Number: ")
    StateInput = input("In which State do you live: ")
    CityInput = input("Where do you live (city): ")


    FileName = input("What should I name your File: ")

    def Encrypting():
        file_path = os.path.join(DATA_DIR, FileName + ".dat")
        with open(file_path, 'wb') as file:
            DataDictionary = {
                'Name': NameInput,
                'Email-ID': EmailID,
                'Password': PasswordInput,
                'PhoneNumber': PhoneNumber,
                'AadharNumber': AadharNumber,
                'State': StateInput,
                'City': CityInput
            }
            pk.dump(DataDictionary, file)

    Encrypting()

# ================= DECRYPT =================
elif Choice.lower() == "d":
    NameInput = input("What is your Good Name Sir/Mam: ")
    def decrypting():
        filename = input("What is your filename: ")
        file_path = os.path.join(DATA_DIR, filename + ".dat")

        with open(file_path, 'rb') as file:
            readfile = pk.load(file)

        print("=" * 40)
        for key, value in readfile.items():
            print(f"{key}: {value}")
        print("=" * 40)

    decrypting()

else:
    print("Invalid choice 🤦‍♂️")

# ================== FEEDBACK ===================
time.sleep(2)
print("I hope that this program worked well for you....")
time.sleep(0.5)
print("If you really enjoyed this program please give a feedback:")
print()
Feedback_Data = input(": ")
Feedback_Dictionary = {NameInput : Feedback_Data}
Feedback_Path = os.path.join(FEEDBACK_DIR, NameInput + ".dat")
Feedback_File = open(Feedback_Path, "ab")
pk.dump(Feedback_Dictionary, Feedback_File)
Feedback_File.close()

# ================= EXIT + FADE =================
pygame.mixer.music.fadeout(2000)
time.sleep(2)
input("Press Enter to Exit...")

os.system('cls' if os.name == 'nt' else 'clear')
