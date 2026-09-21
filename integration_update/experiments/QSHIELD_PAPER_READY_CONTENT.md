# Q-SHIELD: A Dual-Signal Framework for Quantum Attack Detection Under Heterogeneous Quantum Noise

## Abstract

Quantum communication systems are vulnerable to both adversarial
disturbances and legitimate quantum channel noise, making reliable
attack detection challenging. Conventional threshold-based detection
can generate false alarms when channel conditions vary. This work
presents Q-SHIELD, a dual-signal quantum attack detection framework
that combines teleportation mismatch information with Bell measurement
distribution anomaly analysis.

The framework is evaluated under heterogeneous quantum noise models,
multiple adversarial attack scenarios, threshold sensitivity analysis,
baseline comparison, reproducibility experiments, computational
complexity evaluation, and statistical significance testing. The best
balanced configuration achieved an accuracy of 0.9583,
precision of 1.0000, recall of 0.7500, F1 score of
0.8571, and false-positive rate of 0.0000 at a detection
threshold of 0.25.

The dual-signal architecture demonstrated improved performance compared
with individual detection signals. Independent random-seed experiments
showed a mean F1 score improvement from 0.4703 for
mismatch-only detection to 0.6463 for dual-signal detection,
corresponding to an improvement of 0.1760. The observed
improvement was associated with a large effect size
(Cohen's d = 5.5290) within the evaluated simulation
environment.

The results indicate that combining complementary quantum security
signals can improve attack detection reliability while reducing
false-positive decisions under heterogeneous noise conditions.
The findings are limited to simulated quantum circuits and implemented
noise and attack models, motivating future validation on real quantum
hardware.

## Keywords

Quantum Security, Quantum Attack Detection, Quantum Communication, Quantum Noise, Teleportation, Bell Measurement, Anomaly Detection, Adaptive Thresholding

## Main Contributions

1. A dual-signal quantum attack detection architecture combining teleportation mismatch and Bell measurement anomaly information.
2. Experimental evaluation under heterogeneous quantum noise and multiple adversarial attack scenarios.
3. Ablation analysis demonstrating the benefit of combining complementary quantum security signals.
4. Security-sensitivity analysis quantifying the trade-off between false-positive suppression and attack recall.
5. Independent random-seed reproducibility and statistical significance validation of the dual-signal performance improvement.
6. Computational complexity analysis showing that adaptive detection decisions maintain constant-time complexity.

## Final Conclusion

This research introduced Q-SHIELD, a dual-signal framework for quantum
attack detection under heterogeneous quantum channel noise. The framework
integrates teleportation mismatch information and Bell measurement
distribution anomaly analysis to distinguish adversarial disturbances
from legitimate channel variations.

The experimental evaluation showed that the best balanced configuration,
using a detection threshold of 0.25, achieved an accuracy of
0.9583, an F1 score of 0.8571, and a false-positive rate
of 0.0000. Ablation experiments demonstrated that the combined
dual-signal architecture provides a stronger overall balance of detection
performance and false-positive suppression than the individual signals.

Independent random-seed experiments further demonstrated an F1 score
improvement of 0.1760 compared with mismatch-only detection,
with a large observed effect size of Cohen's d = 5.5290. These
results provide statistically supported evidence that multi-signal fusion
can improve quantum attack detection performance within the implemented
simulation environment.

The study also demonstrates that detection threshold selection represents
an important security-sensitivity trade-off. While stronger thresholds
can suppress false alarms, they may reduce attack recall. Therefore,
threshold configuration should be selected according to operational
security requirements.

The current findings are limited to simulated quantum circuits and the
implemented noise and attack models. Future work should validate the
framework on real quantum hardware, larger quantum communication systems,
and additional adversarial strategies.

## Scientifically Supported Claims

### Dual-signal fusion improves overall detection performance.

**Evidence:** Supported by ablation experiments and independent statistical analysis.

**Status:** Experimentally Supported

### Q-SHIELD suppresses false-positive decisions under evaluated noisy conditions.

**Evidence:** Supported by threshold sensitivity and dual-signal evaluation experiments.

**Status:** Supported Within Simulation Scope

### Adaptive decision mechanisms preserve constant-time asymptotic complexity.

**Evidence:** Supported by computational complexity analysis.

**Status:** Experimentally Supported

### Q-SHIELD is universally superior to all quantum security systems.

**Evidence:** Not evaluated against all possible systems and datasets.

**Status:** Do Not Claim

### Q-SHIELD is validated on real quantum hardware.

**Evidence:** Current experiments are simulation based.

**Status:** Do Not Claim

