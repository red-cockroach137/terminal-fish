#!/usr/bin/env bash
set -euo pipefail

# ── Directories ─────────────────────────────────────────────
INSTALL_DIR="$HOME/bin"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$INSTALL_DIR"

FILES=(
    "fish_book.py.en"
    "fish_catcher.sh.en"
    "fish_tank.py.en"
    "fish_tank_colors.py.en"   
)

echo "Installing Terminal Fish files to $INSTALL_DIR ..."

# ── Copy files, remove .en suffix, make executable ──────────
for f in "${FILES[@]}"; do
    if [[ ! -f "$REPO_DIR/$f" ]]; then
        echo "❌ $f not found in source directory"
        exit 1
    fi
    dst_name="${f%.en}"
    dst="$INSTALL_DIR/$dst_name"

    cp "$REPO_DIR/$f" "$dst"
    chmod +x "$dst"

    echo "✅ Installed $dst_name → $dst"
done

# ── Detect shell and rc file ───────────────────────────────
SHELL_NAME="$(basename "$SHELL")"
RC_FILE=""
case "$SHELL_NAME" in
    zsh) RC_FILE="$HOME/.zshrc" ;;
    bash) RC_FILE="$HOME/.bashrc" ;;
    *) RC_FILE="$HOME/.bashrc" ;;  # fallback
esac

# ── Detect terminal ─────────────────────────────────────────
TERMINAL_NAME="${TERM_PROGRAM:-${TERM:-unknown}}"
TERMINAL_BLOCK=""
if [[ "$TERMINAL_NAME" == "iTerm.app" || "$TERMINAL_NAME" == "iTerm2" ]]; then
    TERMINAL_BLOCK='[[ -n "$ITERM_SESSION_ID" ]]'
elif [[ "$TERMINAL_NAME" == "kitty" ]]; then
    TERMINAL_BLOCK='[[ -n "$KITTY_WINDOW_ID" ]]'
elif [[ "$TERMINAL_NAME" == "gnome-terminal" || "$TERMINAL_NAME" == "gnome-terminal-server" ]]; then
    TERMINAL_BLOCK='[[ -n "$VTE_VERSION" ]]'
elif [[ "$TERMINAL_NAME" == "alacritty" ]]; then
    TERMINAL_BLOCK='[[ -n "$ALACRITTY_LOG" ]]'
else
    TERMINAL_BLOCK='true'  # fallback, always run
fi

# ── Add fish_catcher.sh auto-start ─────────────────────────
if [[ -n "$RC_FILE" ]]; then
    if ! grep -Fq "_FISH_TAB_RUN" "$RC_FILE"; then
        echo "" >> "$RC_FILE"
        echo "# Auto-run Terminal Fish catcher on new tab" >> "$RC_FILE"
        echo "if $TERMINAL_BLOCK && [[ \$SHLVL -le 2 ]] && [[ -z \"\$_FISH_TAB_RUN\" ]]; then" >> "$RC_FILE"
        echo "    export _FISH_TAB_RUN=1" >> "$RC_FILE"
        echo "    $INSTALL_DIR/fish_catcher.sh" >> "$RC_FILE"
        echo "fi" >> "$RC_FILE"
        echo "✅ Added fish_catcher auto-run to $RC_FILE"
    fi
fi

# ── Add ~/bin to PATH and aliases ──────────────────────────
if [[ -n "$RC_FILE" ]]; then
    # PATH
    if ! grep -Fq 'export PATH="$HOME/bin:$PATH"' "$RC_FILE"; then
        echo "" >> "$RC_FILE"
        echo "# Add ~/bin to PATH for Terminal Fish" >> "$RC_FILE"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$RC_FILE"
        echo "✅ Added ~/bin to PATH in $RC_FILE"
    fi

    # Aliases
    if ! grep -Fq 'alias fish_book="$HOME/bin/fish_book.py"' "$RC_FILE"; then
        echo "# Terminal Fish aliases" >> "$RC_FILE"
        echo 'alias fish_catcher="$HOME/bin/fish_catcher.sh"' >> "$RC_FILE"
        echo 'alias fish_book="$HOME/bin/fish_book.py"' >> "$RC_FILE"
        echo 'alias fish_tank="$HOME/bin/fish_tank.py"' >> "$RC_FILE"
        echo 'alias fish_tank_colors="$HOME/bin/fish_tank_colors.py"' >> "$RC_FILE"
        echo "✅ Added aliases for fish_book, fish_tank, fish_tank_colors"
    fi
fi

echo ""
echo "All done! Restart your shell or run 'source $RC_FILE' to apply changes. cmd -> fish_catcher fish_book fish_tank"
