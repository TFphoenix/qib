from typing import Sequence
from qib.backend import QuantumProcessor
from qib.backend import ProcessorConfiguration
from qib.circuit import Circuit
from qib.field import Field


class QiskitSimProcessor(QuantumProcessor):

    def __init__(self):
        self.configuration = ProcessorConfiguration(
            # backend_name="WMIQC",
            # backend_version="1.0.0",
            # n_qubits=6,
            # basis_gates=['id', 'x', 'y', 'sx', 'rz', 'cz'],
            # local=False,
            # simulator=False,
            # conditional=False,
            # open_pulse=True
        )

    @property
    def configuration(self):
        return self.configuration

    def submit(self, circ: Circuit, fields: Sequence[Field], description):
        # TODO: transpile circuit into QObj
        # TODO: send QObj to WMI Backend
        # TODO: Register & return quantum process with WMI Backend
        pass

    def query_results(self, experiment):
        pass
