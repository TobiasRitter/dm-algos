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
    # print(entropy([0.1, 0.9]))
    # print(entropy([0.2, 0.8]))
    # print(entropy([0.3, 0.7]))
    # print(entropy([0.5, 0.5]))
    # print(entropy([0.1, 0.1, 0.8]))

    # print(info([[2, 3]]))
    # print(info([[5, 4]]))
    # print(info([[2, 3], [5, 4]]))
    # print(info([[2, 3], [9, 0]]))

    # print(gain([[5, 5]], [[2, 3], [3, 1]]))  # temp
    # print(gain([[5, 5]], [[3, 0], [0, 3], [2, 1]]))  # vis
    # print(gain([[5, 5]], [[1, 3], [4, 1]]))  # depth

    # print(gain([[2, 1]], [[0, 1], [2, 0]]))  # depth
    # print(gain([[2, 1]], [[1, 1], [1, 0]]))  # temp

    # print(gain_ratio([[5, 5]], [[2, 3], [3, 1]]))  # temp
    # print(gain_ratio([[5, 5]], [[3, 0], [0, 3], [2, 1]]))  # vis
    # print(gain_ratio([[5, 5]], [[1, 3], [4, 1]]))  # depth

    # print(gain_ratio([[2, 1]], [[0, 1], [2, 0]]))  # depth
    # print(gain_ratio([[2, 1]], [[1, 1], [1, 0]]))  # temp

    print(info([[2,0],[3,3]]))
    print(info([[4,1],[1,2]]))
    print(info([[5,1],[0,2]]))


if __name__ == "__main__":
    main()
