from __future__ import annotations

from typing import Any
from itertools import combinations
import uuid

from qib.util import const
from qib.field import Particle
from qib.circuit import Circuit
from qib.backend import ExperimentStatus, Experiment, ExperimentResults, ExperimentType, ProcessorConfiguration
from qib.backend.wmi import WMIOptions


class WMIExperiment(Experiment):
    """
    The WMI quantum experiment implementation.
    """
    
    def __init__(self,
                 name: str, 
                 circuit: Circuit,
                 options: WMIOptions,
                 configuration: ProcessorConfiguration,
                 processor_token: str,
                 type: ExperimentType = ExperimentType.QASM):
        super().__init__(name, circuit, options, configuration, type)
        self.processor_token: str = processor_token
        self.qobj_id = uuid.uuid4()
        self.schema_version = const.QOBJ_SCHEMA_VERSION
        
        self._mode: str = None
        self._job_id: str = None
        self._execution_datetime: str = None
        self._validate()
    
    def query_status(self) -> ExperimentStatus:
        if self.status == ExperimentStatus.INITIALIZING:
            raise ValueError("Experiment has to be submitted first.")
        elif (self.status == ExperimentStatus.DONE or
              self.status == ExperimentStatus.ERROR or
              self.status == ExperimentStatus.CANCELLED):
            raise ValueError("Experiment has already been executed.")
        
        # TODO

    def results(self) -> WMIExperimentResults:
        if self._results is not None: return self._results
        # TODO
        # self.query_status() with FRQ, 'till experiment finished, error, or cancelled

    async def wait_for_results(self) -> WMIExperimentResults:
        if self._results is not None: return self._results
        # TODO
        pass
    
    def cancel(self) -> WMIExperimentResults:
        pass
    
    def as_openQASM(self) -> dict:
        qubits: set[Particle] = self.circuit.particles()
        clbits: set[int] = self.circuit.clbits()
        return {
            'qobj_id': str(self.qobj_id),
            'type': self.type.value,
            'schema_version': self.schema_version,
            'experiments': [
                    {
                        'header': {
                            'qubit_labels': {'qubits': [['q', qubit.index] for qubit in qubits]},
                            'n_qubits': len(qubits),
                            'qreg_sizes': {'q': len(qubits)},
                            'clbit_labels': {'clbits': [['c', clbit] for clbit in clbits]},
                            'memory_slots': len(clbits),
                            'creg_sizes': {'q': len(clbits)},
                            'name': self.name,
                            'global_phase': 0.0,
                            'metadata': {}
                            },
                        'config': {
                            'n_qubits': len(qubits),
                            'memory_slots': len(clbits)
                            },
                        'instructions': self.instructions
                    }
                ],
            'header': {
                'backend_name': self.configuration.backend_name,
                'backend_version': self.configuration.backend_version,
                },
            'config': {
                'shots': self.options.shots,
                'memory': self.configuration.memory,
                'meas_level': self.configuration.meas_level,
                'init_qubits': self.options.init_qubits,
                'do_emulation': False,
                'memory_slots': len(clbits),
                'n_qubits': len(qubits),
                
                # TEST: Missing properties
                # 'acquisition_mode': 'integration_trigger',
                # 'averaging_mode': 'single_shot',
                # 'chip': 'dedicatedSimulator',
                # 'log_file_level': 'debug',
                # 'log_level_std': 'info',
                # 'log_level': 'debug',
                # 'loops': {},
                # 'name_suffix': '',
                # 'parameter_binds': [],
                # 'parametric_pulses': [],
                # 'reference_measurement': {'function': 'nothing'},
                # 'relax': True,
                # 'sequence_settings': {},
                # 'store_nt_result': True,
                # 'trigger_time': 0.001,
                # 'weighting_amp': 1.0,
            },
        }
        
    def from_json(self, json: dict) -> WMIExperiment:
        self._job_id = json['job_id']
        self._execution_datetime = json['execution_datetime']
        self._mode = json['mode']
        self._from_wmi_status(json['status'])
        
    def _validate(self):
        # check that the number of shots is not exceeded
        if self.options.shots > self.configuration.max_shots:
            raise ValueError("Number of shots exceeds maximum allowed number of shots.")

        for gate in self.circuit.gates:
            gate_openQASM = gate.as_openQASM()
            gate_name = gate_openQASM['name']
            gate_qubits = gate_openQASM['qubits']
            gate_params = gate_openQASM['params'] if 'params' in gate_openQASM else []
            
            if gate_name != 'measure':
                # check that the gate is supported by the processor
                if gate_name not in self.configuration.basis_gates:
                    raise ValueError(f"Gate {type(gate)} is not supported by the processor.")
                
                # check that the used qubits are configured for the gate
                gate_properties = self.configuration.get_gate_by_name(gate_name)
                if gate_properties is None:
                    raise ValueError(f"Gate {type(gate)} is not configured by the processor.")
                if not gate_properties.check_qubits(gate_qubits):
                    raise ValueError(f"Gate {type(gate)} is not configured for the used qubits.")
                if not gate_properties.check_params(gate_params):
                    raise ValueError(f"Gate {type(gate)} is not configured for the used parameters.")

            # check that gates are performed only on coupled qubits
            if len(gate_qubits) > 1 and self.configuration.coupling_map:
                qubit_pairs = list(combinations(gate_qubits, 2))
                for qubit_pair in qubit_pairs:
                    if qubit_pair not in self.configuration.coupling_map:
                        raise ValueError(f"Gate {type(gate)} is not performed on coupled qubits.")
            
        # check that the number of qubits is adequate
        qubits: set[Particle] = gate.particles()
        qubits_index = [q.index for q in qubits]
        if len(qubits) > self.configuration.n_qubits \
        or min(qubits_index) < 0 \
        or max(qubits_index) >= self.configuration.n_qubits:
            raise ValueError("Number of qubits exceeds maximum allowed number of qubits, or indexes are incorrect.")

    def _from_wmi_status(self, status: str):
        """
        Set the status of the experiment (convert from WMI-specific format).
        """
        if status == 'pending':
            self.status = ExperimentStatus.QUEUED
        elif status == 'active':
            self.status = ExperimentStatus.RUNNING
        elif status == 'finished':
            self.status = ExperimentStatus.DONE
        elif status == 'cancelled':
            self.status = ExperimentStatus.CANCELLED
        elif status == 'offline':
            self.status = ExperimentStatus.ERROR
            self.error = 'The backend is offline.'
        else:
            self.status = ExperimentStatus.ERROR
            self.error = 'Unknown error.'


class WMIExperimentResults(ExperimentResults):
    """
    The WMI quantum experiment results implementation.
    """
        
    def from_json(self, json: dict) -> WMIExperimentResults:
        self._runtime: float = json['runtime']
        self._counts: dict = json['counts'][0]
        return self
