import abc
from typing import Sequence
from qib.operator import AbstractOperator
from qib.field import Field, Particle, Qubit


class Measurement(AbstractOperator):
    """
    Measurement operator for a quantum circuit.

    A quantum measurement represents the corresponding operator that measures a quantum bit into a classical bit,
    and can store the qubits (or in general quantum particles) it operates on.
    """

    def __init__(self, qubits: Sequence[Qubit] = None):
        self.qubits = qubits

    def is_unitary(self):
        """
        A quantum measurement operator is never unitary.
        """
        return False

    def is_hermitian(self):
        """
        A quantum measurement operator is always non-Hermitian.
        """
        return False

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this operator is performed on.
        """
        if self.qubits:
            return len(self.qubits)
        return 0

    def particles(self):
        """
        Return the list of quantum particles the operator is performed on.
        """
        if self.qubits:
            return [q for q in self.qubits]
        return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the operator is performed on.
        """
        if self.qubits:
            return [q.field for q in self.qubits]
        return []

    def as_matrix(self, fields: Sequence[Field]):
        """
        Generate the (sparse) matrix representation of the operator.
        """
        raise NotImplementedError()  # TODO: Decide if this is needed

    def as_qobj_openQASM(self):
        """
        Generate a Qobj OpenQASM representation of the operator.
        """
        return {
            "name": "measure",
            "qubits": [q.index for q in self.qubits],
            "memory": [q.index for q in self.qubits]
        }
