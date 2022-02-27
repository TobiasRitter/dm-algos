from statistics import mean as avg
from math import sqrt

Point = tuple[float, float]
DECIMALS = 3


def pretty_print(iteration: int, clusters: dict[Point, list[Point]]) -> None:
    print(f"step {iteration}:")
    for mean, points in clusters.items():
        x, y = mean
        print(f"({round(x,DECIMALS)}, {round(y,DECIMALS)}) : {points}")
    print("")


def pretty_print_1d(iteration: int, clusters: dict[Point, list[Point]]) -> None:
    print(f"step {iteration}:")
    for mean, points in clusters.items():
        transformed_points = [point[0] for point in points]
        print(f"{round(mean[0],DECIMALS)} : {transformed_points}")
    print("")


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
    one_d: bool = False,
) -> list[Point]:
    clusters: dict[Point, list[Point]] = {mean: [] for mean in means}

    for point in data_points:
        mean = get_closest_mean(point, means)
        clusters[mean] += [point]

    if one_d:
        pretty_print_1d(iteration, clusters)
    else:
        pretty_print(iteration, clusters)

    new_means = [get_mean(point_group) for point_group in clusters.values()]
    return (
        means
        if new_means == means
        else kmeans(data_points, new_means, iteration + 1, one_d)
    )


def kmeans_1d(data_points: list[float], means: list[float], iteration: int = 1):
    transformed_points = [(point, 0) for point in data_points]
    transformed_means = [(mean, 0) for mean in means]
    return kmeans(transformed_points, transformed_means, iteration, True)


def main() -> None:
    data_points = []  # (x, y)
    means = []  # (x, y)
    kmeans(data_points, means)


if __name__ == "__main__":
    main()
