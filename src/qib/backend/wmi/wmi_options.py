from qib.backend.options import Options


class WMIOptions(Options):

    def __init__(self,
                 shots,
                 memory,
                 do_emulation,
                 loops,
                 sequence_settings,
                 reference_measurement,
                 trigger_time,
                 relax,
                 relax_time,
                 default_qubits,
                 weighting_amp,
                 acquisition_mode,
                 averaging_mode,
                 log_level,
                 log_level_std,
                 log_file_level,
                 store_nt_result,
                 name_suffix,
                 meas_level,
                 fridge
                 ):
        super().__init__(shots, memory, do_emulation)
        self.loops = loops
        self.sequence_settings = sequence_settings
        self.reference_measurement = reference_measurement
        self.trigger_time = trigger_time
        self.relax = relax
        self.relax_time = relax_time
        self.default_qubits = default_qubits
        self.weighting_amp = weighting_amp
        self.acquisition_mode = acquisition_mode
        self.averaging_mode = averaging_mode
        self.log_level = log_level
        self.log_level_std = log_level_std
        self.log_file_level = log_file_level
        self.store_nt_result = store_nt_result
        self.name_suffix = name_suffix
        self.meas_level = meas_level
        self.fridge = fridge

    # TODO: Move default_options here
