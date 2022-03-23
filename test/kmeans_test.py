from cmath import sqrt

from kmeans import distance


def test_distance():
    assert distance((1, 0), (0, 0)) == 1
    assert distance((1, 0), (0, 1)) == sqrt(2)
