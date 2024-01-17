from typing import Sequence
from qib.backend import QuantumProcessor, ProcessorConfiguration
from qib.backend.qiskit import QiskitSimExperiment, QiskitSimOptions
from qib.circuit import Circuit
from qib.field import Field


class QiskitSimProcessor(QuantumProcessor):
    _applicant_id_count = 1000

    def __init__(self, access_token: str):
        self.url: str = "https://wmiqc-api.wmi.badw.de/1/qiskitSimulator"
        self.access_token: str = access_token

        self.configuration = ProcessorConfiguration(
            backend_name="QiskitSimulator",
            backend_version="1.0.0",
            n_qubits=3,
            basis_gates=['x', 'sx', 'rz', 'cz'],
            coupling_map=None,
            local=False,
            simulator=True,
            conditional=False,
            open_pulse=False
        )

    @property
    def configuration(self):
        return self.configuration

    def submit_experiment(self, circ: Circuit, fields: Sequence[Field], options: QiskitSimOptions = None) -> QiskitSimExperiment:
        if options is None:
            options = QiskitSimOptions.default()
        # TODO: validate circuit
        # TODO: serialize circuit to Qobj
        # TODO: generate experiment object
        # TODO: submit experiment via HTTP request
        # TODO: return experiment object
        pass

    def _http_put_experiment(self, experiment):
        pass
