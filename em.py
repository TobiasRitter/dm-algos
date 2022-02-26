from math import exp, sqrt, pi

Distribution = tuple[float, float, float]


def normal_dist(x: float, dist: Distribution):
    mu, sigma, p = dist
    return p / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2 / (2 * sigma**2)))


def estimate(x: float, dist: Distribution, distributions: list[Distribution]) -> float:
    prob = normal_dist(x, dist)
    norm = sum([normal_dist(x, d) for d in distributions])
    return prob / norm


def maximize(points: list[float], estimates: list[float]) -> Distribution:
    assignments = list(zip(points, estimates))
    mu = sum([prob * point for point, prob in assignments]) / sum(estimates)
    sigma = sqrt(
        sum([prob * (point - mu) ** 2 for point, prob in assignments]) / sum(estimates)
    )
    p = 0 if len(estimates) == 0 else sum(estimates) / len(estimates)
    return (mu, sigma, p)


def pretty_print(
    iteration: int,
    clusters: dict[Distribution, list[float]],
    points: list[float],
    distributions: list[Distribution],
    decimals: int = 3,
):
    print(f"step {iteration}:")
    print("clusters:")
    for dist, ps in clusters.items():
        mu, sigma, p = dist
        print(
            f"({round(mu,decimals)}, {round(sigma,decimals)}, {round(p,decimals)}) : {ps}"
        )

    print("probabilities:")
    for dist in distributions:
        mu, sigma, p = dist
        probs = [
            round(estimate(point, dist, distributions), decimals) for point in points
        ]
        print(
            f"({round(mu,decimals)},{round(sigma,decimals)},{round(p,decimals)}) : {probs}"
        )
    print("")


def get_dist_assignments(
    point: float, distributions: list[Distribution]
) -> tuple[float, Distribution]:
    estimates = {dist: estimate(point, dist, distributions) for dist in distributions}
    best_dist = max(estimates, key=estimates.get)
    return (point, best_dist)


def get_clusters(
    points: list[float], distributions: list[Distribution]
) -> dict[Distribution, list[float]]:
    assignments = [get_dist_assignments(point, distributions) for point in points]
    clusters = {dist: [] for dist in distributions}

    for point, dist in assignments:
        clusters[dist] += [point]

    return clusters


def em(
    points: list[float],
    distributions: list[Distribution],
    iteration: int = 1,
    groups: list[list[float]] = [],
):
    # assign to points to clusters
    clusters = get_clusters(points, distributions)
    new_groups = list(clusters.values())
    pretty_print(iteration, clusters, points, distributions)

    # update distributions
    new_distributions = []
    for dist in distributions:
        estimates = [estimate(point, dist, distributions) for point in points]
        new_distributions += [maximize(points, estimates)]

    return (
        distributions
        if new_groups == groups
        else em(points, new_distributions, iteration + 1, new_groups)
    )


def main():
    data_points = []
    distributions = []  # (mu, sigma, p)
    em(data_points, distributions)


if __name__ == "__main__":
    main()
