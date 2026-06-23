import math

class MM1K:
    def __init__(self, lambda_, mi, k):
        if lambda_ <= 0:
            raise ValueError("λ deve ser maior que zero")
        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")
        if k < 1:
            raise ValueError("K deve ser >= 1")

        self._lambda_ = float(lambda_)
        self._mi = float(mi)
        self._k = int(k)

    @property
    def rho(self):
        return self._lambda_ / self._mi

    @property
    def rhok1(self):
        return self.rho**(self._k + 1)

    def prob_idle(self):

        if self.rho == 1:
            return 1 / (self._k + 1)

        return (1 - self.rho) / (1 - self.rhok1)

    def prob_n(self, n):
        if n < 0 or n > self._k:
            return 0

        p0 = self.prob_idle()
        return p0 * (self.rho**n)

    def prob_less_equal_n(self, n):
        if n < 0:
            return 0

        n = min(n, self._k)

        return sum(
            self.prob_n(i)
            for i in range(n + 1)
        )

    def prob_greater_equal_n(self, n):
        if n <= 0:
            return 1

        if n > self._k:
            return 0

        return sum(
            self.prob_n(i)
            for i in range(n, self._k + 1)
        )

    def avg_clients_system(self):
        return (
            (self.rho / (1 - self.rho))
            - (((self._k + 1) * self.rhok1) / (1 - self.rhok1))
        )
    
    def avg_clients_queue(self):
        l = self.avg_clients_system()
        return l - (1 - self.prob_idle())

    def effective_lambda(self):
        return self._lambda_ * (1 - self.prob_n(self._k))

    def avg_time_queue(self):
        lq = self.avg_clients_queue()
        return lq / self.effective_lambda()

    def avg_time_system(self):
        l = self.avg_clients_system()
        return l / self.effective_lambda()

    def prob_poisson(self, rate, x):
        if x < 0:
             raise ValueError("x deve ser >= 0")
        return math.exp(-rate) * (rate ** x) / math.factorial(x)