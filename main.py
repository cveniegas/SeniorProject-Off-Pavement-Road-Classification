import os
import cv2
import numpy as np
import argparse
import importlib.util
import PySimpleGUI as sg
from tensorflow.lite.python.interpreter import Interpreter

sg.theme('light green')

layout = [
    [sg.Text('Object Detection Using Tensorflow-trained Classifier', size=(45, 1), font=('Any', 18),
             text_color='#1c86ee', justification='center')],
    [sg.Text('Folder tflite'), sg.In(size=(25, 1), key='modeldir'), sg.FolderBrowse()],
    [sg.Text('Video file'), sg.In('test.mp4', size=(25, 1), key='video'), sg.FileBrowse()],
    [sg.OK(), sg.Cancel()]
]

window = sg.Window('Object Detection - Hornet Engineers', layout, default_element_size=(14, 1), text_justification='right',
                   auto_size_text=False)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == 'OK':
        args = argparse.Namespace(modeldir=values['modeldir'],
                                  video=values['video'])

        MODEL_NAME = args.modeldir
        VIDEO_NAME = args.video

        min_conf_threshold = 0.5
        LABELMAP_NAME = 'labelmap.txt'
        CWD_PATH = os.getcwd()

        PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'detect.tflite')
        PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

        interpreter = Interpreter(model_path=PATH_TO_CKPT)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]

        floating_model = input_details[0]['dtype'] == np.float32
        input_mean = 127.5
        input_std = 127.5

        boxes_idx, classes_idx, scores_idx = 0, 1, 2

        VIDEO_PATH = os.path.join(CWD_PATH, VIDEO_NAME)
        video = cv2.VideoCapture(VIDEO_PATH)
        imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        outname = output_details[0]['name']

        if ('StatefulPartitionedCall' in outname):  # This is a TF2 model
            boxes_idx, classes_idx, scores_idx = 1, 3, 0
        else:  # This is a TF1 model
            boxes_idx, classes_idx, scores_idx = 0, 1, 2

        with open(PATH_TO_LABELS, 'r') as f:
            labels = [line.strip() for line in f.readlines()]

        # Counter window layout
        counter_layout = [
            [sg.Text('Object Counter', size=(20, 1), font=('Any', 14), text_color='#1c86ee')],
            [sg.Text('Count:', size=(10, 1)), sg.Text('0', size=(5, 1), key='counter')]
        ]

        # Create the counter window
        counter_window = sg.Window('Object Counter', counter_layout, default_element_size=(14, 1),
                                   text_justification='right', auto_size_text=False)

        counter = 0
        counter_update_interval = 5  # Update counter window every 5 frames
        frame_counter = 0

        while video.isOpened():
            ret, frame = video.read()
            frame_counter += 1

            if not ret:
                print('Reached the end of the video!')
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)

            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]
            classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]
            scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]

            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

                    object_name = labels[int(classes[i])]
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    label_ymin = max(ymin, labelSize[1] + 10)
                    cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                                  (xmin + labelSize[0], label_ymin + baseLine - 10), (0, 255, 0),
                                  cv2.FILLED) 
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                                2)
                    counter += 1  # Increment the counter when an object is detected

            cv2.imshow('Object detector', frame)

            # Update object counter window every counter_update_interval frames
            if frame_counter % counter_update_interval == 0:
                event_counter, values_counter = counter_window.read(timeout=10)  # Use a timeout to make it non-blocking
                if event_counter == sg.WIN_CLOSED or event_counter == 'Cancel':
                    break
                counter_window['counter'].update(counter)

            if cv2.waitKey(1) == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

        counter_window.close()  # Close the counter window when the main video processing is done

window.close()
