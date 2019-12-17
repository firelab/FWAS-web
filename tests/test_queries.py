from importlib.resources import path as resource_path
import os
import json

from fwas import queries


with resource_path("fwas", "..") as path:
    CACHE_PATH = os.path.join(path, 'tests', 'db_query_output')


# TODO (lmalott): splinter this off into its own package
def run_db_query(fn, record=False):
    """Runs or loads the results of a database query.

    `fn` must be a function that returns `records.RowCollections`.
    If `record` is True, then `fn` is executed and the results
    are serialized to JSON and stored in `CACHE_PATH`.

    If `record` is False, then `fn` is not execute and the results
    are loaded from `CACHE_PATH`.

    This allows us to run database queries and store the results. Similar
    to how the Ruby VCR gem works with external service requests.

    """
    name = fn.__name__
    path = os.path.join(CACHE_PATH, f'{name}.json')
    if record:
        rows = fn()
        with open(path, 'w+') as fh:
            fh.write(rows.export('json'))

    else:
        with open(path, 'r') as fh:
            rows = json.load(fh)

    return rows


def test_alert_violation():
    record = False
    rows = run_db_query(queries.find_alert_violations, record=record)

    assert len(rows) == 7
    row = rows[0]

    assert row['user_id'] == 5
    assert row['reflectivity_violated'] == None
    assert row['temperature_violated']
    assert row['wind_violated']
    assert row['relative_humidity_violated']
    assert not row['precipitation_violated']
