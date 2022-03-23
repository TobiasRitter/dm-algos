from math import exp, sqrt, pi

Distribution = Tuple[float, float, float]
DECIMALS = 3


def normal_dist(x: float, dist: Distribution):
    mu, sigma, p = dist
    return p / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2 / (2 * sigma**2)))


def estimate(x: float, dist: Distribution, distributions: List[Distribution]) -> float:
    prob = normal_dist(x, dist)
    norm = sum([normal_dist(x, d) for d in distributions])
    return prob / norm


def maximize(points: List[float], estimates: List[float]) -> Distribution:
    assignments = list(zip(points, estimates))
    mu = sum([prob * point for point, prob in assignments]) / sum(estimates)
    sigma = sqrt(
        sum([prob * (point - mu) ** 2 for point, prob in assignments]) / sum(estimates)
    )
    p = 0 if len(estimates) == 0 else sum(estimates) / len(estimates)
    return (mu, sigma, p)


def pretty_print(
    iteration: int,
    clusters: Dict[Distribution, List[float]],
    points: List[float],
    distributions: List[Distribution],
):
    print(f"step {iteration}:")
    print("clusters:")
    for dist, ps in clusters.items():
        mu, sigma, p = dist
        print(
            f"({round(mu,DECIMALS)}, {round(sigma,DECIMALS)}, {round(p,DECIMALS)}) : {ps}"
        )

    print("probabilities:")
    for dist in distributions:
        mu, sigma, p = dist
        probs = [
            round(estimate(point, dist, distributions), DECIMALS) for point in points
        ]
        print(
            f"({round(mu,DECIMALS)},{round(sigma,DECIMALS)},{round(p,DECIMALS)}) : {probs}"
        )
    print("")


def get_dist_assignments(
    point: float, distributions: List[Distribution]
) -> Tuple[float, Distribution]:
    estimates = {dist: estimate(point, dist, distributions) for dist in distributions}
    best_dist = max(estimates, key=estimates.get)
    return (point, best_dist)


def get_clusters(
    points: List[float], distributions: List[Distribution]
) -> Dict[Distribution, List[float]]:
    assignments = [get_dist_assignments(point, distributions) for point in points]
    clusters = {dist: [] for dist in distributions}

    for point, dist in assignments:
        clusters[dist] += [point]

    return clusters


def em(
    points: List[float],
    distributions: List[Distribution],
    iteration: int = 1,
    groups: List[List[float]] = [],
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
