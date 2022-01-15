from collections import UserDict, OrderedDict
from collections.abc import Iterable
from _collections_abc import (
    dict_keys,
    dict_values,
    dict_items,
)  # https://github.com/python/typeshed/pull/6888
from .helpers import _is_iterable_but_not_string, _convert_slice_to_list


class kdict(UserDict):
    """
    A dict with k-dimensional keys, sliceable along any of those dimensions.
    """

    # Why we subclass UserDict instead of dict: https://stackoverflow.com/a/7148602/130164 and https://stackoverflow.com/a/64450669/130164 and similar

    def __init__(self, dict=None, **kwargs):
        self.key_len = None

        key_lengths = []
        if dict is not None:
            key_lengths.extend([len(k) for k in dict.keys()])
        if kwargs:
            key_lengths.extend([len(k) for k in kwargs.keys()])

        if len(key_lengths) >= 1:
            self.key_len = key_lengths[0]
            if not all(x == self.key_len for x in key_lengths):
                raise ValueError("All keys must have same length")

        super().__init__(dict, **kwargs)

    def _get_multiple_keys(self, key_template):
        # TODO: can we return a view into the dictionary rather than a copy?
        # see https://stackoverflow.com/q/9329537/130164

        key_transformed = []

        # Convert slices to list
        for ix, k in enumerate(key_template):
            if isinstance(k, slice):
                key_transformed.append(
                    _convert_slice_to_list(k, self.keys(dimensions=ix, unique=False))
                )
            elif _is_iterable_but_not_string(k):
                key_transformed.append(list(k))
            else:
                key_transformed.append(k)

        if len(key_transformed) != len(key_template):
            raise ValueError("something went wrong in slice eval process")

        # confirm all list lengths match
        key_list_lengths = [
            len(k) for k in key_transformed if _is_iterable_but_not_string(k)
        ]
        # print(key_template, key_transformed, key_list_lengths)
        if not all(x == key_list_lengths[0] for x in key_list_lengths):
            raise KeyError("All slices must have same length")

        # transform any remaining scalars into lists of that length
        key_transformed = [
            [k] * key_list_lengths[0] if (not _is_iterable_but_not_string(k)) else k
            for k in key_transformed
        ]

        # take subset
        # check membership against keys() to handle the following scenario:
        # suppose we have keys (1, "a"), (1, "b"), (2, "c"), and user asks for (1, :)
        # in this case, key_transformed will include (1, "c"), which does not actually exist
        # this is tested in test_none_slice_against_mixed_column()
        # TODO: is there a better way to construct key_transformed?
        subset = {k: self.data[k] for k in zip(*key_transformed) if k in self.keys()}

        # Return another kdict
        return self.__class__(dict=subset)

    def __getitem__(self, key):
        if self.key_len is not None and len(key) != self.key_len:
            raise KeyError(key, "wrong key length")

        if any(isinstance(k, slice) or _is_iterable_but_not_string(k) for k in key):
            return self._get_multiple_keys(key)

        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if not self.key_len:
            self.key_len = len(key)
        else:
            if len(key) != self.key_len:
                raise KeyError(key, "wrong key length")
        return super().__setitem__(key, value)

    def keys(self, dimensions=None, unique=True) -> dict_keys:
        """
        Get keys: either return full tuples, or return one column of the tuples (optionally taking unique values only)
        """
        # Get a dict_keys object here to behave more like a dict does,
        # whereas calling UserDict's keys() with super().keys() would give a KeysView, which is a bit different:
        # https://github.com/python/typeshed/pull/6888
        all_keys = self.data.keys()

        if dimensions is None:
            return all_keys

        if isinstance(dimensions, Iterable):
            # requested multiple dimensions. wrap keys in tuples
            key_column = [
                tuple(key[dimension] for dimension in dimensions) for key in all_keys
            ]
        else:
            # requested a single dimension (argument was a scalar, not a list)
            # provide keys as scalars too
            key_column = [key[dimensions] for key in all_keys]

        if unique:
            # get unique values in original order, so can't use set.
            return list(OrderedDict.fromkeys(key_column))
        return key_column

    def values(self) -> dict_values:
        # Return a dict_values object just like dict, rather than UserDict's ValuesView.
        # https://github.com/python/typeshed/pull/6888
        return (
            self.data.values()
        )  # instead of return super().values() or not overriding at all

    def items(self) -> dict_items:
        # Return a dict_items object just like dict, rather than UserDict's ItemsView.
        # https://github.com/python/typeshed/pull/6888
        return (
            self.data.items()
        )  # instead of return super().items() or not overriding at all

    def eject(self):
        return self.data
