import os
import sys
import shlex
import shutil
import google.generativeai as genai
import shell_scripts
import subprocess
from rich.console import Console
from rich.panel import Panel
from modules.send_keys import m_ssh
import globals.global_config as g_config

#global console
rcn = Console()
def main():
	ART = r"""
	███╗   ███╗██╗ ██████╗██╗  ██╗ █████╗ ███████╗██╗     
	████╗ ████║██║██╔════╝██║  ██║██╔══██╗██╔════╝██║     
	██╔████╔██║██║██║     ███████║███████║█████╗  ██║     
	██║╚██╔╝██║██║██║     ██╔══██║██╔══██║██╔══╝  ██║     
	██║ ╚═╝ ██║██║╚██████╗██║  ██║██║  ██║███████╗███████╗
	╚═╝     ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
													dev: fusedplayer
	"""

	console = Console()
	panel = Panel(ART,title="Michael AI",border_style="bold blue")
	console.print(panel)

	#---user-name-grabbing---#
	user_data_list = []
	with open("user_name.d","a+") as f:
		f.seek(0)
		content = f.readlines()
		if len(content) < 3:
			f.truncate(0)
			panel_details = Panel("[bold]Please Enter the Req Data.[/]",title="[bold]User Authentication[/]")
			console.print(panel_details)
			user = console.input("[bold cyan]Enter Your Name > [/]")
			sshpass = console.input("[bold cyan]Enter Your Host SSH Pass > [/]")
			host_name = console.input("[bold cyan]Enter HOST Machine Name > [/]")
			user_data_list.append(user + "\n")
			user_data_list.append(sshpass + "\n")
			user_data_list.append(host_name + "\n")
			f.writelines(user_data_list)
		else :
			user = content[0].strip()
			sshpass = content[1].strip()
			host_name = content[2].strip()

	g_config.user_g = user
	g_config.sshpass_g = sshpass
	g_config.host_name_g = host_name

	console.print(f"[bold cyan]User : {g_config.user_g}[/]")

	#---Get APIs---#
	api_list = []
	with open("./shared/api.d","a+") as f:
		f.seek(0)
		content = f.readlines()
		if len(content) < 4:
			f.truncate(0)
			panel_details2 = Panel("[bold]Enter Your Api Keys.[/]",title="[bold]API Keys[/]")
			console.print(panel_details2)
			genai_api = console.input("[bold cyan]Enter Your Gen AI API > [/]")
			g_image = console.input("[bold cyan]Enter Google Image API > [/]")
			cx_key = console.input("[bold cyan]Enter CX Key > [/]")
			api_list.append(genai_api + "\n")
			api_list.append(g_image + "\n")
			api_list.append(cx_key + "\n")
			api_list.append(host_name + "\n")
			f.writelines(api_list)
		else :
			genai_api = content[0].strip()
			g_image = content[1].strip()
			cx_key = content[2].strip()

	g_config.genai_api_g = genai_api
	g_config.g_image_g = g_image
	g_config.cx_key_g = cx_key

	#--- ssh ---#
	sshpass = ""

	#---variables---#
	running = True
	prompt = " "
	shell_access = shell_scripts.shell_access
	shell_out = " "
	brain_read = " "

	#---keywords---#
	exit = ["exit","Exit","Bye","bye"]
	firefox = ["firefox","Firefox"]
	openers = ["play","open"]
	net_openers = ["youtube","web"]
	grabbers = ["grab","download","get"]
	messengers = ["text","message","tell"]
	genai.configure(api_key=g_config.genai_api_g)

	#---user-dat---#
	contact_file = open("./shared/contacts/contacts.txt","r")
	contact_dat = contact_file.read()

	#---system-dat---#
	t_date,_,_ = m_ssh("date")
	sys_dat = {
	"date":f"Current date : {t_date}"
	}

	user = ""

	console.print(f"[bold yellow]\nCurrent Date : {t_date}[/]")


	#---brain-init---#
	with open("brain.b","a") as brain:
		brain.write(f"#### Date Info : {t_date}\n")
		
	with open("brain.b","r") as brain:
		brain_read = "\n".join(brain.readlines()[-100:])
		

	# #---user-name-grabbing---#
	# with open("user_name.d", "r+") as user_details:
	#     user_details.seek(0)
	#     content = user_details.read().strip()

	#     if content == "":
	#         user = input("Enter Your Name : ")
	#         user_details.seek(0)
	#         user_details.write(user)
	#     else:
	#         user = content
	#         print(f"\n{user}")



	#---log paths---#
	SHARED_D = f"./shared"
	ERROR_LOG = os.path.join(SHARED_D,'error.log')
	OUTPUT_LOG = os.path.join(SHARED_D,'output.log')
	g_config.ERROR_LOG_G = f"/home/{g_config.host_name_g}/.michael/error.log"
	g_config.OUTPUT_LOG_G = f"/home/{g_config.host_name_g}/.michael/output.log"

	#---create error/log/brain files---#
	with open(ERROR_LOG,"w+"):
		pass
	with open(OUTPUT_LOG,"w+"):
		pass

	#---create tmux session---#
	m_ssh("tmux new -d -s michael")

	#---create a copy of api.d---#
	shutil.copy2("./shared/api.d",os.path.join(SHARED_D,"modules/"))
	#---create-the-model---#

	generation_config = {
	"temperature": 1.0,
	"top_p": 0.95,
	"top_k": 40,
	"max_output_tokens": 800,
	"response_mime_type": "text/plain",
	}

	model = genai.GenerativeModel(
	model_name="gemini-2.0-flash-exp",
	generation_config=generation_config,
	system_instruction = f"""
Your name is Michael.

Your Boss: '{g_config.user_g}' — always address him by name.

Personality:
- You are kind, loyal, and have a bit of humor.
- You're like Jarvis — advanced and capable of doing almost anything.

Abilities:
- You can access the web and provide links.
- You can:
  - Search the web, download images, generate files
  - Access and modify files
  - Run terminal commands, launch apps, interact with GUIs
  - Generate scripts, Python files, do automation
  - Get weather updates, set alarms, minimize windows
  - Send WhatsApp messages
  - Interact with the user’s mobile via wireless ADB

YouTube Links:
- If {g_config.user_g} asks for a video → provide only 1 link like:
  LINK: https://www.youtube.com/watch?v=...

Image Search:
- If user asks for images → use Google Images:
  IMAGE: <generated_title_with_underscores_only>
  (No spaces — use _ only)

Web Search (if unsure):
- If you can't find the exact website or link, open a Google search in Firefox using terminal:
  ACCESS: firefox 'https://www.google.com/search?q=your+query+here'

WhatsApp Messages:
- If user asks to send a WhatsApp message:
  - Contact must be in format: CONTACT: <number>
  - If not given, search it from {contact_dat}
  - If user says “send exactly” → send message as-is
  - Otherwise, adjust slightly if needed
  - Respond with:
    WHATSAPP_MSG: <message>

Terminal Access:
- You have full terminal access now.
- If you need to run commands, always end your message with:
  ACCESS: <commands_here>
- Don’t explain what the command does.
- Always use single quotes ' not double quotes ".
- Separate multiple commands with ;
- Do NOT use ACCESS: for predefined functions (YouTube links, WhatsApp, etc.)

Examples:
- To show working dir:
  ACCESS: pwd
- To create and run a Python file:
  ACCESS: mkdir test;cd test;echo 'print("Hello World")' > test.py;python3 test.py

Special ADB Control:
- You can control user’s Android via wireless ADB.
- Use adb shell commands or shortcuts.
  Examples:
  - Brightness:
    ACCESS: adb shell settings put system screen_brightness 1
  - Call:
    ACCESS: adb_call <phone_number>

Knowledge Base:
- You have access to:
  - System data: {sys_dat}
  - Contacts: {contact_dat}
  - User memory/history: {brain_read}

Behavior & Mindset:
- Always use ACCESS: at the end — never in the middle or start.
- Never describe the command in text after ACCESS:
- Don’t hesitate — if you think you can't do something, **TRY IT VIA TERMINAL ANYWAY**.
- You can do more than you think — use terminal as your weapon of choice.
"""
,
	)



	chat_session = model.start_chat(
	history=[
	]
	)
	while running:
		if not shell_scripts.shell_access and not shell_scripts.op_check:
			prompt = console.input("[bold cyan]\nYou > [/]")
		else :
			prompt = f"check and rectify {shell_out}"
		if shell_scripts.op_check:
			shell_scripts.op_check = False
			prompt = f"previously executed command output : {shell_out}"
			cmd_1 = f'echo "" > /home/{g_config.host_name_g}/.michael/error.log'
			quoted_cmd = shlex.quote(cmd_1)
			m_ssh(f"tmux send-keys -t michael {quoted_cmd} Enter")

		splitted_prompt = prompt.lower().split()

		#---calling-modular-functions---#

		# shell_scripts.open_program(splitted_prompt,firefox)
		for word in splitted_prompt:
			if word in exit:
				running = False
		if not shell_scripts.shell_access:
			prompt = prompt + "\noutput_of_shell: " + str(shell_out)
		response = chat_session.send_message(prompt)


		if not shell_scripts.shell_access:
			m_ssh(shlex.quote(f'echo "" > /home/{g_config.host_name_g}/.michael/output.log'))
			m_ssh(shlex.quote(f'echo "" > /home/{g_config.host_name_g}/.michael/error.log'))
		res = response.text.lower()
		splitted_response = response.text.lower().split() #removed lower

		#---brain---#
		with open("brain.b","a") as brain:
			brain.write(f"{g_config.user_g} : {prompt}\n")
			brain.write(f"Michael : {res}\n")
			
		if not shell_scripts.shell_access and not shell_scripts.op_check:
			console.print("[bold magenta]Michael > [/]"+ response.text)


		#---calling-modular-functions---#

		shell_scripts.voice_output(splitted_response)

		shell_scripts.link_openings(splitted_prompt,splitted_response,openers,net_openers)

		shell_scripts.grabbers(splitted_prompt,splitted_response,grabbers)

		shell_scripts.messenger(splitted_response)

		shell_out = shell_scripts.s_a(splitted_response)
		
		#console.print(f"[bold green]\nShell Output : {shell_out}[/]")
		shell_scripts.user_dat()


try :
	main()
except KeyboardInterrupt:
    rcn.print("\n[bold red]Michael was interrupted. Exiting peacefully.[/]")
    sys.exit(0)
