import abc
from qib.operator import AbstractOperator


class Measurement(AbstractOperator):
    """
    Measurement operation for a quantum circuit.

    TODO
    """

    def is_unitary(self):
        """
        A quantum measurement operation is never unitary.
        """
        return False

    @property
    @abc.abstractmethod
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this operation is performed on.
        """

    @abc.abstractmethod
    def particles(self):
        """
        Return the list of quantum particles the operation is performed on.
        """

    @abc.abstractmethod
    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the operation is performed on.
        """

    @abc.abstractmethod
    def inverse(self):
        """
        Return the inverse operator.
        """

    @abc.abstractmethod
    def as_circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """

    @abc.abstractmethod
    def as_tensornet(self):
        """
        Generate a tensor network representation of the gate,
        using an individual tensor axis for each wire.
        """
        
    @abc.abstractmethod
    def as_qobj_openQASM(self):
        """
        Generate a Qobj OpenQASM representation of the gate.
        """

    @abc.abstractmethod
    def __copy__(self):
        """
        Create a copy of the gate.
        """

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
