from collections import UserDict, OrderedDict
from .helpers import _is_iterable_but_not_string, _convert_slice_to_list


class kdict(UserDict):
    """
    n-dimensional dict
    """

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
        key_transformed = []

        # Convert slices to list
        for ix, k in enumerate(key_template):
            if isinstance(k, slice):
                key_transformed.append(
                    _convert_slice_to_list(k, self.keys(dimension=ix, unique=False))
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

        return {k: self.data[k] for k in zip(*key_transformed)}

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

    def keys(self, dimension=None, unique=False):
        """
        Get keys: either return full tuples, or return one column of the tuples (optionally taking unique values only)
        """
        all_keys = super().keys()
        if dimension is None:
            return all_keys
        key_column = [key[dimension] for key in all_keys]
        if unique:
            # get unique values in original order, so can't use set.
            return list(OrderedDict.fromkeys(key_column))
        return key_column
