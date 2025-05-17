#!/usr/bin/env bash
# -------------------------------------------------------------
# check.sh
# Installs/uses a dedicated Python venv and runs
# pdf_keyword_scan.py on a PDF or .bib file, with optional
# keyword and group filtering.
# Usage:
#   ./check.sh --file /path/to/file.pdf [--keywords "kw1,kw2"] [--group "GroupName"]
# -------------------------------------------------------------
set -euo pipefail

# Locate this script’s directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
SCRIPT_PATH="$SCRIPT_DIR/pdf_keyword_scan.py"

# Print usage
usage() {
  cat <<EOF
Usage: $0 --file /path/to/file.pdf|file.bib [--keywords "kw1,kw2"] [--group "GroupName"]
Options:
  -f|--file       Path to the PDF or .bib file to scan (required)
  -k|--keywords   Comma-separated list of keywords to search for (optional)
  -g|--group      Name of the keyword group to filter (.bib mode only) (optional)
  -h|--help       Show this help message
EOF
  exit 1
}

# Parse arguments
if [[ $# -eq 0 ]]; then
  usage
fi

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -f|--file)
      INPUT_FILE="$2"; shift 2;;
    -k|--keywords)
      KEYWORDS="$2"; shift 2;;
    -g|--group)
      GROUP_FILTER="$2"; shift 2;;
    -h|--help)
      usage;;
    *)
      echo "Unknown argument: $1"
      usage;;
  esac
done

# Validate required argument
if [[ -z "${INPUT_FILE:-}" ]]; then
  echo "Error: --file is required."
  usage
fi

# Ensure virtual environment exists, create if needed
if [[ ! -d "$VENV_DIR" ]]; then
  echo "🐍 Creating virtual environment in $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install or upgrade dependencies
echo "⬆️  Upgrading pip and installing dependencies"
python -m pip install --upgrade pip
pip install "PyMuPDF<2" bibtexparser

# Build the Python command
CMD=(python3 "$SCRIPT_PATH")
if [[ -n "${KEYWORDS:-}" ]]; then
  CMD+=(-k "$KEYWORDS")
fi
if [[ -n "${GROUP_FILTER:-}" ]]; then
  CMD+=(-g "$GROUP_FILTER")
fi
# finally, add the positional path argument
CMD+=("$INPUT_FILE")

# Run
echo "🚀 Running pdf_keyword_scan.py"
"${CMD[@]}"

# Deactivate venv
deactivate
rm -rf "$VENV_DIR"
echo "✅ Done."
