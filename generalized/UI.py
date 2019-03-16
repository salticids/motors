import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTabWidget, QFormLayout, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from Construct import Construct
import femmutil as fm

class FEMMUtil(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'FEMM Util'
        self.pages = []     
        self.constructs = []
        # self.materials = []
        self.pfields = []
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

    def cHookHide(self, constrid):
        if self.FEMMState == 1:
            self.constructs[constrid].hide()

    def cHookDrawSegment(self, constrid):
        if self.FEMMState == 1:
            self.constructs[constrid].hide()
            self.constructs[constrid].drawSegment()
            self.constructs[constrid].drawState = 1
            fm.zoom()

    def cHookDraw(self, constrid):
        print(constrid)
        if self.FEMMState == 1:
            self.constructs[constrid].hide()
            self.constructs[constrid].drawSegment()
            self.constructs[constrid].draw()
            self.constructs[constrid].drawState = 2
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
            hitext = QLineEdit()
            hitext.editingFinished.connect(lambda: self.alert('hi!!'))
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
                # elif ptype is Construct.Material:
                    # self.constructs[-1].p.__dict__[parameter].matName
                #     self.pmenus['materials'].append(QComboBox())
                #     self.materials.append(pvalue.matName)
                #     newPage.layout.addRow(parameter, self.pmenus['materials'][-1])
            # # Menu generation needs to be done after all menus exist and all materials have been added.
            # self.generateMenus(self.pmenus['materials'], self.materials)
            newPage.setLayout(newPage.layout)
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

            ## Add rotate field
            newRotate = QWidget()
            newRotate.layout = QFormLayout()
            self.pfields.append(QLineEdit('0'))
            self.pfields[-1].editingFinished.connect(lambda constrid=len(self.constructs)-1, field=self.pfields[-1]: self.rotateConstruct(constrid, field))
            newRotate.layout.addRow('angle', self.pfields[-1])
            newRotate.setLayout(newRotate.layout)
            newConstruct.layout.addWidget(newRotate)

            newConstruct.setLayout(newConstruct.layout)
            self.pages.append([newConstruct, str(len(self.constructs)-1)])

        except TypeError as e:
            print(str(constr),'not a construct', e)

    def genMainPage(self):
        mainPage = QWidget()
        mainPage.layout = QVBoxLayout()
        mainStartButton = QPushButton('connect FEMM')
        mainStartButton.clicked.connect(self.connectFEMM)
        mainPage.layout.addWidget(mainStartButton)
        mainPage.setLayout(mainPage.layout)
        return [mainPage, 'main']

    def initUI(self):
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

    def alert(self, string):
        QMessageBox.question(self, 'Alert', "hi "+string, QMessageBox.Ok, QMessageBox.Ok)
  

from StatorDL import StatorDL

def run():
    app = QApplication([])
    fmutil = FEMMUtil()
    fmutil.register(StatorDL, 3)
    fmutil.register(StatorDL, 4)
    fmutil.initUI()
    app.exec_()

if __name__ == '__main__':
    run()