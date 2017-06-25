import time
import glob
import argparse
import threading
import mido
import numpy as np
import pygame as pg
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip

pg.init()
pg.display.set_caption('midi2movie')

def is_midi_change_msg(msg, msgtype='note_on'):
    return msg is not None and msg.type == msgtype

def is_midi_quit_msg(msg, quitnote):
    return is_midi_change_msg(msg) and msg.note == quitnote

def imdisplay(imarray, screen=None):
    """
    Splashes the given image array on the given pygame screen
    src: https://github.com/Zulko/moviepy/blob/master/moviepy/video/io/preview.py
    """
    a = pg.surfarray.make_surface(imarray.swapaxes(0, 1))
    if screen is None:
        screen = pg.display.set_mode(imarray.shape[:2][::-1])
    screen.blit(a, (0, 0))
    pg.display.flip()

def preview(clip, inport=None, quitnote=None, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000, audio_nbytes=2):
    """
    src: https://github.com/Zulko/moviepy/blob/master/moviepy/video/io/preview.py
    """
    import pygame as pg    

    # compute and splash the first image
    screen = pg.display.set_mode(clip.size)
    audio = audio and (clip.audio is not None)

    if audio:
        # sound will be played in parrallel
        # two synchro-flags to tell whether audio and video are ready
        videoFlag = threading.Event()
        audioFlag = threading.Event()
        # launch the thread
        audiothread = threading.Thread(target=clip.audio.preview,
            args=(audio_fps,audio_buffersize, audio_nbytes,
                    audioFlag, videoFlag))
        audiothread.start()
    
    img = clip.get_frame(0)
    imdisplay(img, screen)
    if audio: # synchronize with audio
        videoFlag.set() # say to the audio: video is ready
        audioFlag.wait() # wait for the audio to be ready
        
    t0 = time.time()
    ti = 0
    t = 1.0/fps
    clips = [c.copy() for c in clip.clips]
    nclips = len(clips)
    for i in xrange(nclips): # start with all clips hidden
        clip.clips[i] = clips[i].subclip(0, 0).copy()
    while True:
        t += 1.0/fps
        for event in pg.event.get():
            continue
        for msg in inport.iter_pending():
            if is_midi_change_msg(msg, 'note_on'): # play clip                
                ci = msg.note % nclips
                clip.clips[ci] = clips[ci].set_start(t).copy()
            elif is_midi_change_msg(msg, 'note_off'): # hide clip                
                ci = msg.note % nclips
                clip.clips[ci] = clips[ci].subclip(0, 0).copy()
            if is_midi_quit_msg(msg, quitnote):
                return msg
        img = clip.get_frame(t)
        t1 = time.time()
        time.sleep(max(0, t - (t1-t0)))
        imdisplay(img, screen)
    return None

def make_clip_grid(clips, ncols, nrows, width=300, height=300):
    """
    http://zulko.github.io/moviepy/getting_started/compositing.html
    """
    cur_clips = []
    c = 0
    for px in np.arange(0.0, 1.0, 1.0/ncols):
        for py in np.arange(0.0, 1.0, 1.0/nrows):
            cur_clip = clips[c]
            cur_clip = cur_clip.resize(width=width) # fit within grid cell
            cur_clip = cur_clip.set_pos((px, py), relative=True) # place in grid
            cur_clips.append(cur_clip.loop()) # must loop given midi handling
            c += 1
    return CompositeVideoClip(cur_clips, size=(ncols*width, nrows*height))

def main(fnms, play_audio=False, port_name=None, quitnote=50):
    """
    plays clips in a grid, where each can start and stop
        independently based on which midi note is being pressed
        i.e., clips play as long as that key is being pressed
    """
    clips = [VideoFileClip(fnm) for fnm in fnms]
    nrows = np.floor(np.sqrt(len(clips))).astype(int)
    ncols = np.ceil(len(clips)*1.0 / nrows).astype(int)
    clip = make_clip_grid(clips, ncols, nrows)
    msg = None
    with mido.open_input(port_name) as inport:
        while not is_midi_quit_msg(msg, quitnote):
            msg = preview(clip, inport, audio=play_audio, quitnote=quitnote)

if __name__ == '__main__':
    ports = mido.get_input_names()
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", action="store_true", 
        help="play audio along with video")
    parser.add_argument("--portname", type=str, 
        help="name of midi port (optional)", choices=ports)
    parser.add_argument("--quitnote", type=int,
        default=50, help="which midi note to quit on")
    args = parser.parse_args()

    if len(ports) == 0:
        print "No midi controllers found."
    else:
        print "Play a note on a midi controller to get started!"
        print "(To quit, play midi note {})".format(args.quitnote)
        fnms = glob.glob('data/*.mp4')
        main(fnms, play_audio=args.audio, port_name=args.portname, quitnote=args.quitnote)
