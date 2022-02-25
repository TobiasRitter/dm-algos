from statistics import mean as avg
from math import sqrt


def pretty_print(iteration: int, clusters) -> None:
    print(f"step {iteration}:")
    for k, v in clusters.items():
        print(k, ":", v)


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def get_mean(points: list[tuple[float, float]]) -> tuple[float, float]:
    return (avg(map(lambda x: x[0], points)), avg(map(lambda x: x[1], points)))


def get_closest_mean(point, means) -> tuple[float, float]:
    distances = {mean: distance(mean, point) for mean in means}
    return min(distances, key=distances.get)


def kmeans(data_points, means, iteration: int):
    clusters = {mean: [] for mean in means}

    for point in data_points:
        mean = get_closest_mean(point, means)
        clusters[mean] += [point]

    pretty_print(iteration, clusters)
    new_means = [get_mean(point_group) for point_group in clusters.values()]
    return (
        means if new_means == means else kmeans(data_points, new_means, iteration + 1)
    )


def main() -> None:
    data_points = [
        (2.5, 3),
        (3, 3),
        (2, 2.75),
        (2.5, 2.5),
        (3, 2.5),
        (0.5, 1),
        (1, 1),
        (3, 1),
        (3.75, 1),
        (0.75, 0.75),
        (1, 0.5),
        (3.5, 0.5),
    ]
    means = [(0.5, 2.5), (5, 2.5), (4.5, 0.5)]
    kmeans(data_points, means, 1)


if __name__ == "__main__":
    main()
