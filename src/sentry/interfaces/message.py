"""
sentry.interfaces.message
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2014 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

__all__ = ('Message',)

from sentry.interfaces.base import Interface
from sentry.utils.safe import trim


class Message(Interface):
    """
    A standard message consisting of a ``message`` arg, and an optional
    ``params`` arg for formatting.

    If your message cannot be parameterized, then the message interface
    will serve no benefit.

    - ``message`` must be no more than 1000 characters in length.

    >>> {
    >>>     "message": "My raw message with interpreted strings like %s",
    >>>     "params": ["this"]
    >>> }
    """
    @classmethod
    def to_python(cls, data, extra={}):
        assert data.get('message')
        kwargs = {
            'message': trim(data['message'], 2048)
        }

        if data.get('params'):
            kwargs['params'] = trim(data['params'], 1024)
        else:
            kwargs['params'] = ()

        position = ""
        if extra:
            position = "%s%s%s" % (extra.get('filename'), extra.get('pathname'), extra.get('lineno'))
        kwargs['position'] = position

        return cls(**kwargs)

    def get_path(self):
        return 'sentry.interfaces.Message'

    def get_hash(self):
        if self.params:
            return [self.message]
        if self.position:
            return [self.position]
        else:
            return [self.message]
