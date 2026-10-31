"""
JEV Research Evaluation Framework
Calculates Expected Calibration Error (ECE), Accuracy, and Latency Metrics.
Ready for Phase 2 offline validation.
"""

import json
import time
import numpy as np
from typing import List, Dict, Any
from jev_client import JevClient, Choice, Score, Noul

API_KEY = "apikey_2998e6693e0329444758839b8e9f443cf4e_b83254734358781cd5052308f8a0426736d50140c91fe368289899f68461840e"


def compute_ece(probs: List[float], labels: List[int], n_bins: int = 10) -> float:
    """
    Computes Expected Calibration Error (ECE).
    :param probs: Predicted confidence / probability for the positive class (or top class).
    :param labels: True binary indicators (1 if prediction correct or positive, 0 otherwise).
    :param n_bins: Number of probability bins.
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n = len(probs)
    if n == 0:
        return 0.0

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        # Get indices of items falling into this bin
        in_bin = [
            j for j, p in enumerate(probs) 
            if (p >= bin_lower and p < bin_upper) or (i == n_bins - 1 and p >= bin_lower and p <= bin_upper)
        ]
        
        if len(in_bin) > 0:
            bin_acc = np.mean([labels[j] for j in in_bin])
            bin_conf = np.mean([probs[j] for j in in_bin])
            bin_weight = len(in_bin) / n
            ece += bin_weight * abs(bin_acc - bin_conf)

    return float(ece)


def run_mini_benchmark():
    client = JevClient(api_key=API_KEY)
    
    # 模拟真实风控/工单流测试样本
    test_cases = [
        {
            "state": "User requested refund: Double billed on annual subscription invoice #9921",
            "ground_truth_team": "billing",
            "is_emergency": 0
        },
        {
            "state": "Database connection refused on production replica, 500 errors spiking",
            "ground_truth_team": "devops",
            "is_emergency": 1
        },
        {
            "state": "Typo in footer link to privacy policy",
            "ground_truth_team": "frontend",
            "is_emergency": 0
        },
        {
            "state": "Credit card processing gateway timed out, customer charged but order failed",
            "ground_truth_team": "billing",
            "is_emergency": 1
        }
    ]

    questions = {
        "team": Choice(
            instructions="Target team to handle this:",
            criteria={
                "billing": "Financial charges, invoices, refunds",
                "devops": "Server infrastructure, database, production outages",
                "frontend": "UI bugs, visual layout, copywriting"
            }
        ),
        "emergency": Noul(
            instructions="Is this an urgent production emergency requiring immediate paging?"
        )
    }

    print(f"Running validation benchmark on {len(test_cases)} sample cases...")
    latencies = []
    choice_correct = []
    noul_probs = []
    noul_labels = []

    for idx, case in enumerate(test_cases):
        t0 = time.time()
        res = client.decide(case["state"], questions)
        elapsed = (time.time() - t0) * 1000
        latencies.append(elapsed)

        pred_choice = res["answers"]["team"]["choice"]
        pred_conf = res["answers"]["team"]["confidence"]
        is_choice_corr = 1 if pred_choice == case["ground_truth_team"] else 0
        choice_correct.append(is_choice_corr)

        pred_noul = res["answers"]["emergency"]["noul"]
        noul_probs.append(pred_noul)
        noul_labels.append(case["is_emergency"])

        print(f"Sample {idx+1}: Latency={elapsed:.1f}ms | Pred Team={pred_choice} (Corr: {is_choice_corr}) | Urgent Prob={pred_noul:.2f} (True: {case['is_emergency']})")

    # Metrics
    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    accuracy = np.mean(choice_correct) * 100
    ece = compute_ece(noul_probs, noul_labels, n_bins=5)

    print("\n" + "=" * 50)
    print("Benchmark Results Summary:")
    print(f"- Choice Accuracy: {accuracy:.1f}%")
    print(f"- Mean Latency: {avg_latency:.1f} ms | P95: {p95_latency:.1f} ms")
    print(f"- Noul Expected Calibration Error (ECE): {ece:.4f}")
    print("=" * 50)


if __name__ == "__main__":
    run_mini_benchmark()
