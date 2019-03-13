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
        self._parwbi = ControlText('back iron width:')
        self._parwbi.value = str(s.wbi)
        self._parwbi.changed_event = self._updateSettings
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

        # Finishing
        self._currentA = ControlText('IA:')
        self._currentA.value = str(s.IA)
        self._currentA.changed_event = self._updateCurrents
        self._currentB = ControlText('IB:')
        self._currentB.value = str(s.IB)
        self._currentB.changed_event = self._updateCurrents
        self._currentC = ControlText('IC:')
        self._currentC.value = str(s.IC)
        self._currentC.changed_event = self._updateCurrents
        self._finishb = ControlButton('finish')
        self._finishb.value = self._finish
        self._resetb = ControlButton('reset')
        self._resetb.value = self._reset

        # Postprocess
        self._sweepAngle = ControlText('Sweep Angle:')
        self._sweepAngle.value = str(s.sweepAngle)
        self._sweepAngle.changed_event = self._updatePost
        self._sweepStepsTorque = ControlText('Steps:')
        self._sweepStepsTorque.value = str(s.stepsTorque)
        self._sweepStepsTorque.changed_event = self._updatePost
        self._sweepTorqueb = ControlButton('Torque Sweep')
        self._sweepTorqueb.value = self._torqueSweep

        # Parametric sweep
        self._sparragEnd = ControlText('end:')
        self._sparragEnd.value = str(s.ragEnd)
        self._sparragEnd.changed_event = self._updatePost
        self._sparragStep = ControlText('step:')
        self._sparragStep.value = str(s.ragStep)
        self._sparragStep.changed_event = self._updatePost
        self._ragTorqueSweepb = ControlButton('Torque Sweep')
        self._ragTorqueSweepb.value = self._ragTorqueSweep


        self._formset = [{
            'a:femm': ['_updateinstantcb'],
            "b:stator": ['_parNt',
                '_parrag',
                '_parwt',
                '_parbt',
                '_parhs',
                '_partfrac',
                '_parcfrac',
                '_parwbi',
                ('_drawstatortoothb', '_drawstatorb', '_hidestatorb')],
            'c:rotor': ['_parNm',
                '_parrsh',
                '_parrr',
                '_parhm',
                '_pardm',
                '_parmfrac',
                ('_drawrotortoothb', '_drawrotorb', '_hiderotorb')],
            'd:finish': ['_currentA',
                '_currentB',
                '_currentC',
                ('_finishb', '_resetb')],
            'e:post': ['_sweepAngle',
                ('_sweepStepsTorque', '_sweepTorqueb')],
            'f:sweep': [('_sparragEnd', '_sparragStep', '_ragTorqueSweepb')]
        }]

        ### internal parameters
        self._show = True

  


    def _updateInstant(self):
        s.updateInstant = self._updateinstantcb.value

    def _updatePost(self):
        s.sweepAngle = float(self._sweepAngle.value)
        s.stepsTorque = int(self._sweepStepsTorque.value)
        s.ragEnd = float(self._sparragEnd.value)
        s.ragStep = float(self._sparragStep.value)

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
        s.wbi = float(self._parwbi.value)
        s.statorOOD = True
        if s.updateInstant:
            s.statorOOD = False
            # main.clearGroup(0) # overlapping issue 
            main.clearGroup(s.statorGroup)
            main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac, s.wbi)
            if not s.statorSingle:
                main.revolveStator(s.Nt)
            main.zoom()
            self._drawstatorb.enabled = True # Tooth can be revolved
    
    def _drawStator(self):
        if s.statorOOD:
            s.statorOOD = False
            main.clearGroup(s.statorGroup)
            main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac, s.wbi)
        main.revolveStator(s.Nt)
        main.zoom()
        s.statorSingle = False

    def _drawStatorTooth(self):
        main.clearGroup(s.statorGroup)
        main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac, s.wbi)
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

    def _updateCurrents(self):
        s.IA = float(self._currentA.value)
        s.IB = float(self._currentB.value)
        s.IC = float(self._currentC.value)
        main.updateCircuits()

    def _finish(self):
        main.generateWindings(s.Nt)
        main.windDoubleLayer(s.Nt)
        main.finish()
    
    def _reset(self):
        main.reset()
        main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac, s.wbi)
        main.rotorTooth(s.Nm, s.rsh, s.rr, s.hm, s.dm, s.mfrac)
        main.zoom()

    def _torqueSweep(self):
        totalAngle = s.sweepAngle
        step = totalAngle / s.stepsTorque
        angles = []
        torques = []
        for i in range(s.stepsTorque):
            main.rotateRotor(i * step)
            torques.append(main.procRotorTorque())
            angles.append(i*step)
        main.plot(angles, torques, self._show)

    def _ragTorqueSweep(self):
        self._show = False
        while(s.rag < s.ragEnd):
            main.clearGroup(s.statorGroup)
            main.statorTooth(s.Nt, s.rag, s.wt, s.bt, s.hs, s.tfrac, s.cfrac, s.wbi)
            main.revolveStator(s.Nt)
            self._finish()
            self._torqueSweep()
            s.rag = s.rag + s.ragStep
        main.plotshow()
        self._show = True

          

if __name__ == '__main__':
    import pyforms

    main.initFemm()
    main.statorTooth()
    main.rotorTooth()
    main.zoom()
    from femm import mi_zoomnatural
    pyforms.start_app(UI)
    main.deinitFemm()