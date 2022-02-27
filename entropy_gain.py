from math import log2

DECIMALS = 3


def entropy(ps: list[float], print_out: bool = True) -> float:
    res = -sum([0 if p == 0 else p * log2(p) for p in ps])
    if print_out:
        print(f"entropy: {round(res, DECIMALS)}")
    return res


def print_info(denom: int, summands: list[tuple[int, float]], res: float) -> None:
    if len(summands) == 1:
        print(f"info: {round(res,DECIMALS)}")
        return

    print_plus = False
    print("info: ", end="")
    for factor, entrop in summands:
        if print_plus:
            print(" + ", end="")
        print(
            f"{round(factor, DECIMALS)} / {round(denom, DECIMALS)} * {round(entrop, DECIMALS)}",
            end="",
        )
        print_plus = True

    print(f" = {round(res, DECIMALS)}")


def info(pss: list[list[int]], print_out: bool = True) -> float:
    pss_sum = sum(sum(pss, []))
    summands = [(sum(ps), entropy([p / sum(ps) for p in ps], False)) for ps in pss]
    res = sum(
        [entropy([p / sum(ps) for p in ps], False) * sum(ps) / pss_sum for ps in pss]
    )

    if print_out:
        print_info(pss_sum, summands, res)

    return res


def gain(
    prev_split: list[list[int]], new_split: list[list[int]], print_out: bool = True
) -> float:
    old = info(prev_split, False)
    new = info(new_split, False)
    res = old - new

    if print_out:
        print(
            f"gain: {round(old,DECIMALS)} - {round(new,DECIMALS)} = {round(res,DECIMALS)}"
        )

    return res


def gain_ratio(
    prev_split: list[list[int]], new_split: list[list[int]], print_out: bool = True
) -> float:
    leaf_sizes = [sum(leaf) for leaf in new_split]
    numerator = gain(prev_split, new_split, False)
    denominator = info([leaf_sizes], False)
    res = numerator / denominator

    if print_out:
        print(
            f"gain ratio: {round(numerator, DECIMALS)} / {round(denominator, DECIMALS)} = {round(res, DECIMALS)}"
        )

    return numerator / denominator


def main():
    pass


if __name__ == "__main__":
    main()
