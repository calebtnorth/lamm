# **L**ocal **A**rea **N**etwork **M**usic **M**anager
### What Is It
LANMM is a web app for managing music from across the same network. Also provides the functionality to upload and delete media. It is optimal for retail or other physical storefronts where music is custom, infrequently changed, and frequently played.

### How LANMM Works
LANMM runs off of the Flask framework to provide a web interface, utilizes Python's threading and subprocess modules to manage music, and uses [ffmpeg](https://www.ffmpeg.org/download.html) to play music.

### Setup
- Install ffplay (from ffmpeg)
    - For **Windows**, make sure ffplay is on the PATH
    - For **Linux**, make sure ffplay is installed under /usr/bin
- Create a folder somewhere to store uploaded music to
- Copy the LAMNN repository into its own folder.
- Create a `.upload` file in the root of the LAMNN repo containing *only* the absolute path to the upload folder created two steps ago

From here, LANMM can be run with any WSGI, for example, [Gunicorn](https://gunicorn.org/).
```bash
python -m gunicorn -b 0.0.0.0:8000 wsgi:app
```
If running on **Linux**, ensure the firewall is open to whatever port LANMM is being run on so other devices on the network can see it.