#!/usr/bin
# LANMM Audio Player
# Creates# a thread with a subprocess to play downloaded files.
# Relies on ffmpeg to be installed at a system level.

from subprocess import Popen, PIPE
from threading import Thread, enumerate
from os import path
from util import FileUtil
from time import sleep

# Inherit AudioPlayer to override run
class AudioPlayer(Thread):

    # Class-wide reference to the subprocess playing audio to
    # ensure duplicate audio streams are not created
    music_subprocess:Popen      = None

    # Pass in the list of file paths to play through
    def __init__(self, queue:list[str]) -> None:
        Thread.__init__(self)

        # Ensure the thread is killed whenever the program shuts down and
        # does not have to be actively managed while it is alive
        self.daemon                 = True

        # Audio player specific variables
        self.queue:list[str]        = queue
        self.index:int              = 0
        self.playing:bool           = False

    # Override Thread run to start playing music in an infinite loop over
    # the queue until the loop in interrupted or the process is killed
    def run(self):
        # Ensure the queue has a filepath to play from
        if not self.queue:
            return

        self.playing = True
        while self.playing:
            # Create a new subprocess to play the filepath via ffplay. Shell is
            # False as to avoid creating an intermediate shell to run the command
            filepath = path.join(FileUtil.upload_path, self.queue[self.index])
            AudioPlayer.music_subprocess = Popen(
                ["ffplay", f"{filepath}", "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "error"], shell=False
            )
            # Wait until the process is complete
            AudioPlayer.music_subprocess.wait()

            # This is an extremely hacky fix to an issue I do not fully understand. However, it seems that when the software is
            # stopped during the music_subprocess.wait, it immediately proceeds to the next file in the queue before the software
            # has a chance to shut down the thread. As a result some part of this software becomes a zombie and continues to play
            # even though the terminal has already exit. Yet, another CTRL+C will kill it. This sleep somehow fixes that with a delay
            sleep(1)

            # Move forward in the queue or wrap around to the front
            self.index += 1
            if abs(self.index) >= len(self.queue):
                self.index = 0
            
    # Killing an entire thread is complicated, however, killing a subprocess is much easier.
    # This subprocess should not be brought back after being killed, even though it is possible to do so
    def kill_thread(self):
        if AudioPlayer.music_subprocess == None:
            return
        
        self.playing = False
        AudioPlayer.music_subprocess.kill()
        AudioPlayer.music_subprocess = None

    # Stop subprocess alone
    def kill_subprocess(self):
        if not AudioPlayer.music_subprocess:
            return
        AudioPlayer.music_subprocess.kill()

    # def pause_subprocess(self):
    #     AudioPlayer.musi

# Return a count of all living AudioPlayer threads 
def audio_thread_count() -> int:
    return len(
        [thread for thread in enumerate()]# if thread is AudioPlayer]
    )