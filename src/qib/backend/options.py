import abc


class Options(abc.ABC):

    @abc.abstractmethod
    def __init__(
            self,
            shots: int,
            memory: bool,
            do_emulation: bool
    ) -> None:
        self.shots = shots
        self.memory = memory
        self.do_emulation = do_emulation
