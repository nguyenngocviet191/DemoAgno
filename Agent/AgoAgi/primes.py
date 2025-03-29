def is_prime(n):
    if n <= 1:
        return false
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return false
    return true

def prime_numbers(limit):
    primes = [num for num in range(2, limit+1) if is_prime(num)]
    output = ''.join(map(str, primes))
    filename = 'output.txt'
    with open(filename, 'w') as file:
        file.write(output)

prime_numbers(100)