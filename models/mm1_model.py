import math

class MM1:

    def __init__(self, lambda_, mi):
        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")
        if lambda_ >= mi:
            raise ValueError("Sistema instável (λ >= μ)")
            
        self._lambda_ = lambda_
        self._mi = mi
        
    @property
    def rho(self):
        return self._lambda_ / self._mi

    @property
    def diff(self):
        return self._mi - self._lambda_

    def prob_n(self, n):
        if n < 0:
            raise ValueError("n deve ser >= 0")
        return (1 - self.rho) * (self.rho ** n)

    def prob_less_equal_n(self, n):
        if n < 0:
            raise ValueError("n deve ser >= 0")
        return 1 - (self.rho ** (n + 1))

    def prob_greater_equal_n(self, n):
        if n < 0:
            raise ValueError("n deve ser >= 0")
        return self.rho ** n

    def prob_greater_r(self, r):
        if r < 0:
            raise ValueError("r deve ser >= 0")
        return self.rho ** (r + 1)

    def prob_idle(self):
        return 1 - self.rho

    def prob_wait_system_greater_than(self, t):
        if t < 0:
            raise ValueError("t deve ser >= 0")
        return math.exp(-self.diff * t)
    
    def prob_wait_queue_greater_than(self, t):
        if t < 0:
            raise ValueError("t deve ser >= 0")
        return self.rho * math.exp(-self.diff * t)

    def avg_clients_system(self):
        return self._lambda_ / self.diff
    
    def avg_clients_queue(self):
        return (self._lambda_ ** 2) / (self._mi * self.diff)

    def avg_time_system(self):
        return 1 / self.diff

    def avg_time_queue(self):
        return self._lambda_ / (self._mi * self.diff)

    def prob_poisson(self, rate, x):
        if x < 0:
            raise ValueError("x deve ser >= 0")
        return math.exp(-rate) * (rate ** x) / math.factorial(x)