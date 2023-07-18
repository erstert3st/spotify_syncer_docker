# spotify_sync_docker_with_flac

**spotify_Syncer with downloads FLAC files, but you need your own captcha solution!**

## To-Do 
remove commits from fork!

Cleanup file hierarchy

add logger

## Features:
- Runs `spotify_sync` CLI continuously in Docker and downloads specific FLAC files
- Also runs on ARM64

## Requirements:
- Docker

## Installation:
1. Create your `config.json` file similar to the one in [spotify_sync](https://github.com/jbh-cloud/spotify_sync).
2. Set up your own captcha solution.
3. Build the Docker image.


### Disclaimer

This tool was written for educational purposes. I will not be responsible if you use this program in bad faith. By using it, you are accepting the [Deezer Terms of Use](https://www.deezer.com/legal/cgu).
    spotify_sync is not affiliated with Deezer.
