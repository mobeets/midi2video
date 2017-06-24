
Play videos using a midi controller.

__How it works__:

Running `python midi2video.py` loads up all `.mp4` files in `data/`, and plays one of them each time you play a note on a connected midi controller.

Options:

* Play audio: `--audio`
* Loop video: `--loop`
* Midi note to quit: `--quitnote 50`

__Requirements__:

- `pip install mido`
- `pip install pygame`
- `pip install moviepy`
