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
    # MM1 — Lista MMs, Exercício 5
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
    # MM1K — Lista MMsK, Exercício 1
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
    # MM1K — Teoria, Exemplo 2
    # λ=3/min, μ=4/min, K=5
    # ------------------------------------------------------------------
    def test_mm1k_teoria_exemplo2(self):
        model = MM1K(3, 4, 5)

        self.assert_close(model.prob_idle(), 0.3041, places=3)
        self.assert_close(model.avg_clients_system(), 1.7009, places=3)
        self.assert_close(model.avg_clients_queue(), 1.005, places=2)
        self.assert_close(model.prob_n(4), 0.09623, places=4)
        self.assert_close(model.avg_time_system(), 0.6111, places=3)
        self.assert_close(model.avg_time_queue(), 0.3611, places=3)

    # ------------------------------------------------------------------
    # MM1N — Lista MMsN, Exercício 1  (fábrica de tecidos, s=1)
    # λ=1/200/h, μ=1/10/h, N=10
    # ------------------------------------------------------------------
    def test_mm1n_matches_answer_key(self):
        model = MM1N(1 / 200, 1 / 10, 10)

        self.assert_close(model.prob_idle(), 0.5380, places=3)
        self.assert_close(model.avg_clients_system(), 0.7593, places=3)
        self.assert_close(model.avg_clients_queue(), 0.2972, places=3)
        self.assert_close(model.avg_time_system(), 16.4330, places=2)
        self.assert_close(model.avg_time_queue(), 6.4330, places=2)

    # ------------------------------------------------------------------
    # MM1N — Teoria, Exemplo 2 (robôs, s=1)
    # N=5, λ=1/30/h, μ=1/3/h
    # ------------------------------------------------------------------
    def test_mm1n_robots_s1(self):
        model = MM1N(1 / 30, 1 / 3, 5)

        self.assert_close(model.prob_idle(), 0.5640, places=3)
        L = model.avg_clients_system()
        self.assert_close(5 - L, 4.360, places=2)   # robôs operacionais
        self.assert_close(model.avg_time_system(), 4.400, places=2)

    # ------------------------------------------------------------------
    # MMS — Lista MMs, Exercício 7 (hospital, s=2)
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
    # MMsK — Lista MMsK, Exercício 3 (aeroporto 1 pista, s=1, k=4)
    # λ=0,25/min, μ=1/3/min
    # ------------------------------------------------------------------
    def test_mmsk_airport_single_runway(self):
        model = MMsK(0.25, 1 / 3, 4, 1)

        self.assert_close(model.avg_clients_queue(), 0.7721, places=3)
        self.assert_close(model.avg_time_queue(), 3.4457, places=3)
        self.assert_close(model.prob_n(4), 0.1037, places=3)

    # ------------------------------------------------------------------
    # MMsK — Lista MMsK, Exercício 4 (aeroporto 2 pistas, s=2, k=5)
    # λ=0,25/min, μ=1/3/min, K=5 total (2 pistas + 3 em espera)
    # Valores calculados com a fórmula padrão M/M/s/K.
    # ------------------------------------------------------------------
    def test_mmsk_airport_two_runways(self):
        model = MMsK(0.25, 1 / 3, 5, 2)

        self.assert_close(model.avg_clients_queue(), 0.1045, places=3)
        self.assert_close(model.avg_time_queue(), 0.4210, places=3)
        self.assert_close(model.prob_n(5), 0.0068, places=3)

    # ------------------------------------------------------------------
    # MMsK — Lista MMsK, Exercício 5 (laboratório s=2, k=5)
    # λ=1/h, μ=4/3/h, K=5 total (2 equipamentos + 3 pacientes esperando)
    # ------------------------------------------------------------------
    def test_mmsk_lab_two_servers(self):
        model = MMsK(1, 4 / 3, 5, 2)

        self.assert_close(model.avg_clients_system(), 0.8495, places=3)
        self.assert_close(model.prob_n(5), 0.0068, places=3)
        self.assert_close(model.avg_time_queue(), 0.1053, places=3)

    # ------------------------------------------------------------------
    # MMsK — Teoria, Exemplo 2 (inspeção de gases, s=3, K=7)
    # λ=1/min, μ=1/6/min  →  trabalhando em por-minuto
    # Gabarito: P0=0.00088, L=6.0631, Lq=3.0920, W=12.2442min, Wq=6.2439min
    # ------------------------------------------------------------------
    def test_mmsk_inspecao_gases(self):
        model = MMsK(1, 1 / 6, 7, 3)

        self.assert_close(model.prob_idle(), 0.00088, places=4)
        self.assert_close(model.avg_clients_system(), 6.0631, places=2)
        self.assert_close(model.avg_clients_queue(), 3.0920, places=2)
        self.assert_close(model.avg_time_system(), 12.2442, places=1)
        self.assert_close(model.avg_time_queue(), 6.2439, places=1)

    # ------------------------------------------------------------------
    # MMsN — Lista MMsN, Exercício 4 (Forrester, s=1, N=3)
    # λ=1/9/h, μ=1/2/h, N=3, s=1
    # ------------------------------------------------------------------
    def test_mmsn_forrester_one_technician(self):
        model = MMsN(1 / 9, 1 / 2, 3, 1)

        self.assert_close(model.avg_clients_system(), 0.7181, places=3)
        self.assert_close(model.avg_time_system(), 2.832, places=2)
        self.assert_close(model.server_utilization(), 0.667, places=2)

    # ------------------------------------------------------------------
    # MMsN — Lista MMsN, Exercício 4 (Forrester, s=2, N=3)
    # ------------------------------------------------------------------
    def test_mmsn_forrester_two_technicians(self):
        model = MMsN(1 / 9, 1 / 2, 3, 2)

        self.assert_close(model.avg_clients_system(), 0.5528, places=3)

    # ------------------------------------------------------------------
    # MMsN — Lista MMsN, Exercício 6 (4M Company, s=2, N=4)
    # λ=1/100/h, μ=1/10/h
    # ------------------------------------------------------------------
    def test_mmsn_4m_company(self):
        model = MMsN(1 / 100, 1 / 10, 4, 2)

        self.assert_close(model.prob_idle(), 0.6820, places=3)
        self.assert_close(model.avg_clients_system(), 0.3677, places=3)
        self.assert_close(model.avg_clients_queue(), 0.0045, places=3)
        self.assert_close(model.avg_time_system(), 10.1239, places=2)
        self.assert_close(model.avg_time_queue(), 0.1239, places=2)

    # ------------------------------------------------------------------
    # MMsN — Teoria, Exemplo 2 (robôs, s=2)
    # N=5, λ=1/30/h, μ=1/3/h
    # ------------------------------------------------------------------
    def test_mmsn_robots_s2(self):
        model = MMsN(1 / 30, 1 / 3, 5, 2)

        L = model.avg_clients_system()
        self.assert_close(5 - L, 4.535, places=2)   # robôs operacionais
        self.assert_close(model.avg_time_system(), 3.075, places=2)

    # ------------------------------------------------------------------
    # MG1 — Lista MG1, Exercício 1
    # λ=0,2, μ=0,25, vários σ²
    # ------------------------------------------------------------------
    def test_mg1_matches_answer_key(self):
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
    # MG1 — Teoria, Exemplo 2a (café expresso, distribuição exponencial)
    # λ=25/h, μ=40/h (90s → 1/40 h média), σ²=1/μ²=1/1600
    # Gabarito: Lq=1,042; L=1,667; Wq=0,042; W=0,067
    # ------------------------------------------------------------------
    def test_mg1_cafe_exponencial(self):
        model = MG1(25, 40, 1 / 1600)

        self.assert_close(model.avg_clients_queue(), 1.042, places=2)
        self.assert_close(model.avg_clients_system(), 1.667, places=2)
        self.assert_close(model.avg_time_queue(), 0.042, places=3)
        self.assert_close(model.avg_time_system(), 0.067, places=3)

    # ------------------------------------------------------------------
    # MG1 — Teoria, Exemplo 2b (café expresso, máquina determinística)
    # σ²=0  →  Lq=0,521; L=1,146; Wq=0,021; W=0,046
    # ------------------------------------------------------------------
    def test_mg1_cafe_deterministico(self):
        model = MG1(25, 40, 0)

        self.assert_close(model.avg_clients_queue(), 0.521, places=2)
        self.assert_close(model.avg_clients_system(), 1.146, places=2)
        self.assert_close(model.avg_time_queue(), 0.021, places=3)
        self.assert_close(model.avg_time_system(), 0.046, places=3)

    # ------------------------------------------------------------------
    # PriorityQueue sem interrupção — Lista MG1+prio, Exercício 6 (ferramentaria)
    # λ=[2,4,2], μ=10, s=1
    # ------------------------------------------------------------------
    def test_priority_nonpreemptive_matches_answer_key(self):
        nonpreemptive = PriorityQueue([2, 4, 2], 10, 1, False).results()
        by_class = {row["classe"]: row for row in nonpreemptive}

        self.assert_close(by_class[1]["W"],  0.2,  places=2)
        self.assert_close(by_class[1]["Wq"], 0.1,  places=2)
        self.assert_close(by_class[1]["L"],  0.4,  places=2)
        self.assert_close(by_class[1]["Lq"], 0.2,  places=2)

        self.assert_close(by_class[2]["W"],  0.35, places=2)
        self.assert_close(by_class[2]["Wq"], 0.25, places=2)
        self.assert_close(by_class[2]["L"],  1.4,  places=2)
        self.assert_close(by_class[2]["Lq"], 1.0,  places=2)

        self.assert_close(by_class[3]["W"],  1.1,  places=2)
        self.assert_close(by_class[3]["Wq"], 1.0,  places=2)
        self.assert_close(by_class[3]["L"],  2.2,  places=2)
        self.assert_close(by_class[3]["Lq"], 2.0,  places=2)

    # ------------------------------------------------------------------
    # PriorityQueue com interrupção — Lista MG1+prio, Exercício 6 (ferramentaria)
    # λ=[2,4,2], μ=10, s=1
    # ------------------------------------------------------------------
    def test_priority_preemptive_matches_answer_key(self):
        preemptive = PriorityQueue([2, 4, 2], 10, 1, True).results()
        by_class = {row["classe"]: row for row in preemptive}

        self.assert_close(by_class[1]["W"],  0.125,  places=3)
        self.assert_close(by_class[1]["Wq"], 0.025,  places=3)
        self.assert_close(by_class[2]["W"],  0.3125, places=3)
        self.assert_close(by_class[2]["Wq"], 0.2125, places=3)
        self.assert_close(by_class[3]["W"],  1.25,   places=2)
        self.assert_close(by_class[3]["Wq"], 1.15,   places=2)

    # ------------------------------------------------------------------
    # PriorityQueue sem interrupção — Teoria, Exemplo 1 (hospital, s=1)
    # μ=3, λ=[0.2,0.6,1.2], s=1
    # Gabarito: W1=0.5714, Wq1=0.23809, W2=0.658, Wq2=0.32467, W3=1.24242, Wq3=0.90909
    # ------------------------------------------------------------------
    def test_priority_hospital_s1_nonpreemptive(self):
        m = PriorityQueue([0.2, 0.6, 1.2], 3, 1, False).results()
        by = {r["classe"]: r for r in m}

        self.assert_close(by[1]["W"],  0.5714,  places=3)
        self.assert_close(by[1]["Wq"], 0.23809, places=4)
        self.assert_close(by[2]["W"],  0.6580,  places=3)
        self.assert_close(by[2]["Wq"], 0.32467, places=4)
        self.assert_close(by[3]["W"],  1.24242, places=4)
        self.assert_close(by[3]["Wq"], 0.90909, places=4)

    # ------------------------------------------------------------------
    # PriorityQueue sem interrupção — Teoria, Exemplo 1 (hospital, s=2)
    # μ=3, λ=[0.2,0.6,1.2], s=2
    # Gabarito: W1=0.36207, Wq1=0.02874
    # ------------------------------------------------------------------
    def test_priority_hospital_s2_nonpreemptive(self):
        m = PriorityQueue([0.2, 0.6, 1.2], 3, 2, False).results()
        by = {r["classe"]: r for r in m}

        self.assert_close(by[1]["W"],  0.36207, places=4)
        self.assert_close(by[1]["Wq"], 0.02874, places=4)
        self.assert_close(by[2]["W"],  0.36649, places=4)
        self.assert_close(by[2]["Wq"], 0.03316, places=4)
        self.assert_close(by[3]["W"],  0.38141, places=4)
        self.assert_close(by[3]["Wq"], 0.04808, places=4)

    # ------------------------------------------------------------------
    # PriorityQueue com interrupção — Teoria, Exemplo 1 (hospital, s=1)
    # μ=3, λ=[0.2,0.6,1.2]
    # Gabarito: W1=0.3571, Wq1=0.0238, W2=0.4870, Wq2=0.1537, W3=1.3636, Wq3=1.0303
    # ------------------------------------------------------------------
    def test_priority_hospital_s1_preemptive(self):
        m = PriorityQueue([0.2, 0.6, 1.2], 3, 1, True).results()
        by = {r["classe"]: r for r in m}

        self.assert_close(by[1]["W"],  0.3571, places=3)
        self.assert_close(by[1]["Wq"], 0.0238, places=3)
        self.assert_close(by[2]["W"],  0.4870, places=3)
        self.assert_close(by[2]["Wq"], 0.1537, places=3)
        self.assert_close(by[3]["W"],  1.3636, places=3)
        self.assert_close(by[3]["Wq"], 1.0303, places=3)

    # ------------------------------------------------------------------
    # PriorityQueue sem interrupção — Teoria, Exemplo 3 (delegacia, s=5)
    # λ=[10,20], μ=7.5, s=5
    # Gabarito: Wq1=0.0201, Wq2=0.1007
    # ------------------------------------------------------------------
    def test_priority_delegacia_s5_nonpreemptive(self):
        m = PriorityQueue([10, 20], 7.5, 5, False).results()
        by = {r["classe"]: r for r in m}

        self.assert_close(by[1]["Wq"], 0.0201, places=3)
        self.assert_close(by[2]["Wq"], 0.1007, places=3)

    # ------------------------------------------------------------------
    # PriorityQueue sem interrupção com μ/σ² por classe — Teoria, Exemplo 2
    # λ1=10, λ2=5, μ1=20, μ2=15, σ²1=σ²2=1/1800 hr², s=1
    # Gabarito: Wq1≈0.0556h, W1≈0.1056h, Wq2≈0.333h, W2≈0.400h, L2≈2.0
    # ------------------------------------------------------------------
    def test_priority_per_class_mu_sigma2(self):
        m = PriorityQueue(
            lambdas=[10, 5],
            mu=20,
            s=1,
            preemptive=False,
            mus=[20, 15],
            sigma2s=[1 / 1800, 1 / 1800],
        ).results()
        by = {r["classe"]: r for r in m}

        self.assert_close(by[1]["Wq"], 100 / 1800, places=4)   # ≈ 0.0556
        self.assert_close(by[1]["W"],  100 / 1800 + 1 / 20, places=4)
        self.assert_close(by[2]["Wq"], 1 / 3, places=3)        # ≈ 0.333
        self.assert_close(by[2]["W"],  1 / 3 + 1 / 15, places=3)
        self.assert_close(by[2]["L"],  2.0, places=2)


class TestValidation(unittest.TestCase):
    """Guard-clause coverage: every ValueError path in constructors and methods."""

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

    def test_mm1k_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MM1K(0, 4, 5)

    def test_mm1k_invalid_mi(self):
        with self.assertRaises(ValueError):
            MM1K(2, 0, 5)

    def test_mm1k_invalid_k(self):
        with self.assertRaises(ValueError):
            MM1K(2, 4, 0)

    def test_mm1n_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MM1N(0, 0.1, 10)

    def test_mm1n_invalid_mi(self):
        with self.assertRaises(ValueError):
            MM1N(0.005, 0, 10)

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

    def test_mmsn_invalid_lambda(self):
        with self.assertRaises(ValueError):
            MMsN(0, 0.5, 3, 1)

    def test_mmsn_invalid_mi(self):
        with self.assertRaises(ValueError):
            MMsN(1 / 9, 0, 3, 1)

    def test_mg1_invalid_mi(self):
        with self.assertRaises(ValueError):
            MG1(0.2, 0, 4)

    def test_mg1_invalid_sigma2_negative(self):
        with self.assertRaises(ValueError):
            MG1(0.2, 0.25, -1)

    def test_mg1_unstable(self):
        with self.assertRaises(ValueError):
            MG1(0.3, 0.25, 4)

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
        with self.assertRaises(ValueError):
            PriorityQueue([5, 5, 5], 10, 1, False)

    def test_priority_per_class_mu_preemptive_raises(self):
        with self.assertRaises(ValueError):
            PriorityQueue([10, 5], 20, 1, True, mus=[20, 15])

    def test_priority_per_class_mu_s_gt1_raises(self):
        with self.assertRaises(ValueError):
            PriorityQueue([10, 5], 20, 2, False, mus=[20, 15])


class TestAdditionalCoverage(unittest.TestCase):
    def assert_close(self, actual, expected, places=4):
        self.assertAlmostEqual(actual, expected, places=places)

    def test_mm1_prob_idle(self):
        self.assert_close(MM1(3, 4).prob_idle(), 0.25)

    def test_mm1_prob_n(self):
        m = MM1(3, 4)
        self.assert_close(m.prob_n(0), 0.25)
        self.assert_close(m.prob_n(2), 0.140625)

    def test_mm1_prob_greater_r(self):
        self.assert_close(MM1(3, 4).prob_greater_r(0), 0.75)

    def test_mm1k_rho_equals_one(self):
        self.assert_close(MM1K(4, 4, 5).prob_idle(), 1 / 6)

    def test_mm1k_prob_n_out_of_range(self):
        m = MM1K(2, 4, 5)
        self.assertEqual(m.prob_n(-1), 0)
        self.assertEqual(m.prob_n(6), 0)

    def test_mm1n_rho(self):
        self.assert_close(MM1N(1 / 200, 1 / 10, 10).rho, 0.5)

    def test_mm1n_prob_n(self):
        m = MM1N(1 / 200, 1 / 10, 10)
        self.assert_close(m.prob_n(0), m.prob_idle())

    def test_mms_prob_n_le_s(self):
        self.assert_close(MMS(2, 3, 2).prob_n(1), 1 / 3)

    def test_mms_prob_n_gt_s(self):
        self.assert_close(MMS(2, 3, 2).prob_n(3), 1 / 27)

    def test_mms_prob_wait_system_alpha_equals_mi(self):
        result = MMS(3, 3, 2).prob_wait_system_greater_than(1)
        self.assertGreater(result, 0)
        self.assertLess(result, 1)

    def test_mmsk_prob_n_out_of_range(self):
        m = MMsK(0.25, 1 / 3, 4, 1)
        self.assertEqual(m.prob_n(-1), 0)
        self.assertEqual(m.prob_n(5), 0)

    def test_mmsk_avg_time_system(self):
        result = MMsK(1, 4 / 3, 5, 2).avg_time_system()
        self.assertGreater(result, 0)
        self.assertFalse(math.isnan(result))

    def test_mmsn_prob_n_out_of_range(self):
        m = MMsN(1 / 9, 1 / 2, 3, 1)
        self.assertEqual(m.prob_n(-1), 0)
        self.assertEqual(m.prob_n(10), 0)

    def test_mg1_p0(self):
        self.assert_close(MG1(0.2, 0.25, 4).p0, 0.2)

    def test_priority_rho_total(self):
        self.assert_close(PriorityQueue([2, 4, 2], 10, 1, False).rho_total, 0.8)

    def test_priority_per_class_mu_rho_total(self):
        # ρ = 10/20 + 5/15 = 0.5 + 0.333 = 0.833
        m = PriorityQueue([10, 5], 20, 1, False, mus=[20, 15])
        self.assert_close(m.rho_total, 10 / 20 + 5 / 15, places=4)


if __name__ == "__main__":
    unittest.main()
