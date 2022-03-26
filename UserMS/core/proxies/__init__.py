"""
-- Proxy
    this is a plugin for creating proxy object and making limitations
    for accessing protected objects whole the project and making scope
    to access proxies.

    * Why we should use proxies?
        We always deal with some objects that we want to use that 
        in project and making limitation for accessing a specified
        object like `request` object or `flash messages`.
        so we make local proxy to handling this problem.

    * How to use local proxy?
        we need a local stack to store objects and protecting them 
        from other object and reduce memorey usage.
        so local proxy lookup only to local stacks and deal with 
        that.
    
    * Let's create a local stack and proxy:

        .. highlight:: python
        .. code-block:: python
            @final
            class Messages(LocalStack):
                pass


            @final
            class Requests(LocalStack):
                pass


            message_context = Messages()
            request_context = Requests()

            message: LocalProxy = LocalProxy[Messages](
                message_context, context=False, stackable=True
            )
            request: Request = LocalProxy[Request](request_context, context=True, stackable=False)
"""

from .proxies import message
from .proxies import request
from .proxies import CurrentUser
