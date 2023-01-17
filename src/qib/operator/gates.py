import abc
import numpy as np
from enum import Enum
from copy import copy
from scipy.linalg import expm, sqrtm, block_diag
from scipy.sparse import csr_matrix
from typing import Sequence, Union
from qib.field import Field, Particle, Qubit
from qib.operator import AbstractOperator


class Gate(AbstractOperator):
    """
    Parent class for quantum gates.

    A quantum gate represents the corresponding unitary operation,
    and can store the qubits (or in general quantum particles) it acts on.
    """

    def is_unitary(self):
        """
        A quantum gate is unitary by definition.
        """
        return True

    @property
    @abc.abstractmethod
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        pass

    @abc.abstractmethod
    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        pass

    @abc.abstractmethod
    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        pass

    @abc.abstractmethod
    def inverse(self):
        """
        Return the inverse operator.
        """
        pass

    @abc.abstractmethod
    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        pass

    @abc.abstractmethod
    def __copy__(self):
        """
        Create a copy of the gate.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        pass


class PauliXGate(Gate):
    """
    Pauli-X gate.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return True

    def as_matrix(self):
        """
        Generate the matrix representation of the Pauli-X gate.
        """
        return np.array([[ 0.,  1.], [ 1.,  0.]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return self

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return PauliXGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        if type(other) == type(self) and other.qubit == self.qubit:
            return True
        return False


class PauliYGate(Gate):
    """
    Pauli-Y gate.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return True

    def as_matrix(self):
        """
        Generate the matrix representation of the Pauli-Y gate.
        """
        return np.array([[ 0., -1j], [ 1j,  0.]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return self

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return PauliYGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class PauliZGate(Gate):
    """
    Pauli-Z gate.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return True

    def as_matrix(self):
        """
        Generate the matrix representation of the Pauli-Z gate.
        """
        return np.array([[ 1.,  0.], [ 0., -1.]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return self

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return PauliZGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class HadamardGate(Gate):
    """
    Hadamard gate.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return True

    def as_matrix(self):
        """
        Generate the matrix representation of the Hadamard gate.
        """
        return np.array([[ 1.,  1.], [ 1., -1.]]) / np.sqrt(2)

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return self

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return HadamardGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class RxGate(Gate):
    """
    X-axis rotation gate.
    """
    def __init__(self, theta: float, qubit: Qubit=None):
        self.theta = theta
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        c = np.cos(self.theta/2)
        s = np.sin(self.theta/2)
        return np.array([[c, -1j*s], [-1j*s, c]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    @property
    def rotation_angle(self):
        """
        The rotation angle
        """
        return self.theta

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return RxGate(-self.theta, self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return RxGate(self.theta, self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit and other.theta == self.theta


class RyGate(Gate):
    """
    Y-axis rotation gate
    """
    def __init__(self, theta: float, qubit: Qubit=None):
        self.theta = theta
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        c = np.cos(self.theta/2)
        s = np.sin(self.theta/2)
        return np.array([[c, -s], [s, c]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    @property
    def rotation_angle(self):
        """
        The rotation angle
        """
        return self.theta

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return RyGate(-self.theta, self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return RyGate(self.theta, self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit and other.theta == self.theta


class RzGate(Gate):
    """
    Z-axis rotation gate
    """
    def __init__(self, theta: float, qubit: Qubit=None):
        self.theta = theta
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        x = np.exp(1j*self.theta/2)
        return np.array([[x.conj(), 0], [0, x]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    @property
    def rotation_angle(self):
        """
        The rotation angle
        """
        return self.theta

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return RzGate(-self.theta, self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return RzGate(self.theta, self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit and other.theta == self.theta


class RotationGate(Gate):
    """
    General rotation gate; the rotation angle and axis are combined into
    a single vector `ntheta` of length 3.
    """
    def __init__(self, ntheta: Sequence[float], qubit: Qubit=None):
        self.ntheta = np.array(ntheta, copy=False)
        if self.ntheta.shape != (3,):
            raise ValueError("'ntheta' must be a vector of length 3")
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        theta = np.linalg.norm(self.ntheta)
        if theta == 0:
            return np.identity(2)
        n = self.ntheta / theta
        return (     np.cos(theta/2)*np.identity(2)
                - 1j*np.sin(theta/2)*np.array([[n[2], n[0] - 1j*n[1]], [n[0] + 1j*n[1], -n[2]]]))

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return RotationGate(-self.ntheta, self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return RotationGate(self.ntheta, self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit and np.allclose(other.ntheta, self.ntheta)


class SGate(Gate):
    """
    S (phase) gate - provides a phase shift of pi/2.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        return np.array([[ 1.,  0.], [ 0.,  1j]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return SAdjGate(self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return SGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class SAdjGate(Gate):
    """
    Adjoint of S gate - provides a phase shift of -pi/2.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        return np.array([[ 1.,  0.], [ 0., -1j]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return SGate(self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return SAdjGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class TGate(Gate):
    """
    T gate - provides a phase shift of pi/4.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        return np.array([[ 1.,  0.], [ 0., (1+1j)/np.sqrt(2)]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return TAdjGate(self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return TGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class TAdjGate(Gate):
    """
    Adjoint of T gate - provides a phase shift of -pi/4.
    """
    def __init__(self, qubit: Qubit=None):
        self.qubit = qubit

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the gate.
        """
        return np.array([[ 1.,  0.], [ 0., (1-1j)/np.sqrt(2)]])

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return 1

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if self.qubit:
            return [self.qubit]
        else:
            return []

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        if self.qubit:
            return [self.qubit.field]
        else:
            return []

    def inverse(self):
        """
        Return the inverse operator.
        """
        return TGate(self.qubit)

    def on(self, qubit: Qubit):
        """
        Act on the specified qubit.
        """
        self.qubit = qubit
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.qubit:
            raise RuntimeError("unspecified target qubit")
        iwire = _map_particle_to_wire(fields, self.qubit)
        if iwire < 0:
            raise RuntimeError("qubit not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, [iwire], csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return TAdjGate(self.qubit)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.qubit == self.qubit


class PhaseFactorGate(Gate):
    """
    Phase factor gate: multiplication by the phase factor :math:`e^{i \phi}`.
    """
    def __init__(self, phi: float, nwires: int):
        self.phi = phi
        self.nwires = nwires
        self.prtcl = []

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the phase factor gate.
        """
        # TODO: generalize base 2
        return np.exp(1j*self.phi) * np.identity(2**self.nwires)

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return self.nwires

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        return self.prtcl

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        flist = []
        for p in self.prtcl:
            if p.field not in flist:
                flist.append(p.field)
        return flist

    def inverse(self):
        """
        Return the inverse operator.
        """
        return PhaseFactorGate(-self.phi, self.nwires)

    def on(self, *args):
        """
        Act on the specified particle(s).
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            prtcl = list(args[0])
        else:
            prtcl = list(args)
        if len(prtcl) != self.nwires:
            raise ValueError(f"require {self.nwires} particles, but received {len(prtcl)}")
        self.prtcl = prtcl
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.prtcl:
            raise RuntimeError("unspecified target particle(s)")
        iwire = [_map_particle_to_wire(fields, p) for p in self.prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        gate = PhaseFactorGate(self.phi, self.nwires)
        gate.on(self.prtcl)
        return gate

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.prtcl == self.prtcl and other.phi == self.phi and other.nwires == self.nwires


class PrepareGate(Gate):
    """
    Vector "preparation" gate.
    """
    def __init__(self, vec, nqubits: int, transpose=False):
        vec = np.array(vec)
        if vec.ndim != 1:
            raise ValueError("expecting a vector")
        if not np.isrealobj(vec):
            raise ValueError("only real-valued vectors supported")
        if vec.shape[0] != 2**nqubits:
            raise ValueError(f"input vector must have length 2^nqubits = {2**nqubits}")
        # note: using 1-norm here by convention
        n = np.linalg.norm(vec, ord=1)
        if abs(n - 1) > 1e-12:
            vec /= n
        self.vec = vec
        self.nqubits = nqubits
        self.qubits = []
        self.transpose = transpose

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        # in general not Hermitian
        # TODO: can one construct a Hermitian realization?
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the "preparation" gate.
        """
        x = np.sign(self.vec) * np.sqrt(np.abs(self.vec))
        # use QR decomposition for extension to full basis
        Q = np.linalg.qr(x.reshape((-1, 1)), mode="complete")[0]
        if np.dot(x, Q[:, 0]) < 0:
            Q[:, 0] = -Q[:, 0]
        if not self.transpose:
            return Q
        else:
            return Q.T

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return self.nqubits

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        return self.qubits

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        flist = []
        for q in self.qubits:
            if q.field not in flist:
                flist.append(q.field)
        return flist

    def inverse(self):
        """
        Return the inverse operator.
        """
        invgate = PrepareGate(self.vec, self.nqubits, not self.transpose)
        if self.qubits:
            invgate.on(self.qubits)
        return invgate

    def on(self, *args):
        """
        Act on the specified qubit(s).
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            qubits = list(args[0])
        else:
            qubits = list(args)
        if len(qubits) != self.nqubits:
            raise ValueError(f"expecting {self.nqubits} qubits, but received {len(qubits)}")
        self.qubits = qubits
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if len(self.qubits) != self.nqubits:
            raise RuntimeError("unspecified qubit(s)")
        prtcl = self.particles()
        iwire = [_map_particle_to_wire(fields, p) for p in prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        gate = PrepareGate(self.vec, self.nqubits, self.transpose)
        gate.on(self.qubits)
        return gate

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return (type(other) == type(self) and other.nqubits == self.nqubits and np.allclose(other.vec, self.vec)
                and other.qubits == self.qubits and other.transpose == self.transpose)


class ControlledGate(Gate):
    """
    A controlled quantum gate with an arbitrary number of control qubits.
    The control qubits have to be set explicitly.
    The target qubits (or particles) are specified via the target gate.
    """
    def __init__(self, tgate: Gate, ncontrols: int, ctrl_state: Sequence[int]=None):
        self.tgate = tgate
        self.ncontrols = ncontrols
        self.control_qubits = []
        # standard case: control is active if all control qubits are in |1> state
        if ctrl_state is None:
            ctrl_state = ncontrols * [1]
        if len(ctrl_state) != ncontrols:
            raise ValueError(f"length of `ctrl_state` must be equal to number of control qubits, {ncontrols}")
        for i in ctrl_state:
            if not (i == 0 or i == 1):
                raise ValueError(f"`ctrl_state` can only contain 0 or 1 bits, received {i}")
        self.ctrl_state = list(ctrl_state)

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return self.tgate.is_hermitian()

    def inverse(self):
        """
        Return the inverse operator.
        """
        invgate = ControlledGate(self.tgate.inverse(), self.ncontrols, self.ctrl_state)
        if self.control_qubits:
            invgate.set_control(self.control_qubits)
        return invgate

    def as_matrix(self):
        """
        Generate the matrix representation of the controlled gate.
        Format: |control> x |target>
        """
        tgmat = self.tgate.as_matrix()
        # target gate corresponds to faster varying indices
        assert self.ncontrols == len(self.ctrl_state)
        cidx = np.zeros(2**self.ncontrols)
        ic = 0
        for j in range(self.ncontrols):
            if self.ctrl_state[j] == 1:
                # first digit is the most significant bit
                ic += 1 << (self.ncontrols - 1 - j)
        cidx[ic] = 1
        return (  np.kron(np.diag(1 - cidx), np.identity(tgmat.shape[0]))
                + np.kron(np.diag(cidx), tgmat))

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return self.tgate.num_wires + self.ncontrols

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        return self.control_qubits + self.tgate.particles()

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        flist = []
        for q in self.control_qubits:
            if q.field not in flist:
                flist.append(q.field)
        for f in self.tgate.fields():
            if f not in flist:
                flist.append(f)
        return flist

    def target_gate(self):
        """
        Get the target gate.
        """
        return self.tgate

    @property
    def num_controls(self):
        """
        The number of control qubits.
        """
        return self.ncontrols

    def set_control(self, *args):
        """
        Set the control qubits.
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            control_qubits = list(args[0])
        else:
            control_qubits = list(args)
        if len(control_qubits) != self.ncontrols:
            raise ValueError(f"require {self.ncontrols} control qubits, but received {len(control_qubits)}")
        self.control_qubits = control_qubits
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if len(self.control_qubits) != self.ncontrols:
            raise RuntimeError("unspecified control qubit(s)")
        if len(self.tgate.particles()) != self.tgate.num_wires:
            raise RuntimeError("unspecified target gate particle(s)")
        prtcl = self.particles()
        iwire = [_map_particle_to_wire(fields, p) for p in prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        gate = ControlledGate(copy(self.tgate), self.ncontrols, self.ctrl_state)
        gate.set_control(self.control_qubits)
        return gate

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return (type(other) == type(self)
                and other.tgate == self.tgate
                and other.ncontrols == self.ncontrols
                and other.ctrl_state == self.ctrl_state
                and other.control_qubits == self.control_qubits)


class MultiplexedGate(Gate):
    """
    Multiplexed gate (control qubits select a unitary), generalizing a controlled gate.
    """
    def __init__(self, tgates: Sequence[Gate], ncontrols: int):
        if len(tgates) != 2**ncontrols:
            assert ValueError(f"require {2**ncontrols} target gates for {ncontrols} control qubits")
        self.tgates = list(tgates)
        self.ncontrols = ncontrols
        self.control_qubits = []

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return all(g.is_hermitian() for g in self.tgates)

    def inverse(self):
        """
        Return the inverse operator.
        """
        invgate = MultiplexedGate([g.inverse() for g in self.tgates], self.ncontrols)
        if self.control_qubits:
            invgate.set_control(self.control_qubits)
        return invgate

    def as_matrix(self):
        """
        Generate the matrix representation of the multiplexed gate.
        """
        tgmat = [g.as_matrix() for g in self.tgates]
        # target gates correspond to faster varying indices
        return block_diag(*tgmat)

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        assert self.tgates
        return self.tgates[0].num_wires + self.ncontrols

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        assert self.tgates
        tprtcl = self.tgates[0].particles()
        for g in self.tgates:
            assert tprtcl == g.particles(), "particles of all target gates must match"
        return self.control_qubits + tprtcl

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        flist = []
        for q in self.control_qubits:
            if q.field not in flist:
                flist.append(q.field)
        assert self.tgates
        for g in self.tgates:
            assert self.tgates[0].fields() == g.fields(), "fields of all target gates must match"
        for f in self.tgates[0].fields():
            if f not in flist:
                flist.append(f)
        return flist

    def target_gates(self):
        """
        Get the target gates.
        """
        return self.tgates

    @property
    def num_controls(self):
        """
        The number of control qubits.
        """
        return self.ncontrols

    def set_control(self, *args):
        """
        Set the control qubits.
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            control_qubits = list(args[0])
        else:
            control_qubits = list(args)
        if len(control_qubits) != self.ncontrols:
            raise ValueError(f"require {self.ncontrols} control qubits, but received {len(control_qubits)}")
        self.control_qubits = control_qubits
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if len(self.control_qubits) != self.ncontrols:
            raise RuntimeError("unspecified control qubit(s)")
        for g in self.tgates:
            if len(g.particles()) != g.num_wires:
                raise RuntimeError("unspecified target gate particle(s)")
        prtcl = self.particles()
        iwire = [_map_particle_to_wire(fields, p) for p in prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        gate = MultiplexedGate(copy(self.tgates), self.ncontrols)
        gate.set_control(self.control_qubits)
        return gate

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return (type(other) == type(self)
                and other.tgates == self.tgates
                and other.ncontrols == self.ncontrols
                and other.control_qubits == self.control_qubits)


class TimeEvolutionGate(Gate):
    """
    Quantum time evolution gate, i.e., matrix exponential,
    given a Hamiltonian `h`: :math:`e^{-i h t}`.
    """
    def __init__(self, h: AbstractOperator, t: float):
        self.h = h
        self.t = t

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        # might be Hermitian in special cases, but difficult to check,
        # so returning False here for simplicity
        return False

    def as_matrix(self):
        """
        Generate the matrix representation of the time evolution gate.
        """
        hmat = self.h.as_matrix().toarray()
        # TODO: exploit that `hmat` is Hermitian for computing the matrix exponential
        return expm(-1j*self.t * hmat)

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        fields = self.h.fields()
        return sum(f.lattice.nsites for f in fields)

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        fields = self.h.fields()
        prtcl = []
        for f in fields:
            prtcl = prtcl + [Particle(f, i) for i in range(f.lattice.nsites)]
        return prtcl

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        return self.h.fields()

    def inverse(self):
        """
        Return the inverse operator.
        """
        return TimeEvolutionGate(self.h, -self.t)

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        prtcl = self.particles()
        assert len(prtcl) == self.num_wires
        iwire = [_map_particle_to_wire(fields, p) for p in prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        return TimeEvolutionGate(self.h, self.t)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return type(other) == type(self) and other.h == self.h and other.t == self.t


class BlockEncodingMethod(Enum):
    """
    Block encoding method.
    """
    Wx  = 1
    Wxi = 2 # inverse Wx
    R   = 3


class BlockEncodingGate(Gate):
    """
    Block encoding gate of a Hamiltonian `h`, assumed to be Hermitian
    and normalized such that its spectral norm is bounded by 1.
    Output state is Hamiltonian applied to principal input state
    if auxiliary qubit(s) is initialized to |0>.
    """
    def __init__(self, h: AbstractOperator, method: BlockEncodingMethod):
        self.h = h
        self.method = method
        self.auxiliary_qubits = []

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        if self.method == BlockEncodingMethod.Wx:
            return False
        elif self.method == BlockEncodingMethod.Wxi:
            return False
        elif self.method == BlockEncodingMethod.R:
            # assuming that `h` is Hermitian
            return True
        raise NotImplementedError(f"encoding method {self.method} not supported yet")

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        fields = self.h.fields()
        return sum(f.lattice.nsites for f in fields) + self.num_aux_qubits

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        if len(self.auxiliary_qubits) != self.num_aux_qubits:
            raise RuntimeError(f"require {self.num_aux_qubits} auxiliary qubits, but have {len(self.auxiliary_qubits)}")
        prtcl = [q for q in self.auxiliary_qubits]  # copy of list
        fields = self.h.fields()
        for f in fields:
            prtcl += [Particle(f, i) for i in range(f.lattice.nsites)]
        return prtcl

    def inverse(self):
        """
        Return the inverse operator.
        """
        if self.method == BlockEncodingMethod.Wx:
            ginv = BlockEncodingGate(self.h, BlockEncodingMethod.Wxi)
            if self.auxiliary_qubits:
                ginv.set_auxiliary_qubits(self.auxiliary_qubits)
            return ginv
        elif self.method == BlockEncodingMethod.Wxi:
            ginv = BlockEncodingGate(self.h, BlockEncodingMethod.Wx)
            if self.auxiliary_qubits:
                ginv.set_auxiliary_qubits(self.auxiliary_qubits)
            return ginv
        elif self.method == BlockEncodingMethod.R:
            return self
        raise NotImplementedError(f"encoding method {self.method} not supported yet")

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        flist = []
        for q in self.auxiliary_qubits:
            if q.field not in flist:
                flist.append(q.field)
        for f in self.h.fields():
            if f not in flist:
                flist.append(f)
        return flist

    def encoded_operator(self):
        """
        Get the encoded operator.
        """
        return self.h

    @property
    def num_aux_qubits(self):
        """
        Number of auxiliary qubits.
        """
        if self.method == BlockEncodingMethod.Wx:
            return 1
        elif self.method == BlockEncodingMethod.Wxi:
            return 1
        elif self.method == BlockEncodingMethod.R:
            return 1
        raise NotImplementedError(f"encoding method {self.method} not supported yet")

    def set_auxiliary_qubits(self, *args):
        """
        Set the auxiliary qubits.
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            auxiliary_qubits = list(args[0])
        else:
            auxiliary_qubits = list(args)
        if len(auxiliary_qubits) != self.num_aux_qubits:
            raise ValueError(f"require {self.num_aux_qubits} auxiliary qubits, but received {len(auxiliary_qubits)}")
        self.auxiliary_qubits = auxiliary_qubits
        # enable chaining
        return self

    def as_matrix(self):
        """
        Generate the matrix representation of the block encoding gate.
        Format: |ancillary> @ |encoded_state>
        """
        # assuming that `h` is Hermitian and that its spectral norm is bounded by 1
        hmat = self.h.as_matrix().toarray()
        sq1h = sqrtm(np.identity(hmat.shape[0]) - hmat @ hmat)
        if self.method == BlockEncodingMethod.Wx:
            return np.block([[hmat, 1j*sq1h], [1j*sq1h, hmat]])
        elif self.method == BlockEncodingMethod.Wxi:
            return np.block([[hmat, -1j*sq1h], [-1j*sq1h, hmat]])
        elif self.method == BlockEncodingMethod.R:
            return np.block([[hmat, sq1h], [sq1h, -hmat]])
        raise NotImplementedError(f"encoding method {self.method} not supported yet")

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if len(self.auxiliary_qubits) != self.num_aux_qubits:
            raise RuntimeError("unspecified auxiliary qubit(s)")
        prtcl = self.particles()
        assert len(prtcl) == self.num_wires
        iwire = [_map_particle_to_wire(fields, p) for p in prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Copy of the gate
        """
        block = BlockEncodingGate(self.h, self.method)
        if self.auxiliary_qubits:
            block.set_auxiliary_qubits(self.auxiliary_qubits)
        return block

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        # TODO: generalize the equivalence test between 2 generic operators...
        return (type(other) == type(self)
                and other.h == self.h
                and other.method == self.method
                and other.auxiliary_qubits == self.auxiliary_qubits)


class ProjectorControlledPhaseShift(Gate):
    """
    Projector-controlled phase shift gate.
    Building block for Qubitization.
    Projector is state |0> on the encoding (auxiliary) qubit
    TODO: generalize for different states
    """
    def __init__(self, theta: float,
                 encoding_qubits:  Union[Qubit, Sequence[Qubit]]=None,
                 auxiliary_qubits: Union[Qubit, Sequence[Qubit]]=None):
        self.theta = theta
        if type(auxiliary_qubits) == Qubit:
            self.auxiliary_qubits = [auxiliary_qubits]
        elif auxiliary_qubits is not None:
            self.auxiliary_qubits = list(auxiliary_qubits)
        if type(encoding_qubits) == Qubit:
            self.encoding_qubits = [encoding_qubits]
        elif auxiliary_qubits is not None:
            self.encoding_qubits = list(encoding_qubits)

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return False

    def inverse(self):
        """
        Return the inverse operator.
        """
        return ProjectorControlledPhaseShift(-self.theta, self.encoding_qubits, self.auxiliary_qubits)

    def set_encoding_qubits(self, *args):
        """
        Set the encoding qubits.
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            encoding_qubits = list(args[0])
        else:
            encoding_qubits = list(args)
        self.encoding_qubits = encoding_qubits
        # enable chaining
        return self

    def set_auxiliary_qubits(self, *args):
        """
        Set the auxiliary qubits.
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            auxiliary_qubits = list(args[0])
        else:
            auxiliary_qubits = list(args)
        self.auxiliary_qubits = auxiliary_qubits
        # enable chaining
        return self

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return len(self.auxiliary_qubits) + len(self.encoding_qubits)

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        return self.auxiliary_qubits + self.encoding_qubits

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        assert len(self.encoding_qubits) != 0
        flist = []
        for aq in self.auxiliary_qubits:
            if aq.field not in flist:
                flist.append(aq.field)
        for eq in self.encoding_qubits:
            if eq.field not in flist:
                flist.append(eq.field)
        return flist

    def set_theta(self, theta):
        """
        Set the angle theta
        """
        self.theta = theta

    def as_matrix(self):
        """
        Generate the matrix representation of the controlled gate.
        Note: The control state is |0> on the encoding qubit (requires applying X gates)
        Format: |auxiliary> x |encoding>
        TODO: generalize for more than one auxiliary qubit
        """
        cp_matrix = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], dtype=float)
        return (  np.kron(np.identity(2), PauliXGate().as_matrix())
                @ cp_matrix
                @ np.kron(RzGate(2*self.theta).as_matrix(), np.identity(2))
                @ cp_matrix
                @ np.kron(np.identity(2), PauliXGate().as_matrix()))

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        """
        iawire = [_map_particle_to_wire(fields, anc_q) for anc_q in self.auxiliary_qubits]
        iewire = [_map_particle_to_wire(fields, enc_q) for enc_q in self.encoding_qubits]
        iwire = iewire + iawire
        """
        iwire = [_map_particle_to_wire(fields, p) for p in self.particles()]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Copy of the gate
        """
        return ProjectorControlledPhaseShift(self.theta, self.encoding_qubits, self.auxiliary_qubits)

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return (type(other) == type(self)
                and other.encoding_qubits == self.encoding_qubits
                and other.auxiliary_qubits == self.auxiliary_qubits
                and other.theta == self.theta)


class GeneralGate(Gate):
    """
    General (user-defined) quantum gate, specified by a unitary matrix.
    """
    def __init__(self, mat, nwires: int):
        mat = np.array(mat, copy=False)
        if mat.shape != (2**nwires, 2**nwires):
            raise ValueError(f"`mat` must be a {2**nwires} x {2**nwires} matrix")
        if not np.allclose(mat @ mat.conj().T, np.identity(mat.shape[0])):
            raise ValueError("`mat` must be unitary")
        self.mat = mat
        self.nwires = nwires
        self.prtcl = []

    def is_hermitian(self):
        """
        Whether the gate is Hermitian.
        """
        return np.allclose(self.mat, self.mat.conj().T)

    def as_matrix(self):
        """
        Return the matrix representation of the gate.
        """
        return self.mat

    @property
    def num_wires(self):
        """
        The number of "wires" (or quantum particles) this gate acts on.
        """
        return self.nwires

    def particles(self):
        """
        Return the list of quantum particles the gate acts on.
        """
        return self.prtcl

    def fields(self):
        """
        Return the list of fields hosting the quantum particles which the gate acts on.
        """
        flist = []
        for p in self.prtcl:
            if p.field not in flist:
                flist.append(p.field)
        return flist

    def inverse(self):
        """
        Return the inverse operator.
        """
        return GeneralGate(self.mat.conj().T, self.nwires)

    def on(self, *args):
        """
        Act on the specified particle(s).
        """
        if len(args) == 1 and isinstance(args[0], Sequence):
            prtcl = list(args[0])
        else:
            prtcl = list(args)
        if len(prtcl) != self.nwires:
            raise ValueError(f"require {self.nwires} particles, but received {len(prtcl)}")
        self.prtcl = prtcl
        # enable chaining
        return self

    def _circuit_matrix(self, fields: Sequence[Field]):
        """
        Generate the sparse matrix representation of the gate
        as element of a quantum circuit.
        """
        for f in fields:
            if f.local_dim != 2:
                raise NotImplementedError("quantum wire indexing assumes local dimension 2")
        if not self.prtcl:
            raise RuntimeError("unspecified target particle(s)")
        iwire = [_map_particle_to_wire(fields, p) for p in self.prtcl]
        if any([iw < 0 for iw in iwire]):
            raise RuntimeError("particle not found among fields")
        nwires = sum([f.lattice.nsites for f in fields])
        return _distribute_to_wires(nwires, iwire, csr_matrix(self.as_matrix()))

    def __copy__(self):
        """
        Create a copy of the gate.
        """
        gate = GeneralGate(self.mat, self.nwires)
        gate.on(self.prtcl)
        return gate

    def __eq__(self, other):
        """
        Check if gates are equivalent.
        """
        return (type(other) == type(self)
                and np.allclose(other.mat, self.mat)
                and other.nwires == self.nwires
                and other.prtcl == self.prtcl)


def _map_particle_to_wire(fields: Sequence[Field], p: Particle):
    """
    Map a particle to a quantum wire.
    """
    i = 0
    for f in fields:
        if p.field == f:
            i += p.index
            return i
        else:
            i += f.lattice.nsites
    # not found
    return -1


def _distribute_to_wires(nwires: int, iwire, gmat: csr_matrix):
    """
    Sparse matrix representation of a quantum gate
    acting on quantum wires in `iwire`.

    Currently assumes that each wire has local dimension 2.
    """
    # complementary wires
    iwcompl = list(set(range(nwires)).difference(iwire))
    assert len(iwire) + len(iwcompl) == nwires

    m = len(iwire)
    assert m <= nwires
    assert gmat.shape == (2**m, 2**m)

    values = np.zeros(2**(nwires - m) * gmat.nnz, dtype=gmat.dtype)
    rowind = np.zeros_like(values, dtype=int)
    colind = np.zeros_like(values, dtype=int)

    # reverse ordering, due to convention that wire 0 corresponds to slowest varying index
    iwire   = [(nwires - 1 - iwire[m - 1 - b]) for b in range(m)]
    iwcompl = [(nwires - 1 - iwcompl[nwires - m - 1 - b]) for b in range(nwires - m)]

    for j in range(2**m):
        r = 0
        for b in range(m):
            if j & (1 << b):
                r += (1 << iwire[b])
        for i in range(gmat.indptr[j], gmat.indptr[j + 1]):
            c = 0
            for b in range(m):
                if gmat.indices[i] & (1 << b):
                    c += (1 << iwire[b])
            rowind[i] = r
            colind[i] = c
    values[:gmat.nnz] = gmat.data

    # copy values (corresponds to Kronecker product with identity)
    for k in range(1, 2**(nwires - m)):
        koffset = 0
        for b in range(nwires - m):
            if k & (1 << b):
                koffset += (1 << iwcompl[b])
        rowind[gmat.nnz*k:gmat.nnz*(k+1)] = rowind[:gmat.nnz] + koffset
        colind[gmat.nnz*k:gmat.nnz*(k+1)] = colind[:gmat.nnz] + koffset
        values[gmat.nnz*k:gmat.nnz*(k+1)] = gmat.data

    return csr_matrix((values, (rowind, colind)), shape=(2**nwires, 2**nwires))
