# Curation scripts

This repo contains scripts that are meant to implement one-off large-scale changes to INSPIRE or gather complex information.

To add a new script, create a new directory under `scripts` containing a single `script.py` file implementing the script logic, then create a PR. Auxiliary files will be generated automatically when merging to master.

## Common patterns

### Search, check & do

Often, a task can be fit into the following pattern:

1. *Search* for a set of records that need to be handled
2. *Check* for each record whether it needs to be modified, or print some metadata from the record
3. Do some modifications on the record passing the check

In those cases, one can subclass the `SearchCheckDo` class which provides logic to perform these operations. The script will have the following structure:

```python
from inspirehep.curation.search_check_do import SearchCheckDo


class MyCustomAction(SearchCheckDo):
    """Explain what this does."""

    # Literature is default, ``search_class`` needs to be set for other
    # collections
    # search_class = LiteratureSearch

    query = ...  # a custom query, like "t electron"

    @staticmethod
    def check(record, logger, state):
	# Use ``record`` to check if it needs to be modified, return True if
	# so. Optionally use ``logger`` to log additional info and ``state`` to # transmit some data to the ``do`` step.
	...

    @statimethod
    def do(record, logger, state):
	# Mutate ``record`` to make modifications.
	# Optionally use ``logger`` to log additional info and ``state`` to
	# retrieve some data to the ``do`` step.
	...


MyCustomAction()
```

Concrete examples can be found [here](https://github.com/inspirehep/inspirehep/blob/master/backend/inspirehep/curation/search_check_do/examples.py).
