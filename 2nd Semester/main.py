import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QCoreApplication, QMetaObject, QObject, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from ui_Project3 import Ui_MainWindow
import cv2
import warnings
import time
from computer_vision import VideoProcessor
from PyQt5.QtWidgets import QMessageBox
videoPath = ""
import os
from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes

class MainWindow(QMainWindow):
    
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.video_thread = VideoProcessThread()
        self.stopPipeline = False
        self.classificationBox = False
        self.trafficAnalysisBox = False
        self.videoProcessBox = False
        global videoPath
        # Connect the stateChanged signals of checkbox1 and checkbox2 to their respective handler functions
        #CLASSIFICATION CHECKBOX
        self.ui.classification.checkState
        self.ui.classification.stateChanged.connect(self.checkbox1_classification_state_changed)
        #TRAFFIC ANALYSIS CHECKBOX
        self.ui.trafficAnalysis.stateChanged.connect(self.checkbox2_trafficAnalysis_state_changed)
        #VIDEOPROCESS CHECKBOX
        self.ui.videoProcess.stateChanged.connect(self.checkbox3_videoProcess_state_changed)
        #BROWSE BUTTON
        self.ui.browseVid.clicked.connect(self.browse_video)
        self.ui.stop.clicked.connect(self.stopButton)
        self.ui.quit.clicked.connect(self.quitButton)
        self.ui.credits.clicked.connect(self.creditsButton)
        # START
        self.ui.start.clicked.connect(self.start_video_processing)

        # Connect the thread's finished signal to video_processing_finished method
        self.video_thread.finished.connect(self.video_processing_finished)
        self.video_thread.progress_updated.connect(self.update_progress_bar)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()
    
    def creditsButton(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Credits")
        msg_box.setText("This application was created by The Hornet Engineers.\n\n"
                        "Team: Ian Ichwara, Aleksandr Dorokhin, and Christian Veniegas\n\n"
                        "Version 0.1.1\n"
                        "© 2024 All rights reserved.")
        msg_box.exec_()

    def stopButton(self):
        try:
            print(" Stopping Video")
            self.video_thread.setPipelineTerminate()
        except:
            self.video_thread.stop()
            print("Error: VideoProcessThread object has no attribute 'pipeline'")

    
    def quitButton(self):
        print(" Quitting Application")
        cv2.destroyAllWindows()
        QApplication.quit()

    def start_video_processing(self):
        if not(self.classificationBox) and not(self.trafficAnalysisBox) and not(self.videoProcessBox) or videoPath=="":
            print("Error: Can't start the video, choose from one of the features or make sure to select a video")
            self.show_error_message("Error: Can't start the video, choose from one of the features or make sure to select a video")
        else:
            print("Starting video processing...")
            self.ui.progressBar.setValue(0)  # Reset progress bar
            self.video_thread.start()

    def video_processing_finished(self):
        print("Video processing finished.")
        self.ui.progressBar.setValue(100)
    
    def update_progress_bar(self, value):
        self.ui.progressBar.setValue(value)

    def browse_video(self):
        options = QFileDialog.Options()
        global videoPath

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov)", options=options)
        if file_name:
            self.ui.path_display.setText(file_name)
            self.video_thread.set_video_path(file_name)
            videoPath = file_name

    def checkbox1_classification_state_changed(self, state):
        if state == Qt.Checked:  # If checkbox2 is checked
            self.ui.trafficAnalysis.setEnabled(False)  # Disable checkbox2
            self.ui.videoProcess.setEnabled(False)  # Disable checkbox3
            self.classificationBox = True

            print("Classification is checked.")
        else:
            self.ui.trafficAnalysis.setEnabled(True)  
            self.ui.videoProcess.setEnabled(True)

    def checkbox2_trafficAnalysis_state_changed(self, state):
        if state == Qt.Checked:  # If checkbox1 is checked
            self.ui.classification.setEnabled(False)  # Disable checkbox1
            self.ui.videoProcess.setEnabled(False)  # Disable checkbox3
            self.trafficAnalysisBox = True
            print("Traffick Analysis is checked.")
        else:
            self.ui.classification.setEnabled(True)  
            self.ui.videoProcess.setEnabled(True)
    
    def checkbox3_videoProcess_state_changed(self, state):
        if state == Qt.Checked:  # If checkbox1 is checked
            self.ui.classification.setEnabled(False)  # Disable checkbox2
            self.ui.trafficAnalysis.setEnabled(False)  # Disable checkbox1
            self.videoProcessBox = True
            print("Video Process is checked.")
        else:
            self.ui.trafficAnalysis.setEnabled(True)  
            self.ui.classification.setEnabled(True)  
    

# Create a custom thread class for video processing
class VideoProcessThread(QThread):
    # Define a signal to indicate when the video processing is finished
    finished = pyqtSignal()
    progress_updated = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.video_path = ""
        self.ui = Ui_MainWindow
        

    def set_video_path(self, path):
        self.video_path = path
    
    def setPipelineTerminate(self):
        self.pipeline.terminate()

    def run(self):
        self.east = self.west = self.north =self.south =self.sum  =0
        on_prediction=render_boxes

        self.pipeline = InferencePipeline.init(
            model_id="vehicle-detection-fjtcf/4",
            video_reference=self.video_path,
            on_prediction=render_boxes
        )

        # Live: Classification
        if mainWindow.ui.classification.isChecked():
            self.pipeline.start()
            self.pipeline.join()
    

        # Live: Traffic Analysis
        if mainWindow.ui.trafficAnalysis.isChecked():
            self.processor = VideoProcessor(
                        roboflow_api_key="7cqKpzjVQJcEn7uiHkdC",
                        model_id="vehicle-detection-fjtcf/4",
                        source_video_path=self.video_path,
                        confidence_threshold=0.3,
                        iou_threshold=0.7,
                        )
            self.processor.process_video()
        # Process: Traffic Analysis
        if mainWindow.ui.videoProcess.isChecked():
            current_directory = os.path.dirname(os.path.abspath(__file__))
            target_video_path = os.path.join(current_directory, "Video_out.mp4")
            self.processor = VideoProcessor(
                        roboflow_api_key="7cqKpzjVQJcEn7uiHkdC",
                        model_id="vehicle-detection-fjtcf/4",
                        source_video_path=self.video_path,
                        target_video_path=target_video_path,
                        confidence_threshold=0.3,
                        iou_threshold=0.7,
                        )
            self.processor.process_video()

        self.east = self.processor.get_east_count()
        self.west = self.processor.get_west_count()
        self.north = self.processor.get_north_count()
        self.south = self.processor.get_south_count()
        self.sum = self.processor.get_sum_count()
        
        print ("Done")
        mainWindow.ui.NorthVar.setText(str(self.north))
        print ("Done")
        mainWindow.ui.SouthVar.setText(str(self.south))
        print ("Done")
        mainWindow.ui.EastVar.setText(str(self.east))
        print ("Done")
        mainWindow.ui.WestVar.setText(str(self.west))
        print ("Done")
        mainWindow.ui.totalVar.setText(str(self.sum))
        print ("Done")
        


    def stop(self):
        self.processor.stop_video()

    def quit(self):
        self.stop()  # Stop the Video Processing thread
        cv2.destroyAllWindows()  # Close all OpenCV windows
        QApplication.quit() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
