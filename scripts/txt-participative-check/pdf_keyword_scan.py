#!/usr/bin/env python3
"""
pdf_keyword_scan.py

A command-line tool to scan PDF or BibTeX (.bib) files for defined thematic keywords,
organize the results by semantic groups, and output matching sentences (with optional
context) along with page numbers and source references.

Features:
  - Defines multiple keyword “families” (e.g., participatory research, engagement,
    advocacy) to group related search terms.
  - Uses PyMuPDF to extract and clean text from PDF pages, handling hyphenated
    line breaks and sentence splitting.
  - Supports .bib files via bibtexparser for bibliographic entries, allowing keyword
    searches in reference metadata.
  - Configurable context mode: include surrounding sentences for richer insights.
  - Provides customizable output writers to merge results, count occurrences,
    and list which documents contain each keyword.
  - Error checks for required dependencies and reports missing packages.

Usage:
    python3 pdf_keyword_scan.py --file path/to/document.pdf [--keywords "kw1,kw2"] [--context]

Requirements:
    - Python 3.6+
    - PyMuPDF (<2):    pip install "PyMuPDF<2"
    - bibtexparser:    pip install bibtexparser
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from typing import List, Tuple, TextIO, Set

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("❌  PyMuPDF is required:  pip install PyMuPDF<2>")

try:
    import bibtexparser
except ImportError:
    sys.exit("❌  The bibtexparser package is required: pip install bibtexparser")

# ---------------------------------------------------------------------------
# Keyword groups (semantic families)
# ---------------------------------------------------------------------------
KEYWORD_GROUPS: List[Tuple[str, List[str]]] = [
    (
        "# ░░ PARTICIPAT* / ACTION-RESEARCH / CBPR ░░",
        [
            "Community-based participatory",
            "community-based participatory research",
            "CBPR",
            "Participatory Autism Research",
            "participatory research",
            "Participatory study",
            "participatory action research",
            "participatory approach",
            "participatory collaboration",
            "participatory decision",
            "participatory design",
            "participatory framework",
            "participatory method",
            "participatory role",
            "participative research",
            "inclusive research",
            "Expert by experience",
            "co-design",
            "co-creation",
        ],
    ),
    (
        "# ░░ INVOLVEMENT & ENGAGEMENT ░░",
        [
            "community involvement",
            "patient involvement",
            "public engagement",
            "public involvement",
            "stakeholder engagement",
            "stakeholder involvement",
            "user involvement",
        ],
    ),
    (
        "# ░░ REPRESENTAT* / ADVOCACY / A-REP ░░",
        [
            "A-REP",
            "autism advocate",
            "autism advocacy",
            "autistic advocate",
            "autistic people representative",
            "autistic representation",
            "autistic representative",
            "autistic self-advocate",
            "autistic researcher",
            "Autism representative",
            "community representative",
            "representative from the autism community",
        ],
    ),
    (
        "# ░░ CONSULTAT* / FORUM / WORKSHOP / GROUP ░░",
        [
            "stakeholder advisory group",
            "community advisory board",
            "community consultation",
            "community forum",
            "stakeholder community",
            "consultation process",
            "consultation with autistic people",
            "consultation with stakeholder",
            "deliberative forum",
            "design workshop",
            "include autistic people",
            "stakeholder consultation",
            "steering committee",
            "steering group",
            "town hall meeting",
            "workshop with stakeholder",
            "codesign workshop",
            "neurodiverse space",
        ],
    ),
    (
        "# ░░ COLLABORAT* / PARTNERSHIP / PEER ░░",
        [
            "collaboration with autistic",
            "community collaboration",
            "equal partner",
            "equitable partner",
            "partnership with autistic",
            "peer-led",
            "autistic-led",
            "peer researcher",
            "stakeholder collaboration",
            "stakeholder perspective",
        ],
    ),
    (
        "# ░░ STAKEHOLDER stand-alone ░░",
        [
            "autism stakeholder",
            "autistic stakeholder",
            "community stakeholder",
            # "community priority",
            # "community priorities",
            # "autistic voice",
        ],
    ),
]

KEYWORDS_DEFAULT: List[str] = [kw for _h, kws in KEYWORD_GROUPS for kw in kws]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compile_patterns(words: List[str]) -> List[Tuple[str, re.Pattern]]:
    """
    Pour chaque mot-clé (potentiellement multi-mot), on découpe en tokens,
    on autorise tiret ou espace entre les tokens, et on applique :
      - « ch » → (?:es)?
      - « y »  → (?:y|ies)
      - sinon → s?
    """
    patterns, seen = [], set()
    for w in words:
        if w in seen:
            continue
        seen.add(w)

        # split sur les espaces (les tirets restent dans le token)
        tokens = w.split()
        esc_tokens = []

        for tok in tokens:
            # échappement + tolérance tiret/espace
            base = re.escape(tok).replace("\\-", "[-\\s]?")
            lower = tok.lower()
            if lower.endswith("ch"):
                # church → church or churches
                esc_tok = base + r"(?:es)?"
            elif lower.endswith("y"):
                # family → family or families
                # on retire le 'y' avant l'alternance
                root = re.escape(tok[:-1]).replace("\\-", "[-\\s]?")
                esc_tok = root + r"(?:y|ies)"
            else:
                # pluriel générique
                esc_tok = base + r"s?"
            esc_tokens.append(esc_tok)

        # on joint les tokens par tiret/espacement facultatif
        esc_pattern = r"[-\s]?".join(esc_tokens)
        pat = re.compile(r"\b" + esc_pattern + r"\b", re.IGNORECASE)
        patterns.append((w, pat))

    return patterns



def clean(text: str) -> str:
    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(s: str) -> List[str]:
    return [frag.strip() for frag in re.split(r"(?<=[.!?])\s+", s) if frag.strip()]

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyse(pdf_path: str, patterns, write_fun, context: bool = False):
    doc = fitz.open(pdf_path)
    dangling = ""
    for idx in range(doc.page_count):
        raw = clean(doc[idx].get_text())
        if not raw:
            continue

        # Gestion de mot-coupé en fin de page
        if dangling:
            raw = dangling + raw
            dangling = ""
        m = re.search(r"(\b\w+)-$", raw)
        if m:
            dangling = m.group(1)
            raw = raw[:-len(m.group(0))]

        # Découpe en phrases
        sents = split_sentences(raw)
        for i, sent in enumerate(sents):
            for kw, pat in patterns:
                if pat.search(sent):
                    if context:
                        prev_sent = sents[i-1] if i > 0 else ""
                        next_sent = sents[i+1] if i < len(sents)-1 else ""
                        # Concatène phrase avant + phrase cible + phrase après
                        ctx = " ".join([ps for ps in (prev_sent, sent, next_sent) if ps])
                        write_fun(idx+1, kw, ctx, pdf_path)
                    else:
                        write_fun(idx+1, kw, sent, pdf_path)
                    break

# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def make_bib_header(entry):
    first_author = entry.get('author','').split(' and ')[0]
    year = entry.get('year','')
    title = entry.get('title','').strip()
    doi = entry.get('doi','')
    url = f"https://doi.org/{doi}" if doi else ''
    return f"\n--------------------------------------------------------------------\
        \n{first_author} ({year}) – {title}\n{url}\
        \n--------------------------------------------------------------------\n\n"


from collections import defaultdict

def make_merged_writer():
    body = []
    counts = defaultdict(int)
    studies = defaultdict(set)
    hit_pdfs = set()
    current = None

    def _w(page, kw, sent, pdf_path):
        # on peut déclarer nonlocal en début de fonction imbriquée
        nonlocal current
        # compte occurrences
        counts[kw] += 1
        # mémorise l'étude pour ce kw
        studies[kw].add(pdf_path)
        # global hits
        hit_pdfs.add(pdf_path)
        # insère un saut quand on change de fichier
        if pdf_path != current:
            body.append('\n')
            current = pdf_path
        body.append(f" Page {page} – \"{kw}\":\n  \"{sent}\"\n\n")

    return _w, body, counts, studies, hit_pdfs


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def write_stats(f: TextIO,
                groups,
                counts: dict,
                studies: dict,
                total: int = None,
                hits: int = None):
    f.write("Keyword occurrences:\n")
    if total is not None and hits is not None:
        pct = hits/total*100 if total else 0
        f.write(f"Total studies           : {total}\n")
        f.write(f"Studies with keyword(s) : {hits}  ({pct:.1f}% )\n\n")
    for hdr, kws in groups:
        f.write(f"{hdr}\n")
        for kw in kws:
            occ = counts.get(kw, 0)
            stu = len(studies.get(kw, []))
            f.write(f" {kw}: {occ} occurrences / {stu} studies\n")
    f.write("\n")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scan PDF or .bib for keywords.")
    ap.add_argument("path", help="PDF file or .bib file to scan")
    ap.add_argument("-g", "--group-filter",
                    help="Filter .bib entries by group keyword (supports OR/AND)")
    ap.add_argument("-k", "--keywords",
                    help="Custom comma-separated keywords")
    ap.add_argument("--context", action="store_true",
                    help="Include the previous and next sentence around each match")
    args = ap.parse_args()

    include_context = args.context

    # Prépare liste de mots-clés et tag pour le nom de fichier
    if args.keywords:
        raw_kw = args.keywords.strip()
        kws = [k.strip() for k in raw_kw.split(",") if k.strip()]
        groups_runtime = [('# Custom keywords', kws)]
        kw_tag = raw_kw.replace(" ", "-").replace(",", "-")
    else:
        kws = KEYWORDS_DEFAULT
        groups_runtime = KEYWORD_GROUPS
        kw_tag = ""

    patterns = compile_patterns(kws)
    target = os.path.abspath(args.path)

    # ----- PDF mode -----
    if os.path.isfile(target) and target.lower().endswith(".pdf"):
        # Writer global
        writer, body, counts, studies, hit_pdfs = make_merged_writer()
        analyse(target, patterns, writer, include_context)

        # Nom de sortie
        base = os.path.splitext(target)[0]
        suffix = f"_{kw_tag}" if kw_tag else ""
        out_name = f"{base}{suffix}_keyword_scan.txt"

        # Écriture
        with open(out_name, "w", encoding="utf-8") as f:
            write_stats(f, groups_runtime, counts, studies)
            f.writelines(body)

        print(f"✅ Results written to {out_name}")
        sys.exit()

    # ----- .bib mode -----
    if os.path.isfile(target) and target.lower().endswith(".bib"):
        bib_dir = os.path.dirname(target)
        with open(target, encoding="utf-8") as bibf:
            db = bibtexparser.loads(bibf.read())

        # Filtrage par groupe(s), si demandé
        entries = db.entries
        if args.group_filter:
            raw = args.group_filter.strip()
            # OR logique
            if re.search(r"\bOR\b", raw, re.IGNORECASE):
                terms = [t.strip().lower().strip('"\'')
                         for t in re.split(r"\bOR\b", raw, flags=re.IGNORECASE)]
                def keep(e):
                    gs = [g.strip().lower() for g in e.get('groups', '').split(',')]
                    return any(term in gs for term in terms)

            # AND logique
            elif re.search(r"\bAND\b", raw, re.IGNORECASE):
                terms = [t.strip().lower().strip('"\'')
                         for t in re.split(r"\bAND\b", raw, flags=re.IGNORECASE)]
                def keep(e):
                    gs = [g.strip().lower() for g in e.get('groups', '').split(',')]
                    return all(term in gs for term in terms)

            # par défaut AND sur virgules ou espaces
            else:
                parts = re.split(r"[,\s]+", raw)
                terms = [t.strip().lower().strip('"\'') for t in parts if t.strip()]
                def keep(e):
                    gs = [g.strip().lower() for g in e.get('groups', '').split(',')]
                    return all(term in gs for term in terms)

            entries = [e for e in entries if keep(e)]

        total = len(entries)

        # Tri par année puis par premier auteur
        def sort_key(e):
            try:
                y = int(e.get('year', '')[:4])
            except ValueError:
                y = 0
            auth = e.get('author', '').split(' and ')[0]
            return (y, auth.lower())
        entries.sort(key=sort_key)

        # Writer global
        w_global, body, counts, studies, hit_pdfs = make_merged_writer()

        # Parcours des références filtrées
        for entry in entries:
            # Extraction du chemin PDF
            ffield = entry.get('file', '')
            m = re.search(r":([^:]+\.pdf):", ffield)
            if not m:
                continue
            pdfname = m.group(1)
            pdfpath = os.path.join(bib_dir, pdfname)
            if not os.path.isfile(pdfpath):
                continue

            # Writer local pour cette entrée
            entry_body = []
            def w_entry(page, kw, sent, pdf_path):
                counts[kw] += 1
                studies[kw].add(pdf_path)
                hit_pdfs.add(pdf_path)
                entry_body.append(f" Page {page} – \"{kw}\":\n  \"{sent}\"\n\n")

            # Analyse avec contexte éventuel
            analyse(pdfpath, patterns, w_entry, include_context)

            # N’ajoute que si on a trouvé quelque chose
            if entry_body:
                body.append(make_bib_header(entry))
                body.extend(entry_body)

        # Nom de sortie .bib
        base_tag = "_bib_keyword_scan"
        suffix = f"_{kw_tag}" if kw_tag else ""
        out = os.path.join(bib_dir, f"{base_tag}{suffix}.txt")

        # Écriture finale
        with open(out, "w", encoding="utf-8") as f:
            write_stats(f, groups_runtime, counts, studies, total, len(hit_pdfs))
            f.writelines(body)

        print(f"✅ Bib report written to {out}")
        sys.exit()

    # Si on arrive ici, c’est une extension non gérée
    ap.error("Path must be a .pdf or .bib file.")

