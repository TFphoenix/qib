from __future__ import annotations

import abc


class Experiment(abc.ABC):
    @abc.abstractmethod
    def query_results(self) -> ExperimentResults:
        """
        Query results of a previously submitted experiment.
        """
        pass

    @abc.abstractmethod
    async def wait_for_results(self) -> ExperimentResults:
        """
        Wait for results of a previously submitted experiment.
        """
        pass


class ExperimentResults(abc.ABC):
    pass
