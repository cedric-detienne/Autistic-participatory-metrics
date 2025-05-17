# pdf\_keyword\_scan Wrapper Script

This repository provides a Bash wrapper script (`check.sh`) that scans a single PDF or an entire corpus defined in a BibTeX file for participatory research keywords. It generates a plain-text report listing every matching sentence (and, if requested, its surrounding sentences via the `--context` flag) along with page numbers and source references. A temporary Python virtual environment is created to run `pdf_keyword_scan.py`, dependencies are installed automatically, and the environment is removed when finished.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)

   * [Options](#options)
   * [Examples](#examples)
4. [Keyword Groups](#keyword-groups)
5. [Integrated Statistics](#integrated-statistics)
6. [Sample Output (.bib mode)](#sample-output-bib-mode)
7. [How It Works](#how-it-works)
8. [Cleanup](#cleanup)

---

## Prerequisites

* **Operating System**: macOS, Linux (with Bash)
* **Python**: Python 3.6 or higher
* **Bash**: version supporting `set -euo pipefail`

Ensure that Python 3 and `bash` are installed and available on your `PATH`.

---

## Installation

1. **Clone the repository** (or copy this folder) to your local machine:

   ```bash
   git clone https://github.com/cedric-detienne/autistic-participatory-metrics.git
   cd autistic-participatory-metrics
   ```

2. **Make the wrapper executable**:

   ```bash
   chmod +x check.sh
   ```

No further installation is required: the script will manage its own Python virtual environment.

---

## Usage

Run the `check.sh` script with the required `--file` argument and optional filtering flags. The generated report begins with a statistical summary of keyword occurrences, followed by detailed hits grouped by semantic families.

```bash
./check.sh --file /path/to/file.pdf [--keywords "kw1,kw2"] [--group "GroupName"]
```

### Options

| Flag               | Description                                                                 | Required? |
| ------------------ | --------------------------------------------------------------------------- | --------- |
| `-f`, `--file`     | Path to the PDF or `.bib` file to analyze                                   | Yes       |
| `-k`, `--keywords` | Comma-separated keywords to search within the document                      | No        |
| `-g`, `--group`    | Name of the semantic keyword group to filter (applies to `.bib` mode)       | No        |
| `--context`        | Include the sentence before and after each keyword occurrence in the output | No        |

---

## Examples

1. **Scan a PDF without filters**

   ```bash
   ./check.sh --file ./corpus/study.pdf
   ```

2. **Scan a PDF with custom keywords**

   ```bash
   ./check.sh \
     --file ./reports/report.pdf \
     --keywords "community engagement"
   ```

3. **Scan a BibTeX library with a group filter**

   ```bash
   ./check.sh \
     --file ./library/research.bib \
     --group "Corpus_A2T_static"
   ```

4. **Combine keywords and group filtering**

   ```bash
   ./check.sh \
     --file ./library/research.bib \
     --group "Corpus_A2T_static" \
     --keywords "co-design"
   ```

---

## Keyword Groups

The script scans for an extensible list of participatory research keywords organized into thematic groups such as:

* **Participatory Research & CBPR** (e.g., "community-based participatory", "CBPR")
* **Involvement & Engagement** (e.g., "public involvement", "stakeholder engagement")
* **Advocacy** (e.g., "autism advocate", "autistic self-advocate")
* **Consultation & Workshops** (e.g., "steering group", "design workshop")
* **Collaboration & Partnership** (e.g., "peer-led", "autistic-led")
* **Stakeholder** (e.g., "community stakeholder")

Each keyword is matched in both singular and plural forms, and the full list is maintained in the `KEYWORD_GROUPS` constant within the Python script. Currently, there are **nearly 70 keywords** across all groups, and this set will evolve as the project advances.

---

## Integrated Statistics

At the beginning of each generated report, a concise statistical summary is provided, including:

* **Total studies**: the number of distinct PDF documents or bibliographic entries analyzed in .bib file.
* **Studies with keyword(s)**: count and percentage of studies where at least one keyword was found.
* **Keyword group breakdown**: for each semantic keyword group, the script lists each keyword along with:

  * the total number of occurrences across all studies, and
  * the number of distinct studies in which the keyword appears.

These metrics help you quickly assess the prevalence of participatory research terms in your corpus before diving into the detailed results.

---

## Sample Output (.bib mode)

Below is an excerpt from a `.bib` report, showing bibliographic headers followed by matched sentences and page numbers.

---

```
--------------------------------------------------------------------        
Pelton, Mirabel K. (2020) – Understanding Suicide Risk in Autistic Adults: Comparing the Interpersonal Theory of Suicide in Autistic and Non-autistic Samples
https://doi.org/10.1007/s10803-020-04393-8        
--------------------------------------------------------------------

 Page 2 – "participatory research":
  "Participatory research has reported that poor understanding and acceptance of such differences is associated with reduced social belonging, independence and quality of life and increased mental health difficulties for autistic people (Cage et al."

 Page 6 – "steering group":
  "Our steering group of autistic adults advised choosing the INQ-10, with comparable validity (Hill et al."

 Page 6 – "participatory method":
  "The VEQ is a 60-item scale which has been developed through participatory methods with autistic adults to reflect adverse life experiences across 10 themes, such as childhood maltreatment, non-suicidal self-injury, bullying and victimisation as a child or adult and discrimination."

 Page 14 – "steering group":
  "Acknowledgments This research has been compiled with the kind support of the Coventry steering group who assisted in selecting and devising the materials for this study."
```

---

## How It Works

1. **Wrapper (`check.sh`)**:

   * Removes any existing `venv/` directory under the script folder.
   * Creates a new Python virtual environment in `venv/`.
   * Activates the environment and installs:

     * `PyMuPDF<2` (for PDF text extraction)
     * `bibtexparser` (for `.bib` parsing)
   * Constructs the Python command with the provided flags and positional file path.
   * Executes `pdf_keyword_scan.py`.
   * Deactivates and deletes the `venv/` folder to clean up.

2. **Scanner (`pdf_keyword_scan.py`)**:

   * Parses the PDF or `.bib` input.
   * Compiles regex patterns for each keyword (with pluralization rules).
   * Extracts sentences (and optional context) containing matches.
   * Writes a structured text report with page numbers, matched phrases, and bibliographic headers (for `.bib` mode).

---

## License

> This script was generated entirely using OpenAI's GPT-4.  
> It is included under the MIT License, in accordance with OpenAI’s Terms of Use.


*For any issues or contributions, please open an issue or pull request on GitHub.*
