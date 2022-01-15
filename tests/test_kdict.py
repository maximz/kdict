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
    assert d.keys(dimensions=0, unique=False) == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    assert d.keys(dimensions=1, unique=True) == ["train", "test"]
    assert d.keys(dimensions=2, unique=True) == ["randomforest", "svm"]
    assert d.keys(dimensions=[1, 2], unique=True) == [
        ("train", "randomforest"),
        ("train", "svm"),
        ("test", "randomforest"),
        ("test", "svm"),
    ]

    assert isinstance(d[1, "test", "svm"], object)

    # Test slices
    assert len(d[0, :, :]) == 4
    assert type(d[0, :, :]) == kdict, "slice should still be a kdict"
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
    d[1, 10, "test"] = object()
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
    d[5, 2, "test"] = object()
    assert len(d[1, 2, :]) == 2


def test_none_slice_against_str_column_with_nones():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, "test"] = object()
    d[1, 2, None] = object()
    d[1, 4, None] = object()
    assert len(d[1, 2, :]) == 3


def test_none_slice_against_int_column():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, 10, "test"] = object()
    assert len(d[1, :, "train"]) == 3


def test_none_slice_against_int_column_with_nones():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, None, "train"] = object()
    d[1, 10, "test"] = object()
    assert len(d[1, :, "train"]) == 4


def test_none_slice_against_mixed_column():
    # this tests two things:
    # - we can slice a column that has both str and int values
    # - when we use slice, it will only take slice of keys that match non-sliced columns,
    #   i.e. it will not attempt to take (1, 2, 'test')

    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 2, 5] = object()
    d[3, 10, "test"] = object()
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


def test_subset_returns_kdict():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, 10, "test"] = object()
    assert type(d[1, :, "train"]) == kdict


def test_subsets_are_separate():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()
    d[1, 10, "test"] = object()

    # get subset
    subset = d[1, :, "train"]
    assert len(subset) == 3

    # modify original
    d[1, 5, "train"] = "now a string"
    d[1, 20, "train"] = "new object"
    # confirm subset has not been modified as a result
    assert subset[1, 5, "train"] != "now a string"
    # and subset should not have new object - subset of keys will not get updated
    assert (1, 20, "train") not in subset.keys()

    # modify subset
    subset[1, 10, "test"] = "now a string as well"
    subset[1, 50, "test"] = "another new object"
    # confirm original has not been modified and has not received new object
    assert d[1, 10, "test"] != "now a string as well"
    assert (1, 50, "test") not in d.keys()


def test_eject():
    d = kdict()
    d[1, 2, "train"] = object()
    d[1, 5, "train"] = object()
    d[1, 10, "train"] = object()

    eject = d.eject()

    assert type(eject) == dict
    assert type(d) == kdict

    assert len(eject.keys()) == len(d.keys())


def test_looks_like_a_dict():
    # want to confirm it mostly looks like a dict
    # e.g. the keys() method should give same return type as dict.keys()
    # the issue is that UserDict may change that
    d = kdict()
    d[1, 2, "train"] = object()
    assert type(d.keys()) == type(d.data.keys())
    assert type(d.values()) == type(d.data.values())
    assert type(d.items()) == type(d.data.items())
