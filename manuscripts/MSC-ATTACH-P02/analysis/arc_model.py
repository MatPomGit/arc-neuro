"""Core Attachment Regulation and Control (ARC) simulator.

The simulator mirrors variables that can later be measured in humans:
current relational state r_t, desired state r*_t, discrepancy e_t, signed
regulatory action u_t, and partner/context responsiveness b_t.

The P/PI/PID controller family is a falsifiable candidate model. Controller
coefficients are dynamic parameters, not psychological questionnaire scores.
No simulator output is a validated probability of attachment disorganization.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import math
from typing import Iterable, Literal

import numpy as np


MODEL_VERSION = "0.4.0"
STRATEGY_NAMES = ("secure", "hyperactivation", "deactivation")
ControllerMode = Literal["p", "pi", "pid"]


def clip01(value: float) -> float:
    return float(np.clip(value, 0.0, 1.0))


def softmax(values: Iterable[float], temperature: float) -> np.ndarray:
    z = np.asarray(tuple(values), dtype=float) / max(float(temperature), 1e-8)
    z -= np.max(z)
    exp_z = np.exp(z)
    return exp_z / exp_z.sum()


@dataclass(frozen=True)
class ARCTraits:
    """Normalized person-level constructs used to generate synthetic data.

    L: attachment anxiety / hyperactivation bias
    U: attachment avoidance / deactivation bias
    C: relational-control propensity
    S: secure-base confidence
    M: mentalized affectivity
    F: emotion-regulation flexibility

    In human analyses these constructs should remain on their validated native
    scales or be modeled as latent variables. [0, 1] is simulation-only.
    """

    L: float = 0.20
    U: float = 0.20
    C: float = 0.30
    S: float = 0.80
    M: float = 0.80
    F: float = 0.80

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1], got {value}.")


@dataclass(frozen=True)
class ControllerGains:
    """Dynamical controller coefficients.

    These parameters are intended to be estimated from repeated human data.
    """

    kp: float
    ki: float = 0.0
    kd: float = 0.0
    integral_leak: float = 0.85

    def __post_init__(self) -> None:
        if not 0.0 <= self.integral_leak <= 1.0:
            raise ValueError("integral_leak must be in [0, 1]")

    def for_mode(self, mode: ControllerMode) -> tuple[float, float, float]:
        if mode == "p":
            return self.kp, 0.0, 0.0
        if mode == "pi":
            return self.kp, self.ki, 0.0
        if mode == "pid":
            return self.kp, self.ki, self.kd
        raise ValueError(f"Unsupported controller mode: {mode}")


@dataclass(frozen=True)
class ARCConfig:
    """Simulation-level parameters, all explicitly reportable."""

    steps: int = 200
    dt: float = 1.0
    responsiveness: float = 0.80
    process_noise: float = 0.004
    perception_noise: float = 0.08
    temperature: float = 0.35
    max_action: float = 0.40
    controller_mode: ControllerMode = "pid"

    # Synthetic mapping C -> controller gains. This is a hypothesis to test.
    kp_min: float = 0.20
    kp_control_scale: float = 0.85
    ki_control_scale: float = 0.24
    kd_control_scale: float = 0.10
    integral_leak: float = 0.85

    # Flexible gain adaptation after threat and ineffective previous action.
    threat_gain: float = 0.20
    feedback_gain: float = 0.35
    opposing_policy_weight: float = 0.25

    recovery_window: int = 12
    settle_threshold: float = 0.04
    settle_hold: int = 4
    overshoot_tolerance: float = 0.04

    # Simulation-only instability index weights. External Z remains separate.
    instability_conflict_weight: float = 0.25
    instability_entropy_weight: float = 0.25
    instability_overshoot_weight: float = 0.20
    instability_inefficacy_weight: float = 0.20
    instability_auc_weight: float = 0.10

    def __post_init__(self) -> None:
        if self.steps < 10:
            raise ValueError("steps must be >= 10")
        if self.dt <= 0:
            raise ValueError("dt must be > 0")
        if self.responsiveness <= 0:
            raise ValueError("responsiveness must be > 0")
        if self.temperature <= 0:
            raise ValueError("temperature must be > 0")
        if self.controller_mode not in ("p", "pi", "pid"):
            raise ValueError("controller_mode must be p, pi, or pid")


@dataclass
class SimulationResult:
    traits: ARCTraits
    config: ARCConfig
    gains: ControllerGains
    target_state: np.ndarray
    perturbation: np.ndarray
    intervals: np.ndarray
    series: dict[str, np.ndarray]
    metrics: dict[str, float]
    regime: str

    def to_csv(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        keys = list(self.series.keys())
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(keys)
            writer.writerows(zip(*(self.series[key] for key in keys)))


def gains_from_control(traits: ARCTraits, config: ARCConfig) -> ControllerGains:
    """Synthetic hypothesis mapping relational-control propensity to gains."""

    return ControllerGains(
        kp=config.kp_min + config.kp_control_scale * traits.C,
        ki=config.ki_control_scale * traits.C,
        kd=config.kd_control_scale * traits.C,
        integral_leak=config.integral_leak,
    )


def default_target_state(traits: ARCTraits) -> float:
    """Synthetic default target used only when no target trajectory is supplied.

    Human analyses should measure r*_t directly. This formula is not the
    operational definition of a person's desired relational state.
    """

    return clip01(0.50 + 0.25 * (traits.L - traits.U))


def constant_target(traits: ARCTraits, config: ARCConfig) -> np.ndarray:
    return np.full(config.steps, default_target_state(traits), dtype=float)


def impulse(config: ARCConfig, step: int = 60, magnitude: float = -0.30) -> np.ndarray:
    values = np.zeros(config.steps, dtype=float)
    if not 0 <= step < config.steps:
        raise ValueError("step outside simulation range")
    values[step] = magnitude
    return values


def box_perturbation(
    config: ARCConfig,
    start: int = 60,
    duration: int = 5,
    total_magnitude: float = -0.30,
) -> np.ndarray:
    values = np.zeros(config.steps, dtype=float)
    if duration <= 0:
        raise ValueError("duration must be > 0")
    if start < 0 or start >= config.steps:
        raise ValueError("start outside simulation range")
    stop = min(config.steps, start + duration)
    values[start:stop] = total_magnitude / max(stop - start, 1)
    return values


def residual_strategy_entropy(
    strategies: np.ndarray,
    error: np.ndarray,
    threshold: float = 0.08,
) -> float:
    """H(X[t+1] | X[t], discrepancy-bin), normalized to [0, 1]."""

    bins = np.where(error > threshold, 1, np.where(error < -threshold, -1, 0))
    counts: dict[tuple[int, int], np.ndarray] = {}

    for index in range(len(strategies) - 1):
        key = (int(strategies[index]), int(bins[index]))
        counts.setdefault(key, np.zeros(3, dtype=int))
        counts[key][int(strategies[index + 1])] += 1

    weighted_entropy = 0.0
    total_weight = 0
    for count in counts.values():
        n = int(count.sum())
        if n < 2:
            continue
        probability = count[count > 0] / n
        entropy = float(-(probability * np.log(probability)).sum() / math.log(3))
        weighted_entropy += n * entropy
        total_weight += n

    return weighted_entropy / total_weight if total_weight else 0.0


def estimate_recovery_rate(error: np.ndarray, start: int, window: int, times: np.ndarray | None = None) -> float:
    """Approximate exponential decay rate; positive values indicate recovery."""

    values = np.abs(error[start : min(len(error), start + window)])
    x = np.arange(len(values), dtype=float) if times is None else times[start : start + len(values)]
    mask = values > 1e-4
    if int(mask.sum()) < 3:
        return float("nan")
    slope = np.polyfit(x[mask], np.log(values[mask]), 1)[0]
    return float(-slope)


def settling_time(
    error: np.ndarray,
    start: int,
    threshold: float,
    hold: int,
    times: np.ndarray | None = None,
) -> float:
    absolute_error = np.abs(error)
    for index in range(start, max(start, len(error) - hold + 1)):
        if np.all(absolute_error[index : index + hold] < threshold):
            return float(index - start if times is None else times[index] - times[start])
    return float("nan")


def classify_regime(result: SimulationResult) -> str:
    """Simulation labels only; not psychological or diagnostic cutoffs."""

    m = result.metrics
    p_secure = m["mean_pi_secure"]

    if (
        m["mean_regulatory_efficacy"] > 0.0
        and m["residual_entropy"] < 0.45
        and m["overshoot_rate"] < 0.15
        and p_secure >= 0.45
    ):
        return "secure-like"

    if (
        m["arc_instability_index"] >= 0.58
        or m["mean_regulatory_efficacy"] < -0.005
    ):
        return "unstable"

    if result.traits.C >= 0.65 and m["mean_regulatory_efficacy"] > 0:
        return "control-dependent"

    if (
        m["mean_pi_hyperactivation"] > m["mean_pi_deactivation"]
        and m["mean_pi_hyperactivation"] > p_secure
    ):
        return "organized-anxious"

    if (
        m["mean_pi_deactivation"] > m["mean_pi_hyperactivation"]
        and m["mean_pi_deactivation"] > p_secure
    ):
        return "organized-avoidant"

    return "integrated-mixed"


def simulate(
    traits: ARCTraits | None = None,
    config: ARCConfig | None = None,
    perturbation: np.ndarray | None = None,
    target_state: np.ndarray | None = None,
    gains: ControllerGains | None = None,
    seed: int = 42,
    initial_state: float | None = None,
    intervals: np.ndarray | None = None,
) -> SimulationResult:
    """Run one ARC trajectory; intervals[t] is the duration of step t."""

    traits = traits or ARCTraits()
    config = config or ARCConfig()
    gains = gains or gains_from_control(traits, config)

    if perturbation is None:
        perturbation = np.zeros(config.steps, dtype=float)
    perturbation = np.asarray(perturbation, dtype=float)
    if len(perturbation) != config.steps:
        raise ValueError("perturbation length must equal config.steps")

    if target_state is None:
        target_state = constant_target(traits, config)
    target_state = np.asarray(target_state, dtype=float)
    if len(target_state) != config.steps:
        raise ValueError("target_state length must equal config.steps")
    if intervals is None:
        intervals = np.full(config.steps, config.dt, dtype=float)
    intervals = np.asarray(intervals, dtype=float)
    if intervals.shape != (config.steps,) or not np.all(np.isfinite(intervals)) or np.any(intervals <= 0):
        raise ValueError("intervals must contain one finite positive duration per step")
    if not np.all(np.isfinite(target_state)) or np.any((target_state < 0) | (target_state > 1)):
        raise ValueError("target_state must contain finite values in [0, 1]")
    if not np.all(np.isfinite(perturbation)):
        raise ValueError("perturbation must contain finite values")

    rng = np.random.default_rng(seed)
    relation_state = (
        float(target_state[0]) if initial_state is None else clip01(initial_state)
    )

    keys = (
        "time",
        "dt",
        "target_state",
        "relation_state",
        "true_error",
        "estimated_state",
        "estimated_error",
        "p_term",
        "i_term",
        "d_term",
        "kp_effective",
        "ki_effective",
        "kd_effective",
        "pi_secure",
        "pi_hyperactivation",
        "pi_deactivation",
        "strategy_conflict",
        "strategy_entropy",
        "policy_alignment",
        "raw_control",
        "action",
        "next_error",
        "regulatory_efficacy",
        "fixed_target_efficacy",
        "action_effect_oracle",
        "target_change",
        "overshoot",
        "strategy",
    )
    history: dict[str, list[float]] = {key: [] for key in keys}

    integral_error = 0.0
    previous_estimated_error = 0.0
    previous_efficacy = 0.0
    elapsed = 0.0

    base_kp, base_ki, base_kd = gains.for_mode(config.controller_mode)

    for time in range(config.steps):
        interval = float(intervals[time])
        target = float(target_state[time])
        true_error = target - relation_state

        perception_sigma = config.perception_noise * (1.0 - traits.M)
        estimated_state = clip01(
            relation_state + rng.normal(0.0, perception_sigma)
        )
        estimated_error = target - estimated_state

        p_term = estimated_error
        integral_error = (
            gains.integral_leak ** (interval / config.dt) * integral_error
            + estimated_error * interval
        )
        d_term = (
            0.0
            if time == 0
            else (estimated_error - previous_estimated_error) / interval
        )

        threat = min(1.0, 2.0 * abs(estimated_error))
        habitual = np.array([traits.S, traits.L, traits.U], dtype=float)
        contextual = np.array(
            [
                traits.S + 0.45 * (1.0 - threat),
                traits.L + 1.50 * max(estimated_error, 0.0),
                traits.U + 1.50 * max(-estimated_error, 0.0),
            ],
            dtype=float,
        )
        utilities = (1.0 - traits.F) * habitual + traits.F * contextual
        probabilities = softmax(utilities, config.temperature)

        negative_feedback = max(-previous_efficacy, 0.0)
        gain_modifier = max(
            0.20,
            1.0
            + traits.F * config.threat_gain * threat
            - traits.F * config.feedback_gain * negative_feedback,
        )
        kp_effective = base_kp * gain_modifier
        ki_effective = base_ki * gain_modifier
        kd_effective = base_kd * gain_modifier

        raw_control = (
            kp_effective * p_term
            + ki_effective * integral_error
            + kd_effective * d_term
        )

        if estimated_error >= 0:
            policy_alignment = (
                probabilities[0]
                + probabilities[1]
                - config.opposing_policy_weight * probabilities[2]
            )
        else:
            policy_alignment = (
                probabilities[0]
                + probabilities[2]
                - config.opposing_policy_weight * probabilities[1]
            )

        action = float(
            np.clip(
                policy_alignment * raw_control,
                -config.max_action,
                config.max_action,
            )
        )

        disturbance = perturbation[time] + rng.normal(0.0, config.process_noise)
        next_state = clip01(
            relation_state
            + config.responsiveness * action
            + disturbance
        )
        no_action_state = clip01(relation_state + disturbance)
        next_target = float(
            target_state[min(time + 1, config.steps - 1)]
        )
        next_error = next_target - next_state

        efficacy = abs(true_error) - abs(next_error)
        fixed_target_efficacy = abs(true_error) - abs(target - next_state)
        action_effect_oracle = abs(target - no_action_state) - abs(target - next_state)
        overshoot = float(
            true_error * next_error < 0
            and abs(next_error) > config.overshoot_tolerance
        )

        conflict = float(4.0 * probabilities[1] * probabilities[2])
        strategy_entropy = float(
            -(probabilities * np.log(probabilities + 1e-12)).sum()
            / math.log(3)
        )
        strategy = int(rng.choice(3, p=probabilities))

        values = (
            elapsed,
            interval,
            target,
            relation_state,
            true_error,
            estimated_state,
            estimated_error,
            p_term,
            integral_error,
            d_term,
            kp_effective,
            ki_effective,
            kd_effective,
            probabilities[0],
            probabilities[1],
            probabilities[2],
            conflict,
            strategy_entropy,
            policy_alignment,
            raw_control,
            action,
            next_error,
            efficacy,
            fixed_target_efficacy,
            action_effect_oracle,
            next_target - target,
            overshoot,
            strategy,
        )
        for key, value in zip(keys, values):
            history[key].append(float(value))

        elapsed += interval
        relation_state = next_state
        previous_estimated_error = estimated_error
        previous_efficacy = efficacy

    series = {key: np.asarray(values) for key, values in history.items()}

    if np.any(perturbation):
        shock_index = int(np.argmax(np.abs(perturbation)))
        recovery_start = min(shock_index + 1, config.steps - 1)
    else:
        recovery_start = 0

    error = series["true_error"]
    auc_error = float(np.sum(np.abs(error[recovery_start:]) * intervals[recovery_start:]))
    auc_norm = auc_error / max(
        float(np.sum(intervals[recovery_start:])),
        1e-8,
    )
    ineffective_fraction = float(
        np.mean(series["regulatory_efficacy"] < 0.0)
    )
    residual_entropy = residual_strategy_entropy(
        series["strategy"].astype(int),
        error,
    )
    overshoot_rate = float(np.mean(series["overshoot"]))
    mean_conflict = float(np.mean(series["strategy_conflict"]))

    w = config
    instability_index = float(
        np.clip(
            w.instability_conflict_weight * mean_conflict
            + w.instability_entropy_weight * residual_entropy
            + w.instability_overshoot_weight * overshoot_rate
            + w.instability_inefficacy_weight * ineffective_fraction
            + w.instability_auc_weight * min(1.0, auc_norm),
            0.0,
            1.0,
        )
    )

    metrics = {
        "kappa": estimate_recovery_rate(
            error,
            recovery_start,
            config.recovery_window,
            series["time"],
        ),
        "settling_time": settling_time(
            error,
            recovery_start,
            config.settle_threshold,
            config.settle_hold,
            series["time"],
        ),
        "error_auc": auc_error,
        "mean_regulatory_efficacy": float(
            np.mean(series["regulatory_efficacy"])
        ),
        "mean_fixed_target_efficacy": float(np.mean(series["fixed_target_efficacy"])),
        "mean_action_effect_oracle": float(np.mean(series["action_effect_oracle"])),
        "ineffective_fraction": ineffective_fraction,
        "overshoot_rate": overshoot_rate,
        "mean_strategy_conflict": mean_conflict,
        "residual_entropy": residual_entropy,
        "mean_strategy_entropy": float(
            np.mean(series["strategy_entropy"])
        ),
        "mean_kp": float(np.mean(series["kp_effective"])),
        "mean_ki": float(np.mean(series["ki_effective"])),
        "mean_kd": float(np.mean(series["kd_effective"])),
        "mean_pi_secure": float(np.mean(series["pi_secure"])),
        "mean_pi_hyperactivation": float(
            np.mean(series["pi_hyperactivation"])
        ),
        "mean_pi_deactivation": float(
            np.mean(series["pi_deactivation"])
        ),
        "arc_instability_index": instability_index,
    }

    result = SimulationResult(
        traits=traits,
        config=config,
        gains=gains,
        target_state=target_state,
        perturbation=perturbation,
        intervals=intervals,
        series=series,
        metrics=metrics,
        regime="unclassified",
    )
    result.regime = classify_regime(result)
    return result
