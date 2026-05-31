import pytest
import operator
from hypothesis import strategies as st, given
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize
from fabulous_collections.segment_tree import SegmentTree


class SegmentTreeMachine(RuleBasedStateMachine):
    @initialize(data=st.lists(st.integers(), min_size=1, max_size=100))
    def init_tree(self, data):
        self.model = list(data)
        self.tree = SegmentTree(data, operator.add, identity=int)

    @rule(idx=st.integers(), new_val=st.integers())
    def update_node(self, idx, new_val):
        idx %= len(self.model)
        self.model[idx] = new_val
        self.tree.update(idx, new_val)

    @rule(
        lo=st.integers(min_value=0, max_value=99),
        hi=st.integers(min_value=0, max_value=99),
    )
    def query_range(self, lo, hi):
        lo %= len(self.model)
        hi %= len(self.model)
        lo, hi = min(lo, hi), max(lo, hi)
        expected = sum(self.model[lo:hi])
        assert self.tree.query(lo, hi) == expected


TestSegmentTree = SegmentTreeMachine.TestCase


@given(st.lists(st.integers()), st.integers(), st.integers())
def test_readonly_query(lst, lo, hi):
    segment_tree = SegmentTree(lst, operator.add, int)
    assert segment_tree.query(lo, hi) == sum(lst[lo:hi])


def test_invalid_update_idx():
    segment_tree = SegmentTree([1, 2, 3], operator.add, int)
    with pytest.raises(IndexError):
        segment_tree.update(4, 1)

    with pytest.raises(IndexError):
        segment_tree.update(-1, 1)
