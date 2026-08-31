# Create Service in MAc


## Bas


```bash
mkdir -p ~/Library/LaunchAgents
vim ~/Library/LaunchAgents/com.ollama.server.plist
which ollama

/opt/homebrew/bin/ollama

# Start
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.ollama.server.plist

# Enable
launchctl enable gui/$(id -u)/com.ollama.server

# check
launchctl print gui/$(id -u)/com.ollama.server

```
