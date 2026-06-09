class MG1:

    def __init__(self, lambda_, mi, sigma2):

        if mi <= 0:
            raise ValueError("μ deve ser maior que zero")

        if sigma2 < 0:
            raise ValueError("σ² deve ser >= 0")

        rho = lambda_ / mi

        if rho >= 1:
            raise ValueError("Sistema instável (ρ >= 1)")

        self.lambda_ = lambda_
        self.mi = mi
        self.sigma2 = sigma2

    @property
    def rho(self):
        return self.lambda_ / self.mi

    @property
    def p0(self):
        return 1 - self.rho

    def avg_clients_queue(self):
        return (
            (self.lambda_ ** 2) * self.sigma2 +
            self.rho ** 2
        ) / (2 * (1 - self.rho))

    def avg_time_queue(self):
        return self.avg_clients_queue() / self.lambda_

    def avg_clients_system(self):
        return self.avg_clients_queue() + self.rho

    def avg_time_system(self):
        return self.avg_time_queue() + (1 / self.mi)