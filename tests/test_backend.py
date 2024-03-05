import os
import uuid
import numpy as np
import unittest
from unittest.mock import Mock
import json
import requests
import qib


class TestBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock Data
        with open(f"{os.path.dirname(__file__)}/data/wmi_qsim.json") as f:
            mock_file: dict = json.load(f)
            cls.mock_experiment_request = mock_file["submitExperimentRequest"]
            cls.mock_experiment_response_json = mock_file["submitExperimentResponse"]
            cls.mock_results_request = mock_file["queryResultsRequest"]
            cls.mock_results_response_json = mock_file["queryResultsResponse"]
        cls.mock_experiment_response = requests.Response()
        cls.mock_results_response = requests.Response()
        cls.mock_experiment_response.json = Mock(return_value = cls.mock_experiment_response_json)
        cls.mock_results_response.json = Mock(return_value = cls.mock_results_response_json)
        uuid.uuid4 = Mock(return_value = "5197daa3-624c-42a6-8bb0-3f5ed2be2b3b")
        qib.util.networking.http_put = Mock(return_value = cls.mock_experiment_response)
        qib.util.networking.http_post = Mock(return_value = cls.mock_results_response)
        
    def test_tensor_network(self):
        """
        Test tensor network processor functionality.
        """
        field = qib.field.Field(
            qib.field.ParticleType.QUBIT, qib.lattice.IntegerLattice((2,)))
        qa = qib.field.Qubit(field, 0)
        qb = qib.field.Qubit(field, 1)
        # Hadamard gate
        hadamard = qib.HadamardGate(qa)
        # CNOT gate
        cnot = qib.ControlledGate(qib.PauliXGate(qb), 1).set_control(qa)
        # construct a simple quantum circuit
        circuit = qib.Circuit()
        circuit.append_gate(hadamard)
        circuit.append_gate(cnot)
        self.assertTrue(circuit.fields() == [field])
        h_cnot = cnot.as_matrix() @ np.kron(hadamard.as_matrix(), np.identity(2))
        self.assertTrue(np.array_equal(
            circuit.as_matrix([field]).toarray(), h_cnot))
        processor = qib.backend.TensorNetworkProcessor()
        processor.submit(circuit, {
            "filename": f"{os.path.dirname(__file__)}/data/bell_circuit_tensornet.hdf5"
            })

    def test_wmi_qsim_valid(self):
        """
        Test WMI Qiskit Simulator processor functionality.
        (Scenario: Valid Experiment Submission)
        """
        # Qubits
        field = qib.field.Field(
            qib.field.ParticleType.QUBIT, qib.lattice.IntegerLattice((2,)))
        qa = qib.field.Qubit(field, 0)
        qb = qib.field.Qubit(field, 1)
        qc = qib.field.Qubit(field, 2)

        # Circuit
        circuit = qib.Circuit([
            qib.HadamardGate(qa),
            qib.HadamardGate(qb),
            qib.ControlledGate(qib.PauliZGate(qb), 1).set_control(qa),
            qib.MeasureInstruction([qa, qb, qc])
        ])

        # Processor & Experiment Options
        processor = qib.backend.wmi.WMIQSimProcessor(access_token = "AccessToken")
        options = qib.backend.wmi.WMIOptions(
            shots = 1024,
            init_qubits = True,
            do_emulation = False)
        
        # Submit Experiment
        experiment = processor.submit_experiment(
            name = "UnitTest",
            circ = circuit,
            options = options)            
        self.assertEqual(experiment.as_qasm(), self.mock_experiment_request["qobj"])
        self.assertEqual(experiment.status, qib.backend.ExperimentStatus.QUEUED)
        self.assertEqual(experiment.job_id, "1454ef78dae611ee923e842b2badd5e4")
        self.assertEqual(experiment._execution_datetime, "2024-03-05T11:47:01.350846")
        
        # Query Results
        results = experiment.results()
        self.assertEqual(experiment.status, qib.backend.ExperimentStatus.DONE)
        self.assertEqual(results.get_counts(), self.mock_results_response_json["counts"][0])
        self.assertEqual(results.runtime, self.mock_results_response_json["runtime"])

    def test_wmi_qsim_invalid(self):
        """
        Test WMI Qiskit Simulator processor functionality.
        (Scenario: Invalid Experiment Submission)
        """
        # Set-Up
        field = qib.field.Field(
            qib.field.ParticleType.QUBIT, qib.lattice.IntegerLattice((2,)))
        qa = qib.field.Qubit(field, 0)
        qb = qib.field.Qubit(field, 1)
        qc = qib.field.Qubit(field, 2)
        qd = qib.field.Qubit(field, 3)
        processor = qib.backend.wmi.WMIQSimProcessor(access_token = "AccessToken")
        
        # Invalid Experiment: Shots exceeded
        with self.assertRaises(ValueError) as err:
            processor.submit_experiment(
                name = "UnitTest",
                circ = qib.Circuit([
                    qib.PauliXGate(qa),
                    qib.MeasureInstruction([qa])
                    ]),
                options = qib.backend.wmi.WMIOptions(shots = 2**20))

        # Invalid Experiment: Gate not supported
        with self.assertRaises(ValueError) as err:
            processor.submit_experiment(
                name = "UnitTest",
                circ = qib.Circuit([
                    qib.RotationGate([75, 75, 75], qa),
                    qib.MeasureInstruction([qa])
                    ]))
            
        # Invalid Experiment: Gate qubits not configured
        with self.assertRaises(ValueError) as err:
            processor.submit_experiment(
                name = "UnitTest",
                circ = qib.Circuit([
                    qib.PauliXGate(qd),
                    qib.MeasureInstruction([qa])
                    ]))
        
        # Invalid Experiment: Gate parameters not configured
        qib.RzGate.as_qasm = Mock(return_value = {
            "name": "rz",
            "qubits": [0],
            "params": [75, 85, 95]
        })
        with self.assertRaises(ValueError) as err:
            processor.submit_experiment(
                name = "UnitTest",
                circ = qib.Circuit([
                    qib.RzGate(75, qa),
                    qib.MeasureInstruction([qa])
                    ]))
        
        # Invalid Experiment: Number of qubits exceeded
        with self.assertRaises(ValueError) as err:
            processor.submit_experiment(
                name = "UnitTest",
                circ = qib.Circuit([
                    qib.PauliXGate(qa),
                    qib.MeasureInstruction([qa, qb, qc, qd])
                    ]))

if __name__ == "__main__":
    unittest.main()
