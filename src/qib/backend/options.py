from __future__ import annotations

import abc


class Options(abc.ABC):
    """
    Parent class for a quantum experiment options.

    The options of a quantum experiment performed on a given
    quantum processor.
    """

    @abc.abstractmethod
    def __init__(
            self,
            shots: int,
    ) -> None:
        self.shots: int = shots

    @staticmethod
    @abc.abstractmethod
    def default() -> Options:
        """
        The default options of a given processor.
        """
