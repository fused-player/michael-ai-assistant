import shlex
import subprocess
import globals.global_config as config


def m_ssh(command):
    
    ROOT_W = f"sshpass -p {shlex.quote(config.sshpass_g)} ssh -o StrictHostKeyChecking=accept-new {config.host_name_g}@172.17.0.1 source /home/{config.host_name_g}/.michael/venv/bin/activate && {shlex.quote(command)}"
    cmd = subprocess.run(shlex.split(ROOT_W),capture_output=True)

    return cmd.stdout , cmd.stderr , cmd.returncode