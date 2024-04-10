# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProjectLfvXDX.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1475, 180)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1475, 180))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 1451, 145))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.label)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetNoConstraint)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.NorthVar = QLabel(self.widget)
        self.NorthVar.setObjectName(u"NorthVar")

        self.horizontalLayout_4.addWidget(self.NorthVar)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.SouthVar = QLabel(self.widget)
        self.SouthVar.setObjectName(u"SouthVar")

        self.horizontalLayout_4.addWidget(self.SouthVar)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.EastVar = QLabel(self.widget)
        self.EastVar.setObjectName(u"EastVar")

        self.horizontalLayout_4.addWidget(self.EastVar)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.WestVar = QLabel(self.widget)
        self.WestVar.setObjectName(u"WestVar")

        self.horizontalLayout_4.addWidget(self.WestVar)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.totalVar = QLabel(self.widget)
        self.totalVar.setObjectName(u"totalVar")

        self.horizontalLayout_4.addWidget(self.totalVar)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.classification = QCheckBox(self.widget)
        self.classification.setObjectName(u"classification")

        self.verticalLayout_2.addWidget(self.classification)

        self.trafficAnalysis = QCheckBox(self.widget)
        self.trafficAnalysis.setObjectName(u"trafficAnalysis")

        self.verticalLayout_2.addWidget(self.trafficAnalysis)

        self.videoProcess = QCheckBox(self.widget)
        self.videoProcess.setObjectName(u"videoProcess")

        self.verticalLayout_2.addWidget(self.videoProcess)

        self.progressBar = QProgressBar(self.widget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setValue(0)

        self.verticalLayout_2.addWidget(self.progressBar)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setMaximumSize(QSize(95, 40))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.path_display = QTextBrowser(self.widget)
        self.path_display.setObjectName(u"path_display")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.path_display.sizePolicy().hasHeightForWidth())
        self.path_display.setSizePolicy(sizePolicy3)
        self.path_display.setMaximumSize(QSize(400, 30))

        self.horizontalLayout_3.addWidget(self.path_display)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.browseVid = QPushButton(self.widget)
        self.browseVid.setObjectName(u"browseVid")

        self.horizontalLayout_2.addWidget(self.browseVid)

        self.start = QPushButton(self.widget)
        self.start.setObjectName(u"start")

        self.horizontalLayout_2.addWidget(self.start)

        self.stop = QPushButton(self.widget)
        self.stop.setObjectName(u"stop")

        self.horizontalLayout_2.addWidget(self.stop)

        self.credits = QPushButton(self.widget)
        self.credits.setObjectName(u"credits")

        self.horizontalLayout_2.addWidget(self.credits)

        self.quit = QPushButton(self.widget)
        self.quit.setObjectName(u"quit")

        self.horizontalLayout_2.addWidget(self.quit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hornet-Engineers: Off Pavement Traffic Analyzer", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\n" "Features:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"North-Outbound:", None))
        self.NorthVar.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"South-Outbound:", None))
        self.SouthVar.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"East-Outbound:", None))
        self.EastVar.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"West-Outbound:", None))
        self.WestVar.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Total Counts:", None))
        self.totalVar.setText("")
        self.classification.setText(QCoreApplication.translate("MainWindow", u"Live: Classification", None))
        self.trafficAnalysis.setText(QCoreApplication.translate("MainWindow", u"Live: Traffic Analysis", None))
        self.videoProcess.setText(QCoreApplication.translate("MainWindow", u"Video .mp4 Process", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"  Video Path:", None))
        self.browseVid.setText(QCoreApplication.translate("MainWindow", u"Browse Video", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.credits.setText(QCoreApplication.translate("MainWindow", u"Credits", None))
        self.quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))

class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())