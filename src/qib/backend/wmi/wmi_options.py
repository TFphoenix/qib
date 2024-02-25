from __future__ import annotations

from qib.backend.options import Options


class WMIOptions(Options):
    """
    The WMI Qiskit Simulator quantum experiment options.
    """

    def __init__(self,
                 shots = 1024,
                 init_qubits = True,
                 do_emulation = False,
                 loops={},
                 sequence_settings={},
                 reference_measurement={'function': 'nothing'},
                 trigger_time=0.001,
                 relax=True,
                 relax_time=None,
                 default_qubits=None,
                 weighting_amp=1.0,
                 acquisition_mode='integration_trigger',
                 averaging_mode='single_shot',
                 log_level='debug',
                 log_level_std='info',
                 log_file_level='debug',
                 store_nt_result=True,
                 name_suffix='',
                 meas_level=2,
                 fridge='badwwmi-021-xld105'
                 ):
        super().__init__(shots, init_qubits)
        self.do_emulation = do_emulation

    @staticmethod
    def default() -> WMIOptions:
        return WMIOptions()
