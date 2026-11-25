import os
from dataclasses import dataclass
from typing import Mapping

_REQUIRED = {
    "base_url": "PDFCO_MCP_BASE_URL",
    "upstream_url": "PDFCO_MCP_UPSTREAM_URL",
    "upstream_client_id": "PDFCO_MCP_UPSTREAM_CLIENT_ID",
    "upstream_client_secret": "PDFCO_MCP_UPSTREAM_CLIENT_SECRET",
    "jwt_signing_key": "PDFCO_MCP_JWT_SIGNING_KEY",
}


@dataclass(frozen=True)
class HostedSettings:
    base_url: str
    upstream_url: str
    upstream_client_id: str
    upstream_client_secret: str
    jwt_signing_key: str

    def __repr__(self) -> str:
        # Keep the secrets out of tracebacks and logs.
        return f"HostedSettings(base_url={self.base_url!r}, upstream_url={self.upstream_url!r})"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "HostedSettings":
        env = os.environ if env is None else env
        if env.get("X_API_KEY"):
            raise RuntimeError(
                "X_API_KEY is set. Hosted mode resolves each user's key through "
                "OAuth and must not run with a server-wide key."
            )
        missing = [name for name in _REQUIRED.values() if not env.get(name)]
        if missing:
            raise RuntimeError(
                "Hosted mode needs these environment variables: " + ", ".join(missing)
            )
        values = {field: env[name] for field, name in _REQUIRED.items()}
        values["base_url"] = values["base_url"].rstrip("/")
        values["upstream_url"] = values["upstream_url"].rstrip("/")
        return cls(**values)
