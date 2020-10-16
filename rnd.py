from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib
import numpy as np

class Generator(object):
    
    def __init__(self, key):
        self.seed(key)

    def seed(self, seed):
        if isinstance(seed, int):
            seed = b"%d" % (seed,)
        elif isinstance(seed, str):
            seed = seed.encode("utf-8")
        self.Key = seed
        h = hashlib.sha256()
        h.update(self.Key)
        self.HashedKey = h.digest()
        self.X = self.HashedKey[:16]
        self.AES = AES.new(self.HashedKey, AES.MODE_ECB, b'0'*16)

    def next(self):
        y = self.AES.encrypt(self.X)
        self.X = y
        return int.from_bytes(y, byteorder='little')
        
    def generate(self):
        while True:
            yield self.next()
            
    def __iter__(self):
        return self
        
    def reset(self):
        self.seed(self.Key)
        
def sample(g, pop, n):
    # assume n is much less than len(pop)
    N = len(pop)
    used = np.zeros(N, dtype=np.bool)
    out = []
    for _ in range(n):
        i = g.next() % N
        while used[i]:
            i = g.next() % N
        used[i] = 1
        out.append(pop[i])
    return out
            
if __name__ == "__main__":
    g = GeneratorECB("abcd")
    for _ in range(10):
        print(g.next())
        
    pop = list(range(100))
    print(sample(g, pop, 10))
    print(sample(g, pop, 10))
    
    
    