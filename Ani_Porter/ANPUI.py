from PySide2 import QtWidgets, QtCore, QtGui
import os
import maya.cmds as cmds

import AniPorterLibrary
reload(AniPorterLibrary)

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'AnimLib')


class AniPorterUI(QtWidgets.QDialog):
    def __init__(self):
        super(AniPorterUI, self).__init__()

        self.setWindowTitle('Ani_Porter beta')
        self.libs = AniPorterLibrary.AniPorterLibrary()
        self.buildUI()

    def buildUI(self):
        self.libs.find()
        layout = QtWidgets.QVBoxLayout(self)

        image = QtWidgets.QLabel()
        imgpath = os.path.join(DIRECTORY, 'anplogo.png')
        image.setPixmap(QtGui.QPixmap(imgpath))
        layout.addWidget(image)

        # write tab
        writeWidget = QtWidgets.QWidget()
        w_layout = QtWidgets.QVBoxLayout(writeWidget)
        w_text = QtWidgets.QLabel()
        w_text.setText("<h1>Export Settings</h1>")
        w_layout.addWidget(w_text)
        self.outModeA = QtWidgets.QRadioButton("All", self)
        self.outModeB = QtWidgets.QRadioButton("Selected range", self.outModeA)
        self.outModeA.setChecked(True)
        self.outModeA.clicked.connect(self.txtOff)
        self.outModeB.clicked.connect(self.txtAct)
        w_layout.addWidget(self.outModeA)
        w_layout.addWidget(self.outModeB)

        self.groupBox = QtWidgets.QGroupBox("Range")

        startOBJ = QtWidgets.QWidget()
        startHLO = QtWidgets.QHBoxLayout(startOBJ)
        self.startTXT = QtWidgets.QLabel()
        self.startTXT.setText("Start:")
        startHLO.addWidget(self.startTXT)
        self.startField = QtWidgets.QLineEdit()
        self.startField.setValidator(QtGui.QIntValidator())
        self.startField.setDisabled(True)
        startHLO.addWidget(self.startField)

        endObj = QtWidgets.QWidget()
        endHLO = QtWidgets.QHBoxLayout(endObj)
        self.endTXT = QtWidgets.QLabel()
        self.endTXT.setText("End:")
        endHLO.addWidget(self.endTXT)
        self.endField = QtWidgets.QLineEdit()
        self.endField.setValidator(QtGui.QIntValidator())
        self.endField.setDisabled(True)
        endHLO.addWidget(self.endField)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(startOBJ)
        vbox.addWidget(endObj)
        vbox.addStretch(1)
        self.groupBox.setLayout(vbox)
        w_layout.addWidget(self.groupBox)
        self.groupBox.hide()

        saveGRP = QtWidgets.QGroupBox("Save as")
        saveObj = QtWidgets.QWidget()
        saveVLO = QtWidgets.QVBoxLayout(saveObj)
        self.saveField = QtWidgets.QLineEdit()
        saveVLO.addWidget(self.saveField)
        vbox2 = QtWidgets.QVBoxLayout()
        vbox2.addWidget(saveObj)
        vbox2.addStretch(1)
        saveGRP.setLayout(vbox2)
        w_layout.addWidget(saveGRP)

        self.errorTXT = QtWidgets.QLabel()
        self.errorTXT.setText("")
        w_layout.addWidget(self.errorTXT)

        actbtn = QtWidgets.QPushButton('Action')
        actbtn.clicked.connect(self.ExpAct)
        w_layout.addWidget(actbtn)


        # read tab
        readWidget = QtWidgets.QWidget()
        r_layout = QtWidgets.QVBoxLayout(readWidget)
        r_text = QtWidgets.QLabel()
        r_text.setText("<h1>Import Settings</h1>")
        r_layout.addWidget(r_text)

        self.itemlist = QtWidgets.QComboBox()
        for item in self.libs:
            self.itemlist.addItem(item)
        r_layout.addWidget(self.itemlist)

        importbtn = QtWidgets.QPushButton('Action')
        importbtn.clicked.connect(self.ImpAct)
        r_layout.addWidget(importbtn)

        main_tab = QtWidgets.QTabWidget()
        main_tab.addTab(writeWidget, "Export Mode")
        main_tab.addTab(readWidget, "Import Mode")
        layout.addWidget(main_tab)

    def txtOff(self):
        self.startField.setDisabled(True)
        self.endField.setDisabled(True)
        self.startTXT.setText('Start:')
        self.endTXT.setText("End:")
        self.groupBox.hide()

    def txtAct(self):
        self.startField.setDisabled(False)
        self.endField.setDisabled(False)
        self.startTXT.setText("<strong>Start:</strong>")
        self.endTXT.setText("<strong>End:</strong>")
        self.groupBox.show()

    def listUpdate(self):
        self.itemlist.clear()
        for item in self.libs:
            self.itemlist.addItem(item)

    def ExpAct(self):
        self.errorTXT.setText("")
        if len(self.saveField.text()) != 0:
            if self.outModeA.isChecked():
                sTime = cmds.playbackOptions(q=True, minTime=True)
                eTime = cmds.playbackOptions(q=True, maxTime=True)
            if self.outModeB.isChecked():
                sTime = int(self.startField.text())
                eTime = int(self.endField.text())
            name = self.saveField.text()
            print sTime, eTime, name
            self.libs.save(name=name, start=sTime, end=eTime)
            self.libs.find()
            self.listUpdate()
        else:
            self.errorTXT.setText("<strong>ERROR Input name!!</strong>")

    def ImpAct(self):
        tgt = self.itemlist.currentText()
        self.libs.load(name=tgt, directory=DIRECTORY)


def showUI():
    ui = AniPorterUI()
    ui.show()
    return ui
