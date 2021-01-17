# How to generate big prime numbers -- Miller-Rabin

A prime number is a positive integer, greater than 1, that has only two positive
divisors: 1 and itself.

Here are the first prime numbers:
2, 3, 5,7, 11, 13, 17, 19, 23, 29, 31, 37, 41, ...
There is an infinity of prime numbers! But as we are going to see, big prime
numbers are hard to find.

But big prime numbers are useful for applications, like cryptography.

The security of several public-key cryptography algorithms is based on the fact
that big prime numbers are hard to find. A well known example is the RSA
algorithm. During the key generation step, you have to choose 2 primes, __p__
and __q__, and calculate their product, __n = p*q__. The security of RSA is
based on the fact that it's very hard to find __p__ and __q__ given __n__.

Of course, the bigger __p__ and __q__ are, the harder it is to find them given
__n__.

So let's see how we can generate big prime numbers.

## The problem of prime numbers

There is no pattern to find prime numbers, so how can we find primes?

### Prime numbers density

pi(n) is the number of prime numbers <= __n__. For example, pi(10) = 4, because
2, 3, 5, and 7 are the only primes <= __10__.

The _prime number theorem_ states that __n / ln(n)__ is a good approximation of
__pi(n)__ because when __n__ tends to infinity, __pi(n) / (n / ln(n)) = 1__.

It means the probability that a randomly chosen number is prime is __1 /
ln(n)__, because there are __n__ positive integers <= __n__ and approximately
__n / ln(n)__ primes, and __(n / ln(n)) / n = (1 / ln(n))__.

For example, the probability to find a prime number of 1024 bits is __1 / (ln
(2^1024)) = (1 / 710)__.

As we know that primes are odd (except 2), we can increase this probability by
2, so on average, to generate a 1024 bits prime number, we have to test __355__
numbers randomly generated.

### How to test that a number is prime

There is a simple way to be sure that an integer (I will call it __n__) is
prime. We need to divide __n__ by each integer __d__ such that __1 < d < n__. If
one value of __d__ divides __n__, then __n__ is _composite_.A

Else, the only divisors of __n__ are __1__ and __n__. So by definition, __n__ is
_prime_.A

There are some easy improvements by the way:

- We only have to test to __sqrt(n)__, because if __n = p*q__ (composite), __p
  <= sqrt(n)__ or __q <= sqrt(n)__. In the case where __p = q__, we have __n =
  p*p__ with __p = sqrt(n)__. In the other case, where __p != q__, either __p >
  sqrt(n)__ and __q < sqrt(n)__, or __q > sqrt(n)__ and __p < sqrt(n)__.
- We only have ot test with __2__ and all the __odd__ numbers to __sqrt(n)__
  because __2__ divides all even numbers, so if __2__ doesn't divide __n__, the
  other even numbers will not.

```python
def is_prime(n):
    # test if n is even
    if n % 2 == 0:
        return False

    # test each odd number from 3 to sqrt(n)
    for i in range(3, sqrt(n), 2):
        if n % d == 0:
            return False

    # n is necessarily prime
    return True
```

Runtime complexity: __O(sqrt(n))__

Not bad, but in practice, when __n__ is very big (an integer on 1024 bits, or
more), it takes a while...

So how can we generate big prime numbers quickly for cryptography purposes?

