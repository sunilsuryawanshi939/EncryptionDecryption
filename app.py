from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import os
from PIL import Image
from os.path import splitext, join, isfile
from photocrypt import open_image, encrypt_image, decrypt_image
from photocrypt.crypto.RSA import load_key, generate_key, save_keypair

import audio 
#----------------------------------------
@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img

#----------------------------------------
st.set_page_config(layout="wide")
# st.header("Header goes here")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

AES_KEY =''
AES_IV = ''
audioFileName = ''

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Image', 'Audio', 'Video'], 
                         iconName=['dashboard', 'music_video', 'video_library'], default_choice=0)
    use_cui = False
    encryption = None

if tabs =='Image':
    st.title("Image")
    # st.write('Name of option is {}'.format(tabs))
    with st.expander("About Image encryption"):
        st.write("Write your instructions here")
    

    #--------------------------------------------------------------------------------------------------
    col1, col2 ,col3= st.columns(3)
    with col1:
        st.header("Select Process")
        todo = st.radio("What to perform Encryption/Decryption ?",('Encrypt', 'Decrypt'))
        if todo == 'Encrypt':
            encryption = 'encrypt'
            st.write('You selected Encrypt.')
        else:
            encryption = 'decrypt'
            st.write("You selected Decrypt.")

    with col2:
        st.header("Select Key")
        key_type = st.radio("Which key to use public/private ?",('Public', 'Private'))
        if key_type == 'Public':
            key_path  = "public.pem"
            st.write('You selected Public key.')
        else:
            key_path  = "private.pem"
            st.write("You selected Private key.")

    with col3:
        st.header("Upload Image")
        image_file = st.file_uploader('Upload image File', type=['jpg','jpeg','png']) #'pdf', 'docx', 'txt',


    #--------------------------------------------------------------------------------------------------
    if image_file is not None:
        # #Create a folder for Saving files
        if not os.path.exists('imageFolder'):
            os.makedirs('imageFolder')

        # #get uploaded image filename
        st.write("Filename: ",image_file.name)

        col1, col2 = st.columns(2)

        with col1:
            st.header("Uploaded Image")
            img = load_image(image_file)
            st.image(img,caption="This is your uploaded image", width=None, use_column_width='always')

            imagesFolderPath = "imageFolder/"+image_file.name
            with open(imagesFolderPath,"wb") as f:
                f.write(image_file.getbuffer())
            st.success(f'{imagesFolderPath} file is saved')

        with col2:
            st.header("Processed Image")
            image = open_image(imagesFolderPath)
            image_path, image_ext = splitext(imagesFolderPath)
            key = load_key(key_path)

            if encryption == 'encrypt':
                encrypted = encrypt_image(image, key)
                encrypted.save(f'{image_path}_enc{image_ext}')
                print(f'image encrypted in {image_path}_enc{image_ext}')
                # st.write(f'image encrypted in {image_path}_enc{image_ext}')

                pro_img = load_image(f'{image_path}_enc{image_ext}')
                st.image(pro_img,caption="This is your encrypted image", width=None, use_column_width='always')
                st.success(f'{image_path}_enc{image_ext} encrypted file saved')

                encrypted_image_path = f'{image_path}_enc{image_ext}'
                encrypted_image_name = image_path.split('/')[-1]
                full_enc_img_name    = f'{encrypted_image_name}_enc{image_ext}'

                with open(encrypted_image_path, "rb") as file:
                    btn = st.download_button(
                            label="Download Encrypted Image",
                            data=file,
                            file_name= full_enc_img_name,
                            mime="image/png"
                        )

            else:
                decrypted = decrypt_image(image, key)
                decrypted.save(f'{image_path}_dec{image_ext}')
                print(f'image decrypted in {image_path}_dec{image_ext}')
                # st.write(f'image decrypted in {image_path}_dec{image_ext}')

                pro_img = load_image(f'{image_path}_dec{image_ext}')
                st.image(pro_img,caption="This is your decrypted image", width=None, use_column_width='always')
                st.success(f'{image_path}_dec{image_ext} decrypted file saved')

                decrypted_image_path = f'{image_path}_dec{image_ext}'
                decrypted_image_name = image_path.split('/')[-1]
                full_dec_img_name    = f'{decrypted_image_name}_dec{image_ext}'

                with open(decrypted_image_path, "rb") as file:
                    btn = st.download_button(
                            label="Download Decrypted Image",
                            data=file,
                            file_name = full_dec_img_name,
                            mime="image/png"
                        )

elif tabs == 'Audio':
    st.title("Audio")
    # st.write('Name of option is {}'.format(tabs))
    with st.expander("About Audio Encryption"):
        st.write("Write your instructions here")
    #--------------------------------------------------------------------------------------------------
    col1, col2 ,col3 = st.columns(3)
    with col1:
        st.header("Select Process")
        todo = st.radio("What to perform Encryption/Decryption ?",('Encrypt', 'Decrypt'))
        if todo == 'Encrypt':
            thetask = 'encrypt'
            st.write('You selected Encrypt.')
        else:
            thetask = 'decrypt'
            st.write("You selected Decrypt.")

    with col2:
        st.header("Generate Key")
        if thetask == 'decrypt':
            if st.button('Read Key'):

                AES_KEY, AES_IV  = audio.readAESKey()
                st.write('AES key Read')
            else:
                st.write('AES key unread')
        else:
            if st.button('Get Key'):
                st.write('AES key generated')
                AES_KEY, AES_IV  = audio.genAESKey()
            else:
                st.write('AES key absent')

    with col3:
        st.header("Upload Audio")
        audio_file = st.file_uploader('Upload audio File', type=['wav']) #'pdf', 'docx', 'txt',

    #--------------------------------------------------------------------------------------------------
    if audio_file is not None:
        # #Create a folder for Saving files
        if not os.path.exists('audioFolder'):
            os.makedirs('audioFolder')

        # #get uploaded image filename
        st.write("Filename: ",audio_file.name)
        AES_KEY, AES_IV  = audio.readAESKey()

        col1, col2 = st.columns(2)

        with col1:
            st.header("Uploaded Audio")
            
            audioFolderPath = "audioFolder/"+audio_file.name
            audioFileName   = audio_file.name

            with open(audioFolderPath,"wb") as f:
                f.write(audio_file.getbuffer())
            st.success(f'{audioFolderPath} file is saved')

            #----------------------------------------
            # fs, data = audio.wavfile.read(audioFolderPath)
            # audio.plt.plot(data)            # fs = sampling frequency = 44.1kHz
            # audio.plt.title("Original Audio Plot")
            #----------------------------------------
            
            aud_file = open(audioFolderPath, 'rb')
            audio_bytes = aud_file.read()
            st.audio(audio_bytes, format='audio/ogg')


        with col2:
            st.header("Processed Audio")
            wavAudioFile = audioFolderPath
            audio_folder_filename, audio_ext = splitext(audioFolderPath)

            if thetask == 'encrypt':
                enc_audio_filepath = audio.encryptAudio('audioFolder', audioFileName, wavAudioFile, AES_KEY, AES_IV)
                st.success(f'{enc_audio_filepath} file is saved')

                enc_aud_file = open(enc_audio_filepath, 'rb')
                audio_bytes = enc_aud_file.read()
                st.audio(audio_bytes, format='audio/ogg')  

                print("enc_audio_filepath :",enc_audio_filepath)
                print(enc_audio_filepath.split('/', 2)[1])
                enc_audio_filename = enc_audio_filepath.split('/', 2)[1]



                with open(enc_audio_filepath, "rb") as file:
                    btn = st.download_button(
                            label="Download Encrypted Audio",
                            data=file,
                            file_name = enc_audio_filename,
                            mime="wav/mp3"
                        )

            else:
                dec_audio_filepath = audio.decryptAudio('audioFolder', audioFileName, wavAudioFile, AES_KEY, AES_IV)
                st.success(f'{dec_audio_filepath} file is saved')

                dec_aud_file = open(dec_audio_filepath, 'rb')
                audio_bytes = dec_aud_file.read()
                st.audio(audio_bytes, format='audio/ogg') 

                print("dec_audio_filepath :",dec_audio_filepath)
                print(dec_audio_filepath.split('/', 2)[1])
                dec_audio_filename = dec_audio_filepath.split('/', 2)[1]

                with open(dec_audio_filepath, "rb") as file:
                    btn = st.download_button(
                            label="Download Decrypted Audio",
                            data=file,
                            file_name = dec_audio_filename,
                            mime="wav/mp3"
                        )
           
           
elif tabs == 'Video':
    st.title("Video")
    st.write('Name of option is {}'.format(tabs))
    