
Play videos using a midi controller.

__How it works__:

Running `python midi2video.py` loads up all `.mp4` files in `data/`, and plays one of them on loop. If you have a midi controller plugged in, pressing different notes will change the video being played.

Note: The audio is not played. :(

__Requirements__:

- `opencv` with ffmpeg (osx install help [here](https://github.com/Homebrew/homebrew-science/issues/2862#issuecomment-219263259))
- `mido` (`pip install mido`)
