# Kdict: dict with multi-dimensional, sliceable keys

[![](https://img.shields.io/pypi/v/kdict.svg)](https://pypi.python.org/pypi/kdict)
[![CI](https://github.com/maximz/kdict/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/maximz/kdict/actions/workflows/ci.yaml)
[![](https://img.shields.io/badge/docs-here-blue.svg)](https://kdict.maximz.com)
[![](https://img.shields.io/github/stars/maximz/kdict?style=social)](https://github.com/maximz/kdict)

_kdict_ is like _dict_ for multi-dimensional keys. With _kdict_, you can easily filter and slice your dictionary by key dimensions.

**Example: machine learning model evaluation.** Suppose you're evaluating several models on three cross validation folds, each with a training set and a test set.

Before _kdict_, you might store evaluation scores in a nested dictionary. But that's cumbersome and error-prone. Here's what it would take to get the mean accuracy for a particular model across all folds:

```python
# To access inner nested data without kdict, you'd need to write iterators like this:
import numpy as np
np.mean(
    [
        data[fold_id][fold_label]["lasso"]
        for fold_id in data.keys()
        for fold_label in data[fold_id].keys()
    ]
)
```

**_kdict_ makes storing and accessing this type of data a breeze. No more nesting:**

```python
# Store data in a three-dimensional kdict.
# Dimensions: fold ID, fold label, model name
data = kdict(...)

# Slice the kdict to get lasso model's mean accuracy across all folds:
# data[:, :, 'lasso'] is a subset of the full dictionary
np.mean(list(data[:, :, 'lasso'].values()))
```

In this example, `data` is a three-dimensional _kdict_ that you can slice along any dimension. So how did we make this kdict?

```python
from kdict import kdict
data = kdict() # make a blank kdict
for fold_id in range(3):
    for fold_label in ['train', 'test']:
        for model_name in ['lasso', 'randomforest']:
            # add an entry for each fold ID, fold label, and model name
            data[fold_id, fold_label, model_name] = get_model_score(
                fold_id,
                fold_label,
                model_name
            )
```

The syntax, in a nutshell:

- Read or write a single element by accessing `[key_dimension_1, key_dimension_2]` and so on.
- Or get a subset of the dictionary by slicing, e.g. `[:, key_dimension_2]`.

## Installation

```bash
pip install kdict
```

## Usage

### Create a _kdict_

Import: `from kdict import kdict`

Create a blank _kdict_: `data = kdict()`. Or initialize from an existing dict: `data = kdict(existing_dict)`. You can also use a dict comprehension there, such as:

```python
data = kdict({
    (fold_id, fold_label, model_name): get_model_score(fold_id, fold_label, model_name)
    for model_name in ['lasso', 'randomforest']
    for fold_label in ['train', 'test']
    for fold_id in range(3)
})
```

### Slice a _kdict_

Access an individual item with `data[0, 'train', 'lasso']`.

Or get a subset of the dictionary with slices: `data[0, :, :]` will have all items where the first dimension of the key is 0. This slice is also a _kdict_, so you can keep slicing and filtering further.

You can also iterate over specific key dimensions:

```python
# get final dimension of the keys
available_models = data.keys(dimensions=2)

# or get all pairs of first two dimensions
for fold_id, fold_label in data.keys(dimensions=[0, 1]):
    ... # now do something with data[fold_id, fold_label, :]
```

### Eject

A _kdict_ behaves just like a _dict_, except all keys must have the same number of dimensions.

To get a raw _dict_ back, call `data.eject()`.


## Development

Submit PRs against `develop` branch, then make a release pull request to `master`.

```bash
# Install requirements
pip install --upgrade pip wheel
pip install -r requirements_dev.txt

# Install local package
pip install -e .

# Install pre-commit
pre-commit install

# Run tests
make test

# Run lint
make lint

# bump version before submitting a PR against master (all master commits are deployed)
bump2version patch # possible: major / minor / patch

# also ensure CHANGELOG.md updated
```
