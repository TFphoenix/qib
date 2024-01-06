import abc
from typing import Sequence
from qib.circuit import Circuit
from qib.field import Field


class QuantumProcessor(abc.ABC):

    @property
    @abc.abstractmethod
    def configuration(self):
        pass

    @abc.abstractmethod
    def submit(self, circ: Circuit, fields: Sequence[Field], description):
        """
        Submit a quantum circuit to a backend provider,
        returning a "job" object to query the results.
        """
        pass

    @abc.abstractmethod
    def query_results(self, job):
        """
        Query results of a previously submitted job.
        """
        pass


class ProcessorConfiguration:

    def __init__(
            self,
            backend_name: str,
            backend_version: str,
            n_qubits: int,
            basis_gates: Sequence[str],
            local: bool,
            simulator: bool,
            conditional: bool,
            open_pulse: bool
    ) -> None:
        self.backend_name = backend_name
        self.backend_version = backend_version
        self.n_qubits = n_qubits
        self.basis_gates = basis_gates
        self.local = local
        self.simulator = simulator
        self.conditional = conditional
        self.open_pulse = open_pulse


class ProcessorOptions:

    def __init__(
            self,
    ) -> None:
        pass  # TODO
