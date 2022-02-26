from statistics import mean as avg
from math import sqrt

Point = tuple[float, float]


def pretty_print(
    iteration: int,
    clusters: dict[Point, list[Point]],
    decimals: int = 3,
) -> None:
    print(f"step {iteration}:")
    for mean, points in clusters.items():
        x, y = mean
        print(f"({round(x,decimals)}, {round(y,decimals)}) : {points}", ":", points)


def distance(a: Point, b: Point) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def get_mean(points: list[Point]) -> Point:
    return (avg(map(lambda x: x[0], points)), avg(map(lambda x: x[1], points)))


def get_closest_mean(point: Point, means: list[Point]) -> Point:
    distances = {mean: distance(mean, point) for mean in means}
    return min(distances, key=distances.get)


def kmeans(
    data_points: list[Point],
    means: list[Point],
    iteration: int = 1,
) -> list[Point]:
    clusters: dict[Point, list[Point]] = {mean: [] for mean in means}

    for point in data_points:
        mean = get_closest_mean(point, means)
        clusters[mean] += [point]

    pretty_print(iteration, clusters)
    new_means = [get_mean(point_group) for point_group in clusters.values()]
    return (
        means if new_means == means else kmeans(data_points, new_means, iteration + 1)
    )


def main() -> None:
    data_points = []  # (x, y)
    means = []
    kmeans(data_points, means)


if __name__ == "__main__":
    main()
