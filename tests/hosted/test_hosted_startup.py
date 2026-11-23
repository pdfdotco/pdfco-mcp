import sys

import pytest

import pdfco.mcp as entry
from pdfco.mcp.hosted.settings import HostedSettings

ENV = {
    "PDFCO_MCP_BASE_URL": "https://mcp.test/",
    "PDFCO_MCP_UPSTREAM_URL": "https://oauth.test",
    "PDFCO_MCP_UPSTREAM_CLIENT_ID": "id",
    "PDFCO_MCP_UPSTREAM_CLIENT_SECRET": "secret",
    "PDFCO_MCP_JWT_SIGNING_KEY": "signing",
}


def test_settings_read_from_environment():
    settings = HostedSettings.from_env(ENV)
    assert settings.base_url == "https://mcp.test"
    assert "secret" not in repr(settings) and "signing" not in repr(settings)


@pytest.mark.parametrize("name", sorted(ENV))
def test_missing_setting_fails_startup(name):
    env = {k: v for k, v in ENV.items() if k != name}
    with pytest.raises(RuntimeError, match=name):
        HostedSettings.from_env(env)


def test_server_wide_api_key_refuses_startup():
    with pytest.raises(RuntimeError, match="X_API_KEY"):
        HostedSettings.from_env({**ENV, "X_API_KEY": "k"})


def test_hosted_command_serves_on_the_given_port(monkeypatch):
    import uvicorn

    calls = []
    monkeypatch.setattr(uvicorn, "run", lambda app, **kwargs: calls.append(kwargs))
    for name, value in ENV.items():
        monkeypatch.setenv(name, value)
    monkeypatch.delenv("X_API_KEY", raising=False)
    monkeypatch.setattr(sys, "argv", ["pdfco-mcp", "hosted", "9000"])
    entry.main()
    assert calls[0]["port"] == 9000
