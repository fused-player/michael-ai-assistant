#!/bin/bash
#Michael AI Docker Installation

echo "Doing Some Host Side Work for Michael to Work ..."

mkdir -p /home/$USER/.michael

python3 -m venv /home/$USER/.michael/venv

cp -r ./host_files/* /home/$USER/.michael/

source /home/$USER/.michael/venv/bin/activate && pip install -r /home/$USER/.michael/host_requirements.txt

source /home/$USER/.michael/venv/bin/activate && playwright install firefox

chmod +x initial.sh

sudo bash initial.sh

sudo mv ./modules/adb_call.sh /usr/local/bin/adb_call

echo "Installation Completed !!!,Michael is Ready..."
