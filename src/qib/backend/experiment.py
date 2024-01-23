from __future__ import annotations

import abc
from enum import Enum
from qib.circuit import Circuit
from qib.backend import Options


class ExperimentStatus(str, Enum):
    INITIALIZING = 'INITIALIZING'
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    ERROR = 'ERROR'
    CANCELLED = 'CANCELLED'


class ExperimentType(str, Enum):
    QASM = 'OpenQASM'
    PULSE = 'OpenPulse'


class Experiment(abc.ABC):
    """
    Parent class for a quantum experiment.

    The actual quantum experiment performed on a given quantum processor.
    """

    @abc.abstractmethod
    def __init__(
            self,
            circuit: Circuit,
            options: Options,
            type: ExperimentType = ExperimentType.QASM
    ) -> None:
        self.id: int = 0
        self.status: ExperimentStatus = ExperimentStatus.INITIALIZING
        self.instructions: list = circuit.as_openQASM()
        self.options: Options = options
        self.type: ExperimentType = type

    @abc.abstractmethod
    def query_status(self) -> ExperimentResults:
        """
        Query the current status of a previously submitted experiment.
        """
        # TODO: Ensure that experiment was submitted (status != INITIALIZING)

    @abc.abstractmethod
    async def wait_for_results(self) -> ExperimentResults:
        """
        Wait for results of a previously submitted experiment.
        """
        # TODO: Ensure that experiment was submitted (status != INITIALIZING)

    @abc.abstractmethod
    async def cancel(self) -> ExperimentResults:
        """
        Cancel a previously submitted experiment.
        """

    @abc.abstractmethod
    def as_openQASM(self) -> dict:
        """
        Get the Qobj OpenQASM representation of the experiment.
        """


class ExperimentResults(abc.ABC):
    """
    Parent class for a quantum experiment results.

    The results of a quantum experiment performed on a given
    quantum processor.
    """
