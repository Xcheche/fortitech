import logging

logger = logging.getLogger(__name__)

def debug_user(strategy, details, user=None, *args, **kwargs):
    logger.debug(
        "DEBUG: user=%r, strategy=%r, details=%r, args=%r, kwargs=%r",
        user, strategy, details, args, kwargs,
    )
    return {}

# If you need this function included in SOCIAL_AUTH_PIPELINE, add the import path
# ('myapp.pipeline.debug_user') to your Django settings (e.g. in settings.py) instead
# of mutating the pipeline at module import time.
