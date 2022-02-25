from math import exp, sqrt, pi

Distribution = tuple[float, float, float]


def pretty_print(clusters: dict[Distribution, list[float]], iteration: int):
    print(f"step {iteration}:")
    for k, v in clusters.items():
        print(k, ":", v)


def estimate(x: float, dist: Distribution):
    mu, sigma, p = dist
    return p / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2 / (2 * sigma**2)))


def normed_estimate(x: float, dist: Distribution, dists: list[Distribution]) -> float:
    prob = estimate(x, dist)
    norm = sum([estimate(x, d) for d in dists])
    return prob / norm


def maximize(points: list[float], estimates: list[float]) -> Distribution:
    assignments = list(zip(points, estimates))
    mu = sum([prob * point for point, prob in assignments]) / sum(estimates)
    sigma = sqrt(
        sum([prob * (point - mu) ** 2 for point, prob in assignments]) / sum(estimates)
    )
    p = 0 if len(estimates) == 0 else sum(estimates) / len(estimates)
    return (mu, sigma, p)


def get_prob(point: float, dists: list[Distribution]) -> tuple[float, Distribution]:
    estimates = {dist: normed_estimate(point, dist, dists) for dist in dists}
    best_dist = max(estimates, key=estimates.get)
    return (point, best_dist)


def get_clusters(
    points: list[float], dists: list[Distribution]
) -> dict[Distribution, list[float]]:
    assignments = [get_prob(point, dists) for point in points]
    clusters = {dist: [] for dist in dists}

    for point, dist in assignments:
        clusters[dist] += [point]

    return clusters


def em(points: list[float], dists: list[Distribution], iteration: int):
    # assign to points to clusters
    clusters = get_clusters(points, dists)
    pretty_print(clusters, iteration)

    # update distributions
    new_dists = []
    for dist in dists:
        estimates = [normed_estimate(point, dist, dists) for point in points]
        new_dists += [maximize(points, estimates)]

    return dists if new_dists == dists else em(points, new_dists, iteration + 1)


def main():
    data_points = [0.76, 0.86, 1.12, 3.05, 3.51, 3.75]
    dists = [(1.12, 1, 0.5), (3.05, 1, 0.5)]
    em(data_points, dists, 1)


if __name__ == "__main__":
    main()
