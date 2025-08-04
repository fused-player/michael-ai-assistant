# Michael AI - Dockerized Personal AI Assistant

Michael is a self-contained AI assistant packaged in a Docker image, designed to run on Linux systems with access to audio, automation tools, and shared host files. This setup allows for easy deployment across multiple machines.Based on gemini.

## NOTE

- Get your Gemini API from [here](https://aistudio.google.com/apikey)
- If you want the image grabbing feature you need follow the steps.
  1. get the custom search (api)key from [here](https://developers.google.com/custom-search/v1/introduction/?apix=true). click on get a key.
  2. get the cx key from [here](https://programmablesearchengine.google.com/controlpanel/all). select add and copy the search engine id.
- All the Above mentioned process will be simplified in upcoming releases. an alternative will be implemented.

## System Requirements

- Linux (Wayland or X11)
- Docker installed and running
- `tmux`, `ydotool`, `ydotoold` installed
- User added to the `docker` and `input` groups



## 1. Pull the Docker Image

```bash
docker pull fusedplayer49/michael_ai:latest
```



## 2. Create the Docker Container

```bash
docker create --name michael   -v /home/$USER/.michael:/usr/local/app/shared   --privileged=true   -e XDG_RUNTIME_DIR=/tmp/xdg  --device=/dev/snd:/dev/snd   -it fusedplayer49/michael_ai:latest

```

Note: The `.michael` directory will be automatically created later by the installer if not present.



## 3. Clone the Repository

```bash
git clone https://github.com/fused-player/michael-ai-assistant.git
cd michael-ai-assistant
```



## 4. Run the Host Installer

```bash
chmod +x install.sh
./install.sh
```

This script sets up required host-side files and integrations with your user environment.



## 5. Install Host Utilities

Ensure the following packages are installed:

```bash
sudo apt install tmux ydotool ydotoold openssh-server
```
start and enable ssh service:

```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```

Add your user to the `input` group to allow low-level device input access:

```bash
sudo usermod -aG input $USER
```

Then reboot your system:

```bash
reboot
```



## 6. Start the Container

After reboot, you can start Michael using one of the following methods:

Using the provided script:

```bash
./start_michael.sh
```

Or directly via Docker:

```bash
docker start -ai michael
```



## 7. Additional Notes

- The `.michael` directory on your host is used to persist shared data between the container and your system.
- The setup handles most dependencies automatically.

## 8. Initial Usage

- Initially Your Asked to enter some deatils along with API keys.
- Your Name --> The name you want your ai to call you.
- Host SSH pass --> Enter your (machine's) user's pass.
- Host Machine Name --> your current session username.
- All the Above details are used only for communication between docker container and host. only your name is passed to AI not the Password.

## License

MIT License
