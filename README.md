# Autistic Participatory Metrics

**Status**: *Preliminary research phase*

## Project Overview

**Autistic Participatory Metrics** is a citizen-led research initiative aimed at developing empirical methods and tools to assess the extent and quality of participatory approaches in autism research. The project focuses particularly on how autistic individuals are involved in the design, conduct, and dissemination of autism-related scientific work.

This is an independent, exploratory initiative in an early stage of development. It is not affiliated with any research consortium or institution. All contributions are voluntary and made without any conflict of interest (COI).

---

## Objectives

The project currently focuses on three main directions:

### 1. Surveying and Adapting Existing Frameworks

To review tools and frameworks used to evaluate participatory processes in health, social sciences, and disability research. The goal is to:

- Identify which aspects are applicable to autism research,
- Adapt or extend tools where necessary,
- Develop new indicators if existing ones are insufficient.

A dedicated **bibliographic database** has been created to centralize academic resources on participatory practices involving autistic people in autism science.  
This database is **regularly updated** as the project progresses and new relevant sources are identified.

The database is publicly accessible in **BibTeX** format here:  
[`participation_studies.bib`](methodology/jabref/)

The contents are also available as a **structured APA-style list**:  
[`participation_studies_list.md`](methodology/jabref/Export/participation_studies_list.md)


### 2. Developing Document and Corpus Analysis Tools

To build tools to support the identification and analysis of participatory practices within:

- **Individual research articles** (e.g., structured annotations, keyword detection),
- **Research corpora** (e.g., document sets from a single funding source or consortium).

These tools currently include Python scripts:

- **[apa-bib-export](scripts/apa-bib-export)** – a shell wrapper that reads a `.bib` file and produces APA-style bibliographies in Markdown or html.
- **[txt-participative-check](scripts/txt-participative-check)** –  a shell wrapper that scans PDFs (or a corpus defined in a `.bib` file) for **participatory research keywords** and outputs a structured text report.

### 3. Creating Analytic Frameworks for Participation

To explore methods to:

- Analyze how autistic individuals are represented in the research process (as authors, advisors, co-researchers, participants),
- Document these roles systematically across multiple documents or corpora,
- Compare degrees and types of participation over time or across projects.

---

## Application to Research Corpora

The first case study will focus on **peer-reviewed publications** resulting from research funded by the [AIMS-2-TRIALS](docs/case-studies/AIMS-2-TRIALS/aims_2_trials_overview.md) European consortium.

These publications will form the analysed corpus and serve as the basis for evaluating participatory practices.

All collected and processed documents are either publicly available or shared with the explicit consent of their authors.

The analysis will be fully independent from the consortium or its members.

---

## License and Contribution

All tools, indicators, and analyses are developed independently and non-commercially. No conflicts of interest apply. 

The source code is available under the **MIT License** (for code), and content is shared under the **Creative Commons Attribution 4.0 License (CC-BY 4.0)**.

Contributions are welcome. Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.
