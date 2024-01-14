from typing import Sequence
from qib.backend import QuantumProcessor, ProcessorConfiguration
from qib.backend.qiskit import QiskitSimExperiment, QiskitSimOptions
from qib.circuit import Circuit
from qib.field import Field


class QiskitSimProcessor(QuantumProcessor):

    def __init__(self):
        self.configuration = ProcessorConfiguration(
            backend_name="QiskitSimulator",
            backend_version="1.0.0",
            n_qubits=3,
            basis_gates=['x', 'sx', 'rz', 'cz'],
            local=False,
            simulator=True,
            conditional=False,
            open_pulse=False
        )

    @property
    def configuration(self):
        return self.configuration

    def submit_experiment(self, circ: Circuit, fields: Sequence[Field], options: QiskitSimOptions) -> QiskitSimExperiment:
        # TODO: transpile circuit into QObj
        # TODO: generate experiment object
        # TODO: submit experiment via HTTP request
        # TODO: return experiment object
        pass
