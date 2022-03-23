from numpy import nanmean
from numpy import nan
from scipy.stats import pearsonr

DECIMALS = 3


def filter(xs: List[float], ys: List[float]) -> Tuple[List[float], List[float]]:
    x_out = []
    y_out = []
    for x, y in list(zip(xs, ys)):
        if x is not nan and y is not nan:
            x_out += [x]
            y_out += [y]
    return (x_out, y_out)


def weighted_corr(
    xs: List[float], ys: List[float], denom: int, print_out: bool = True
) -> float:
    xs_new, ys_new = filter(xs, ys)
    pears = pearsonr(xs_new, ys_new)[0]
    res = pears * len(xs_new) / denom

    if print_out:
        print(
            f"weighted corr: ({len(xs_new)} / {denom}) * {round(pears, DECIMALS)} = {round(res, DECIMALS)}"
        )
    return res


def print_forecast(
    target_bar: float,
    corrs: List[float],
    centered_ratings: List[float],
    norm: float,
    res: float,
):
    print(f"forecast: {round(target_bar,DECIMALS)} + (", end="")
    print_plus = False
    for corr, rating in list(zip(corrs, centered_ratings)):
        if print_plus:
            print(" + ", end="")
        print(f"{round(corr, DECIMALS)} * {round(rating, DECIMALS)}", end="")
        print_plus = True

    print(f") / {round(norm,DECIMALS)} = {round(res, DECIMALS)}")
    pass


def forecast(
    target_bar: float,
    corrs: List[float],
    centered_ratings: List[float],
    print_out: bool = True,
) -> float:
    num = sum([w * r for w, r in list(zip(corrs, centered_ratings))])
    norm = sum([abs(w) for w in corrs])
    res = target_bar + num / norm

    if print_out:
        print_forecast(target_bar, corrs, centered_ratings, norm, res)
    return res


def forecast_data(
    target_ratings: List[float],
    other_ratings: List[List[float]],
    denom: int,
    index: int,
    print_out: bool = True,
) -> float:
    target_bar = nanmean(target_ratings)
    xss_centered = [[x - nanmean(xs) for x in xs] for xs in other_ratings]
    centered_ratings = [xs[index] for xs in xss_centered]
    corrs = [weighted_corr(target_ratings, xs, denom, False) for xs in other_ratings]
    return forecast(target_bar, corrs, centered_ratings, print_out)


def main():
    pass


if __name__ == "__main__":
    main()
