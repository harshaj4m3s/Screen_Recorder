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


def record_cam(name, cam_size):
    cam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter('cam_'+name+'.mp4', fourcc, 20.0, cam_size)
    while cam.isOpened:
        q, frame = cam.read()
        if q:
            frame = cv2.resize(frame, cam_size)
            out.write(frame)
            if cv2.waitKey(1) and STOP:
                break
        else:
            break


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
    cam = cv2.VideoCapture(0)
    cam_size = (int(SCREEN.width//4.5), int(SCREEN.height//4.5))
    while not STOP and cam.isOpened():
        q, frame_cam = cam.read()
        if q:
            frame_cam = np.array(frame_cam)
            scale_percent = 4.5
            frame_cam = cv2.resize(frame_cam, cam_size)
            frame_cam = cv2.cvtColor(frame_cam, cv2.COLOR_BGR2RGB)
        else:
            pass
        x_offset, y_offset = SCREEN.width-20 - \
            cam_size[0], SCREEN.height-20-cam_size[1]
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame[y_offset:y_offset+cam_size[1],
              x_offset:x_offset+cam_size[0]] = frame_cam
        out.write(frame)
    print('successfully saved to  :  {}.mp4'.format(_file_name))
    cv2.destroyAllWindows()
    out.release()


SCREEN = pyautogui.size()
STOP = False

if __name__ == '__main__':
    main()
