from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

import random
import string
from Crypto.Cipher import AES
import os

#----------------------------------------
def readAudio(wavAudioFile):
    with open(wavAudioFile, 'rb') as fd:
        wavAudioFileContents = fd.read()
    return wavAudioFileContents

def plotAudio(wavAudioFile):
    fs, data = wavfile.read(wavAudioFile)
    plt.plot(data)            # fs = sampling frequency = 44.1kHz
    plt.title("Original Audio Plot")


def playAudio(wavAudioFile):
    fs, data = wavfile.read(wavAudioFile)
    sd.play(data, fs)

def genAESKey():
    AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
    AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    print("AES Key is ", AES_KEY)
    print("AES Initialization vector is ", AES_IV)

    f = open("AES_KEY.key", "w")
    f.write(AES_KEY)
    f.close()

    g = open("AES_IV.key", "w")
    g.write(AES_IV)
    g.close()

    return AES_KEY, AES_IV

def readAESKey():
    f = open("AES_KEY.key", "r")
    AES_KEY = f.read()
    f.close()

    g = open("AES_IV.key", "r")
    AES_IV = g.read()
    g.close()

    return AES_KEY, AES_IV

def encryptAudio(audioFolder, audioFileName, wavAudioFile, AES_KEY, AES_IV):
    with open(wavAudioFile, 'rb') as fd:
        contents = fd.read()

    encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    encrypted_audio = encryptor.encrypt(contents)

    enc_audio_filepath  = audioFolder + '/enc_' + audioFileName
    with open(enc_audio_filepath, 'wb') as fd:
        fd.write(encrypted_audio)
    print("An encrypted audio file titled \" {enc_audio_filepath} \" is generated.")
    
    return enc_audio_filepath

def decryptAudio(audioFolder, audioFileName, wavAudioFile, AES_KEY, AES_IV):
    with open(wavAudioFile, 'rb') as fd:
        contents = fd.read()

    decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    decrypted_audio = decryptor.decrypt(contents)

    dec_audio_filepath  = audioFolder + '/dec_' + audioFileName 
    with open(dec_audio_filepath, 'wb') as fd:
        fd.write(decrypted_audio)
    print("An decrypted audio file titled \" {dec_audio_filepath} \" is generated.")
    
    return dec_audio_filepath
#-----------------------------------------

fs, data = wavfile.read('audio.wav')
plt.plot(data)            # fs = sampling frequency = 44.1kHz
plt.title("Original Audio Plot")

with open('audio.wav', 'rb') as fd:
    contents = fd.read()


# sd.play(data, fs)

# #--------------------------

# AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))

# AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

# print("AES Key is ", AES_KEY)
# print("AES Initialization vector is ", AES_IV)

# encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
# encrypted_audio = encryptor.encrypt(contents)

# with open('encrypted_audio_file.wav', 'wb') as fd:
#     fd.write(encrypted_audio)
# print("A file titled 'encrypted_audio_file.wav' is generated which is the encrypted audio to be communicated")


# #------Decryption ----------------
# with open('encrypted_audio_file.wav', 'rb') as fd:
#     contents = fd.read()

# decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
# decrypted_audio = decryptor.decrypt(contents)

# with open('decrypted_audio_file.wav', 'wb') as fd:
#     fd.write(decrypted_audio)

# fs, data = wavfile.read('decrypted_audio_file.wav')
# plt.plot(data)            # fs = sampling frequency = 44.1kHz
# plt.title("Original Audio Plot")
# data_1 = np.asarray(data, dtype = np.int32)

# sd.play(data, fs)