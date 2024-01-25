from typing import Any

from qib.util import const
from qib.circuit import Circuit
from qib.backend import Experiment, ExperimentResults, ExperimentType, Options
from qib.backend.qiskit import QiskitSimOptions, QiskitSimExperiment, QiskitSimExperimentResults


class QiskitSimExperiment(Experiment):
    """
    The WMI Qiskit Simulator quantum experiment implementation.
    """
    
    def __init__(self, circuit: Circuit, options: QiskitSimOptions, type: ExperimentType = ExperimentType.QASM):
        super().__init__(circuit, options, type)
        self.qobj_id = const.QOBJ_ID_QISM_EXPERIMENT
        
    def query_status(self) -> QiskitSimExperimentResults:
        # TODO: Ensure that experiment was submitted (status != INITIALIZING)
        pass
    
    async def wait_for_results(self) -> QiskitSimExperimentResults:
        # TODO: Ensure that experiment was submitted (status != INITIALIZING)
        pass
    
    def cancel(self) -> QiskitSimExperimentResults:
        pass
    
    def as_openQASM(self) -> dict:
        qubits = self.circuit.particles()
        bits = self.circuit.bits()
        return {
            'qobj_id': self.qobj_id,
            'type': self.type.value,
            'schema_version': const.QOBJ_SCHEMA_VERSION,
            'experiments': [
                    {
                        'header': {}, # TODO
                        'config': {}, # TODO
                        'instructions': self.instructions
                    }
                ],
            'header': {
                "backend_name": const.BACK_QSIM_NAME,
                "backend_version": const.BACK_QSIM_VERSION,
                },
            'config': {
                'shots': self.options.shots,
                'memory': True,
                'meas_level': 2,
                'init_qubits': self.options.init_qubits,
                'do_emulation': False,
                'memory_slots': len(bits),
                'n_qubits': len(qubits)
            },
        }


class QiskitSimExperimentResults(ExperimentResults):
    pass
