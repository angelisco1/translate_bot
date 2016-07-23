import sys
import time
import telepot
import subprocess
from textblob import TextBlob
from os import path
from gtts import gTTS


TEMP_PATH = "./tmp/"
WAV = ".wav"
SOURCE_LANG = 'es'
TARGET_LANG = 'en'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    from_user =  msg.get('from')
    username = from_user.get('username')
    first_name = from_user.get('first_name')

    if content_type == 'text':
        text = msg.get('text')
        new_audio_name = "text_" + TARGET_LANG + WAV

        # Translate text
        translated_text = translateText(text)

        # Text to speech
        new_path = TEMP_PATH + new_audio_name
        parseTextToSpeech(new_path, translated_text)

        # Send message
        bot.sendMessage(chat_id, translated_text)
        
        # Send voice
        bot.sendVoice(chat_id, open(new_path, 'rb'))


def translateText(text):
    text_blob = TextBlob(text)
    translated_text = text_blob.translate(from_lang=SOURCE_LANG, to=TARGET_LANG)
    return str(translated_text)
    

def parseTextToSpeech(audio_name, text):
    tts = gTTS(text=text, lang=TARGET_LANG)
    tts.save(audio_name)




TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('I\'m listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
