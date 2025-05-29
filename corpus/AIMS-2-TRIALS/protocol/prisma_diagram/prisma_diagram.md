flowchart TD
    %% ─────────── Styles ───────────
    classDef title fill:#bbdefb,stroke:#0d47a1,stroke-width:2px,color:#0d47a1;
    classDef kept  fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px,color:#1b5e20;
    classDef excl  fill:#ffebee,stroke:#c62828,stroke-width:1px,color:#b71c1c;

    %% ─────────── Global Title ───────────
    T0([Phase A – Corpus-Building<br/><i>First reviewer</i>]):::title

    %% ─────────── Identification ───────────
    subgraph ID [Identification]
      direction TB
      I1[Dimensions search<br/>(n = …)]:::kept
      I2[Initial dataset<br/>(n = …)]:::kept
    end

    %% ─────────── Automatic & Abstract Screening ───────────
    subgraph SC [Automatic & Abstract Screening]
      direction TB
      S1[JabRef: no abstract<br/>(– n)]:::excl
      S2[No autism terms<br/>(– n)]:::excl
      S3[After screening<br/>(n = …)]:::kept
    end

    %% ─────────── Full-text Screening ───────────
    subgraph FT [Full-text Screening]
      direction TB
      F1[Not actually about autism<br/>(– n)]:::excl
      F2[Not in English<br/>(– n)]:::excl
      F3[Duplicate preprints<br/>(– n)]:::excl
      F4[No funding section<br/>(– n)]:::excl
      F5[After full-text screening<br/>(n = …)]:::kept
    end

    %% ─────────── Supplementary Sources ───────────
    subgraph SP [Supplementary Sources]
      direction TB
      P1[Europe PMC<br/>(n = …)]:::kept
      P2[CORDIS<br/>(n = …)]:::kept
      P3[Project website<br/>(n = …)]:::kept
      P4[Duplicates & exclusions<br/>(– n)]:::excl
      P5[Merged dataset<br/>(n = …)]:::kept
    end

    %% ─────────── Funding Eligibility ───────────
    subgraph EL [Funding Eligibility]
      direction TB
      E1[Not funded by A2T<br/>(– n)]:::excl
      E2[Ambiguous support<br/>(– n)]:::excl
      E3[Final corpus<br/>(n = …)]:::kept
    end

    %% ─────────── Flow ───────────
    T0 --> I1 --> I2 --> S1
    S1 --> S2 --> S3 --> F1
    F1 --> F2 --> F3 --> F4 --> F5
    F5 --> P1 & P2 & P3
    P1 --> P4
    P2 --> P4
    P3 --> P4
    P4 --> P5 --> E1 --> E2 --> E3
