import math

class MMsN:
    def __init__(self, lambda_, mi, N, s):
        if lambda_ <= 0:
            raise ValueError("λ deve ser maior que zero")
        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")

        self._lambda_ = float(lambda_)
        self._mi = float(mi)
        self._N = int(N)
        self._s = int(s)
        

    @property
    def rho(self):
        return (self._N * self._lambda_) / (self._s * self._mi)
    
    @property
    def lambda_div_mi(self):
        return self._lambda_ / self._mi

    def server_utilization(self):
        return self.rho

    def prob_idle(self):
        sum1 = sum((math.factorial(self._N) / (math.factorial(self._N - i) * math.factorial(i))) * (self.lambda_div_mi ** i)
        for i in range(self._s))
        sum2 = sum((math.factorial(self._N) / (math.factorial(self._N - i) * math.factorial(self._s) * (self._s ** (i - self._s)))) * (self.lambda_div_mi ** i)
        for i in range(self._s, self._N + 1))

        return 1 / (sum1 + sum2)

    def prob_n(self, num):
        if num < 0 or num > self._N:
            return 0
        if num < self._s:
            return (math.factorial(self._N) / (math.factorial(self._N - num) * math.factorial(num))) * (self.lambda_div_mi ** num) * self.prob_idle()
        return (math.factorial(self._N) / (math.factorial(self._N - num) * math.factorial(self._s) * (self._s ** (num - self._s)))) * (self.lambda_div_mi ** num) * self.prob_idle()

    def avg_clients_system(self):
        return sum(i * self.prob_n(i) for i in range(1, self._N + 1))
    
    def avg_clients_queue(self):
        return self.avg_clients_system() - (self.lambda_div_mi * (self._N - self.avg_clients_system()))

    def effective_lambda(self):
        return self._lambda_ * (self._N - self.avg_clients_system())

    def avg_time_queue(self):
        lq = self.avg_clients_queue()
        return lq / self.effective_lambda()

    def avg_time_system(self):
        l = self.avg_clients_system()
        return l / self.effective_lambda()