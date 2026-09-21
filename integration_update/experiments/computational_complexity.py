"""
Q-SHIELD
PHASE 5B: COMPUTATIONAL COMPLEXITY AND SCALABILITY ANALYSIS

This experiment evaluates the computational overhead introduced by
blind adaptive thresholding compared with conventional fixed thresholding.

Evaluation dimensions:
1. Decision latency
2. Adaptive threshold computation overhead
3. Scalability with shot count
4. Scalability with number of probes
"""

import csv
import time
import statistics

import numpy as np

from qshield.quantum.teleportation import TeleportationEngine


# ================================================================
# CONFIGURATION
# ================================================================

FIXED_THRESHOLD = 0.26
BASE_THRESHOLD = 0.26
ADAPTATION_FACTOR = 0.4

BENCHMARK_ITERATIONS = 10000

SHOT_COUNTS = [
    128,
    256,
    512,
    1024,
    2048
]

PROBE_COUNTS = [
    10,
    25,
    50,
    100,
    200
]

QUANTUM_RUNS = 5


# ================================================================
# ADAPTIVE THRESHOLD FUNCTIONS
# ================================================================

def estimate_noise(mismatch_rate):
    """
    Blind channel disturbance estimation.

    The estimator uses only the observed mismatch rate
    and does not require knowledge of the true simulator
    noise probability.
    """

    return min(
        mismatch_rate * 1.5,
        0.50
    )


def adaptive_threshold(mismatch_rate):
    """
    Compute blind adaptive rejection threshold.
    """

    estimated_noise = estimate_noise(
        mismatch_rate
    )

    threshold = (
        BASE_THRESHOLD
        + ADAPTATION_FACTOR
        * estimated_noise
    )

    return min(
        threshold,
        0.46
    )


# ================================================================
# FIXED THRESHOLD BENCHMARK
# ================================================================

def benchmark_fixed_decision():

    mismatch_values = np.random.uniform(
        0,
        0.7,
        BENCHMARK_ITERATIONS
    )

    start_time = time.perf_counter()

    decisions = []

    for mismatch in mismatch_values:

        reject = mismatch > FIXED_THRESHOLD

        decisions.append(reject)

    end_time = time.perf_counter()

    total_time = (
        end_time - start_time
    )

    average_time = (
        total_time
        / BENCHMARK_ITERATIONS
    )

    return {
        "total_time": total_time,
        "average_time": average_time,
        "decisions": len(decisions)
    }


# ================================================================
# ADAPTIVE THRESHOLD BENCHMARK
# ================================================================

def benchmark_adaptive_decision():

    mismatch_values = np.random.uniform(
        0,
        0.7,
        BENCHMARK_ITERATIONS
    )

    start_time = time.perf_counter()

    decisions = []

    for mismatch in mismatch_values:

        threshold = adaptive_threshold(
            mismatch
        )

        reject = mismatch > threshold

        decisions.append(reject)

    end_time = time.perf_counter()

    total_time = (
        end_time - start_time
    )

    average_time = (
        total_time
        / BENCHMARK_ITERATIONS
    )

    return {
        "total_time": total_time,
        "average_time": average_time,
        "decisions": len(decisions)
    }


# ================================================================
# SHOT COUNT SCALABILITY
# ================================================================

def benchmark_shot_scalability():

    results = []

    print()
    print("-" * 95)
    print("SHOT COUNT SCALABILITY")
    print("-" * 95)

    for shots in SHOT_COUNTS:

        execution_times = []

        engine = TeleportationEngine(
            shots=shots
        )

        for _ in range(QUANTUM_RUNS):

            start_time = time.perf_counter()

            result = engine.run(
                bit=0,
                basis="Z",
                noise_type="depolarizing",
                noise_probability=0.10,
                attack_type="none"
            )

            end_time = time.perf_counter()

            execution_times.append(
                end_time - start_time
            )

        mean_time = statistics.mean(
            execution_times
        )

        std_time = statistics.stdev(
            execution_times
        ) if len(execution_times) > 1 else 0

        print(
            f"Shots={shots:<6} | "
            f"Mean Time={mean_time:.6f}s | "
            f"Std={std_time:.6f}s"
        )

        results.append({

            "shots": shots,

            "mean_execution_time":
                mean_time,

            "std_execution_time":
                std_time,

            "mean_mismatch":
                result["mismatch_rate"]

        })

    return results


# ================================================================
# PROBE COUNT SCALABILITY
# ================================================================

def benchmark_probe_scalability():

    results = []

    print()
    print("-" * 95)
    print("PROBE COUNT SCALABILITY")
    print("-" * 95)

    for probes in PROBE_COUNTS:

        mismatch_values = np.random.uniform(
            0,
            0.7,
            probes
        )

        # Fixed Threshold

        start_time = time.perf_counter()

        for mismatch in mismatch_values:

            _ = mismatch > FIXED_THRESHOLD

        fixed_time = (
            time.perf_counter()
            - start_time
        )

        # Adaptive Threshold

        start_time = time.perf_counter()

        for mismatch in mismatch_values:

            threshold = adaptive_threshold(
                mismatch
            )

            _ = mismatch > threshold

        adaptive_time = (
            time.perf_counter()
            - start_time
        )

        overhead = (
            adaptive_time / fixed_time
            if fixed_time > 0
            else 0
        )

        print(
            f"Probes={probes:<5} | "
            f"Fixed={fixed_time:.8f}s | "
            f"Adaptive={adaptive_time:.8f}s | "
            f"Overhead={overhead:.2f}x"
        )

        results.append({

            "probes": probes,

            "fixed_time":
                fixed_time,

            "adaptive_time":
                adaptive_time,

            "overhead_ratio":
                overhead

        })

    return results


# ================================================================
# COMPUTATIONAL COMPLEXITY ANALYSIS
# ================================================================

def complexity_analysis():

    return [

        {
            "component":
                "Fixed Threshold Decision",

            "time_complexity":
                "O(1)",

            "space_complexity":
                "O(1)",

            "description":
                "Single comparison between mismatch and fixed threshold."
        },

        {
            "component":
                "Noise Estimation",

            "time_complexity":
                "O(1)",

            "space_complexity":
                "O(1)",

            "description":
                "Constant-time estimation from observed mismatch."
        },

        {
            "component":
                "Adaptive Threshold Computation",

            "time_complexity":
                "O(1)",

            "space_complexity":
                "O(1)",

            "description":
                "Arithmetic adjustment of threshold based on estimated noise."
        },

        {
            "component":
                "N Probe Evaluation",

            "time_complexity":
                "O(N)",

            "space_complexity":
                "O(1)",

            "description":
                "Each probe requires independent constant-time decision."
        }

    ]


# ================================================================
# MAIN
# ================================================================

def main():

    print()
    print("=" * 100)
    print("Q-SHIELD")
    print("PHASE 5B: COMPUTATIONAL COMPLEXITY AND SCALABILITY ANALYSIS")
    print("=" * 100)

    print()
    print(f"Decision Benchmark Iterations: {BENCHMARK_ITERATIONS}")
    print(f"Quantum Runs per Shot Count: {QUANTUM_RUNS}")


    # ============================================================
    # DECISION LATENCY
    # ============================================================

    print()
    print("-" * 100)
    print("DECISION LATENCY BENCHMARK")
    print("-" * 100)

    fixed_result = benchmark_fixed_decision()

    adaptive_result = benchmark_adaptive_decision()

    overhead = (
        adaptive_result["average_time"]
        / fixed_result["average_time"]
    )

    print()
    print(
        f"Fixed Average Decision Time: "
        f"{fixed_result['average_time'] * 1e6:.4f} microseconds"
    )

    print(
        f"Adaptive Average Decision Time: "
        f"{adaptive_result['average_time'] * 1e6:.4f} microseconds"
    )

    print(
        f"Relative Computational Overhead: "
        f"{overhead:.2f}x"
    )


    # ============================================================
    # SHOT SCALABILITY
    # ============================================================

    shot_results = benchmark_shot_scalability()


    # ============================================================
    # PROBE SCALABILITY
    # ============================================================

    probe_results = benchmark_probe_scalability()


    # ============================================================
    # COMPLEXITY TABLE
    # ============================================================

    complexity_results = complexity_analysis()

    print()
    print("=" * 100)
    print("THEORETICAL COMPUTATIONAL COMPLEXITY")
    print("=" * 100)

    print()

    print(
        f"{'Component':<35}"
        f"{'Time':<15}"
        f"{'Space':<15}"
    )

    print("-" * 65)

    for item in complexity_results:

        print(
            f"{item['component']:<35}"
            f"{item['time_complexity']:<15}"
            f"{item['space_complexity']:<15}"
        )


    # ============================================================
    # SAVE DECISION BENCHMARK
    # ============================================================

    decision_rows = [

        {
            "method": "Fixed",

            "iterations":
                BENCHMARK_ITERATIONS,

            "total_time":
                fixed_result["total_time"],

            "average_time":
                fixed_result["average_time"]

        },

        {
            "method": "Blind Adaptive",

            "iterations":
                BENCHMARK_ITERATIONS,

            "total_time":
                adaptive_result["total_time"],

            "average_time":
                adaptive_result["average_time"]

        }

    ]

    with open(
        "experiments/computational_latency_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "method",
                "iterations",
                "total_time",
                "average_time"
            ]
        )

        writer.writeheader()

        writer.writerows(
            decision_rows
        )


    # ============================================================
    # SAVE SHOT RESULTS
    # ============================================================

    with open(
        "experiments/shot_scalability_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "shots",
                "mean_execution_time",
                "std_execution_time",
                "mean_mismatch"
            ]
        )

        writer.writeheader()

        writer.writerows(
            shot_results
        )


    # ============================================================
    # SAVE PROBE RESULTS
    # ============================================================

    with open(
        "experiments/probe_scalability_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "probes",
                "fixed_time",
                "adaptive_time",
                "overhead_ratio"
            ]
        )

        writer.writeheader()

        writer.writerows(
            probe_results
        )


    # ============================================================
    # SAVE COMPLEXITY RESULTS
    # ============================================================

    with open(
        "experiments/complexity_analysis.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "component",
                "time_complexity",
                "space_complexity",
                "description"
            ]
        )

        writer.writeheader()

        writer.writerows(
            complexity_results
        )


    # ============================================================
    # FINAL INTERPRETATION
    # ============================================================

    print()
    print("=" * 100)
    print("COMPUTATIONAL ANALYSIS CONCLUSION")
    print("=" * 100)

    print()

    print(
        "1. Fixed thresholding requires O(1) decision time."
    )

    print(
        "2. Blind adaptive thresholding also requires O(1) "
        "decision time."
    )

    print(
        "3. Adaptive thresholding introduces only constant-time "
        "arithmetic operations."
    )

    print(
        "4. System-level probe evaluation scales linearly O(N) "
        "with the number of probes."
    )

    print(
        "5. The adaptive method does not change the asymptotic "
        "computational complexity of the detection system."
    )

    print()
    print("Results saved:")

    print(
        "1. experiments/computational_latency_results.csv"
    )

    print(
        "2. experiments/shot_scalability_results.csv"
    )

    print(
        "3. experiments/probe_scalability_results.csv"
    )

    print(
        "4. experiments/complexity_analysis.csv"
    )

    print()
    print("=" * 100)
    print("PHASE 5B COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    main()