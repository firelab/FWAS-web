from datetime import datetime
from urllib.parse import urljoin

import pytz
from flask import request
from flask_wtf import Form


def get_current_utc_datetime():
    return datetime.now(pytz.utc)


def safe_next_url(target: str) -> str:
    """
    Ensure a relative URL path is on the same domain as this host.
    This protects against the 'Open redirect vulnerability'.
    """
    return urljoin(request.host_url, target)


class ModelForm(Form):
    def __init__(self, obj=None, prefix="", **kwargs):
        Form.__init__(self, obj=obj, prefix=prefix, **kwargs)
        self._obj = obj
