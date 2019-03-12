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

        # General settings
        self._updateinstantcb = ControlCheckBox('update instantly', changed_event = self._updateInstant)
        self._updateinstantcb.value = s.updateInstant

        # Stator  parameters
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
        # Stator control
        self._drawstatorb = ControlButton('draw stator')
        self._drawstatorb.value = self._drawStator
        self._drawstatortoothb = ControlButton('draw tooth')
        self._drawstatortoothb.value = self._drawStatorTooth
        self._hidestatorb = ControlButton('hide stator')
        self._hidestatorb.value = self._hideStator

        # Rotor parameters
        self._parNm = ControlText('rotor teeth:')
        self._parNm.value = str(s.Nm)
        self._parNm.changed_event = self._updateRotorSettings
        self._parrsh = ControlText('shaft radius:')
        self._parrsh.value = str(s.rsh)
        self._parrsh.changed_event = self._updateRotorSettings
        self._parrr = ControlText('rotor radius:')
        self._parrr.value = str(s.rr)
        self._parrr.changed_event = self._updateRotorSettings
        self._parhm = ControlText('magnet height:')
        self._parhm.value = str(s.hm)
        self._parhm.changed_event = self._updateRotorSettings
        self._pardm = ControlText('magnet depth:')
        self._pardm.value = str(s.dm)
        self._pardm.changed_event = self._updateRotorSettings
        self._parmfrac = ControlText('magnet phase fraction:')
        self._parmfrac.value = str(s.mfrac)
        self._parmfrac.changed_event = self._updateRotorSettings
        # Rotor control
        self._drawrotorb = ControlButton('draw rotor')
        self._drawrotorb.value = self._drawRotor
        self._drawrotortoothb = ControlButton('draw tooth')
        self._drawrotortoothb.value = self._drawRotorTooth
        self._hiderotorb = ControlButton('hide rotor')
        self._hiderotorb.value = self._hideRotor

        self._formset = [{
            'a:femm': ['_updateinstantcb'],
            "b:stator": ['_parNt',
                '_parrag',
                '_parwt',
                '_parbt',
                '_parhs',
                '_partfrac',
                '_parcfrac',
                ('_drawstatortoothb', '_drawstatorb', '_hidestatorb')],
            'c:rotor': ['_parNm',
                '_parrsh',
                '_parrr',
                '_parhm',
                '_pardm',
                '_parmfrac',
                ('_drawrotortoothb', '_drawrotorb', '_hiderotorb')]
        }]

    def _updateInstant(self):
        s.updateInstant = self._updateinstantcb.value

    def _updateRotorSettings(self):
        s.Nm = float(self._parNm.value)
        s.rsh = float(self._parrsh.value)
        s.rr = float(self._parrr.value)
        s.hm = float(self._parhm.value)
        s.dm = float(self._pardm.value)
        s.mfrac = float(self._parmfrac.value)
        s.rotorOOD = True
        if s.updateInstant:
            s.rotorOOD = False
            main.clearGroup(s.rotorGroup)
            main.rotorTooth(s.Nm, s.rsh, s.rr, s.hm, s.dm, s.mfrac)
            if not s.rotorSingle:
                main.revolveRotor(s.Nm)
            main.zoom()
            # self._drawstatorb.enabled = True # Tooth can be revolved
    
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
            if not s.statorSingle:
                main.revolveStator(s.Nt)
            main.zoom()
            self._drawstatorb.enabled = True # Tooth can be revolved
    
    def _drawStator(self):
        if s.statorOOD:
            s.statorOOD = False
            main.clearGroup(s.statorGroup)
            main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac)
        main.revolveStator(s.Nt)
        main.zoom()
        s.statorSingle = False

    def _drawStatorTooth(self):
        main.clearGroup(s.statorGroup)
        main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac)
        main.zoom()
        self._drawstatorb.enabled = True # Tooth can be revolved
        s.statorSingle = True


    def _hideStator(self):
        main.clearGroup(s.statorGroup)
        main.zoom()
        self._drawstatorb.enabled = False # Ensure one tooth is drawn first

    def _drawRotor(self):
        if s.rotorOOD:
            s.rotorOOD = False
            main.clearGroup(s.rotorGroup)
            main.rotorTooth(s.Nm, s.rsh, s.rr, s.hm, s.dm, s.mfrac)
        main.revolveRotor(s.Nm)
        main.zoom()
        s.rotorSingle = False

    def _drawRotorTooth(self):
        main.clearGroup(s.rotorGroup)
        main.rotorTooth(s.Nm, s.rsh, s.rr, s.hm, s.dm, s.mfrac)
        main.zoom()
        self._drawrotorb.enabled = True # Tooth can be revolved
        s.rotorSingle = True


    def _hideRotor(self):
        main.clearGroup(s.rotorGroup)
        main.zoom()
        self._drawrotorb.enabled = False # Ensure one tooth is drawn first

if __name__ == '__main__':
    import pyforms

    main.initFemm()
    main.statorTooth()
    main.rotorTooth()
    main.zoom()
    from femm import mi_zoomnatural
    pyforms.start_app(UI)
    main.deinitFemm()