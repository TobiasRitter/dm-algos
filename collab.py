from numpy import nanmean
from numpy import nan
from scipy.stats import pearsonr

DECIMALS = 3


def filter(xs: list[float], ys: list[float]) -> tuple[list[float], list[float]]:
    x_out = []
    y_out = []
    for x, y in list(zip(xs, ys)):
        if x is not nan and y is not nan:
            x_out += [x]
            y_out += [y]
    return (x_out, y_out)


def weighted_corr(
    xs: list[float], ys: list[float], denom: int, print_out: bool = True
) -> float:
    xs_new, ys_new = filter(xs, ys)
    res = pearsonr(xs_new, ys_new)[0] * len(xs_new) / denom

    if print_out:
        print(f"weighted corr: {round(res, DECIMALS)}")
    return res


def forecast(y_bar: float, corrs: list[float], centered_ratings: list[float]) -> float:
    num = sum([w * r for w, r in list(zip(corrs, centered_ratings))])
    denom = sum([abs(w) for w in corrs])
    return y_bar + num / denom


def forecast_data(
    ys: list[float], xss: list[list[float]], denom: int, index: int
) -> float:
    y_bar = nanmean(ys)
    xss_centered = [[x - nanmean(xs) for x in xs] for xs in xss]
    centered_ratings = [xs[index] for xs in xss_centered]
    corrs = [weighted_corr(ys, xs, denom, False) for xs in xss]
    res = forecast(y_bar, corrs, centered_ratings)
    return res


def main():
    pass


if __name__ == "__main__":
    main()
