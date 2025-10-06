#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
termux-setup-storage >/dev/null 2>&1 || true
cd "$(dirname "$0")/.."

TS=$(date +%Y%m%d-%H%M%S)
OUT="$HOME/backups"
DEST="/storage/emulated/0/Download"
mkdir -p "$OUT"

MODE="${1:-minimal}"  # minimal | full
NAME="llmbox-$MODE-$TS.zip"

EXCLUDES=(-x ".git/*" -x "node_modules/*")
if [ "$MODE" = "minimal" ]; then
  EXCLUDES+=(-x ".venv/*" -x "__pycache__/*" -x "dist/*" -x "build/*" -x "*.egg-info/*")
fi

echo "🧠 Creating backup: $NAME"
start=$(date +%s)
zip -rv "$OUT/$NAME" . "${EXCLUDES[@]}" | pv -l > /dev/null
end=$(date +%s)
elapsed=$((end - start))

cp "$OUT/$NAME" "$DEST/" || true
sha256sum "$OUT/$NAME" | tee "$OUT/$NAME.sha256"
echo "✅ Backup written to: $OUT/$NAME"
echo "📥 Copy also at: $DEST/$NAME (if permitted)"
echo "⏱️ Duration: ${elapsed}s"
