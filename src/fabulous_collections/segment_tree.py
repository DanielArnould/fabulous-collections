from typing import Final
from collections.abc import Callable, Sequence


# TODO: Replace with sentinel upon 3.15 release
class _MissingType: ...


_MISSING: Final = _MissingType()


class SegmentTree[T]:
    """Generic data structure for efficient range queries and point updates.

    A segment tree computes the result of an associative operation over a
    half-open interval [lo, hi) in O(log N) time, while allowing individual
    elements to be updated in O(log N) time.

    >>> import operator
    >>> # Create a segment tree for answering sum queries
    >>> tree = SegmentTree([1, 2, 3, 4, 5], operator.add, int)
    >>> tree.query(0, 5)                # sum of all elements
    15
    >>> tree.query(1, 4)                # sum of elements at indices 1, 2, 3
    9
    >>> tree.update(2, 10)              # replace the '3' at index 2 with '10'
    >>> tree.query(1, 4)                # the same query now reflects the update
    16
    >>> tree.query(4, 2)                # invalid/empty ranges return the identity
    0

    References:
        cp-algorithms: https://cp-algorithms.com/data_structures/segment_tree.html
    """

    def __init__(
        self,
        data: Sequence[T],
        combine: Callable[[T, T], T],
        identity: Callable[[], T],
    ) -> None:
        self._length = len(data)
        self._combine = combine
        self._identity = identity
        self._tree: list[T | _MissingType] = [_MISSING] * 4 * self._length
        self._build(data, 1, 0, self._length)

    def _build(self, data: Sequence[T], vertex: int, lo: int, hi: int) -> None:
        if lo == hi - 1:
            self._tree[vertex - 1] = data[lo]
        elif lo < hi - 1:
            mid = (lo + hi) // 2

            self._build(data, vertex * 2, lo, mid)
            left = self._tree[(vertex * 2) - 1]
            assert not isinstance(left, _MissingType), (
                "A left child was not built correctly!"
            )

            self._build(data, vertex * 2 + 1, mid, hi)
            right = self._tree[(vertex * 2 + 1) - 1]
            assert not isinstance(right, _MissingType), (
                "A right child was not built correctly!"
            )

            self._tree[vertex - 1] = self._combine(left, right)

    def query(self, lo: int, hi: int) -> T:
        """Evaluate the combine function over the half-open interval [lo, hi).

        >>> import operator
        >>> tree = SegmentTree([10, 20, 30], operator.add, int)
        >>> tree.query(0, 2)            # sum of index 0 and 1
        30
        >>> tree.query(2, 2)            # empty range
        0
        """
        return self._query(1, 0, self._length, max(lo, 0), min(hi, self._length))

    def _query(self, vertex: int, range_lo: int, range_hi: int, lo: int, hi: int) -> T:
        if lo >= hi:
            return self._identity()
        if lo == range_lo and hi == range_hi:
            res = self._tree[vertex - 1]
            assert not isinstance(res, _MissingType), (
                f"_MissingType in range [{lo}, {hi})"
            )
            return res

        mid = (range_lo + range_hi) // 2
        return self._combine(
            self._query(vertex * 2, range_lo, mid, lo, min(hi, mid)),
            self._query(vertex * 2 + 1, mid, range_hi, max(lo, mid), hi),
        )

    def update(self, index: int, new_val: T) -> None:
        """Replace the element at ``index`` with ``new_val``.

        >>> import operator
        >>> tree = SegmentTree([1, 1, 1], operator.add, int)
        >>> tree.update(1, 5)           # list becomes [1, 5, 1]
        >>> tree.query(0, 3)
        7
        """
        if index < 0 or index >= self._length:
            raise IndexError(
                f"{index} is out of bounds! Expected an index in the range [0, {self._length})"
            )
        self._update(1, 0, self._length, index, new_val)

    def _update(self, vertex: int, lo: int, hi: int, index: int, new_val: T) -> None:
        if lo == hi - 1:
            self._tree[vertex - 1] = new_val
        else:
            mid = (lo + hi) // 2
            if index < mid:
                self._update(vertex * 2, lo, mid, index, new_val)
            else:
                self._update(vertex * 2 + 1, mid, hi, index, new_val)

            left = self._tree[(vertex * 2) - 1]
            assert not isinstance(left, _MissingType), "A left child is missing!"

            right = self._tree[(vertex * 2 + 1) - 1]
            assert not isinstance(right, _MissingType), "A right child is missing!"

            self._tree[vertex - 1] = self._combine(left, right)

    def __len__(self) -> int:
        """Return the number of elements tracked by the segment tree."""
        return self._length
