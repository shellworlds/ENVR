import math


def hadamard_probability(theta: float) -> float:
    amp = math.cos(theta / 2)
    return amp * amp


def grover_iteration_count(space_size: int) -> int:
    return max(1, int((math.pi / 4) * math.sqrt(space_size)))


if __name__ == "__main__":
    print({
        "h_prob_theta_1.2": round(hadamard_probability(1.2), 6),
        "grover_n1024": grover_iteration_count(1024),
    })
