from enum import Enum
from math import sqrt
from statistics import mean

from scipy.stats import norm, t

DECIMALS = 3


class H1(Enum):
    EQUAL = 1
    GREATER = 2
    LESS = 3


def conf_interval(
    x_bar: float,
    sigma_or_s: float,
    n: int,
    alpha: float,
    use_z: bool,
) -> tuple[float, float]:
    p = 1 - alpha / 2
    val_c = norm.ppf(p) if use_z else t.ppf(p, n - 1)
    diff = val_c * sigma_or_s / sqrt(n)
    return (round(x_bar - diff, DECIMALS), round(x_bar + diff, DECIMALS))


def get_se2(xs: list[float]):
    return sum([(x - mean(xs)) ** 2 for x in xs]) / (len(xs) - 1)


def get_p(alpha: float, h1: H1):
    return 1 - alpha / 2 if h1 == H1.EQUAL else 1 - alpha


def check(val_0: float, val_c: float, h1: H1) -> bool:
    if h1 == H1.GREATER:
        return val_0 > val_c
    if h1 == H1.LESS:
        return val_0 < val_c
    return abs(val_0) > abs(val_c)


def test(val_0: float, val_c: float, h1: H1, use_z: bool):
    distribution = "z" if use_z else "t"

    if h1 == H1.EQUAL:
        print(f"|{distribution}_0|: {round(abs(val_0),DECIMALS)}")
        print(f"|{distribution}_c|: {round(abs(val_c),DECIMALS)}")
    else:
        print(f"{distribution}_0: {round(val_0,DECIMALS)}")
        print(f"{distribution}_c: {round(val_c,DECIMALS)}")

    outcome = "rejected" if check(val_0, val_c, h1) else "not rejected"
    print(f"H_0 is {outcome}")
    print("")


def z_test(
    x_bar: float,
    sigma: float,
    n: int,
    alpha: float,
    h1: H1,
    mu_zero: float = 0,
):
    z0 = (x_bar - mu_zero) / sigma * sqrt(n)
    zc = norm.ppf(get_p(alpha, h1))
    test(z0, zc, h1, True)


def t_test(
    x_bar: float,
    sigma: float,
    n: int,
    alpha: float,
    h1: H1,
    mu_zero: float = 0,
):
    t0 = (x_bar - mu_zero) / sigma * sqrt(n)
    tc = t.ppf(get_p(alpha, h1), n - 1)
    test(t0, tc, h1, False)


def t_test_data(
    xs: list[float],
    alpha: float,
    h1: H1,
    mu_zero: float = 0,
):
    n = len(xs)
    x_bar = mean(xs)
    t0 = (x_bar - mu_zero) / sqrt(get_se2(xs)) * sqrt(n)
    tc = t.ppf(get_p(alpha, h1), n - 1)
    test(t0, tc, h1, False)


def welch(
    x_bar: float,
    y_bar: float,
    se_x: float,
    se_y: float,
    n_x: int,
    n_y: int,
    df: int,
    alpha: float,
    h1: H1,
    mu_zero: float = 0,
):
    se = se_x / n_x + se_y / n_y
    t0 = (x_bar - y_bar - mu_zero) / sqrt(se)
    tc = t.ppf(get_p(alpha, h1), df)
    test(t0, tc, h1, False)


def welch_data(
    xs: list[float],
    ys: list[float],
    df: int,
    alpha: float,
    h1: H1,
    mu_zero: float = 0,
):
    se2 = get_se2(xs) / len(xs) + get_se2(ys) / len(ys)
    t0 = (mean(xs) - mean(ys) - mu_zero) / sqrt(se2)
    tc = t.ppf(get_p(alpha, h1), df)
    test(t0, tc, h1, False)


def paired_t_data(
    xs: list[float],
    ys: list[float],
    alpha: float,
    h1: H1 = H1.GREATER,
    mu_zero: float = 0,
):
    """h1 = H1.GREATER means xs > ys
    
    If h1 == H1.LESS, the critical value tc is inverted"""
    ds = [x - y for x, y in list(zip(xs, ys))]
    d_bar = mean(ds)
    se2 = get_se2(ds)
    n = len(ds)
    t0 = (d_bar - mu_zero) / sqrt(se2) * sqrt(n)
    tc = t.ppf(get_p(alpha, h1), n - 1)
    print(f"d_bar: {round(d_bar, DECIMALS)}")
    print(f"se^2: {round(se2, DECIMALS)}")
    test(t0, -tc if h1 == H1.LESS else tc, h1, False)


def main():
    pass


if __name__ == "__main__":
    main()
