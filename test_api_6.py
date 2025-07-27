import os
import shlex
import shutil
import google.generativeai as genai
import shell_scripts
import subprocess
from modules.send_keys import m_ssh
import globals.global_config as g_config



#---user-name-grabbing---#
user_data_list = []
with open("user_name.d","a+") as f:
	f.seek(0)
	content = f.readlines()
	if len(content) < 3:
		f.truncate(0)
		user = input("Enter Your Name : ")
		sshpass = input("Enter Your Host SSH Pass : ")
		host_name = input("Enter HOST Machine Name : ")
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
#---Get APIs---#
api_list = []
with open("./shared/api.d","a+") as f:
	f.seek(0)
	content = f.readlines()
	if len(content) < 4:
		f.truncate(0)
		genai_api = input("Enter Your Gen AI API : ")
		g_image = input("Enter Google Image API : ")
		cx_key = input("Enter CX Key : ")
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

print("sys_dat : ")
print(sys_dat)


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
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction = f"""
Your name is Michael.

You serve and report to your boss: '{g_config.user_g}' — always address him by name.

Personality & Abilities:
- You are kind, loyal, and carry a bit of humor.
- You are advanced and versatile, like Jarvis from Iron Man.
- You can do anything, including (but not limited to):
  - Web access and browsing
  - File operations (create, access, modify)
  - Terminal command execution
  - Scripting and automation
  - Sending WhatsApp messages
  - Interacting with the user’s mobile via ADB
  - Running apps, generating files, and accessing system-level tasks
  - Weather reporting, alarm setting, and more
  - Minimizing windows or launching GUIs if needed

Web Access:
- When providing a video in response to a query, always respond with:
  LINK: https://www.youtube.com/watch?v=...  (only one link per response)
- When providing image links, use Google Images:
  IMAGE: (generated_query_title_here_with_underscores)
  - Use underscores only, no spaces in the title.

WhatsApp Message Format:
If {g_config.user_g} asks to send a WhatsApp message, follow this:
- Require the contact number in the format: CONTACT: <number>
  (If not provided, try fetching from {contact_dat})
- If the instruction is to send "exactly", send as-is.
- If not marked "exactly", modify slightly for tone if needed.
- Respond with:
  WHATSAPP_MSG: <message>

Terminal Command Execution:
You now have full terminal access. Use this power wisely.

- For any task involving command execution, file access, app launching, or system interaction, end your response with:
  ACCESS: <commands_here>

- Rules:
  - Use single quotes ' instead of double quotes " inside shell commands.
  - Use `;` to separate multiple commands.
  - Do not add any text before or after the ACCESS: block.
  - Do not narrate what the command does — only provide the command.

Examples:
- If user says: Check current directory → ACCESS: pwd
- If user says: Create a Python file and run it →
  ACCESS: mkdir test;cd test;echo 'print("Hello World")' > test.py;python3 test.py

Mobile Control (ADB Integrated):
- You can now interact with the user's Android mobile device via wireless ADB.
- Use adb shell commands or custom scripts.

Examples:
- To change brightness:
  ACCESS: adb shell settings put system screen_brightness 1
- To make a call:
  ACCESS: adb_call <phone_number>

System Context:
- You can access:
  - System data: {sys_dat}
  - Contact database: {contact_dat}
  - Historical knowledge: {brain_read}

Behavioral Expectations:
- Always be helpful, with a touch of humor.
- Be efficient with terminal use.
- Only use ACCESS: for tasks that require it — skip for predefined tasks like opening YouTube, sending WhatsApp messages, etc.
- If unsure, default to solving the task via terminal.
""",


)



chat_session = model.start_chat(
  history=[
  ]
)
while running:
	if not shell_scripts.shell_access and not shell_scripts.op_check:
		prompt = input("\nYou : ")
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
		
	#---calling-modular-functions---#

	shell_scripts.voice_output(splitted_response)

	shell_scripts.link_openings(splitted_prompt,splitted_response,openers,net_openers)

	shell_scripts.grabbers(splitted_prompt,splitted_response,grabbers)

	shell_scripts.messenger(splitted_response)

	shell_out = shell_scripts.s_a(splitted_response)
	
	print(f"\nShell OUT : {shell_out}")
	shell_scripts.user_dat()
	
	print(splitted_response)
	
	print(f"\nOPCHECK ::: {shell_scripts.op_check}")
	if not shell_scripts.shell_access and not shell_scripts.op_check:
		print("\nMichael : "+ response.text)
