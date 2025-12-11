#!/usr/bin/env bash

# ------------------------------------------------------------
# Automated Terminal Setup Script
# ------------------------------------------------------------
# This script performs the following actions:
#   1. Installs the Fira Code Nerd Font (if not already present).
#   2. Installs the Starship prompt using a POSIX‑compatible shell.
#   3. Ensures Cargo's bin directory is on the PATH.
#   4. Adds Starship initialization to ~/.bashrc (or ~/.zshrc if you use Zsh).
#   5. Creates a minimal Starship configuration (~/.config/starship.toml).
#   6. Optionally activates a Python virtual environment named 'myvenv'.
#
# Run this script once after cloning the repository or on a fresh machine.
# ------------------------------------------------------------

set -euo pipefail

# ---------- Helper Functions ----------
log() {
  echo -e "[\033[1;34mINFO\033[0m] $*"
}
error() {
  echo -e "[\033[1;31mERROR\033[0m] $*" >&2
  exit 1
}

# ---------- 1. Install Nerd Font (Fira Code) ----------
FONT_DIR="$HOME/.local/share/fonts"
FIRA_ZIP_URL="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/FiraCode.zip"
if [[ -d "$FONT_DIR" && -n $(find "$FONT_DIR" -name "*FiraCodeNerdFont*.ttf" 2>/dev/null) ]]; then
  log "Fira Code Nerd Font already installed. Skipping download."
else
  log "Downloading and installing Fira Code Nerd Font..."
  mkdir -p "$FONT_DIR"
  curl -L "$FIRA_ZIP_URL" -o "/tmp/FiraCode.zip"
  unzip -o "/tmp/FiraCode.zip" -d "$FONT_DIR"
  rm -f "/tmp/FiraCode.zip"
  fc-cache -f "$FONT_DIR"
  log "Font installation complete."
fi

# ---------- 2. Install Starship (POSIX sh) ----------
if command -v starship >/dev/null 2>&1; then
  log "Starship already installed (version: $(starship --version))."
else
  log "Installing Starship using POSIX sh..."
  curl -fsSL https://starship.rs/install.sh -o /tmp/starship-install.sh
  sh /tmp/starship-install.sh --yes
  rm -f /tmp/starship-install.sh
  log "Starship installation finished."
fi

# ---------- 3. Ensure Cargo bin is on PATH ----------
CARGO_BIN="$HOME/.cargo/bin"
if [[ ":$PATH:" != *":$CARGO_BIN:"* ]]; then
  log "Adding Cargo bin directory to PATH in ~/.profile"
  echo "export PATH=\"$CARGO_BIN:\$PATH\"" >> "$HOME/.profile"
  export PATH="$CARGO_BIN:$PATH"
fi

# ---------- 4. Add Starship init to shell rc ----------
# Detect which shell you primarily use (bash or zsh). Default to bash.
SHELL_NAME="bash"
if [[ "${SHELL##*/}" == "zsh" ]]; then
  SHELL_NAME="zsh"
fi
RC_FILE="$HOME/.${SHELL_NAME}rc"
if ! grep -q "starship init $SHELL_NAME" "$RC_FILE"; then
  log "Appending Starship init to $RC_FILE"
  echo "eval \"\$(starship init $SHELL_NAME)\"" >> "$RC_FILE"
else
  log "Starship init already present in $RC_FILE"
fi

# ---------- 5. Create Starship config (optional) ----------
STARSHIP_CONFIG_DIR="$HOME/.config"
mkdir -p "$STARSHIP_CONFIG_DIR"
STARSHIP_TOML="$STARSHIP_CONFIG_DIR/starship.toml"
if [[ ! -f "$STARSHIP_TOML" ]]; then
  log "Creating default Starship config at $STARSHIP_TOML"
  cat > "$STARSHIP_TOML" <<'EOF'
add_newline = false

[character]
success_symbol = "[❯](bold green)"
error_symbol   = "[❯](bold red)"

[directory]
style = "bold cyan"
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = " "
style = "bold purple"

[python]
symbol = "🐍 "
style = "bold yellow"

[time]
format = "[$time]($style) "
style = "dim white"
EOF
else
  log "Starship config already exists; leaving untouched."
fi

# ---------- 6. Optional: Activate Python virtual environment ----------
if [[ -d "$HOME/Documents/genaiproject/dp/document_portal/myvenv" ]]; then
  log "Adding convenient alias to activate the virtual environment."
  # Add alias to the same rc file used above
  if ! grep -q "alias activate_myvenv" "$RC_FILE"; then
    echo "alias activate_myvenv='source $HOME/Documents/genaiproject/dp/document_portal/myvenv/bin/activate'" >> "$RC_FILE"
    log "Alias 'activate_myvenv' added. Use it in a new terminal to activate the venv."
  fi
else
  log "Virtual environment directory not found; skipping alias creation."
fi

log "Setup complete!"
log "Please restart your terminal or run 'source $RC_FILE' to apply the changes."
