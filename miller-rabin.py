from random import randrange, getrandbits

class MillerRabin:
    """ The Miller Rabin algorithm.

    The algorithm.
    1) Generate a prime candidate.
    2) Test if the generated number is prime.
    3) If the number is not prime, restart from beginning.

    """

    def __init__(self):
        print('Hello world, I am a MillerRabin object instance!')

    def is_prime(self, n, k=128):
        """ Test if a number if prime.

            Args:
                n -- int -- the number to test
                k -- int -- the numebr of tests to do

            return True if n is prime
        """
        # Test if n is not even.
        # But care, 2 is prime !
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False
        # find r and s
        s = 0
        r = n - 1
        while r & 1 == 0:
            s += 1
            r // 2
        # do k tests
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a, r, n) # pow(base, exp, mod)
            if x != 1 and x != n - 1:
                j = 1
                while j < s and x != n - 1:
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True

    def generate_prime_candidate(self, length):
        """ Generate an odd integer randomly

            Args:
                length -- int -- the length of the number to generate, in bits

            return an integer
        """
        # generate random bits
        p = getrandbits(length)
        # apply a mask to set MSB and LSB to 1
        p |= (1 << length - 1) | 1

        return p

    def generate_prime_number(self, length=1024):
        """ Generate a prime

            Args:
                length -- int -- length of the prime to generate, in bits

            return a prime
        """
        p = 4
        # keep generating while the primality test fail
        while not is_prime(p, 128):
            p = generate_prime_candidate(length)
        return p

