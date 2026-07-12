# ECSS standards in SDoc format

This folder provides tooling and templates for working with ECSS standards in StrictDoc.

## EARM import script

The [standards/import_ecss_earm_excel.py](standards/import_ecss_earm_excel.py) script converts the ECSS Applicability Requirement Matrix (EARM) Excel export into SDoc files, one SDoc file per ECSS document. This allows the requirements of all ECSS standards to be obtained directly from the official EARM Excel export and turned into StrictDoc-readable documents. See the docstring at the top of the script for step-by-step usage instructions, including where to download the EARM Excel file from and how to generate the StrictDoc HTML export.

The EARM Excel export is flat and does not contain the section/chapter structure of the original standards. [standards/ECSS_TOC.md](standards/ECSS_TOC.md) describes how to recreate this `[[SECTION]]` hierarchy for the generated `.sdoc` files using AI, by deriving the clause/annex tree from each requirement's `ECSS_REQ_ID` and pulling the corresponding section titles from the standard's source PDF.

## ECSS DRDs

The [drd/](drd/) folder provides ECSS Document Requirements Definitions (DRDs) as SDoc templates, organized by standard (e.g. `ECSS-E-ST-40C`) and document type (e.g. `RB`, `TS`).
