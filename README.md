
Play videos using a midi controller. Example application: [cat piano](http://mobeets.github.io/made/cat-piano).

__How it works: midi2video__:

Running `python midi2video.py` loads up all `.mp4` files in `data/`, and plays one of them each time you play a note on a connected midi controller.

Options:

* Play audio: `--audio`
* Loop video: `--loop`
* Midi note to quit: `--quitnote 50`

__How it works: midi2video2__:

Running `python midi2video2.py` arranges clips in a grid, and plays each clip as long as the corresponding midi note is being played. Audio is not an option here.

Options:

* Size of each video: `--size 150`
* Midi note to quit: `--quitnote 50`
* Mapfile for specifying video rotation and pad order: `--mapfile video_map.yml`

__Install requirements__: `pip install -r requirements.txt`
