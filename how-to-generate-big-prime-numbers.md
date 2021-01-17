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

## Probabilistic tests

Probabilistic algorithms are much faster than the one above, but we can't be
100% sure that __n__ is prime.

In fact, a probabilitics test is absolutely right when it says that __n__ is
composite. But when it says that __n__ is prime, there is a (very low) chance
that __n__ is actually not prime.

Here, we will see a famous probabilistic algorithm, called _Miller-Rabin_. But
before, let's go through some maths that will help us understand how this
algorithm works.

### Fermat primality test

Given __n__, a prime number, and __a__, an integer such that __1 <= a <= n-1__,
the _Fermat's little theorem_ says that __a^(n-1) = 1 (mod n)__.

So for an integer __n__, we just have to find a value of __a__ for which
__a^(n-1) != 1 (mod n)__ to prove that __n__ is composite. Such value for __a__
is called a _Fermat witness_.

On the other hand, if we find a value of __a__ that verify the Fermat's theorem,
we just show that __n__ satisfies Fermat's theorem for the base __a__, and
appears to be prime. In this case, we say that __n__ is _pseudo-prime of base
a_.

But if in a later test, we finally find that this __n__ is composite, then, the
previous values of __a__ for whose __a^(n-1) != 1 (mod n)__ are called _Fermat
liars_, because they lied about the fact that __n__ is actually composite.

### Carmichael numbers

There are some composite numbers that satisfies the _Fermat's little theorem_
for all possible values of __a__. As you guessed, these numbers are called...
_Carmichael numbers_ (so much suspense...).

The first 3 are __561__, __1105__, and __1729__.

There are only __255__ Carmichael numbers __< 10^8__, and __20138200 < 10^21__.
So if you generate a random number __n < 10^8__, the probability that __n__ is a
Carmichael number is __2.55*10^(-6)__. As you can see, it's very low! But the
Fermat primality test is not perfect, because of these numbers.A

Miller-Rabin is more advanced that Fermat's primality test, and Carmichael
numbers are not a problem.

### Trivial and nontrivial square root

We define __p > 2__, a prime.A

We know that __1__ and __-1__ always give __1__ when squared: __1^2 = (-1)^2 = 1
(mod p)__. They are called _trivial square root_.A

But sometimes, there are _nontrivial square root_ of __1__ modulo __p__. We
define __a__, an integer, to be a _nontrivial square root_ of __1 (mod p)__ if
__a^2 = 1 (mod p)__.

> _For example:_
> 3^2 = 9 = 1 (mod 8)
> so __3__ is _non trivial square root_ of __1__ modulo __8__.

If __1__ has a square root other than __1__ and __-1__ modulo __n__ (a
nontrivial square root), then __n__ must be composite.A

### Miller-Rabin

The goal of Miller-Rabin is to find a nontrivial square root of __1__ modulo
__n__.

Take back the _Fermat's little theorem_: __a^(n-1) = 1 (mod n)__.A

For Miller-Rabin, we need to find __r__ and __s__ such that __(n-1) = r*(2^s)__,
with __r__ odd.A

Then, we pick __a__, an integer in the range __[1, n-1]__.A

- If __a^r != 1 (mod n)__ and __a^((2^j)r) != -1 (mod n)__ for all __j__ such
  that __0 <= j <= s-1__, then __n__ is not prime and __a__ is called a _strong
  witness to compositeness for n_.
- On the other hand, if __a^r = 1 (mod n)__ or __a^((2^j)r) = -1 (mod n)__ for
  some __j__ such as __0 <= j <= s-1__, then __n__ is said to be a _strong
  pseudo-prime to the base a_, and __a__ is called a _strong liar to primality
  for n_.

## So, how to generate big prime numbers?

Now, we know all the theory we need to generate prime numbers. So... let's do
it! :)

### The algorithm

- __Generate a prime candidate__. Say we want a 1024 bits prime number. Start by
  generating 1024 bits randomly. Set the MSB to 1, to make sure that the number
  hold 1024 bits. Set the LSB to 1 to make sure that it is an odd number.
- __Test if the generated number if prime__ with Miller-Rabin. Run the test many
  times to make it more efficient.
- If the number is not prime, __restart__ from the beginning.


