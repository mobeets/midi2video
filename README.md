
Play videos using a midi controller.

__How it works__:

Running `python midi2video.py` loads up all `.mp4` files in `data/`, and plays one of them on loop. If you have a midi controller plugged in, pressing different notes will change the video being played.

Options:

* Play audio: `--audio`
* Loop video: `--loop`
* Midi note to quit: `--quitnote 50`

__Requirements__:

- `mido`
- `pygame`
- `moviepy`
