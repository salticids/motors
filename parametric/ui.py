import settings as s

from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlSlider
from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlCheckBox

import main

class UI(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('femm tool')

        self._parNt = ControlText('stator teeth: ')
        self._parNt.value = str(s.Nt)
        self._parNt.changed_event = self._updateSettings
        self._parrag = ControlText('radius to stator: ')
        self._parrag.value = str(s.rag)
        self._parrag.changed_event = self._updateSettings
        self._parwt = ControlText('tooth thickness: ')
        self._parwt.value = str(s.wt)
        self._parwt.changed_event = self._updateSettings
        self._parbt = ControlText('root width: ')
        self._parbt.value = str(s.bt)
        self._parbt.changed_event = self._updateSettings
        self._parhs = ControlText('slot height: ')
        self._parhs.value = str(s.hs)
        self._parhs.changed_event = self._updateSettings
        self._partfrac = ControlText('tooth phase fraction: ')
        self._partfrac.value = str(s.tfrac)
        self._partfrac.changed_event = self._updateSettings
        self._parcfrac = ControlText('coil phase fraction: ')
        self._parcfrac.value = str(s.cfrac)
        self._parcfrac.changed_event = self._updateSettings

        self._updateinstantcb = ControlCheckBox('update instantly', changed_event = self._updateInstant)
        self._updateinstantcb.value = s.updateInstant

        self._drawstatorb = ControlButton('draw stator')
        self._drawstatorb.value = self._drawStator
        self._drawstatortoothb = ControlButton('draw tooth')
        self._drawstatortoothb.value = self._drawStatorTooth
        self._hidestatorb = ControlButton('hide stator')
        self._hidestatorb.value = self._hideStator

        self._formset = [{
            'a:femm': ['_drawstatorb'],
            "b:stator": ['_parNt',
                '_parrag',
                '_parwt',
                '_parbt',
                '_parhs',
                '_partfrac',
                '_parcfrac',
                '_updateinstantcb',
                ('_drawstatortoothb', '_drawstatorb', '_hidestatorb')]
        }]

    def _updateInstant(self):
        s.updateInstant = self._updateinstantcb.value
    
    def _updateSettings(self):
        s.Nt = float(self._parNt.value)
        s.rag = float(self._parrag.value)
        s.wt = float(self._parwt.value)
        s.bt = float(self._parbt.value)
        s.hs = float(self._parhs.value)
        s.tfrac = float(self._partfrac.value)
        s.cfrac = float(self._parcfrac.value)
        s.statorOOD = True
        if s.updateInstant:
            s.statorOOD = False
            main.clearGroup(0) # overlapping issue 
            main.clearGroup(s.statorGroup)
            main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac)
            main.zoom()
            self._drawstatorb.enabled = True # Tooth can be revolved
    
    def _drawStator(self):
        if s.statorOOD:
            s.statorOOD = False
            main.clearGroup(s.statorGroup)
            main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac)
        main.revolveStator(s.Nt)
        main.zoom()

    def _drawStatorTooth(self):
        main.clearGroup(s.statorGroup)
        main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac)
        main.zoom()
        self._drawstatorb.enabled = True # Tooth can be revolved


    def _hideStator(self):
        main.clearGroup(s.statorGroup)
        main.zoom()
        self._drawstatorb.enabled = False # Ensure one tooth is drawn first

if __name__ == '__main__':
    import pyforms

    main.initFemm()
    main.statorTooth()
    main.zoom()
    from femm import mi_zoomnatural
    pyforms.start_app(UI)
    main.deinitFemm()