import random
from Crypto.Util import number

class DiffieHellman(object):
    """ Generates a secret key between two parties using private keys
    without revealing the private keys to each other as well as the
    public.
    """

    def __init__(self, g_bits=8, n_bits=4000):
        # g is usually a small prime number
        self.g = number.getPrime(g_bits)

        # n needs to be big for the security to work.
        # n is often 2,000 bits long or 4,000 bits more common now.
        # But n can't be too big because you won't gain much in security
        # but you lose in efficiency
        self.n = number.getPrime(n_bits)

    def get_a(self):
        # a is somewhere between 1 and n
        return random.randint(1, self.n)

    def get_ga(self, a):
        return (self.g**a) % self.n

    def get_secret_key(self, ga, b):
        return (ga**b) % self.n

if __name__ == '__main__':
    # Initialize Diffie Hellman objects
    dh = DiffieHellman(4, 8)

    # Get rand a and b
    rand_a = dh.get_a()
    rand_b = dh.get_a()

    # Get exchange keys
    ga = dh.get_ga(rand_a)
    gb = dh.get_ga(rand_b)

    # Compute secret keys, should expect the same values
    secret_key_a = dh.get_secret_key(gb, rand_a)
    secret_key_b = dh.get_secret_key(ga, rand_b)

    # Print values
    print('DIFFIE HELLMAN VALUES:')
    print(f'  a: a={rand_a}, ga={ga}, secret_key={secret_key_a}')
    print(f'  b: b={rand_b}, gb={gb}, secret_key={secret_key_b}')

