#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="$HOME/bin"

# ── Remove installed files ───────────────────────────────────
FILES=(
    "fish_book.py"
    "fish_catcher.sh"
    "fish_tank.py"
    "fish_tank_colors.py"
)

echo "Removing Terminal Fish files from $INSTALL_DIR ..."
for f in "${FILES[@]}"; do
    dst="$INSTALL_DIR/$f"
    if [[ -f "$dst" ]]; then
        rm "$dst"
        echo "✅ Removed $dst"
    else
        echo "⚠️  $dst not found, skipping"
    fi
done

# ── Detect shell rc file ─────────────────────────────────────
SHELL_NAME="$(basename "$SHELL")"
case "$SHELL_NAME" in
    zsh)  RC_FILE="$HOME/.zshrc" ;;
    bash) RC_FILE="$HOME/.bashrc" ;;
    *)    RC_FILE="$HOME/.bashrc" ;;
esac

# ── Remove injected block from rc file via Python ────────────
if [[ -f "$RC_FILE" ]]; then
    echo "Cleaning $RC_FILE ..."

    python3 - "$RC_FILE" <<'PYEOF'
import sys, re

path = sys.argv[1]
with open(path, "r") as f:
    content = f.read()

# Remove the auto-run block (multiline: comment + if...fi)
content = re.sub(
    r'\n*# Auto-run Terminal Fish catcher on new tab\n'
    r'if .+?_FISH_TAB_RUN.+?\n'
    r'.*?export _FISH_TAB_RUN=1\n'
    r'.*?/bin/fish_catcher\.sh\n'
    r'fi\n?',
    '', content, flags=re.DOTALL
)

# Remove PATH line + its comment
content = re.sub(
    r'\n*# Add ~/bin to PATH for Terminal Fish\n'
    r'export PATH="\$HOME/bin:\$PATH"\n?',
    '', content
)

# Remove aliases block + its comment
content = re.sub(
    r'\n*# Terminal Fish aliases\n'
    r'(?:alias fish_(?:catcher|book|tank|tank_colors)=.*\n)+',
    '', content
)

with open(path, "w") as f:
    f.write(content)

print("✅ Done")
PYEOF

fi

echo ""
echo "All done! Run 'source $RC_FILE' to apply changes."
