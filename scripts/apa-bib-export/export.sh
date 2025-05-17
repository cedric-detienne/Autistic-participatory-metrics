#!/usr/bin/env bash
# Usage: export.sh --file /path/to/library.bib [--group GroupName]

# Parse arguments
template="Usage: $0 --file /path/to/file.bib [--group GroupName]"
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -f|--file)
      BIBFILE="$2"; shift 2;;
    -g|--group)
      GROUP="$2"; shift 2;;
    *)
      echo "Unknown argument: $1"; echo "$template"; exit 1;;
  esac
done

if [ -z "$BIBFILE" ]; then
  echo "Error: --file argument is required."
  echo "$template"
  exit 1
fi

# Set up export directory
EXPORT_DIR=$(dirname "$BIBFILE")/Export
rm -rf "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR"

# Create and activate virtual environment
python3 -m venv "$EXPORT_DIR/env"
source "$EXPORT_DIR/env/bin/activate"

# Install dependencies
pip install --upgrade pip
pip install bibtexparser pylatexenc markdown

# Execute Python export script
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
pyscript="$SCRIPT_DIR/apa_bib_export.py"
CMD=(python3 "$pyscript" --file "$BIBFILE")
if [ ! -z "$GROUP" ]; then
  CMD+=(--group "$GROUP")
fi
${CMD[@]}

# Deactivate venv
deactivate