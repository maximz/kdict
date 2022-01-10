from kdict.helpers import _is_iterable_but_not_string


def test_is_iterable_but_not_string():
    assert _is_iterable_but_not_string([1, 2, 3])
    assert _is_iterable_but_not_string({1, 2, 3, "a"})
    assert _is_iterable_but_not_string({"a": 5, "b": 6})
    assert _is_iterable_but_not_string((1, 2, 3))
    assert not _is_iterable_but_not_string("str")
    assert not _is_iterable_but_not_string(5)
