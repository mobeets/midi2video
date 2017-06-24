import numpy as np
import mido
import cv2

class VideoManager:
    """
    loads a set of video files,
        and plays each video when a midi key is pressed
    NOTE: no audio
    """
    def __init__(self, fnms, port_name=None, do_loop=True):
        self.fnms = fnms
        self.caps = self.load_all(fnms)
        self.curInd = 0
        self.cap = self.caps[self.curInd]
        self.not_done = True
        self.do_loop = do_loop
        self.port_name = port_name
        self.inport = mido.open_input(self.port_name)

    def load_all(self, fnms):
        return [cv2.VideoCapture(fnm) for fnm in fnms]

    def loop(self):
        self.show()
        self.check_midipress()
        self.not_done = self.check_keypress()

    def show(self):
        if not self.cap.isOpened():
            return
        not_at_end, frame = self.cap.read()
        if not_at_end:
            cv2.imshow('frame', frame)
        elif self.do_loop: # restart video
            self.cap.set(0, 0)

    def check_midipress(self):
        msg = self.inport.poll()
        if msg is None:
            return True
        if msg.type != 'note_on':
            return True
        self.curInd = msg.note % len(self.caps)
        self.cap = self.caps[self.curInd]
        self.cap.set(0,0)
        return True

    def check_keypress(self):
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'): # quit
            return False
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for cap in self.caps:
            cap.release()
        cv2.destroyAllWindows()
        self.inport.close()

def main(fnms):
    ports = mido.get_input_names()
    if len(ports) == 0:
        print "No midi ports found."
        return
    print "(Press a midi key to change the video, and 'q' to quit)"
    with VideoManager(fnms) as M:
        while M.not_done:
            M.loop()

if __name__ == '__main__':
    main(['data/CatsA.mp4', 'data/CatsB.mp4', 'data/CatsC.mp4'])
