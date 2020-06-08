import numpy as n
import glob
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import re

def upload_file(fname):
    token=open("dropbox.key").readlines()[0].strip()

    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(token)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError:
        sys.exit("ERROR: Invalid access token; try re-generating an "
                 "access token from the app console on the web.")
        
    with open(fname, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + fname + " to Dropbox as " + "/"+fname + "...")
        try:
            dbx.files_upload(f.read(), "/"+fname, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
            else:
                print(err)
                


if __name__ == "__main__":
    upload_file("vs/2020-06-08/2020-06-08.mp4")
    
