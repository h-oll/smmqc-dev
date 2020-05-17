import random
from cqc.pythonLib import CQCConnection

from qia_atomic.qpzlib.qpzlib import qpzlib
from qia_atomic.qpzlib.mappings.simulaqron import mapping

with CQCConnection("Alice") as Alice: 
    _ = qpzlib(mapping, Alice)

    client_num = 10 
    client_bits = [random.randrange(2) for i in range(client_num)]
    client_bases = [1 + random.randrange(2) for i in range(client_num)]

    client_qubits = [_.prep.pauli(client_bits[i], client_bases[i]) for i in range(client_num)]
    server_qubit = _.prep.pauli(0,1)

    register = client_qubits + [server_qubit]

    # complete graph version
    for i in range(client_num + 1):
        for j in range(i):
            _.gate.CZ(register[i], register[j])                   

    # only server version
    for i in range(client_num):
        _.gate.CZ(register[i], register[client_num])
    
    print('Hello', client_bases, client_bits)

    
