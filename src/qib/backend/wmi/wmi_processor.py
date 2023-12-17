from typing import Sequence
from qib.backend import QuantumProcessor
from qib.circuit import Circuit
from qib.field import Field


class WMIProcessor(QuantumProcessor):

    def __init__(self):
        pass

    def submit(self, circ: Circuit, fields: Sequence[Field], description):
        # TODO: transpile circuit into QObj
        # TODO: send QObj to WMI Backend
        # TODO: Register & return quantum process with WMI Backend
        pass

    def query_results(self, job):
        pass
