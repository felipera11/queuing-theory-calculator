import math

class MMS:
    def __init__(self, lambda_, mi, s):
        if lambda_ <= 0:
            raise ValueError("λ deve ser maior que zero")
        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")
        if s < 2:
            raise ValueError("s deve ser >= 2 (Para s=1, use o modelo MM1)")

        self._lambda_ = float(lambda_)
        self._mi = float(mi)
        self._s = int(s)

        if self.rho >= 1:
            raise ValueError(f"Sistema instável: a taxa de ocupação (ρ = {self.rho:.2f}) deve ser menor que 1.")

    @property
    def rho(self):
        return self._lambda_ / (self._s * self._mi)

    @property
    def a(self):
        return self._lambda_ / self._mi

    @property
    def p0(self):
        soma = 0
        for n in range(self._s):
            soma += (self.a ** n) / math.factorial(n)

        termo_final = ((self.a ** self._s) / math.factorial(self._s)) * (
            1 / (1 - self.rho)
        )
        return 1 / (soma + termo_final)

    def prob_n(self, n):
        if n < 0:
            raise ValueError("n deve ser >= 0")
        if n <= self._s:
            return ((self.a ** n) / math.factorial(n)) * self.p0
        else:
            return ((self.a ** n) / (
                math.factorial(self._s) * (self._s ** (n - self._s))
            )) * self.p0

    def avg_clients_queue(self):
        return (
            self.p0
            * (self.a ** self._s)
            * self.rho
            / (math.factorial(self._s) * ((1 - self.rho) ** 2))
        )

    def avg_time_queue(self):
        return self.avg_clients_queue() / self._lambda_

    def avg_clients_system(self):
        return self.avg_clients_queue() + self.a

    def avg_time_system(self):
        return self.avg_time_queue() + (1 / self._mi)

    def prob_wait_queue_greater_than(self, t):
        """P(Wq > t)"""
        if t < 0:
            raise ValueError("t deve ser >= 0")

        # Erlang C
        c = (
            ((self.a ** self._s) / math.factorial(self._s))
            * (1 / (1 - self.rho))
            * self.p0
        )

        return c * math.exp(-(self._s * self._mi - self._lambda_) * t)

    def prob_wait_system_greater_than(self, t):
        """P(W > t)"""
        if t < 0:
            raise ValueError("t deve ser >= 0")

        # Erlang C
        c = (
            ((self.a ** self._s) / math.factorial(self._s))
            * (1 / (1 - self.rho))
            * self.p0
        )

        alpha = self._s * self._mi - self._lambda_

        # Caso especial para evitar divisão por zero
        if abs(alpha - self._mi) < 1e-9:
            return math.exp(-self._mi * t) * (
                1 + c * self._mi * t
            )

        termo1 = (1 - c) * math.exp(-self._mi * t)

        termo2 = c * (
            (
                alpha * math.exp(-self._mi * t)
                - self._mi * math.exp(-alpha * t)
            )
            / (alpha - self._mi)
        )

        return termo1 + termo2