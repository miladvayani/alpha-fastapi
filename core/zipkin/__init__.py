"""
Applications instrumented with aiozipkin report timing data to zipkin. 
The Zipkin UI also presents a Dependency diagram showing how many traced 
requests went through each application.

If you are troubleshooting latency problems or errors, 
you can filter or sort all traces based on the application, 
length of trace, annotation, or timestamp.

**How to use aiozipkin manager?**

.. code-block:: python

    from zipkin import ZipkinManager
    from zipkin import ZipkinEndpoint
    from zipkin import ZipkinTracerConfig

    zipkin = ZipkinManager(
        configs=ZipkinTracerConfig(
            zipkin_address=root.config["ZIPKIN_ADDRESS"],
            local_endpoint=ZipkinEndpoint(
                serviceName=root.config.get("ZIPKIN_SERVICE_NAME"),
                ipv4="127.0.0.1",
                port=8080,
                ipv6=None,
            ),
        )
    )

            
"""

from .base import ZipkinManager
from .base import ZipkinEndpoint
from .base import ZipkinTracerConfig
from .base import KINDS


__all__ = ["ZipkinManager", "ZipkinEndpoint", "ZipkinTracerConfig", "KINDS"]
