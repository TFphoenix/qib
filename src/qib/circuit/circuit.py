from typing import Sequence
from qib.operator import Gate
from qib.field import Field


class Circuit:
    """
    A quantum circuit consists of a list of quantum gates.

    We follow the convention that the first gate in the list is applied first.
    """
    def __init__(self, gates: Sequence[Gate]=[]):
        self.gates = list(gates)

    def append_gate(self, gate: Gate):
        """
        Append a quantum gate.
        """
        self.gates.append(gate)

    def fields(self):
        """
        List of all fields appearing in the circuit.
        Warning: the order of fields may change at every iteration
        """
        f = set()
        for g in self.gates:
            f = f.union(g.fields())
        return list(f)

    def as_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the circuit.
        """
        if not self.gates:
            raise RuntimeError("missing gates, hence cannot compute matrix representation of circuit")
        # Warning: do not use the ones saved in self.fields() because the order is not fixed 
        if not fields:
            raise RuntimeError("missing fields, hence cannot compute matrix representation of circuit")
        mat = self.gates[0]._circuit_matrix(fields)
        for g in self.gates[1:]:
            mat = g._circuit_matrix(fields) @ mat
        return mat
