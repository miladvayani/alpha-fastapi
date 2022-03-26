from dataclasses import dataclass
import ssl as _ssl

from dataclasses import field


@dataclass
class Credentials:
    """Rabbit Robust Connection Crenentials Parameters."""

    host: str
    port: int
    login: str
    password: str
    ssl: bool = True
    ssl_options: dict = field(
        default_factory=dict(
            ca_certs="cacert.pem",
            certfile="cert.pem",
            keyfile="key.pem",
            cert_reqs=_ssl.CERT_REQUIRED,
        )
    )
    client_properties: dict = None

    def dict(self):
        return self.__dict__
