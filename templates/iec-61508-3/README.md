# IEC 61508 Safety Lifecycle Templates

This directory contains StrictDoc templates for the **IEC 61508:2010** functional safety
standard (*Functional safety of electrical/electronic/programmable electronic
safety-related systems*).

The templates cover the software-focused safety lifecycle defined in
IEC 61508-3:2010 and the overall safety management activities of IEC 61508-1:2010.

## Document Set

| File | Document | Standard reference |
|------|----------|--------------------|
| `01_overall_safety_plan.sdoc` | Overall Safety Plan (OSP) | IEC 61508-1:2010, §6.2 |
| `02_hazard_risk_analysis.sdoc` | Hazard and Risk Analysis (HARA) | IEC 61508-1:2010, §7.4, Annex D |
| `03_safety_requirements_spec.sdoc` | Safety Requirements Specification (SRS) | IEC 61508-1:2010, §7.6 |
| `04_sw_safety_requirements_spec.sdoc` | Software Safety Requirements Specification (SSRS) | IEC 61508-3:2010, §7.2 |
| `05_sw_design_spec.sdoc` | Software Design Specification (SDS) | IEC 61508-3:2010, §7.3–7.4 |
| `06_sw_test_spec_report.sdoc` | Software Test Specification and Report (STS/STR) | IEC 61508-3:2010, §7.7–7.8 |
| `07_sw_safety_plan.sdoc` | Software Safety Plan (SSP / SQAP) | IEC 61508-3:2010, §6.2 |

The shared grammar is in `iec_61508_grammar.sgra` and is imported by all
document templates.

## Key Features

### SIL Applicability Fields

Every `REQUIREMENT` node carries four fields that encode the SIL applicability
of the corresponding requirement or technique, based on IEC 61508-3:2010
Tables A.1–A.10:

| Field | Meaning |
|-------|---------|
| `SIL_1` | Applicability at SIL 1 |
| `SIL_2` | Applicability at SIL 2 |
| `SIL_3` | Applicability at SIL 3 |
| `SIL_4` | Applicability at SIL 4 |

Values: `HR` (Highly Recommended), `R` (Recommended), `NR` (Not Recommended),
`--` (Not applicable).

This allows StrictDoc's query engine to filter requirements by SIL level.
For example, to list all requirements that are Highly Recommended at SIL 3:

```
strictdoc export . --filter "SIL_3 == 'HR'"
```

Or in the web UI: use the **Search** panel with the expression above.

### Traceability

The templates are designed with the full traceability chain in mind:

```
HARA (HAZ-xxx)
  └─▶ SRS (SRS-xxx)
        └─▶ SSRS (SSRS-xxx)
              ├─▶ SDS (SDS-xxx)
              └─▶ STS (STS-xxx)
```

Each `REQUIREMENT` node uses `RELATIONS: TYPE: Parent` to establish
upward traceability. StrictDoc generates the bidirectional traceability
matrix automatically.

### Risk Graph (HARA)

The `HAZARD` node models the IEC 61508-1:2010 Annex D Risk Graph parameters:

- `RISK_GRAPH_C` – Consequence (C1–C4)
- `RISK_GRAPH_F` – Frequency/exposure (F1–F2)
- `RISK_GRAPH_P` – Possibility of avoidance (P1–P2)
- `RISK_GRAPH_W` – Probability of unwanted occurrence (W1–W3)
- `SIL_REQUIRED` – SIL determined from the Risk Graph

The `RISK_METHOD_ALT` field is available for documenting alternative risk
estimation methods (e.g. LOPA, numerical risk targets per IEC 61508-1 Annex C).

## Getting Started

1. Install StrictDoc:
   ```
   pip install strictdoc
   ```

2. Copy the `iec-61508/` directory to your project:
   ```
   cp -r templates/iec-61508/ my-project/docs/
   ```

3. Edit `strictdoc.toml` to set the project title and input paths.

4. Start the web server to edit documents interactively:
   ```
   strictdoc server .
   ```

5. Replace all placeholder text (`<...>`) with project-specific content.

6. Assign UIDs following your project's numbering convention.

7. Export to HTML or PDF:
   ```
   strictdoc export .
   ```

## Customisation

The grammar file `iec_61508_grammar.sgra` can be extended to add
project-specific fields. For example, to add an `OWNER` field or a custom
`ASIL`-equivalent field, edit the grammar and add the field to the relevant
element definition.

## Disclaimer

These templates are intended as a starting point to assist engineers in
structuring IEC 61508 safety lifecycle documentation using StrictDoc.
They do **not** constitute legal or certification advice and do **not**
guarantee compliance with IEC 61508 or any regulatory requirement.
The templates must be adapted to the specific system, context, and applicable
SIL by a competent functional safety engineer. Always verify the current version
of IEC 61508 and consult your Functional Safety Assessor.

## References

- IEC 61508-1:2010 – General requirements
- IEC 61508-2:2010 – Requirements for E/E/PE safety-related systems
- IEC 61508-3:2010 – Software requirements
- [StrictDoc documentation](https://strictdoc.readthedocs.io)
