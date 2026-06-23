import math


class MMsK:
    def __init__(self, lambda_, mi, k, s):
        if lambda_ <= 0:
            raise ValueError("λ deve ser maior que zero")
        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")
        if k < 1:
            raise ValueError("K deve ser >= 1")
        if k < s:
            raise ValueError("K deve ser >= s")

        self._lambda_ = float(lambda_)
        self._mi = float(mi)
        self._k = int(k)
        self._s = int(s)

    @property
    def lambda_div_mi(self):
        return self._lambda_ / self._mi

    @property
    def rho(self):
        return self._lambda_ / (self._s * self._mi)

    def prob_idle(self):
        # P0 = 1 / [Σ(n=0..s-1) a^n/n!  +  a^s/s! × Σ(n=s..K) ρ^(n-s)]
        sum1 = sum(
            (self.lambda_div_mi ** i) / math.factorial(i)
            for i in range(self._s)
        )
        sum2 = (
            (self.lambda_div_mi ** self._s) / math.factorial(self._s)
        ) * sum(
            self.rho ** (j - self._s)
            for j in range(self._s, self._k + 1)
        )
        return 1 / (sum1 + sum2)

    def prob_n(self, n):
        if n < 0 or n > self._k:
            return 0
        if n < self._s:
            return ((self.lambda_div_mi ** n) / math.factorial(n)) * self.prob_idle()
        else:
            return ((self.lambda_div_mi ** n) / (
                math.factorial(self._s) * (self._s ** (n - self._s))
            )) * self.prob_idle()

    def avg_clients_queue(self):
        x = 1 - self.rho
        power = self.rho ** (self._k - self._s)
        div = (
            self.prob_idle()
            * (self.lambda_div_mi ** self._s)
            * self.rho
        ) / (math.factorial(self._s) * (x ** 2))
        brackets = 1 - power - (self._k - self._s) * power * x
        return div * brackets

    def avg_clients_system(self):
        sum1 = sum(i * self.prob_n(i) for i in range(self._s))
        sum2 = sum(self.prob_n(i) for i in range(self._s))
        lq = self.avg_clients_queue()
        return sum1 + lq + self._s * (1 - sum2)

    def effective_lambda(self):
        return self._lambda_ * (1 - self.prob_n(self._k))

    def avg_time_queue(self):
        return self.avg_clients_queue() / self.effective_lambda()

    def avg_time_system(self):
        return self.avg_clients_system() / self.effective_lambda()
