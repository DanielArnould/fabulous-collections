from typing import Final
from collections.abc import Callable, Sequence


# TODO: Replace with sentinel upon 3.15 release
class _MissingType: ...


_MISSING: Final = _MissingType()


class SegmentTree[T]:
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
        return self._length
