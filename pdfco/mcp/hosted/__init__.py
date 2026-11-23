"""Hosted mode: the PDF.co tools over Streamable HTTP behind an OAuth proxy.

Each request carries a proxy-issued JWT. The proxy swaps it for the user's
PDF.co OAuth token, the verifier exchanges that token for the user's API key
through `/oauth/userinfo`, and the tools call `api.pdf.co` with that key.
"""
