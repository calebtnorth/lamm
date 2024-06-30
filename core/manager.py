# LANMM Media Manager
# Interface with the player to create and manage audio threads

from random import shuffle
from util import FileUtil
from core.player import AudioPlayer

class MediaManager:
    # Class-wide reference to the thread ensures duplicate threads
    # are not created accidentally and the living thread can be controlled
    media_thread:AudioPlayer    = None
    random_queue:bool           = False

    # Start a new thread for music 
    @staticmethod
    def start_media() -> str:
        if MediaManager.media_thread and MediaManager.media_thread.playing:
            return "Media is already playing"

        # Shuffle if need be
        queue = FileUtil.dump_uploads()
        if MediaManager.random_queue:
            shuffle(queue)

        # Check if queue is empty
        if not queue:
            return "Upload music"

        # Delete the old thread and replace the media_thread reference
        # with a new AudioPlayer object with a new queue
        if MediaManager.media_thread:
             MediaManager.media_thread.kill_thread()
        MediaManager.media_thread = AudioPlayer(queue)
        MediaManager.media_thread.start()

        return "Music started"

    # Stop the music
    @staticmethod
    def stop_media() -> str:
        if not MediaManager.media_thread:
            return "No media to stop"
        MediaManager.media_thread.kill_thread()
        MediaManager.media_thread = None

        return "Media stopped"

    # Pause / unpause the music
    @staticmethod
    def pause_media():
        if not MediaManager.media_thread:
            return
        

    # Merge the thread into the main thread. This should only be called when
    # the software is being shut down
    @staticmethod
    def cleanup():
        if not MediaManager.media_thread:
            return
        MediaManager.media_thread.kill_thread()
        MediaManager.media_thread.join()

    # Stop the current song and modify the index of the player.
    # Returns a bool to indicate the success of the method call
    @staticmethod
    def forward_queue() -> str:
        thread = MediaManager.media_thread

        # Make sure thread exists and the music isn't already playing
        if not MediaManager.is_playing():
            return "Media is not playing"
        
        # Push index forward
        thread.kill_subprocess()
        return "Skipped forward"

    @staticmethod
    def reverse_queue():
        thread = MediaManager.media_thread

        # Make sure the music isn't already playing
        if not MediaManager.is_playing():
            return "Media is not playing"
        
        # Push index back. It's okay for the index to go negative because
        # that mimics looping around to zero anyway, and the loop advancing
        # normally will eventually work out any negative indexes
        thread.kill_subprocess()
        thread.index -= 2
        return "Skipped back"
    
    @staticmethod
    def is_playing() -> bool:
        if not MediaManager.media_thread:
            return False
        return MediaManager.media_thread.playing
    
    # Determines if the Thead exists or not
    @staticmethod
    def is_real() -> bool:
        return not MediaManager.media_thread == None