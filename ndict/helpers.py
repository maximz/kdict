from collections.abc import Iterable


def _is_iterable_but_not_string(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))


def _convert_slice_to_list(s, lst):
    # need to slice by value, not by index. this is a loc, not an iloc

    # if slice has defined start-stop (e.g. 3:6, not :), only return non-null numeric values that are between start and stop of the slice

    # if slice is infinite, i.e. :, return all values

    return [
        l
        for l in lst
        if (
            (l is not None)
            and (not s.start or l >= s.start)
            and (not s.stop or l <= s.stop)
        )
        or (not s.start and not s.stop)
    ]
