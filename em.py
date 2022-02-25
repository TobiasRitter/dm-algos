from math import exp, sqrt, pi
from re import S


Distribution = tuple[float, float, float]
Assignment = tuple[float, float]


def pretty_print(
    clusters: dict[Distribution, list[Assignment]], iteration: int
) -> None:
    print(f"step {iteration}:")
    for k, assignments in clusters.items():
        points = list(map(lambda x: x[0], assignments))
        print(k, ":", points)


def estimate(x: float, dist: Distribution) -> float:
    mu, sigma, p = dist
    return p / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2 / (2 * sigma**2)))


def maximize(dist: Distribution, assignments: list[Assignment]) -> Distribution:
    probs = list(map(lambda x: x[1], assignments))
    mu = sum([prob * point for point, prob in assignments]) / sum(probs)
    sigma = sqrt(
        sum([prob * (point - mu) ** 2 for point, prob in assignments]) / sum(probs)
    )
    p = 0 if len(probs) == 0 else sum(probs) / len(probs)
    return (mu, sigma, p)


def get_prob(
    point: float, dists: list[Distribution]
) -> tuple[float, Distribution, float]:
    norm = sum([estimate(point, dist) for dist in dists])
    estimates = {dist: estimate(point, dist) for dist in dists}
    best_dist = max(estimates, key=estimates.get)
    best_estimate = max(estimates.values()) / norm
    return (point, best_dist, best_estimate)


def get_clusters(
    points: list[float], dists: list[Distribution]
) -> dict[Distribution, list[Assignment]]:
    estimates = [get_prob(point, dists) for point in points]
    clusters = {dist: [] for dist in dists}

    for point, dist, estimate in estimates:
        clusters[dist] += [(point, estimate)]

    return clusters


def em(points: list[float], dists: list[Distribution], iteration: int):
    clusters = get_clusters(points, dists)
    new_dists = []

    pretty_print(clusters, iteration)

    # update distributions
    for dist, assignments in clusters.items():
        new_dists += [maximize(dist, assignments)]

    return dists if new_dists == dists else em(points, new_dists, iteration + 1)


def main():
    data_points = [0.76, 0.86, 1.12, 3.05, 3.51, 3.75]
    dists = [(1.12, 1, 0.5), (3.05, 1, 0.5)]
    em(data_points, dists, 1)


if __name__ == "__main__":
    main()
