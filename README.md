# Curation scripts

This repo contains scripts that are meant to implement one-off large-scale changes to INSPIRE or gather complex information.

To add a new script, create a new directory under `scripts` containing a single `script.py` file implementing the script logic, then create a PR. Auxiliary files will be generated automatically when merging to master.

## Common patterns

### Search, check & do

Often, a task can be fit into the following pattern:

1. _Search_ for a set of records that need to be handled
2. _Check_ for each record whether it needs to be modified, or print some metadata from the record
3. _Do_ some modifications on the record passing the check

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
        # so. Optionally use ``logger`` to log additional info and ``state`` to
        # transmit some data to the ``do`` step.
        ...

    @staticmethod
    def do(record, logger, state):
        # Mutate ``record`` to make modifications.
        # Optionally use ``logger`` to log additional info and ``state`` to
        # retrieve some data to the ``do`` step.
        ...


MyCustomAction()
```

Concrete examples can be found [here](https://github.com/inspirehep/inspirehep/blob/master/backend/inspirehep/curation/search_check_do/examples.py) or under [scripts](/scripts/).

#### Logging

By default, when running the script, the output will contain which record was checked and whether the check was positive and hence the record modified. If you want to output additional information from the record in the `check` or `do` phase, you can use the `logger` that's passed to the method. It is an instance of a [structlog](https://www.structlog.org/en/stable/getting-started.html) logger. You can use it similarly to the standard library logger (with methods like `warning` or `info` to be used depending on the importance of the message): you can pass it a string for the message and additional arbitrary arguments with extra data you want to output. For example, you could do

```python
logger.info(
    "More details about the record.",
    title=record["title"],
    first_author=record.set_value("authors[0].full_name"),
)
```

The recid is included automatically, you don't need to add it yourself.
