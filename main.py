import pyautogui
import cv2
import numpy as np
import keyboard
import threading
import argparse
import os
from datetime import datetime


def exit_handler():
    global STOP
    STOP = True


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Records screen and store it in mp4 format with 20 fps by default. \
            Recordings can be found at recordings folder in relative path. \
                Press ctrl+alt+s to STOP recording ')
    parser.add_argument('--output', dest='output',
                        required=False, help="target file name   <<OPTIONAL>>")
    parser.add_argument('--audio', dest='audio', action='store_true',
                        help='Boolean flag for including Audio in the Recording')
    parser.add_argument('--cam', dest='cam', action='store_true',
                        help='Boolean flag for including Camera feed in the Recording')
    return parser.parse_args()


def main():
    '''Records screen and store it in mp4 format with 20 fps by default. 
            Recordings can be found at recordings folder in relative path. 
                Press ctrl+alt+s to STOP recording'''
    if not os.path.exists(os.path.join(os.getcwd(), 'recordings')):
        os.mkdir('recordings')
    args = parse_arguments()
    _file_name = args.output
    _include_audio = args.audio
    if not _file_name:
        _file_name = 'recording_'+str(int(datetime.timestamp(datetime.now())))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    keyboard.add_hotkey('ctrl+alt+s', exit_handler)
    out = cv2.VideoWriter(os.path.join(
        'recordings', _file_name+'.mp4'), fourcc, 20.0, SCREEN)
    while not STOP:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
    print('successfully saved to  :  {}.mp4'.format(_file_name))
    cv2.destroyAllWindows()
    out.release()


SCREEN = pyautogui.size()
STOP = False

if __name__ == '__main__':
    main()
