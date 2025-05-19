#!/usr/bin/env bash
# Usage: export.sh --file /path/to/library.bib [--group GroupName] [--output md|tex]
set -euo pipefail

# Print usage
usage() {
  cat <<EOF
Usage: $0 --file /path/to/file.bib [--group GroupName] [--output md|tex]
Options:
  -f|--file     Path to the BibTeX file to export (required)
  -g|--group    Name of the group to filter entries (optional)
  -o|--output   Output format: 'md' for Markdown or 'tex' for LaTeX (default: tex)
  -h|--help     Show this help message
EOF
  exit 1
}

# Default output format
OUTPUT_FORMAT="tex"

# Parse arguments
if [[ $# -eq 0 ]]; then
  usage
fi

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -f|--file)
      BIBFILE="$2"; shift 2;;
    -g|--group)
      GROUP="$2"; shift 2;;
    -o|--output)
      OUTPUT_FORMAT="$2"; shift 2;;
    -h|--help)
      usage;;
    *)
      echo "Unknown argument: $1"
      usage;;
  esac
done

# Validate required argument
if [[ -z "${BIBFILE:-}" ]]; then
  echo "Error: --file is required."
  usage
fi

# Set up export directory
EXPORT_DIR="$(dirname "$BIBFILE")/Export"
rm -rf "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR"

# Create & activate virtual environment
python3 -m venv "$EXPORT_DIR/env"
source "$EXPORT_DIR/env/bin/activate"

# Install dependencies
pip install --upgrade pip
pip install bibtexparser pylatexenc markdown

# Build and run the Python command
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYSCRIPT="$SCRIPT_DIR/apa_bib_export.py"

CMD=(python3 "$PYSCRIPT" --file "$BIBFILE" --output "$OUTPUT_FORMAT")
if [[ -n "${GROUP:-}" ]]; then
  CMD+=(--group "$GROUP")
fi

echo "🚀 Running: ${CMD[*]}"
"${CMD[@]}"

# Deactivate venv
deactivate
echo "✅ Export complete (format: $OUTPUT_FORMAT). Files are in $EXPORT_DIR."
