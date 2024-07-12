# A voice assistant based on [Your Name]'s AI
# Running on Windows 11

from llama_chat import chat_with_llama
import speech_recognition as sr
from datetime import date
from gtts import gTTS
from io import BytesIO
from pygame import mixer 
import threading
import queue
import time
 
mixer.init()

# Global counters
today_date = str(date.today())
num_user_requests = 0 
num_tts_conversions = 0 
num_audio_playbacks = 0
 
all_messages = []  # Stores chat messages

# Function to handle user requests and interact with Llama3
def chat_with_llama(request_text, text_queue, llama_finished):
    
    global num_user_requests, all_messages
    
    all_messages.append({'role': 'user', 'content': request_text})
 
    response = chat_with_llama(
        model='llama3',
        messages=all_messages,
        stream=True,
    )
    
    short_string = ''  
    reply_text = ''
    record_to_file("AI: ") 

    for chunk in response:
        content_text = chunk['message']['content']

        short_string = "".join([short_string, content_text])
 
        if len(short_string) > 40:
             
            print(short_string, end='', flush=True) 

            text_queue.put(short_string.replace("*", ""))
            
            num_user_requests += 1 
            
            reply_text = "".join([reply_text, short_string])
            
            short_string = ''

        else:
            continue
        
        time.sleep(0.2)
     
    if len(short_string) > 0: 
        print(short_string, flush=True) 
        short_string = short_string.replace("*", "")
        text_queue.put(short_string)                          

        num_user_requests += 1 
            
        reply_text = "".join([reply_text, short_string])
        
    all_messages.append({'role': 'assistant', 'content': reply_text})
    record_to_file(f"{reply_text}") 
    
    llama_finished.set()  # Signal completion of text generation by Llama

# Function to convert text to speech and play it
def record_to_file(text):
 
    mp3_file = BytesIO()
    tts = gTTS(text, lang="en", tld='us') 
    tts.write_to_fp(mp3_file)

    mp3_file.seek(0)
    
    try:
        mixer.music.load(mp3_file, "mp3")
        mixer.music.play()
        while mixer.music.get_busy(): 
            time.sleep(0.1)

    except KeyboardInterrupt:
        mixer.music.stop()
        mp3_file.close()
 
    mp3_file.close()	

# Function to convert text to speech and add to queue
def text_to_sound(text_queue, text_done, llama_finished, audio_queue, stop_event):

    global num_user_requests, num_tts_conversions
 
    while not stop_event.is_set():  
        
        if not text_queue.empty():
            text = text_queue.get(timeout=0.5)  
 
            num_tts_conversions += 1 
 
            mp3_file = BytesIO()
            tts = gTTS(text, lang="en", tld='us') 
            tts.write_to_fp(mp3_file)
        
            audio_queue.put(mp3_file)
            
            text_queue.task_done()
 
        if llama_finished.is_set() and num_tts_conversions == num_user_requests: 
            time.sleep(0.2)
            text_done.set()
            break 
        
# Function to play audio from queue
def play_audio_from_queue(audio_queue, text_done, stop_event):
 
    global num_tts_conversions, num_audio_playbacks 
    
    while not stop_event.is_set():  
 
        mp3_audio = audio_queue.get()  
        
        num_audio_playbacks += 1 
        
        mp3_audio.seek(0)
 
        mixer.music.load(mp3_audio, "mp3")
        mixer.music.play()
        
        while mixer.music.get_busy(): 
            time.sleep(0.1)
 
        audio_queue.task_done() 
 
        if text_done.is_set() and num_tts_conversions == num_audio_playbacks: 
            break  

# Append conversation to log file 
def log_activity(text):
    global today_date
    filename = 'recordedlog-' + today_date + '.txt'
    with open(filename, "a", encoding='utf-8') as file:
        file.write(text + "\n")
        file.close 

# Default language for the AI model 
used_language = "en-EN"

# Main function  
def start():
    global today_date, used_language, num_user_requests, num_tts_conversions, num_audio_playbacks, all_messages
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 400    
    i = 1
    is_sleeping = True 
    
    while True:     
        with microphone as source:            
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Listening ...")
            
            try: 
                audio_input = recognizer.listen(source, timeout=20, phrase_time_limit=30)
                input_text = recognizer.recognize_google(audio_input, language=used_language)
 
                if is_sleeping == True:
                    if "vocal signal" in input_text.lower():  # Replace with your wake word
                        request_text = input_text.lower().split("vocal signal")[1]
                        
                        is_sleeping = False
                        log_activity(f"_"*40)                    
                        today_date = str(date.today())  
                        
                        all_messages = []                      
                     
                        if len(request_text) < 2:
                            record_to_file("Hey, there, what can I assist you with?")
                            log_activity(f"AI: Hey, there, what can I assist you with? \n")
                            continue                      

                    else:
                        continue
                      
                else: 
                    
                    request_text = input_text.lower()

                    if "that's all" in request_text:
                                               
                        log_activity(f"You: {request_text}\n")
                        
                        record_to_file("Bye now")
                        
                        log_activity(f"AI: Bye now. \n")                        

                        print('Bye now')
                        
                        is_sleeping = True
                        continue
                    
                    if "vocal signal" in request_text:
                        request_text = request_text.split("vocal signal")[1]                        

                log_activity(f"You: {request_text}\n ")

                print(f"You: {request_text}\n AI: ", end='')

                text_queue = queue.Queue()
                audio_queue = queue.Queue()
                
                llama_finished = threading.Event()                
                data_available = threading.Event() 
                text_done = threading.Event() 
                busy_now = threading.Event()
                stop_event = threading.Event()                
     
                llama_thread = threading.Thread(target=chat_with_llama, args=(request_text, text_queue, llama_finished,))
                tts_thread = threading.Thread(target=text_to_sound, args=(text_queue, text_done, llama_finished, audio_queue, stop_event,))
                play_thread = threading.Thread(target=play_audio_from_queue, args=(audio_queue, text_done, stop_event,))
 
                llama_thread.start()
                tts_thread.start()
                play_thread.start()

                llama_finished.wait()

                llama_thread.join()  
                time.sleep(0.5)
                audio_queue.join()
              
                stop_event.set()  
                tts_thread.join()
 
                play_thread.join()  

                num_user_requests = 0 
                num_tts_conversions = 0 
                num_audio_playbacks = 0
 
                print('\n')
 
            except Exception as e:
                continue 
 
if __name__ == "__main__":
    start()
