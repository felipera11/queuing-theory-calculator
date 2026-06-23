import math


class PriorityQueue:

    def __init__(self, lambdas: list[float], mu: float, s: int, preemptive: bool,
                 mus: list[float] = None, sigma2s: list[float] = None):
        if mu <= 0:
            raise ValueError("μ deve ser maior que zero")
        if s < 1:
            raise ValueError("s deve ser >= 1")
        if any(l < 0 for l in lambdas):
            raise ValueError("Todas as taxas λ devem ser >= 0")
        if len(lambdas) == 0:
            raise ValueError("Informe ao menos uma classe")

        # Per-class service rates (optional, non-preemptive s=1 only)
        if mus is not None:
            if len(mus) != len(lambdas):
                raise ValueError("mus deve ter o mesmo número de elementos que lambdas")
            if any(m <= 0 for m in mus):
                raise ValueError("Todas as taxas μ devem ser > 0")
            if preemptive:
                raise ValueError("Prioridade com interrupção requer μ único para todas as classes")
            if s != 1:
                raise ValueError("μ por classe só é suportado para s=1")
            self.mus = [float(m) for m in mus]
        else:
            self.mus = [float(mu)] * len(lambdas)

        # Per-class variances: default = 1/μ² (exponential)
        if sigma2s is not None:
            if len(sigma2s) != len(lambdas):
                raise ValueError("sigma2s deve ter o mesmo número de elementos que lambdas")
            if any(v < 0 for v in sigma2s):
                raise ValueError("Todas as variâncias σ² devem ser >= 0")
            self.sigma2s = [float(v) for v in sigma2s]
        else:
            self.sigma2s = [1.0 / (m ** 2) for m in self.mus]

        self._use_general = (mus is not None)

        # Check stability
        if self._use_general:
            rho_total = sum(lam / m for lam, m in zip(lambdas, self.mus))
        else:
            rho_total = sum(lambdas) / (s * mu)
        if rho_total >= 1:
            raise ValueError(f"Sistema instável (ρ = {rho_total:.4f} >= 1)")

        self.lambdas = [float(l) for l in lambdas]
        self.mu = float(mu)
        self.s = s
        self.preemptive = preemptive
        self.lambda_total = sum(lambdas)

    @property
    def r(self):
        return self.lambda_total / self.mu

    @property
    def rho_total(self):
        if self._use_general:
            return sum(lam / m for lam, m in zip(self.lambdas, self.mus))
        return self.lambda_total / (self.s * self.mu)

    def _sigma(self, k: int) -> float:
        """Σ(i=1 to k) λᵢ/(sμ) for equal-μ; Σλᵢ/μᵢ for general."""
        if self._use_general:
            return sum(self.lambdas[i] / self.mus[i] for i in range(k))
        return sum(self.lambdas[:k]) / (self.s * self.mu)

    def _base_term(self) -> float:
        s, mu, r, lam = self.s, self.mu, self.r, self.lambda_total
        soma = sum((r ** j) / math.factorial(j) for j in range(s))
        return math.factorial(s) * (s * mu - lam) / (r ** s) * soma + s * mu

    def _numerator_general(self) -> float:
        """Σ λᵢ(σᵢ² + 1/μᵢ²) — numerator of Pollaczek-Khinchine mean-value formula."""
        return sum(self.lambdas[i] * (self.sigma2s[i] + 1.0 / (self.mus[i] ** 2))
                   for i in range(len(self.lambdas)))

    def _W_k(self, k: int) -> float:
        sigma_k_minus_1 = self._sigma(k - 1)
        sigma_k = self._sigma(k)

        if self._use_general:
            # Non-preemptive, general service, s=1
            # Wq_k = Σλᵢ(σᵢ²+1/μᵢ²) / [2(1−σ_{k−1})(1−σ_k)]
            denom = 2 * (1 - sigma_k_minus_1) * (1 - sigma_k)
            if denom <= 0:
                raise ValueError(f"Denominador inválido para classe {k}")
            Wq_k = self._numerator_general() / denom
            return Wq_k + 1.0 / self.mus[k - 1]

        if self.preemptive:
            denom = (1 - sigma_k_minus_1) * (1 - sigma_k)
            if denom <= 0:
                raise ValueError(f"Denominador inválido para classe {k}")
            return (1 / self.mu) / denom
        else:
            base = self._base_term()
            denom = base * (1 - sigma_k_minus_1) * (1 - sigma_k)
            if denom <= 0:
                raise ValueError(f"Denominador inválido para classe {k}")
            return 1 / denom + 1 / self.mu

    def _mms_W(self, lam: float) -> float:
        """W for an M/M/s queue with arrival rate lam (used for preemptive s>1)."""
        s, mu = self.s, self.mu
        rho = lam / (s * mu)
        if rho >= 1:
            raise ValueError("Sistema instável")
        a = lam / mu
        soma = sum((a ** n) / math.factorial(n) for n in range(s))
        termo_final = (a ** s) / math.factorial(s) * (1 / (1 - rho))
        P0 = 1 / (soma + termo_final)
        Lq = P0 * (a ** s) * rho / (math.factorial(s) * ((1 - rho) ** 2))
        Wq = Lq / lam if lam > 0 else 0
        return Wq + (1 / mu)

    def _W_preemptive_multi_server(self) -> list[float]:
        """W per class for preemptive priority with s>1 servers."""
        Ws = []
        for k in range(len(self.lambdas)):
            lambda_acumulado = sum(self.lambdas[:k + 1])
            W_bar = self._mms_W(lambda_acumulado)
            if k == 0:
                Ws.append(W_bar)
            else:
                soma = sum(self.lambdas[i] * Ws[i] for i in range(k))
                Wk = (lambda_acumulado * W_bar - soma) / self.lambdas[k]
                Ws.append(Wk)
        return Ws

    def results(self) -> list[dict]:
        out = []

        if self.preemptive and self.s > 1:
            Ws = self._W_preemptive_multi_server()
            for k, lam_k in enumerate(self.lambdas, start=1):
                W_k = Ws[k - 1]
                mu_k = self.mus[k - 1]
                Wq_k = W_k - 1.0 / mu_k
                lam_ref = sum(self.lambdas[:k])
                L_k = lam_ref * W_k
                Lq_k = L_k - lam_ref / mu_k
                out.append({"classe": k, "lambda": lam_k, "mu": mu_k,
                            "W": W_k, "L": L_k, "Wq": Wq_k, "Lq": Lq_k})
            return out

        for k, lam_k in enumerate(self.lambdas, start=1):
            W_k = self._W_k(k)
            mu_k = self.mus[k - 1]
            Wq_k = W_k - 1.0 / mu_k
            if self.preemptive:
                lam_ref = sum(self.lambdas[:k])
            else:
                lam_ref = lam_k
            L_k = lam_ref * W_k
            Lq_k = L_k - lam_ref / mu_k
            out.append({"classe": k, "lambda": lam_k, "mu": mu_k,
                        "W": W_k, "L": L_k, "Wq": Wq_k, "Lq": Lq_k})
        return out
