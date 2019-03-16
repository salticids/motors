import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTabWidget, QFormLayout, QLabel, QVBoxLayout, QCheckBox, QComboBox
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

    def connectFEMM(self):
        if self.FEMMState == 0:
            fm.initFemm()


    def updateParam(self, constrid, param, field):
        self.constructs[constrid].p.__dict__[param] = float(field.text())
        # print(self.constructs[constrid].p.__dict__[param])
        if self.constructs[constrid].p.__dict__['autoUpdate'] and self.FEMMState == 1:
            self.constructs[constrid].update()

    def toggleParam(self, constrid, param, field):
        self.constructs[constrid].p.__dict__[param] = field.isChecked()
        # print(self.constructs[constrid].p.__dict__[param])
        if self.constructs[constrid].p.__dict__['autoUpdate'] and self.FEMMState == 1:
            self.constructs[constrid].update()

    # def generateMenus(self, menus, options):
    #     for menu in menus:
    #         for option in options:
    #             index = menu.currentIndex()+1
    #             menu.insertItem(index, option)

    def register(self, constr):
        try:
            if not issubclass(constr, Construct):
                raise TypeError

            self.constructs.append(constr())
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
                    self.pfields[-1].stateChanged.connect(lambda p=parameter, constrid=len(self.constructs)-1, field=self.pfields[-1]: self.toggleParam(constrid, p, field))
                    newPage.layout.addRow(parameter, self.pfields[-1])
                # elif ptype is Construct.Material:
                #     self.pmenus['materials'].append(QComboBox())
                #     self.materials.append(pvalue.matName)
                #     newPage.layout.addRow(parameter, self.pmenus['materials'][-1])
            # # Menu generation needs to be done after all menus exist and all materials have been added.
            # self.generateMenus(self.pmenus['materials'], self.materials)
            newPage.setLayout(newPage.layout)
            self.pages.append([newPage, str(len(self.constructs)-1)])

        except TypeError as e:
            print(str(constr),'not a construct', e)

    def genMainPage(self):
        mainPage = QWidget()
        mainPage.layout = QFormLayout()
        hitext = QLineEdit()
        hitext.editingFinished.connect(lambda: self.alert('hi!!'))
        mainPage.layout.addRow(QLabel('hi'), hitext)
        mainPage.setLayout(mainPage.layout)
        return [mainPage, 'main']

    def initUI(self):
        self.application = QWidget()
        self.applayout = QVBoxLayout()
        self.tabs = QTabWidget()
        for construct in self.constructs:
            print(construct.p.__dict__)
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
    fmutil.register(StatorDL)
    fmutil.constructs[0].p.Nt = 10
    fmutil.initUI()
    app.exec_()

if __name__ == '__main__':
    run()