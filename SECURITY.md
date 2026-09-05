# Security Documentation

## Principles
- Never commit secrets to this repository.
- Use environment variables for sensitive data.
- Regularly rotate tokens.
- Only grant necessary permissions to MCP servers.

## Sensitive Files (Git Ignore)
All credentials and runtime state are excluded. Do not unignore them.

```gitignore
.env
.env.*
*.pem
*.key
credentials.*
tokens.*
node_modules/
dist/
build/
logs/
*.log
cache/
```
