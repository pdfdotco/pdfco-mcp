import sys

import pytest

import pdfco.mcp as entry


@pytest.fixture
def run(monkeypatch):
    """Capture the arguments main() passes to FastMCP.run instead of starting a server."""
    calls = []
    monkeypatch.setattr(entry.mcp, "run", lambda **kwargs: calls.append(kwargs))
    return calls


def invoke(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["pdfco-mcp", *argv])
    entry.main()


def test_no_arguments_runs_stdio(monkeypatch, run):
    invoke(monkeypatch)
    assert run == [{"transport": "stdio"}]


def test_streamable_http_without_path_uses_fastmcp_default(monkeypatch, run):
    invoke(monkeypatch, "streamable-http", "8000")
    assert run == [{"transport": "streamable-http", "host": "0.0.0.0", "port": 8000}]


def test_streamable_http_with_path(monkeypatch, run):
    invoke(monkeypatch, "streamable-http", "8000", "/pdf")
    assert run[0]["path"] == "/pdf"


def test_sse_without_port_is_rejected(monkeypatch, run):
    with pytest.raises(ValueError, match="sse transport requires a port number"):
        invoke(monkeypatch, "sse")
    assert run == []


def test_unknown_transport_is_rejected(monkeypatch, run):
    with pytest.raises(ValueError, match="Invalid transport: websocket"):
        invoke(monkeypatch, "websocket", "8000")
    assert run == []
