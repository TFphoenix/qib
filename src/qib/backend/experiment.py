from __future__ import annotations

import abc
from enum import Enum

from qib.circuit import Circuit
from qib.backend import Options, ProcessorConfiguration, ProcessorCredentials


class ExperimentStatus(str, Enum):
    INITIALIZING = 'INITIALIZING'
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    ERROR = 'ERROR'
    CANCELLED = 'CANCELLED'


class ExperimentType(str, Enum):
    QASM = 'QASM'
    PULSE = 'PULSE'


class Experiment(abc.ABC):
    """
    Parent class for a quantum experiment.

    The actual quantum experiment performed on a given quantum processor.
    """

    @abc.abstractmethod
    def __init__(
            self,
            name: str,
            circuit: Circuit,
            options: Options,
            configuration: ProcessorConfiguration,
            credentials: ProcessorCredentials,
            type: ExperimentType,
    ):
        self.name: str = name
        self.circuit = circuit
        self.options: Options = options
        self.type: ExperimentType = type
        self.configuration: ProcessorConfiguration = configuration
        self.credentials = credentials
        self._initialize()

    @abc.abstractmethod
    def query_status(self) -> ExperimentStatus:
        """
        Query the current status of a previously submitted experiment.
        
        If the experiment was already executed successfully when calling this method,
        the results will be automatically populated
        """
        
    @abc.abstractmethod
    def results(self) -> ExperimentResults:
        """
        Get the results of a a previously submitted experiment (BLOCKING).
        """

    @abc.abstractmethod
    async def wait_for_results(self) -> ExperimentResults:
        """
        Wait for the results of a previously submitted experiment (NON-BLOCKING).
        """

    @abc.abstractmethod
    def cancel(self) -> ExperimentResults:
        """
        Cancel a previously submitted experiment.
        """

    @abc.abstractmethod
    def as_openQASM(self) -> dict:
        """
        Get the Qobj OpenQASM representation of the experiment.
        """
        
    @abc.abstractmethod
    def from_json(self, json: dict) -> Experiment:
        """
        Update an experiment object from a JSON dictionary.
        """

    @abc.abstractmethod
    def _validate(self):
        """
        Validate the experiment in the context of its quantum processor.
        """

    def _initialize(self):
        """
        Initialize the experiment.
        """
        self.error: str = None
        self.id: int = 0
        self.instructions: list = self.circuit.as_openQASM()
        self.status: ExperimentStatus = ExperimentStatus.INITIALIZING
        self._results: ExperimentResults = None


class ExperimentResults(abc.ABC):
    """
    Parent class for a quantum experiment results.

    The results of a quantum experiment performed on a given
    quantum processor.
    """
    
    @abc.abstractmethod
    def from_json(self, json: dict) -> ExperimentResults:
        """
        Initialize an experiment results object from a JSON dictionary.
        """
