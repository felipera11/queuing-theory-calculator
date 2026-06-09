
import math


class PriorityQueue:

    def __init__(self, lambdas: list[float], mu: float, s: int, preemptive: bool):
        
        if mu <= 0:
            raise ValueError("μ deve ser maior que zero")
        if s < 1:
            raise ValueError("s deve ser >= 1")
        if any(l < 0 for l in lambdas):
            raise ValueError("Todas as taxas λ devem ser >= 0")
        if len(lambdas) == 0:
            raise ValueError("Informe ao menos uma classe")

        lambda_total = sum(lambdas)
        rho_total = lambda_total / (s * mu)

        if rho_total >= 1:
            raise ValueError(f"Sistema instável (ρ = {rho_total:.4f} >= 1)")

        self.lambdas = lambdas
        self.mu = mu
        self.s = s
        self.preemptive = preemptive
        self.lambda_total = lambda_total

    @property
    def r(self):
        """r = λ_total / μ"""
        return self.lambda_total / self.mu

    @property
    def rho_total(self):
        return self.lambda_total / (self.s * self.mu)

    def _sigma(self, k: int) -> float:
        """Σ(i=1 to k) λᵢ / (s*μ)  — soma das k primeiras classes"""
        return sum(self.lambdas[:k]) / (self.s * self.mu)

    def _base_term(self) -> float:
        """
        Termo base compartilhado na fórmula sem interrupção:
          s! * (sμ - λ) / rˢ * Σ(j=0 to s-1) rʲ/j!  +  sμ
        """
        s = self.s
        mu = self.mu
        r = self.r
        lam = self.lambda_total

        soma = sum((r ** j) / math.factorial(j) for j in range(s))
        return math.factorial(s) * (s * mu - lam) / (r ** s) * soma + s * mu

    def _W_k(self, k: int) -> float:
        """
        Tempo médio no sistema para a classe k (índice 1-based).
        """
        sigma_k_minus_1 = self._sigma(k - 1)   # Σ i=1..k-1
        sigma_k = self._sigma(k)                # Σ i=1..k

        if self.preemptive:
            # COM interrupção
            denom = (1 - sigma_k_minus_1) * (1 - sigma_k)
            if denom <= 0:
                raise ValueError(f"Denominador inválido para classe {k} (sistema sobrecarregado)")
            return (1 / self.mu) / denom
        else:
            # SEM interrupção
            base = self._base_term()
            denom = base * (1 - sigma_k_minus_1) * (1 - sigma_k)
            if denom <= 0:
                raise ValueError(f"Denominador inválido para classe {k} (sistema sobrecarregado)")
            return 1 / denom + 1 / self.mu

    def results(self) -> list[dict]:
        """Retorna lista de dicionários com métricas por classe.

        Com interrupção (preemptivo):
          L_k  = (Σλᵢ, i=1..k) * W_k   — lambda acumulado até k
          Lq_k = L_k - (Σλᵢ, i=1..k) / μ

        Sem interrupção:
          L_k  = λ_k * W_k
          Lq_k = L_k - λ_k / μ
        """
        out = []
        for k, lam_k in enumerate(self.lambdas, start=1):
            W_k = self._W_k(k)
            Wq_k = W_k - 1 / self.mu

            lam_ref = lam_k

            L_k  = lam_ref * W_k
            Lq_k = L_k - lam_ref / self.mu

            out.append({
                "classe": k,
                "lambda": lam_k,
                "W":  W_k,
                "L":  L_k,
                "Wq": Wq_k,
                "Lq": Lq_k,
            })
        return out