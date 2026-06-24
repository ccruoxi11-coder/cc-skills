# Stage 08 — Citation & data/code availability (FAIR + ethics)

**Goal:** a reference list and availability/ethics statements that satisfy journal policy and FAIR.

## Steps

1. **References** — export a clean reference-manager file (`.bib`/`.ris`) with verified metadata via
   `scripts/ref_search_verify.py`; match the venue's citation style; remove duplicates and dead DOIs.
2. **Data Availability statement** — for each result-bearing dataset, name the access route:
   *public* (repository + accession/DOI), *controlled access* (committee + procedure), *third-party*
   (owner + how to request), or *restricted* (state the reason and the realistic route). FAIR:
   persistent identifier, license, README/metadata. Don't write "available on reasonable request" as
   the sole route for primary data if a repository is feasible — journals increasingly reject it.
3. **Code Availability** — repository URL/DOI (Zenodo for an archived release), license, version, and
   the environment/seed needed to reproduce. State exactly which results the code reproduces.
4. **Reproducibility specifics** — random seeds, framework versions, hardware, and the exact data
   splits (or a script that regenerates them).
5. **Ethics & privacy** — IRB/ethics approval ID, consent (or waiver), Declaration of Helsinki (or
   institutional/animal equivalent), and the de-identification + applicable regime (HIPAA/GDPR/local).

## Common pitfalls

- "Available on request" used to dodge sharing; missing license; broken accession.
- Code released without environment/seed → not reproducible.
- Inventing an approval number or consent wording — **never**. Use `[待补充：伦理审批号]` and require a
  verified value from the author (this is a legal statement, not prose).

## Output

The `.bib`/`.ris` path, the Data and Code Availability statements (with placeholders where unverified),
and the ethics/privacy paragraph template.
