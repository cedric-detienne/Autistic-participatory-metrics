## 1 ▪ Purpose of the `.bib` File

This file consolidates **all publicly accessible bibliographic data** used to build the corpora analysed in the **Autistic Participatory Metrics** project.  
Keeping the references in **BibTeX** format allows us to

* store every citation in **one plain-text file**;
* reuse the data seamlessly with open-source tools (Python, R, etc.);
* track every change through Git version control.

> **Note:** The PDF files linked to each bibliographic entry (i.e., the full-text studies) are **not included in this repository** because they cannot be redistributed without permission.  
> However, JabRef can automatically retrieve most PDFs via their DOI once the `.bib` file is opened.

---

## 2 ▪ Opening and Editing the Library

> **Recommended software:** [**JabRef**](https://www.jabref.org/) — an open-source reference manager available for Windows, macOS and Linux.

* Download JabRef and open .bib file; all entries and groups will load automatically.  
* The project’s **Python scripts** (todo) will interact directly with this file; no conversion is required.

---

## 3 ▪ Structure of a BibTeX Entry (example)

```bibtex
@Article{Lombardi2023,
  author           = {Lombardi, Laura and Le Clerc, Sigrid and Wu, Ching-Lien and Bouassida, Jihène and Boukouaci, Wahid and Sugusabesan, Sobika and Richard, Jean-Romain and Lajnef, Mohamed and Tison, Maxime and Le Corvoisier, Philippe and Barau, Caroline and Banaschewski, Tobias and Holt, Rosemary and Durston, Sarah and Persico, Antonio M. and Oakley, Bethany and Loth, Eva and Buitelaar, Jan and Murphy, Declan and Leboyer, Marion and Zagury, Jean-François and Tamouza, Ryad},
  title            = {A human leukocyte antigen imputation study uncovers possible genetic interplay between gut inflammatory processes and autism spectrum disorders},
  journal          = {Translational Psychiatry},
  year             = {2023},
  volume           = {13},
  number           = {1},
  month            = {July},
  doi              = {10.1038/s41398-023-02550-y},
  issn             = {2158-3188},
  abstract         = {Autism spectrum disorders (ASD) are neurodevelopmental conditions that are, for subsets of individuals, underpinned by dysregulated immune processes including inflammation, autoimmunity, and dysbiosis. (...)},
  file             = {:Lombardi2023.pdf:PDF:https://www.nature.com/articles/s41398-023-02550-y.pdf},
  groups           = {Fund_A2T, Funding_Research, Funding_Research_No_Resp, Fund_EuAims, Corpus_A2T_static, Doc_Type_Research, Source_Doc_A2T_A2TWebsite, Access_Open},
  creationdate     = {2025-04-28T22:34:45},
  modificationdate = {2025-05-15T16:13:35},
  publisher        = {Springer Science and Business Media LLC}
}
```
## 4 ▪ JabRef Groups: Principles and Usage

JabRef supports two types of groups:

| Group type | Description | Example used in this project |
| -----------|-------------| ----------------------------- |
| **Static** | Manually assigned to an entry. | `Corpus_A2T_static`, `Doc_Type_Research`, `Access_Open` |
| **Dynamic**| Automatically created based on criteria (e.g., field, keyword). | Entries with `year > 2020`, etc. |

> **Important:** only **static groups** are written into the `groups` field.  
> Dynamic groups remain defined in JabRef but are not stored in the `.bib` file itself.

### Main Groups in Use (subject to change)

| Group | Purpose |
| ----- | ------- |
| **Funding** | Indicates whether an entry explicitly mentions consortium funding. |
| **Corpus\_A2T\_static** | Confirms inclusion in the AIMS-2-TRIALS corpus. |
| **Doc\_Type** | Identifies the document type: original research, review, protocol, commentary, etc. |
| **Participation** | *(under construction)* flags studies that claim participatory methods involving autistic people. |


---

## 5 ▪ First Corpus: AIMS-2-TRIALS *(in progress)*

The project begins with a corpus of publications funded by (or authored by researchers funded by) the AIMS-2-TRIALS European consortium. (*See: [AIMS-2-TRIALS Consortium Overview](../../docs/case-studies/AIMS-2-TRIALS/aims_2_trials_overview.md)*)


### Inclusion criteria *(initial version)*  
- Studies **listed on the “Publications” page** of the official consortium website ([archived snapshot](<https://web.archive.org/web/20250501093805/https://www.aims-2-trials.eu/news/publications/>)).  
- Additional records retrieved through a structured search on [Europe PMC](<https://europepmc.org>).

### Exclusion criteria *(initial version)*  
- Articles that **do not explicitly mention the consortium**—either by name or grant identifier—in their funding (or equivalent) section.  
- Studies **unrelated to autism**.

> The inclusion and exclusion criteria will be refined and documented in greater detail as the project progresses.

**Objective:** Quantify the share of studies incorporating active autistic participation, using the `Participation` group in the `.bib` file.  
This analysis is yet to be carried out and will be conducted in a transparent and fully documented manner.

A markdown list of all references in this corpus—automatically generated from the latest `.bib` file via the `apa-bib-export` script—can be found here: [corpus_autism_research_list.md](../../corpus/jabref/Export/corpus_autism_research_list.md)

---

## 6 ▪ Interacting via Python Scripts *(to&nbsp;do)*

Python utilities will be added to the `scripts/` folder as the project matures.  
Planned tools include, for example:

- **Keyword-guided corpus scanner**  
  - Iterates over every document in a selected corpus.  
  - Uses a configurable list of keywords commonly linked to indicators of **participatory research** (e.g., *co-design*, *stakeholder panel*, *lived experience*).
  - Extracts the sentence (or surrounding context) where each keyword appears.
  - Compiles all snippets into a structured text file that associates each excerpt with its full bibliographic reference.
  - Serves as a first-pass filter to identify studies that may demonstrate explicit participatory practices.

Additional scripts—for parsing the `.bib` file, generating summary tables, or visualising participation indicators—will also be shared here when ready.


## 7 ▪ Ongoing Development and Availability

The `.bib` library is a **living document** and will evolve as the project progresses:

* **Participation indicators** are refined or expanded.  
* New **research corpora** are integrated.  
* Manual reviews or automated pipelines add, update, or correct JabRef groups.

The file is openly licensed and publicly hosted in this repository.  
Contributions—such as additional references, group corrections, or metadata improvements—are welcome via **pull requests** or **issues**.

---

*Last updated: 15 May 2025*
