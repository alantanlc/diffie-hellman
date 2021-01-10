import random

class DiffieHellman(object):
    """ Generates a secret key between two parties using private key
    without having to exposing the private key to each other
    as well as the public.
    """

    def __init__(self, g, n):
        # g is usually a small prime number
        self.g = random.getrandbits(8)

        # n needs to be big for the security to work.
        # n is often 2,000 bits long or 4,000 bits more common now.
        # But n can't be too big because you won't gain much in security
        # but you lose in efficiency
        self.n = random.getrandbits(4000)

    def get_a(self):
        # a is somewhere between 1 and n but it's random and n is so vast.
        return rand(1, n)

    def get_ag(self):
        # ag
        return (g**self.get_a) % n

    def get_secret_key(self, b):
        # abg
        return (self.get_ag**b) % n
