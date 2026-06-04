# EN 50716:2023 Railway Software Development Templates

This directory contains StrictDoc templates for the **EN 50716:2023** standard
(*Railway applications – Communication, signalling and processing systems –
Software for railway control and protection systems*).

EN 50716:2023 supersedes EN 50128:2011 and EN 50657:2017, unifying the software
requirements for both generic railway control software and application data
systems. The templates cover the full software lifecycle defined in EN 50716,
from planning through deployment and maintenance.

## Document set

| File | Documents covered | Table A.1 deliverables | Clause |
|------|-------------------|------------------------|--------|
| `01_software_planning.sdoc` | Software Quality Assurance Plan (SQAP), Planning Verification Report, Software Configuration Management Plan (SCMP), Software Verification Plan (SVP), Software Validation Plan (SValP) | docs 1–5 | §5.3 |
| `02_sw_requirements_spec.sdoc` | Software Requirements Specification (SRS), Overall SW Test Specification, SW Requirements Verification Report | docs 6–8 | §7.2 |
| `03_architecture_design.sdoc` | Architecture Specification, Design Specification, Interface Specifications, Integration Test Specifications, Architecture & Design Verification Report | docs 9–14 | §7.3 |
| `04_component_design.sdoc` | Component Design Specification, Component Test Specification, Component Design Verification Report | docs 15–17 | §7.4 |
| `05_component_impl_test.sdoc` | Source Code, Component Test Report, Source Code Verification Report | docs 18–20 | §7.5 |
| `06_integration.sdoc` | SW Integration Test Report, HW-SW Integration Test Report, SW Integration Verification Report | docs 21–23 | §7.6 |
| `07_overall_testing_validation.sdoc` | Overall SW Test Report, Validation Report, Tools Validation Report, Release Note | docs 24–27 | §7.7 |
| `08_application_data.sdoc` | All application data documents (Application Requirements Specification through Application Release Note) | docs 28–38 | §8 |
| `09_deployment_maintenance.sdoc` | Software Deployment Manual, Deployment Records, Deployment Verification Report, Software Maintenance Plan, Software Change Records, Software Maintenance Records, Software Maintenance Verification Report | docs 39–45 | §9 |

The shared grammar is in `en_50716_grammar.sgra` and is imported by all document templates.

## Key Features

### Software Integrity Levels

EN 50716:2023 defines five integrity levels: **Basic Integrity**, **SIL 1**, **SIL 2**,
**SIL 3**, and **SIL 4**. The `BASIC` field captures applicability at the Basic
Integrity level, which is new compared to IEC 61508. Basic Integrity applies to
software that does not perform safety functions but is part of a safety-related
system.

### SIL Applicability Fields

Every `REQUIREMENT` node carries five fields encoding the applicability of the
corresponding requirement or technique per EN 50716:2023 Table A.1:

| Field | Meaning |
|-------|---------|
| `BASIC` | Applicability at Basic Integrity level |
| `SIL_1` | Applicability at SIL 1 |
| `SIL_2` | Applicability at SIL 2 |
| `SIL_3` | Applicability at SIL 3 |
| `SIL_4` | Applicability at SIL 4 |

Values: `M` (Mandatory), `HR` (Highly Recommended), `R` (Recommended),
`NR` (Not Recommended), `--` (Not applicable).

The `M` value (Mandatory) is used alongside `HR`/`R`/`NR`/`--` and represents
requirements that are unconditionally required at a given integrity level,
regardless of the development approach chosen.

This allows StrictDoc's query engine to filter requirements by integrity level.
For example, to list all requirements that are Mandatory at SIL 4:

```
strictdoc export . --filter "SIL_4 == 'M'"
```

Or in the web UI: use the **Search** panel with the expression above.

### TEST_CASE Nodes

Test specifications use `TEST_CASE` nodes with `RELATIONS: TYPE: Parent, ROLE: Verifies`
to establish explicit traceability from test cases to the requirements they verify.
StrictDoc renders these as a separate "verified by" link in the traceability matrix.

### Dual Spec/Report Format

Some documents cover both specification and result sides within a single file.
For example, `08_application_data.sdoc` covers docs 30/33 (Application Test
Specification and Application Test Report) and docs 36/37 (Application Integration
Test Specification and Application Integration Test Report). Placeholder sections
separate spec from report content.

### ACTION_ITEM Nodes

`ACTION_ITEM` nodes are used for problem reports and change records (DCR-xxx).
Each `ACTION_ITEM` has `STATUS` (Open / Closed / Deferred), `OWNER`, and `DUE_DATE`
fields, and can be linked to the requirement or test case that triggered it.
In `09_deployment_maintenance.sdoc`, DCR-xxx entries document approved software
changes from request through implementation and verification closure.

## Traceability Chain

The templates are designed with the full lifecycle traceability chain in mind:

```
SP (planning, SP-xxx)
  └─▶ SRS (SRS-xxx)
        └─▶ SAD (architecture/design, SAD-xxx)
              └─▶ CD (component design, CD-xxx)
                    └─▶ CI (component implementation, CI-xxx)
                          └─▶ INT (integration, INT-xxx)
                                └─▶ VAL (validation, VAL-xxx)
                                      ├─▶ APP (application data, APP-xxx)
                                      └─▶ DM (deployment/maintenance, DM-xxx)
```

Each `REQUIREMENT` node uses `RELATIONS: TYPE: Parent` to establish upward
traceability. StrictDoc generates the bidirectional traceability matrix automatically.

## Getting Started

1. Install StrictDoc:
   ```
   pipx install strictdoc
   ```

2. Copy the `en-50716/` directory to your project:
   ```
   cp -r templates/en-50716/ my-project/docs/
   ```

3. Start the web server to edit documents interactively:
   ```
   strictdoc server .
   ```

4. Replace all placeholder text (`<...>`) with project-specific content.

5. Assign UIDs following your project's numbering convention (e.g. SP-001, SRS-001).

6. Export to HTML:
   ```
   strictdoc export .
   ```
   To export to PDF, additionally provide `--formats=html,html2pdf`:
   ```
   strictdoc export . --formats=html,html2pdf
   ```

## Relationship to IEC 61508 Templates

EN 50716:2023 uses its own self-contained grammar (`en_50716_grammar.sgra`),
which is **not** compatible with or dependent on the IEC 61508 grammar
(`iec_61508_grammar.sgra`). The two template sets are independent and cannot
be mixed within the same StrictDoc project without custom grammar configuration.
The principal differences from the IEC 61508 templates are the addition of the
`BASIC` integrity level field, the `M` (Mandatory) applicability value, and the
application data lifecycle (Clause 8).

## Disclaimer

These templates are intended as a starting point to assist engineers in
structuring EN 50716:2023 software lifecycle documentation using StrictDoc.
They do **not** constitute legal or certification advice and do **not**
guarantee compliance with EN 50716:2023 or any regulatory requirement.
The templates must be adapted to the specific system, context, and applicable
integrity level by a competent railway software engineer. Always verify the
current version of EN 50716 and consult your Independent Safety Assessor (ISA).

## References

- EN 50716:2023 – Railway applications – Software for railway control and protection systems
- EN 50126-1:2017 – Railway applications – RAMS – Part 1: Generic RAMS process
- EN 50126-2:2017 – Railway applications – RAMS – Part 2: Systems approach to safety
- [StrictDoc documentation](https://strictdoc.readthedocs.io)
