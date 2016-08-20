"""Internet-related functions."""

import application, wx, os, os.path
from requests import get
from lyricscraper import lyrics
from .util import prune_library

def download_track(url, path):
 """Download URL to path."""
 response = get(url)
 folder = os.path.dirname(path)
 if not os.path.isdir(folder):
  os.makedirs(folder)
 with open(path, 'wb') as f:
  application.library_size += f.write(response.content)
 wx.CallAfter(prune_library) # Delete old tracks if necessry.

def get_lyrics(track):
 """Get the lyrics of the provided track."""
 return lyrics.get_lyrics(track.artist, track.title)
