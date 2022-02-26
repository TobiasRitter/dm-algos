from math import log2


def entropy(ps: list[float]) -> float:
    return -sum([0 if p == 0 else p * log2(p) for p in ps])


def info(pss: list[list[int]]) -> float:
    pss_sum = sum(sum(pss, []))
    return sum([entropy([p / sum(ps) for p in ps]) * sum(ps) / pss_sum for ps in pss])


def gain(prev_split: list[list[int]], new_split: list[list[int]]) -> float:
    return info(prev_split) - info(new_split)


def gain_ratio(prev_split: list[list[int]], new_split: list[list[int]]) -> float:
    leaf_sizes = [sum(leaf) for leaf in new_split]
    return gain(prev_split, new_split) / info([leaf_sizes])


def main():
    pass


if __name__ == "__main__":
    main()
