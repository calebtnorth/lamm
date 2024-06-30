# LANMM (LAN Media Manager) Front Page
# The web dashboard to control the audio player.

from flask import (
    Flask, Request, Response,                   # Classes
    render_template_string, flash, redirect,    # Functions
    request                                     # Variables
)
from os import path, urandom
from core import MediaManager
from util import FileUtil

# Create the web framework object and specify where it should save all the 
# uploaded audio files. Limit max upload size to 100 megabytes (roughly 10min)
# The secret key has to do with flashes and security. Don't touch it, it's needed
app:Flask                       = Flask(__name__)
app.config["MAX_CONTENT_PATH"]  = 100_000_000
app.config["SECRET_KEY"]        = urandom(16).hex()

### HOMEPAGE
@app.route("/")
def home() -> str:
    """
    The LANMM Home Page
    """

    # This is not exactly encouraged programming behavior but manually reading
    # the HTML template like this is easier and quicker than "proper" methods.
    # At this scale there is no real downside to doing it this way
    with open("./panel.html") as template:
        return render_template_string(
            template.read(),
            file_list = FileUtil.dump_uploads()
        )

### MEDIA MANAGEMENT
@app.route("/media", methods=["POST"])
def media():
    # If this endpoint is being called without information return to the homepage
    if not request.method == "POST":
        return redirect("/")

    # Same reason as above. The type given by .keys() does not implicitly
    # convert to a list so I have to force it
    buttons:list = list(request.form.to_dict().keys())

    MediaManager.random_queue = bool(request.form.get("random", None))
    
    if "start" in buttons:              flash(MediaManager.start_media())
    if "stop" in buttons:               flash(MediaManager.stop_media())
    if "forward" in buttons:            flash(MediaManager.forward_queue())
    if "previous" in buttons:           flash(MediaManager.reverse_queue())
    # if "pause" in buttons:              MediaManager.pause_media()

    return redirect("/")

### UPLOAD
@app.route("/upload", methods=["POST"])
def upload():
    """
    Given a request object with a track property, save the track to the user defined upload path
    """

    if request.method != "POST":
        return redirect("/")
    
    # All these functions must run without the music playing
    if MediaManager.is_playing():
        flash("Stop media before modifying files")
        return redirect("/")

    # Check if a file got uploaded. The get function's second parameter
    # means .get will return None if the first one cannot be found
    if not request.files.get("track", None):
        flash("Upload an audio file first!")
        redirect("/")

    # Pull the file from the request object and save it to the upload path
    new_track = request.files.get("track")
    track_name = new_track.filename
    new_track.save(
        path.join(FileUtil.upload_path, track_name)
    )

    flash("Uploaded new track!")
    return redirect("/")

### DELETION
@app.route("/delete", methods=["POST"])
def delete():
    """
    Remove a single upload or multiple uploads
    """

    # This should never be True if /delete is called with a post request but it might
    # occur so this acts a fallback and simply redirects the page home
    if not request.form.get("file-list-entry", None):
        redirect("/")

    # Delete the track
    for filename in request.form.getlist("file-list-entry"):
        FileUtil.delete_upload(filename)

    return redirect("/")

### CHECK ARGUMENTS AND RUN APP
if __name__ == "__main__":
    # app.run is followed by this cleanup function because in this context CTRL+C closes 
    # the Flask function and not the entire program, leaving the Thread running alone
    app.run()
    MediaManager.cleanup()