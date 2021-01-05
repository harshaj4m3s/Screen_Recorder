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


def add_assets(imageName, url='https://raw.githubusecontent.com/harshaj4m3s/Screen_Recorder/master/assets/mouse.png'):
    import requests
    filename = os.path.join(os.getcwd(), imageName)
    with open(filename, 'wb') as f:
        res = requests.get(url, stream=True)
        if not res.ok:
            return False
        for block in res.iter_content(1024):
            if not block:
                break
            f.write(block)
    return True


def load_mouse_png():
    assets = os.path.join(os.getcwd(), 'assets')
    if not os.path.exists(assets):
        if not add_assets('mouse.png'):
            print('Cannot load mouse.png')
            return None
    mouse = cv2.imread(os.path.join(assets, 'mouse.png'))
    return mouse


def add_cursor(bg):
    overlay = load_mouse_png()
    if overlay is None:
        return bg
    x, y = pyautogui.position()
    ans = overlay_mouse(bg, overlay, x, y)
    return ans


def overlay_mouse(background, overlay, x, y):
    # print(background)
    background_width, background_height = background.shape[1], background.shape[0]
    if y >= background_height or x >= background_width:
        return background
    height, width = overlay.shape[0], overlay.shape[1]
    if x+width > background_width:
        width = background_width-x
        overlay = overlay[:, :width]
    if y+height > background_height:
        height = background_height-y
        overlay = overlay[:height]
    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones(
                    (overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype)*255
            ],
            axis=2,
        )
    overlay_image = overlay[..., :3]
    mask = overlay_image/255.0
    background[y:y+height, x:x+width] = (1.0-mask) * \
        background[y:y+height, x:x+width]+mask*overlay_image
    return background


def main():
    '''Records screen and store it in mp4 format with 20 fps by default. 
            Recordings can be found at "/recordings" folder in relative path. 
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
            frame_cam = cv2.resize(frame_cam, cam_size)
            #frame_cam = cv2.cvtColor(frame_cam, cv2.COLOR_BGR2RGB)
        else:
            pass
        x_offset, y_offset = SCREEN.width-20 - \
            cam_size[0], SCREEN.height-20-cam_size[1]
        img = pyautogui.screenshot()
        img = np.array(img)
        #img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img = add_cursor(img)
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
