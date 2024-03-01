from __future__ import annotations

from typing import Sequence

from qib.backend.options import Options


class WMIOptions(Options):
    """
    The WMI Qiskit Simulator quantum experiment options.
    """

    def __init__(self,
                #  required
                 shots: int = 1024,
                 init_qubits: bool = True,
                 do_emulation: bool = False,
                #  optional
                 acquisition_mode: str = None,
                 acquisition_type: str = None,
                 averaging_mode: str = None,
                 chip: str = None,
                 debug: bool = None,
                 default_qubits: Sequence[str] = None,
                 fridge: str = None,
                 log_file_level: str = None,
                 log_level_std: str = None,
                 log_level: str = None,
                 loops: dict = None,
                 meas_return: str = None,
                 n_calibration_points: int = None,
                 name_suffix: str = None,
                 parameter_binds: Sequence[dict] = None,
                 parametric_pulses: Sequence[dict] = None,
                 reference_measurement: dict = None,
                 relax_time: int = None,
                 relax: bool = None,
                 sequence_settings: dict = None,
                 store_nt_result: bool = None,
                 trigger_time: float = None,
                 weighting_amp: float = None
                 ):
        # required
        super().__init__(shots, init_qubits)
        self.do_emulation: bool = do_emulation
        
        # optional
        self.acquisition_mode: str = acquisition_mode
        self.acquisition_type: str = acquisition_type
        self.averaging_mode: str = averaging_mode
        self.chip: str = chip
        self.debug: bool = debug
        self.default_qubits: Sequence[str] = default_qubits
        self.fridge: str = fridge
        self.log_file_level: str = log_file_level
        self.log_level_std: str = log_level_std
        self.log_level: str = log_level
        self.loops: dict = loops
        self.meas_return: str = meas_return
        self.n_calibration_points: int = n_calibration_points
        self.name_suffix: str = name_suffix
        self.parameter_binds: Sequence[dict] = parameter_binds
        self.parametric_pulses: Sequence[dict] = parametric_pulses
        self.reference_measurement: dict = reference_measurement
        self.relax_time: int = relax_time
        self.relax: bool = relax
        self.sequence_settings: dict = sequence_settings
        self.store_nt_result: bool = store_nt_result
        self.trigger_time: float = trigger_time
        self.weighting_amp: float = weighting_amp

    def optional(self) -> dict:
        optional: dict = {}
        if self.acquisition_mode: optional['acquisition_mode'] = self.options.acquisition_mode
        if self.acquisition_type: optional['acquisition_type'] = self.options.acquisition_type
        if self.averaging_mode: optional['averaging_mode'] = self.options.averaging_mode
        if self.chip: optional['chip'] = self.options.chip
        if self.debug: optional['debug'] = self.options.debug
        if self.default_qubits: optional['default_qubits'] = self.options.default_qubits
        if self.fridge: optional['fridge'] = self.options.fridge
        if self.log_file_level: optional['log_file_level'] = self.options.log_file_level
        if self.log_level: optional['log_level'] = self.options.log_level
        if self.log_level_std: optional['log_level_std'] = self.options.log_level_std
        if self.loops: optional['loops'] = self.options.loops
        if self.meas_return: optional['meas_return'] = self.options.meas_return
        if self.n_calibration_points: optional['n_calibration_points'] = self.options.n_calibration_points
        if self.name_suffix: optional['name_suffix'] = self.options.name_suffix
        if self.parameter_binds: optional['parameter_binds'] = self.options.parameter_binds
        if self.parametric_pulses: optional['parametric_pulses'] = self.options.parametric_pulses
        if self.reference_measurement: optional['reference_measurement'] = self.options.reference_measurement
        if self.relax: optional['relax'] = self.options.relax
        if self.relax_time: optional['relax_time'] = self.options.relax_time
        if self.sequence_settings: optional['sequence_settings'] = self.options.sequence_settings
        if self.store_nt_result: optional['store_nt_result'] = self.options.store_nt_result
        if self.trigger_time: optional['trigger_time'] = self.options.trigger_time
        if self.weighting_amp: optional['weighting_amp'] = self.options.weighting_amp
        return optional
