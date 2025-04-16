# PDF.co MCP

#### Sample `.cursor/mcp.json` for test in cursor
```json
{
  "mcpServers": {
    "pdfco": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/pdfco-mcp",
        "run",
        "main.py"
      ],
      "env": {
        "X_API_KEY": "YOUR_TEST_KEY"
      }
    }
  }
}
```