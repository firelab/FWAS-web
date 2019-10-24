"""
Scheduled and background tasks for FWAS.
"""

from .notify import check_alerts


def run_check_alerts():
    # TODO (lmalott): turn this into a scheduled job
    check_alerts()
