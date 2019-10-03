def check_alerts():
    """
    1. Retrieve alert
    2. Create a buffer around the alert location with radius
    3. Compute the band min/max values within that radius
    4. Check values against preconfigured alert thresholds
    5. Record violations and queue notifications to be sent.
    """
