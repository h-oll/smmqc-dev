import unittest
import random
import math
from cqc.pythonLib import CQCConnection
from hypothesis import given, example, settings
import hypothesis.strategies as st

from qia_atomic.qpzlib.qpzlib import qpzlib
from qia_atomic.qpzlib.mappings.simulaqron import mapping

def luka_prep(client_preps):

    print('.', end='', flush=True) 
        
    # State prepapration

    client_num = len(client_preps)
    client_bits = [client_preps[i][0] for i in range(client_num)]
    client_bases = [client_preps[i][1] for i in range(client_num)]

    client_qubits = [_.prep.pauli(client_bits[i], client_bases[i]) for i in range(client_num)]
    server_qubit = _.prep.pauli(0,1)

    register = client_qubits + [server_qubit]

    # Entangling operation 
    for i in range(client_num + 1):
        for j in range(i):
            _.gate.CZ(register[i], register[j])                   

    # Parameter output
    def minus_state_selector (bit, basis):
        if (bit == 1 and basis == 1): return 1
        else: return 0

    def one_state_selector (bit, basis):
        if (bit == 1 and basis == 2): return 1
        else: return 0

    b = [_.meas.pauli(register[i], 1) for i in range(client_num)]
    c = [minus_state_selector(client_bits[i], client_bases[i]) for i in range(client_num)]
    d = [one_state_selector(client_bits[i], client_bases[i]) for i in range(client_num)]
    sum_d = sum(d)
    
    #return (register[client_num], b, c, d, sum_d)

    # Comparision with direct evolution 

    n = sum(1 for basis in client_bases if basis == 1)
    e = [b[i] + c[i] + sum_d for i in range(client_num)]
    z = sum(e) + math.floor(n / 2)

    if (n % 2 == 1): _.H(server_qubit)
    if (z % 2 == 1): _.Z(server_qubit)

    assert ( _.meas.pauli(server_qubit,1) == 0)

if __name__ == "__main__": 
    
    with CQCConnection("Alice") as Alice: 
        _ = qpzlib(mapping, Alice)

        @settings(deadline=None)
        @given(
            st.lists(
                st.tuples(
                    st.integers(min_value=0, max_value=1),
                    st.integers(min_value=1, max_value=2)),
                min_size=1,
                max_size=10))
        def test_luka_prep(client_preps): luka_prep(client_preps)

        test_luka_prep()

        

