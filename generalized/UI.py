import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTabWidget, QFormLayout, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from Construct import Construct
import femmutil as fm

qapp = QApplication([])

class FEMMUtil(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'FEMM Utility'
        self.pages = []     
        self.constructs = []
        # self.materials = []
        self.pfields = []
        self.sweepBoxParam = False
        self.sweepBoxConstruct = False
        self.sweepFieldStart = False
        self.sweepFieldEnd = False
        self.sweepFieldStep = False
        # self.pmenus = {
        #     'materials': []
        # }
        self.FEMMState = 0 # 0 off; 1 connected
        self.pages.append(self.genMainPage())

    def getIn(self, field):
        try: 
            return float(field.text())
        except ValueError:
            field.setText('0')
            return 0

    def connectFEMM(self):
        if self.FEMMState == 0:
            fm.initFemm()
            fm.getMat('Air')
            for construct in self.constructs:
                construct.setup()
            self.FEMMState = 1

    def updateConstruct(self, constrid):
        # print(self.constructs[constrid].p.__dict__['autoUpdate'])
        if self.constructs[constrid].p.__dict__['autoUpdate'] and self.FEMMState == 1:
            self.constructs[constrid].update()

    def updateParam(self, constrid, param, field):
        # for construct in self.constructs:
        #     print(construct.p.__dict__)
        self.constructs[constrid].p.__dict__[param] = self.getIn(field)
        self.updateConstruct(constrid)

    def toggleParam(self, constrid, param, field):
        self.constructs[constrid].p.__dict__[param] = field.isChecked()
        self.updateConstruct(constrid)

    def updateCircuit(self, constrid, param, field):
        I = self.getIn(field)
        self.constructs[constrid].p.__dict__[param].current = I
        if self.FEMMState == 1:
            fm.modCircuit(self.constructs[constrid].p.__dict__[param].circName, I)

    def cHookHide(self, constrid):
        if self.FEMMState == 1:
            self.constructs[constrid].hide()
            fm.zoom()


    def cHookDrawSegment(self, constrid):
        if self.FEMMState == 1:
            fm.femmgroupmode = self.constructs[constrid].group
            self.constructs[constrid].hide()
            self.constructs[constrid].drawSegment()
            self.constructs[constrid].drawState = 1
            fm.femmgroupmode = 0
            fm.zoom()

    def cHookDraw(self, constrid):
        if self.FEMMState == 1:
            fm.femmgroupmode = self.constructs[constrid].group
            self.constructs[constrid].hide()
            self.constructs[constrid].drawSegment()
            self.constructs[constrid].draw()
            self.constructs[constrid].drawState = 2
            fm.femmgroupmode = 0
            fm.rot(self.constructs[constrid].angle, self.constructs[constrid].group)
            fm.zoom()

    def rotateConstruct(self, constrid, field):
        if self.constructs[constrid].drawState == 2:
            newAngle = self.getIn(field)
            fm.rot(newAngle - self.constructs[constrid].angle, self.constructs[constrid].group)
            self.constructs[constrid].angle = newAngle

    # def generateMenus(self, menus, options):
    #     for menu in menus:
    #         for option in options:
    #             index = menu.currentIndex()+1
    #             menu.insertItem(index, option)

    def register(self, constr, group = 0):
        try:
            if not issubclass(constr, Construct):
                raise TypeError

            self.constructs.append(constr())
            if group > 0:
                self.constructs[-1].group = group
            newConstruct = QWidget()
            newConstruct.layout = QVBoxLayout()
            newPage = QWidget()
            newPage.layout = QFormLayout()
            newCircuits = QWidget()
            newCircuits.layout = QFormLayout()
            for parameter in self.constructs[-1].p.params():
                ptype = type(self.constructs[-1].p.__dict__[parameter])
                pvalue = self.constructs[-1].p.__dict__[parameter]
                if ptype is int or ptype is float:
                    self.pfields.append(QLineEdit())
                    self.pfields[-1].setText(str(pvalue))
                    self.pfields[-1].editingFinished.connect(lambda p=parameter, constrid=len(self.constructs)-1, field=self.pfields[-1]: self.updateParam(constrid, p, field))
                    newPage.layout.addRow(parameter, self.pfields[-1])
                elif ptype is bool:
                    self.pfields.append(QCheckBox())
                    self.pfields[-1].stateChanged.connect(lambda state, p=parameter, constrid=len(self.constructs)-1, field=self.pfields[-1]: self.toggleParam(constrid, p, field))
                    newPage.layout.addRow(parameter, self.pfields[-1])
            ### todo: materials dropdown
                # elif ptype is Construct.Material:
                    # self.constructs[-1].p.__dict__[parameter].matName
                #     self.pmenus['materials'].append(QComboBox())
                #     self.materials.append(pvalue.matName)
                #     newPage.layout.addRow(parameter, self.pmenus['materials'][-1])
            # # Menu generation needs to be done after all menus exist and all materials have been added.
            # self.generateMenus(self.pmenus['materials'], self.materials)
                elif ptype is Construct.Circuit:
                    self.pfields.append(QLineEdit())
                    self.pfields[-1].setText(str(pvalue.current))
                    self.pfields[-1].editingFinished.connect(lambda param=parameter, constrid=len(self.constructs)-1, field=self.pfields[-1]: self.updateCircuit(constrid, param, field))
                    newCircuits.layout.addRow(self.constructs[-1].p.__dict__[parameter].circName, self.pfields[-1])
            newPage.setLayout(newPage.layout)
            newCircuits.setLayout(newCircuits.layout)

            newConstruct.layout.addWidget(newPage)

            ## Add common buttons 
            newButtons = QWidget()
            newButtons.layout = QHBoxLayout()
            # Draw segment
            newDrawSegmentButton = QPushButton('draw segment')
            newDrawSegmentButton.clicked.connect(lambda checked, constrid=len(self.constructs)-1: self.cHookDrawSegment(constrid))
            newButtons.layout.addWidget(newDrawSegmentButton)
            # Draw whole
            newDrawButton = QPushButton('draw')
            newDrawButton.clicked.connect(lambda checked, constrid=len(self.constructs)-1: self.cHookDraw(constrid))
            newButtons.layout.addWidget(newDrawButton)
            # Hide 
            newHideButton = QPushButton('hide')
            newHideButton.clicked.connect(lambda checked, constrid=len(self.constructs)-1: self.cHookHide(constrid))
            newButtons.layout.addWidget(newHideButton)
            # Add to page
            newButtons.setLayout(newButtons.layout)
            newConstruct.layout.addWidget(newButtons)

            newConstruct.layout.addWidget(newCircuits)

            ## Add rotate field
            newRotate = QWidget()
            newRotate.layout = QFormLayout()
            self.pfields.append(QLineEdit('0'))
            self.pfields[-1].editingFinished.connect(lambda constrid=len(self.constructs)-1, field=self.pfields[-1]: self.rotateConstruct(constrid, field))
            newRotate.layout.addRow('angle', self.pfields[-1])
            newRotate.setLayout(newRotate.layout)
            newConstruct.layout.addWidget(newRotate)

            newConstruct.setLayout(newConstruct.layout)
            self.pages.append([newConstruct, type(self.constructs[-1]).__name__]) #str(len(self.constructs)-1)])

        except TypeError as e:
            print(str(constr),'not a construct', e)

    def fillEmpty(self):
        if self.FEMMState == 0:
            return
        radii = []
        for construct in self.constructs:
            if construct.drawState > 0:
                radii.append(construct.rInner)
                radii.append(construct.rOuter)
        fm.fillEmpty(radii)
        fm.zoom()

    # Generate first page of FEMM utility
    def genMainPage(self):
        mainPage = QWidget()
        mainPage.layout = QVBoxLayout()
        
        # Start FEMM Button
        mainStartButton = QPushButton('connect FEMM')
        mainStartButton.clicked.connect(self.connectFEMM)
        mainPage.layout.addWidget(mainStartButton)

        
        mainPage.setLayout(mainPage.layout)
        return [mainPage, 'main']

    def postPrep(self):
        # clear group 0
        fm.clearGroup(0)
        # fill air gaps
        self.fillEmpty()
        # make abc
        fm.abc()

    def postAnalyze(self, window):
        fm.analyze()
        window.clear()
        for i in range(len(self.constructs)):
            window.append('T'+str(i)+': '+str(round(fm.postGetTorque(self.constructs[i].group),4))+'Nm')

    def genPostPage(self):
        postPage = QWidget()
        postPage.layout = QVBoxLayout()
        # Fill empty space button
        postFillButton = QPushButton('fill empty space')
        postFillButton.clicked.connect(self.fillEmpty)
        postPage.layout.addWidget(postFillButton)
        # prepare for analysis
        postPrepButton = QPushButton('prepare model')
        postPrepButton.clicked.connect(self.postPrep)
        postPage.layout.addWidget(postPrepButton)
        # do analysis,
        # print analysis info
        postInfo = QTextEdit()
        postInfo.setReadOnly(True)
        postAnalyzeButton = QPushButton('analyze')
        postAnalyzeButton.clicked.connect(lambda state, window=postInfo: self.postAnalyze(window))
        postPage.layout.addWidget(postAnalyzeButton)
        postPage.layout.addWidget(postInfo)
        # postInfo.append('hi')

        postPage.setLayout(postPage.layout)
        return [postPage, 'post']

    def sweepConstructSelected(self, index):
        self.sweepBoxParam.clear()
        self.sweepBoxParam.addItem('angle')
        print(index)
        if index > 0:
            # self.sweepBoxParam.addItem('...')
            for parameter in self.constructs[index-1].p.params():
                ptype = type(self.constructs[index-1].p.__dict__[parameter])
                if ptype is int or ptype is float:
                    self.sweepBoxParam.addItem(parameter)
            self.sweepParamSelected(0)

    def sweepParamSelected(self, index):
        cindex = self.sweepBoxConstruct.currentIndex() - 1
        param = self.sweepBoxParam.currentText()
        if param == 'angle':
            self.sweepFieldStart.setText(str(self.constructs[cindex].angle))
            self.sweepFieldEnd.setText(str(self.constructs[cindex].angle))
            self.sweepFieldStep.setText('0')

        else:
            self.sweepFieldStart.setText(str(self.constructs[cindex].p.__dict__[param]))
            self.sweepFieldEnd.setText(str(self.constructs[cindex].p.__dict__[param]))
            self.sweepFieldStep.setText('0')

    def genSweepPage(self):
        sweepPage = QWidget()
        sweepPage.layout = QVBoxLayout()
        
        # form: construct select
        self.sweepBoxConstruct = QComboBox()
        self.sweepBoxConstruct.addItem('')
        for i in range(len(self.constructs)):
            self.sweepBoxConstruct.addItem(type(self.constructs[i]).__name__)
        self.sweepBoxConstruct.activated.connect(self.sweepConstructSelected)
        # form: parameter select
        self.sweepBoxParam = QComboBox()
        self.sweepBoxParam.activated.connect(self.sweepParamSelected)
        self.sweepBoxParam.addItem('test')

        paramSelectForm = QWidget()
        paramSelectForm.layout = QFormLayout()
        paramSelectForm.layout.addRow('construct', self.sweepBoxConstruct)
        paramSelectForm.layout.addRow('parameter', self.sweepBoxParam)
        paramSelectForm.setLayout(paramSelectForm.layout)

        # hbox: start, end, step for parameter sweep
        self.sweepFieldStart = QLineEdit()
        self.sweepFieldEnd = QLineEdit()
        self.sweepFieldStep = QLineEdit()
        paramBounds = QWidget()
        paramBounds.layout = QHBoxLayout()
        paramBounds.layout.addWidget(QLabel('start'))
        paramBounds.layout.addWidget(self.sweepFieldStart)
        paramBounds.layout.addWidget(QLabel('end'))
        paramBounds.layout.addWidget(self.sweepFieldEnd)
        paramBounds.layout.addWidget(QLabel('step'))
        paramBounds.layout.addWidget(self.sweepFieldStep)
        paramBounds.setLayout(paramBounds.layout)

        # button

        sweepPage.layout.addWidget(paramSelectForm)
        sweepPage.layout.addWidget(paramBounds)
        sweepPage.setLayout(sweepPage.layout)
        return [sweepPage, 'sweep']

    ## initUI: generate all pages beside main and construct pages, then start application and show window
    def initUI(self):
        self.pages.append(self.genPostPage())
        self.pages.append(self.genSweepPage())
        
        self.application = QWidget()
        self.applayout = QVBoxLayout()
        self.tabs = QTabWidget()
        # for construct in self.constructs:
        #     print(construct.p.__dict__)
        for page in self.pages:
            self.tabs.addTab(page[0], page[1])
        self.applayout.addWidget(self.tabs)
        self.application.setLayout(self.applayout)
        self.application.show()
        qapp.exec_()


if __name__ == '__main__':
    from StatorDL import StatorDL
    fmutil = FEMMUtil()
    fmutil.initUI()
