import os
import sys
import time
import subprocess
from pywaykit import send_msg

type = sys.argv[1]
contact = sys.argv[2]
message = sys.argv[3:]
message = ' '.join(message)
host = os.environ("USER")

if os.path.exists(f"/home/{host}/pywaykit/firefox_whatsapp_profile"):

    send_msg(
        phone_no=contact,
        message=message,
        silent=True
    )
else :
    send_msg(phone_no=contact,message="login",silent=False)