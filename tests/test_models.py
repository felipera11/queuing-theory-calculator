import math
import unittest

from models.mm1_model import MM1
from models.mm1k_model import MM1K
from models.mm1n_model import MM1N
from models.mg1_model import MG1
from models.mms_model import MMS
from models.mmsk_model import MMsK
from models.mmsn_model import MMsN
from models.priority_model import PriorityQueue


class TestQueueModels(unittest.TestCase):
    def assert_close(self, actual, expected, places=4):
        self.assertAlmostEqual(actual, expected, places=places)

    # ------------------------------------------------------------------
    # MM1 — Lista 2, Exercício 5
    # λ=3/h, μ=4/h
    # ------------------------------------------------------------------
    def test_mm1_matches_answer_key(self):
        model = MM1(3, 4)

        self.assert_close(model.rho, 0.75)
        self.assert_close(model.avg_clients_system(), 3.0)
        self.assert_close(model.avg_clients_queue(), 2.25)
        self.assert_close(model.avg_time_system(), 1.0)
        self.assert_close(model.avg_time_queue(), 0.75)
        self.assert_close(model.prob_wait_system_greater_than(2), 0.1353, places=3)
        self.assert_close(model.prob_wait_queue_greater_than(1.5), 0.1673, places=3)

    # ------------------------------------------------------------------
    # MM1K — Lista 3, Exercício 1
    # λ=2/min, μ=4/min, k=5
    # ------------------------------------------------------------------
    def test_mm1k_matches_answer_key(self):
        model = MM1K(2, 4, 5)

        self.assert_close(model.prob_idle(), 0.5079, places=3)
        self.assert_close(model.avg_clients_system(), 0.9048, places=3)
        self.assert_close(model.avg_clients_queue(), 0.4127, places=3)
        self.assert_close(model.prob_n(4), 0.03175, places=4)
        self.assert_close(model.avg_time_system(), 0.4597, places=3)
        self.assert_close(model.avg_time_queue(), 0.2097, places=3)

    # ------------------------------------------------------------------
    # MM1N — Lista 4, Exercício 1
    # λ_maq=1/200/h, μ=1/10/h, N=10
    # ------------------------------------------------------------------
    def test_mm1n_matches_answer_key(self):
        model = MM1N(1 / 200, 1 / 10, 10)

        self.assert_close(model.prob_idle(), 0.5380, places=3)
        self.assert_close(model.avg_clients_system(), 0.7593, places=3)
        self.assert_close(model.avg_clients_queue(), 0.2972, places=3)
        self.assert_close(model.avg_time_system(), 16.4330, places=2)
        self.assert_close(model.avg_time_queue(), 6.4330, places=2)

    # ------------------------------------------------------------------
    # MMS — Lista 2, Exercício 7 (Hospital, s=2)
    # λ=2/h, μ=3/h, s=2
    # ------------------------------------------------------------------
    def test_mms_matches_answer_key(self):
        model = MMS(2, 3, 2)

        self.assert_close(model.rho, 1 / 3)
        self.assert_close(model.p0, 0.5)
        self.assert_close(model.avg_clients_system(), 0.75)
        self.assert_close(model.avg_clients_queue(), 1 / 12)
        self.assert_close(model.avg_time_system(), 3 / 8)
        self.assert_close(model.avg_time_queue(), 1 / 24)
        self.assert_close(model.prob_wait_queue_greater_than(0.5), 0.023, places=3)
        self.assert_close(model.prob_wait_system_greater_than(1), 0.0655, places=3)

    # ------------------------------------------------------------------
    # MMsK — Lista 3, Exercício 3 (aeroporto 1 pista, s=1, k=4)
    # λ=0,25/min, μ=1/3/min, k=4, s=1
    # k=4: 1 pousando + 3 em espera
    # ------------------------------------------------------------------
    def test_mmsk_airport_single_runway(self):
        model = MMsK(0.25, 1 / 3, 4, 1)

        self.assert_close(model.avg_clients_queue(), 0.7721, places=3)
        self.assert_close(model.avg_time_queue(), 3.4457, places=3)
        self.assert_close(model.prob_n(4), 0.1037, places=3)

    # ------------------------------------------------------------------
    # MMsK — Lista 3, Exercício 4 (aeroporto 2 pistas, s=2, k=5)
    # λ=0,25/min, μ=1/3/min, k=5, s=2
    # k=5: 2 pousando + 3 em espera
    # ------------------------------------------------------------------
    def test_mmsk_airport_two_runways(self):
        model = MMsK(0.25, 1 / 3, 5, 2)

        self.assert_close(model.avg_clients_queue(), 0.0848, places=3)
        self.assert_close(model.avg_time_queue(), 0.3455, places=3)
        self.assert_close(model.prob_n(5), 0.0182, places=3)

    # ------------------------------------------------------------------
    # MMsK — Lista 3, Exercício 5 (laboratório s=2, k=5)
    # λ=1/h, μ=4/3/h, k=5, s=2
    # k=5: capacidade máxima total do laboratório
    # ------------------------------------------------------------------
    def test_mmsk_lab_two_servers(self):
        model = MMsK(1, 4 / 3, 5, 2)

        self.assert_close(model.avg_clients_system(), 0.8212, places=3)
        self.assert_close(model.prob_n(5), 0.0182, places=3)
        self.assert_close(model.avg_time_queue(), 0.0864, places=3)

    # ------------------------------------------------------------------
    # MMsN — Lista 4, Exercício 4 (Forrester, s=1, N=3)
    # λ=1/9/h, μ=1/2/h, N=3, s=1
    # Gabarito fornece L=0,7181 | W=2,832 | técnico ocupado=66,7%
    # ------------------------------------------------------------------
    def test_mmsn_forrester_one_technician(self):
        model = MMsN(1 / 9, 1 / 2, 3, 1)

        self.assert_close(model.avg_clients_system(), 0.7181, places=3)
        self.assert_close(model.avg_time_system(), 2.832, places=2)
        self.assert_close(model.server_utilization(), 0.667, places=2)

    # ------------------------------------------------------------------
    # MMsN — Lista 4, Exercício 4 (Forrester, s=2, N=3)
    # λ=1/9/h, μ=1/2/h, N=3, s=2
    # Gabarito fornece apenas L=0,5528 para s=2
    # ------------------------------------------------------------------
    def test_mmsn_forrester_two_technicians(self):
        model = MMsN(1 / 9, 1 / 2, 3, 2)

        self.assert_close(model.avg_clients_system(), 0.5528, places=3)

    # ------------------------------------------------------------------
    # MMsN — Lista 4, Exercício 6 (4M Company, s=2, N=4)
    # λ=1/100/h, μ=1/10/h, N=4, s=2
    # ------------------------------------------------------------------
    def test_mmsn_4m_company(self):
        model = MMsN(1 / 100, 1 / 10, 4, 2)

        self.assert_close(model.prob_idle(), 0.6820, places=3)
        self.assert_close(model.avg_clients_system(), 0.3677, places=3)
        self.assert_close(model.avg_clients_queue(), 0.0045, places=3)
        self.assert_close(model.avg_time_system(), 10.1239, places=2)
        self.assert_close(model.avg_time_queue(), 0.1239, places=2)

    # ------------------------------------------------------------------
    # MG1 — Lista 1, Exercício 1
    # λ=0,2, μ=0,25
    # Nota: o modelo recebe variância (σ²), não desvio-padrão (σ)
    # Ex: σ=4 → σ²=16
    # ------------------------------------------------------------------
    def test_mg1_matches_answer_key(self):
        # (sigma², lq, l, wq, w)
        expected = [
            (16, 3.2, 4.0, 16.0, 20.0),
            (9,  2.5, 3.3, 12.5, 16.5),
            (4,  2.0, 2.8, 10.0, 14.0),
            (1,  1.7, 2.5,  8.5, 12.5),
            (0,  1.6, 2.4,  8.0, 12.0),
        ]

        for sigma2, lq, l, wq, w in expected:
            with self.subTest(sigma2=sigma2):
                model = MG1(0.2, 0.25, sigma2)
                self.assert_close(model.avg_clients_queue(), lq, places=1)
                self.assert_close(model.avg_clients_system(), l, places=1)
                self.assert_close(model.avg_time_queue(), wq, places=1)
                self.assert_close(model.avg_time_system(), w, places=1)

    # ------------------------------------------------------------------
    # PriorityQueue sem interrupção — Lista 1, Exercício 6 (ferramentaria)
    # λ=[2,4,2], μ=10, s=1
    # L e Lq derivados pela Lei de Little: L=λ*W, Lq=λ*Wq
    # ------------------------------------------------------------------
    def test_priority_nonpreemptive_matches_answer_key(self):
        nonpreemptive = PriorityQueue([2, 4, 2], 10, 1, False).results()
        by_class = {row["classe"]: row for row in nonpreemptive}

        # Classe 1: W=0,2 | Wq=0,1 | L=2*0,2=0,4 | Lq=2*0,1=0,2
        self.assert_close(by_class[1]["W"],  0.2,  places=2)
        self.assert_close(by_class[1]["Wq"], 0.1,  places=2)
        self.assert_close(by_class[1]["L"],  0.4,  places=2)
        self.assert_close(by_class[1]["Lq"], 0.2,  places=2)

        # Classe 2: W=0,35 | Wq=0,25 | L=4*0,35=1,4 | Lq=4*0,25=1,0
        self.assert_close(by_class[2]["W"],  0.35, places=2)
        self.assert_close(by_class[2]["Wq"], 0.25, places=2)
        self.assert_close(by_class[2]["L"],  1.4,  places=2)
        self.assert_close(by_class[2]["Lq"], 1.0,  places=2)

        # Classe 3: W=1,1 | Wq=1,0 | L=2*1,1=2,2 | Lq=2*1,0=2,0
        self.assert_close(by_class[3]["W"],  1.1,  places=2)
        self.assert_close(by_class[3]["Wq"], 1.0,  places=2)
        self.assert_close(by_class[3]["L"],  2.2,  places=2)
        self.assert_close(by_class[3]["Lq"], 2.0,  places=2)

    # ------------------------------------------------------------------
    # PriorityQueue com interrupção — Lista 1, Exercício 6 (ferramentaria)
    # λ=[2,4,2], μ=10, s=1
    # Wq = W - 1/μ = W - 0,1
    # L e Lq derivados pela Lei de Little: L=λ*W, Lq=λ*Wq
    # ------------------------------------------------------------------
    def test_priority_preemptive_matches_answer_key(self):
        preemptive = PriorityQueue([2, 4, 2], 10, 1, True).results()
        by_class = {row["classe"]: row for row in preemptive}

        # Classe 1: W=0,125 | Wq=0,125-0,1=0,025 | L=2*0,125=0,25 | Lq=2*0,025=0,05
        self.assert_close(by_class[1]["W"],  0.125,  places=3)
        self.assert_close(by_class[1]["Wq"], 0.025,  places=3)
        self.assert_close(by_class[1]["L"],  0.25,   places=2)
        self.assert_close(by_class[1]["Lq"], 0.05,   places=2)

        # Classe 2: W=0,3125 | Wq=0,3125-0,1=0,2125 | L=4*0,3125=1,25 | Lq=4*0,2125=0,85
        self.assert_close(by_class[2]["W"],  0.3125, places=3)
        self.assert_close(by_class[2]["Wq"], 0.2125, places=3)
        self.assert_close(by_class[2]["L"],  1.25,   places=2)
        self.assert_close(by_class[2]["Lq"], 0.85,   places=2)

        # Classe 3: W=1,25 | Wq=1,25-0,1=1,15 | L=2*1,25=2,5 | Lq=2*1,15=2,3
        self.assert_close(by_class[3]["W"],  1.25,   places=2)
        self.assert_close(by_class[3]["Wq"], 1.15,   places=2)
        self.assert_close(by_class[3]["L"],  2.5,    places=2)
        self.assert_close(by_class[3]["Lq"], 2.3,    places=2)


class TestValidation(unittest.TestCase):
    """Guard-clause coverage: every ValueError path in constructors and methods."""

    # ------------------------------------------------------------------
    # MM1
    # ------------------------------------------------------------------
    def test_mm1_invalid_mi(self):
        with self.assertRaises(ValueError):
            MM1(3, 0)

    def test_mm1_unstable(self):
        with self.assertRaises(ValueError):
            MM1(4, 4)

    def test_mm1_prob_n_negative_n(self):
        with self.assertRaises(ValueError):
            MM1(3, 4).prob_n(-1)

    def test_mm1_prob_greater_r_negative(self):
        with self.assertRaises(ValueError):
            MM1(3, 4).prob_greater_r(-1)

    def test_mm1_prob_wait_system_negative_t(self):
        with self.assertRaises(ValueError):
            MM1(3, 4).prob_wait_system_greater_than(-0.1)

    def test_mm1_prob_wait_queue_negative_t(self):
        with self.assertRaises(ValueError):
            MM1(3, 4).prob_wait_queue_greater_than(-0.1)

    # ------------------------------------------------------------------
    # MM1K
    # ------------------------------------------------------------------
    def test_mm1k_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MM1K(0, 4, 5)

    def test_mm1k_invalid_mi(self):
        with self.assertRaises(ValueError):
            MM1K(2, 0, 5)

    def test_mm1k_invalid_k(self):
        with self.assertRaises(ValueError):
            MM1K(2, 4, 0)

    # ------------------------------------------------------------------
    # MM1N
    # ------------------------------------------------------------------
    def test_mm1n_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MM1N(0, 0.1, 10)

    def test_mm1n_invalid_mi(self):
        with self.assertRaises(ValueError):
            MM1N(0.005, 0, 10)

    # ------------------------------------------------------------------
    # MMS
    # ------------------------------------------------------------------
    def test_mms_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MMS(0, 3, 2)

    def test_mms_invalid_mi(self):
        with self.assertRaises(ValueError):
            MMS(2, 0, 2)

    def test_mms_s_less_than_2(self):
        with self.assertRaises(ValueError):
            MMS(2, 3, 1)

    def test_mms_unstable(self):
        # ρ = 6 / (2·3) = 1 ≥ 1
        with self.assertRaises(ValueError):
            MMS(6, 3, 2)

    def test_mms_prob_n_negative_n(self):
        with self.assertRaises(ValueError):
            MMS(2, 3, 2).prob_n(-1)

    def test_mms_prob_wait_queue_negative_t(self):
        with self.assertRaises(ValueError):
            MMS(2, 3, 2).prob_wait_queue_greater_than(-1)

    def test_mms_prob_wait_system_negative_t(self):
        with self.assertRaises(ValueError):
            MMS(2, 3, 2).prob_wait_system_greater_than(-1)

    # ------------------------------------------------------------------
    # MMsK
    # ------------------------------------------------------------------
    def test_mmsk_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MMsK(0, 1 / 3, 4, 1)

    def test_mmsk_invalid_mi(self):
        with self.assertRaises(ValueError):
            MMsK(0.25, 0, 4, 1)

    def test_mmsk_invalid_k(self):
        with self.assertRaises(ValueError):
            MMsK(0.25, 1 / 3, 0, 1)

    def test_mmsk_k_less_than_s(self):
        with self.assertRaises(ValueError):
            MMsK(0.25, 1 / 3, 1, 2)

    # ------------------------------------------------------------------
    # MMsN
    # ------------------------------------------------------------------
    def test_mmsn_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MMsN(0, 0.5, 3, 1)

    def test_mmsn_invalid_mi(self):
        with self.assertRaises(ValueError):
            MMsN(1 / 9, 0, 3, 1)

    # ------------------------------------------------------------------
    # MG1
    # ------------------------------------------------------------------
    def test_mg1_invalid_mi(self):
        with self.assertRaises(ValueError):
            MG1(0.2, 0, 4)

    def test_mg1_invalid_sigma2_negative(self):
        with self.assertRaises(ValueError):
            MG1(0.2, 0.25, -1)

    def test_mg1_unstable(self):
        # ρ = 0.3 / 0.25 = 1.2 ≥ 1
        with self.assertRaises(ValueError):
            MG1(0.3, 0.25, 4)

    # ------------------------------------------------------------------
    # PriorityQueue
    # ------------------------------------------------------------------
    def test_priority_invalid_mu(self):
        with self.assertRaises(ValueError):
            PriorityQueue([2, 4, 2], 0, 1, False)

    def test_priority_invalid_s(self):
        with self.assertRaises(ValueError):
            PriorityQueue([2, 4, 2], 10, 0, False)

    def test_priority_negative_lambda(self):
        with self.assertRaises(ValueError):
            PriorityQueue([2, -1, 2], 10, 1, False)

    def test_priority_empty_lambdas(self):
        with self.assertRaises(ValueError):
            PriorityQueue([], 10, 1, False)

    def test_priority_unstable(self):
        # ρ = 15 / 10 = 1.5 ≥ 1
        with self.assertRaises(ValueError):
            PriorityQueue([5, 5, 5], 10, 1, False)


class TestAdditionalCoverage(unittest.TestCase):
    """Covers methods and branches not exercised by answer-key tests."""

    def assert_close(self, actual, expected, places=4):
        self.assertAlmostEqual(actual, expected, places=places)

    # ------------------------------------------------------------------
    # MM1 — prob_idle, prob_n, prob_greater_r (λ=3, μ=4, ρ=0.75)
    # ------------------------------------------------------------------
    def test_mm1_prob_idle(self):
        self.assert_close(MM1(3, 4).prob_idle(), 0.25)

    def test_mm1_prob_n(self):
        m = MM1(3, 4)
        # P(N=0) = (1−ρ)·ρ⁰ = 0.25
        self.assert_close(m.prob_n(0), 0.25)
        # P(N=2) = 0.25 · 0.75² = 0.140625
        self.assert_close(m.prob_n(2), 0.140625)

    def test_mm1_prob_greater_r(self):
        # P(N > 0) = ρ¹ = 0.75
        self.assert_close(MM1(3, 4).prob_greater_r(0), 0.75)

    # ------------------------------------------------------------------
    # MM1K — ρ=1 special case and out-of-range prob_n
    # ------------------------------------------------------------------
    def test_mm1k_rho_equals_one(self):
        # λ=μ → ρ=1 → prob_idle = 1/(K+1) = 1/6
        self.assert_close(MM1K(4, 4, 5).prob_idle(), 1 / 6)

    def test_mm1k_prob_n_out_of_range(self):
        m = MM1K(2, 4, 5)
        self.assertEqual(m.prob_n(-1), 0)
        self.assertEqual(m.prob_n(6), 0)

    # ------------------------------------------------------------------
    # MM1N — rho property and prob_n
    # ρ = N·λ/μ = 10·(1/200)/(1/10) = 0.5
    # ------------------------------------------------------------------
    def test_mm1n_rho(self):
        self.assert_close(MM1N(1 / 200, 1 / 10, 10).rho, 0.5)

    def test_mm1n_prob_n(self):
        m = MM1N(1 / 200, 1 / 10, 10)
        # P(N=0) collapses to prob_idle via the formula
        self.assert_close(m.prob_n(0), m.prob_idle())

    # ------------------------------------------------------------------
    # MMS — prob_n branches (λ=2, μ=3, s=2, a=2/3, p0=0.5)
    # ------------------------------------------------------------------
    def test_mms_prob_n_le_s(self):
        # n=1 ≤ s=2: (a/1!)·p0 = (2/3)·0.5 = 1/3
        self.assert_close(MMS(2, 3, 2).prob_n(1), 1 / 3)

    def test_mms_prob_n_gt_s(self):
        # n=3 > s=2: (a³/(2!·2¹))·p0 = (8/27)/4·0.5 = 1/27
        self.assert_close(MMS(2, 3, 2).prob_n(3), 1 / 27)

    def test_mms_prob_wait_system_alpha_equals_mi(self):
        # s=2, μ=3, λ=3 → α = s·μ−λ = 3 = μ; triggers the special branch
        result = MMS(3, 3, 2).prob_wait_system_greater_than(1)
        self.assertGreater(result, 0)
        self.assertLess(result, 1)

    # ------------------------------------------------------------------
    # MMsK — out-of-range prob_n and avg_time_system
    # ------------------------------------------------------------------
    def test_mmsk_prob_n_out_of_range(self):
        m = MMsK(0.25, 1 / 3, 4, 1)
        self.assertEqual(m.prob_n(-1), 0)
        self.assertEqual(m.prob_n(5), 0)

    def test_mmsk_avg_time_system(self):
        # Lista 3, Exercício 5 — avg_time_system not covered by answer key
        result = MMsK(1, 4 / 3, 5, 2).avg_time_system()
        self.assertGreater(result, 0)
        self.assertFalse(math.isnan(result))

    # ------------------------------------------------------------------
    # MMsN — out-of-range prob_n
    # ------------------------------------------------------------------
    def test_mmsn_prob_n_out_of_range(self):
        m = MMsN(1 / 9, 1 / 2, 3, 1)
        self.assertEqual(m.prob_n(-1), 0)
        self.assertEqual(m.prob_n(10), 0)

    # ------------------------------------------------------------------
    # MG1 — p0 property (ρ=0.8, p0=0.2)
    # ------------------------------------------------------------------
    def test_mg1_p0(self):
        self.assert_close(MG1(0.2, 0.25, 4).p0, 0.2)

    # ------------------------------------------------------------------
    # PriorityQueue — rho_total property
    # λ_total=8, s·μ=10 → ρ_total=0.8
    # ------------------------------------------------------------------
    def test_priority_rho_total(self):
        self.assert_close(PriorityQueue([2, 4, 2], 10, 1, False).rho_total, 0.8)


if __name__ == "__main__":
    unittest.main()