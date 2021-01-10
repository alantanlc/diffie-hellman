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

        # a is somewhere between 1 and n
        self.a = random.randint(1, self.n)

    def get_ag(self):
        return (self.g**self.a) % self.n

    def get_secret_key(self, b):
        return (self.get_ag()**b) % self.n

if __name__ == '__main__':
    # Initialize Diffie Hellman objects
    dh_a = DiffieHellman()
    dh_b = DiffieHellman()

    # Get exchange keys
    ag = dh_a.get_ag()
    bg = dh_b.get_bg()

    # Compute secret keys, should expect the same values
    secret_key_a = dh_a.get_secret_key(bg)
    secret_key_b = dh_b.get_secret_key(ag)

    print('Secret key from a:')
    print(secret_key_a)
    print('\n')

    print('Secret key from b:')
    print(secret_key_b)

