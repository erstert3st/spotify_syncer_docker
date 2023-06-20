import pytest
from flac.flaccer import Flaccer

from spotify_sync.cli import SpotifySyncApp

app = SpotifySyncApp()
app.sync_spotify()


# def test_login():
#     print("start test:")

def test_copy():
    print("start test:")

def test_spotify_sync_login():
    print("start test:")

def test_spotify_sync_authorize(): #
    print("start test:")


# def test_spotify_sync_dry_run(): #
#     print("start test:")

def test_download_flac():
    print("start test:")



if __name__ == "__main__":
    pytest.main(["tests.py"])