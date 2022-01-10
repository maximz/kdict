#!/usr/bin/env python

import pytest
from kdict import kdict


def test_main():
    d = kdict()
    for fold_id in range(3):
        for fold_label in ["train", "test"]:
            for model_name in ["randomforest", "svm"]:
                d[fold_id, fold_label, model_name] = object()
    assert len(d) == 12

    assert len(d.keys()) == 12
    assert d.keys(dimension=0, unique=False) == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    assert d.keys(dimension=1, unique=True) == ["train", "test"]
    assert d.keys(dimension=2, unique=True) == ["randomforest", "svm"]

    assert isinstance(d[1, "test", "svm"], object)

    assert len(d[0, :, :]) == 4
    assert len(d[:, :, "randomforest"]) == 6

    assert len(d[0, "train", :]) == 2
    assert len(d[0, :, "randomforest"]) == 2

    assert len(d[[1, 2], "train", "svm"]) == 2

    del d[1, "test", "svm"]
    assert len(d) == 11


def test_list_get():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, 10, "test"] = object()
    assert len(d[1, [5, 10], "train"]) == 2


@pytest.mark.xfail(raises=KeyError)
def test_list_and_slice_together_get():
    # KeyError: 'All slices must have same length'
    # TODO: we should treat ":" slice as a "get all" / "no filters for this column"
    # right now this is failing because we interpret this as: [1, [5, 10], ['train', 'train', 'train', 'test']]
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, 10, "test"] = object()
    d[1, [5, 10], :]


def test_int_slice_against_int_column():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    assert len(d[1, 1:9, "train"]) == 2


@pytest.mark.xfail(raises=TypeError)
def test_int_slice_against_str_column():
    # TypeError: '>=' not supported between instances of 'str' and 'int'
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, "test"] = object()
    assert len(d[1, 2, 3:6]) == 0


@pytest.mark.xfail(raises=TypeError)
def test_int_slice_against_mixed_column():
    # TypeError: '>=' not supported between instances of 'str' and 'int'
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, 5] = object()
    assert len(d[1, 2, 3:6]) == 0


def test_none_slice_against_str_column():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, "test"] = object()
    assert len(d[1, 2, :]) == 2


def test_none_slice_against_str_column_with_nones():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, "test"] = object()
    d[1, 2, None] = object()
    assert len(d[1, 2, :]) == 3


def test_none_slice_against_int_column():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    assert len(d[1, :, "train"]) == 3


def test_none_slice_against_int_column_with_nones():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, None, "train"] = object()
    assert len(d[1, :, "train"]) == 4


def test_none_slice_against_mixed_column():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, 5] = object()
    assert len(d[1, 2, :]) == 2


def test_update():
    a = kdict()
    a[1, 2, 3] = "test"
    assert len(a) == 1
    a.update({(1, 2, 4): "test"})
    assert len(a) == 2


@pytest.mark.xfail(raises=KeyError)
def test_key_length_enforced_in_update():
    # KeyError: ((1, 2), 'wrong key length')
    a = kdict()
    a[1, 2, 3] = "test"
    a.update({(1, 2, 4): "test"})
    assert len(a) == 2
    a.update({(1, 2): "test"})


@pytest.mark.xfail(raises=KeyError)
def test_key_length_enforced_in_get():
    # KeyError: ('1', 'wrong key length')
    a = kdict()
    a[1, 2, 3] = "test"
    a["1"]


@pytest.mark.xfail(raises=ValueError)
def test_key_length_enforced_in_constructor():
    # ValueError: All keys must have same length
    kdict({("a", 2): 5, "b": 6})


def test_constructor():
    kdict({("a", 2): 5})
    kdict(a=5)
    kdict({("a", 2): 5, ("b", 7): 6})
    kdict({"a": 2}, b=7)
