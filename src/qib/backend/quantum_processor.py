from __future__ import annotations

import abc
from typing import Sequence
from qib.circuit import Circuit
from qib.field import Field
from qib.backend import Experiment, ExperimentResults, Options


class QuantumProcessor(abc.ABC):

    @property
    @abc.abstractmethod
    def configuration(self) -> ProcessorConfiguration:
        pass

    @abc.abstractmethod
    def submit_experiment(self, circ: Circuit, fields: Sequence[Field], options: Options) -> Experiment:
        """
        Submit a quantum circuit, fields, and options to a backend provider,
        returning an "experiment" object to query the results.
        """
        pass


class ProcessorConfiguration:

    def __init__(
            self,
            backend_name: str,
            backend_version: str,
            n_qubits: int,
            basis_gates: Sequence[str],
            coupling_map: Sequence[Sequence[int]],
            local: bool,
            simulator: bool,
            conditional: bool,
            open_pulse: bool,
            max_shots: int
    ) -> None:
        self.backend_name = backend_name
        self.backend_version = backend_version
        self.n_qubits = n_qubits
        self.basis_gates = basis_gates
        self.coupling_map = coupling_map
        self.local = local
        self.simulator = simulator
        self.conditional = conditional
        self.open_pulse = open_pulse
        self.max_shots = max_shots
