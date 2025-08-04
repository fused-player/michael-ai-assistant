import subprocess 
import torch
import os
from TTS.api import TTS
import pygame
import time
import shlex
from pydub import AudioSegment
import globals.global_config as g_config
from modules.send_keys import m_ssh
from modules.audio_effects import bass_boost
from rich.console import Console
from rich.progress import track

console = Console()
os.environ["TTS_CACHE_DIR"] = "models/tts"

op_check = False
shell_access = False

# def open_program(splitted_prompt,firefox):
# 	for word in splitted_prompt:
# 		if word in firefox:
# 			m_ssh("sleep 1")
# 			m_ssh(f'tmux send-keys -t michael "firefox" C-m')



def link_openings(splitted_prompt, splitted_response, openers, link_openers):
    case1 = False
    case2 = False
    actual_link = ""
    
    for index, word in track(enumerate(splitted_response),description="Checking for Links..."):
        if word == "link:":
            actual_link = splitted_response[index + 1]
    
    for word in splitted_prompt:
        if not case1 and word in openers:
            case1 = True
        if not case2 and word in link_openers:
            case2 = True

    if case1 and case2 and actual_link:
        m_ssh("sleep 3")
        inner_cmd = f'firefox --new-window {actual_link}'
        quoted_cmd = shlex.quote(inner_cmd)
        m_ssh(f"tmux send-keys -t michael {quoted_cmd} C-m")


def voice_output(splitted_response):
	import pygame
	pygame.init()
	pygame.mixer.init()

	for index,word in track(enumerate(splitted_response),description="Preparing Voice..."):
		if word == "link:":
			splitted_response = splitted_response[0:index]
	for index,word in enumerate(splitted_response):
		if word == "image:":
			splitted_response = splitted_response[0:index]

	response = ' '.join(splitted_response)
	device = "cuda" if torch.cuda.is_available() else "cpu"

	tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)

	tts.tts_to_file(response, speaker_wav="audio/clone/audio.wav", language = "en",file_path="audio/m_temp/output.wav",stability = 1)
	# Load audio file (Conqui output)
	audio = AudioSegment.from_file("audio/m_temp/output.wav")

	# Apply bass boost
	bass_audio = bass_boost(audio, boost_db=15, cutoff_freq=120)

	# Save or play the new audio
	bass_audio.export("audio/m_temp/output_bass.wav", format="wav")

	pygame.mixer.music.load("audio/m_temp/output_bass.wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(10)

def grabbers(splitted_prompt,splitted_response,grabbers):
	case1 = False
	case2 = False
	for index,word in track(enumerate(splitted_response),description="Checking for Image Requests..."):
		if word == "link:":
			splitted_response = splitted_response[0:index]
	for index,word in enumerate(splitted_response):
		if word == "image:":
			cooked_query = splitted_response[index + 1:]

			for index,word in enumerate(splitted_prompt):
				if word in grabbers:
					case1 = True
				if word == "few":
					case2 = True

	if case1 and not case2:
		m_ssh(f"python3 ./michael/modules/i_grabber.py 'one' {cooked_query}")
	elif case1 and case2:
		m_ssh(f"python3 ./michael/modules/i_grabber.py 'few' {cooked_query}")


def messenger(splitted_response):
    contact_number = None
    message_tokens = []
    capturing = False

    for word in track(splitted_response,description="Checking for Message Requests..."):
        if word == "whatsapp_msg:":
            capturing = True
            continue
        elif word == "contact:":
            capturing = False
            continue

        if capturing:
            message_tokens.append(word)
        elif word.startswith("+"):
            contact_number = word

    if contact_number and message_tokens:
        message = ' '.join(message_tokens)
        quoted_message = shlex.quote(message)
        console.print(f"[bold green]Contact[/]: {contact_number}")
        console.print(f"[bold green]Message[/]: {message}")
        m_ssh(f"python3 /home/{g_config.host_name_g}/.michael/modules/m_messenger.py 'whatsapp' {contact_number} {quoted_message}")


def user_dat():
	print(" ")
	#with open("data/contacts/c_dat.vcf","r") as contact_info:
		#print(contact_info.read())


def s_a(sr):
	global shell_access,op_check
	for index,word in track(enumerate(sr),description="Processing commands..."):
		if word == "access:":
			sr = sr[index+1:]
			sr = ' '.join(sr)

			
			console.print(f'[bold bright_red]\nexec cmd :[/] {sr}')
			log_command = f"{sr} 2> {g_config.ERROR_LOG_G}"
			m_ssh(f'tmux send-keys -t michael {shlex.quote(log_command)} C-m')
			m_ssh(f'bash -c {shlex.quote(f"tmux capture-pane -t michael -S- -p > {g_config.OUTPUT_LOG_G}")}')

			with open(f"./shared/error.log","r") as temp:
				if not temp.readline() == "":
					shell_access = True
					op_check = False
					e_file = open("./shared/error.log")
					e_dat = e_file.read()
					return e_dat
				else:
					shell_access = False
					op_check = True
					f_file = open("./shared/output.log")
					f_dat = f_file.read().strip()
					return f_dat
