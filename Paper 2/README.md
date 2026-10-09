# BearWave Paper 2: Borneo field trial

Supporting data and analysis for **HF Communication for Rainforest Wildlife Monitoring: Field Evaluation of an NVIS-Oriented System** (working manuscript title).

The April 2023 trial evaluated modest-output HF messaging for conservation monitoring around the Danau Girang Field Centre, Malaysian Borneo. The current analysis covers seven reception windows, deployment context, temporal signal variation, regional ionospheric conditions and a separate October 2023 processor diagnostic test.

## Start here

| Material | Contents |
| --- | --- |
| [Analysis protocol](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/ANALYSIS_PROTOCOL_v1.3.txt) | Current retrospective analysis rules, inclusion decisions, units, time conventions and interpretation |
| [Reproduction guide](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/README.txt) | One-command analysis, dependencies and source boundaries |
| [Data dictionary](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/DATA_DICTIONARY.txt) | Field definitions, units and traffic categories |
| [Finding-to-evidence index](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/claim_evidence.csv) | Manuscript findings linked to inputs and calculated results |
| [Current configuration table](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/inputs/current_configuration.csv) | Radio, nominal RF power and deployment context for each window |
| [Reception windows](data/reconstructed_trials_2026-10-05/test_index.csv) | W1–W7 counts and first/last reception times; per-window files in the same directory |
| [Calculated results](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/results) | SNR/DT summaries, reception intervals, time-of-day comparisons, map analysis and Pi diagnostics |
| [Figures and numerical inputs](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/figures) | Editable plots, source series and solar-interference image |
| [Trial documentation and photographs](field_documentation/README.md) | Original trial plan, plan-to-implementation summary, chronology, equipment details and photo gallery |
| [Data attribution](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/ATTRIBUTION.txt) | GIRO, NEXION, NOAA and Australian Bureau of Meteorology acknowledgments |

## Reproduce the reported numerical results

From the repository root, using Python 3.10 or later:

```bash
python3 "Paper 2/data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/reproduce.py"
```

The core analysis uses the Python standard library and included files; it needs no account, network access or private source folder. It performs 22 checks and writes `results/validation.json`. Do not use Python's `-O` option. The [guide](data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/README.txt) also explains optional extraction from original maps, workbook and trial-report charts; those optional operations use Pillow/openpyxl.

The package reproduces the analysis from processed reception records. Original radio-message text and encoded frames are not redistributed, so upstream raw-log parsing, sender classification and deduplication are outside this rerun. The complete identified reception inventory is analysed, with separate summaries for the earlier selection and additional observations.

## What the evidence supports

Repeated HF message reception was observed at 5.357, 7.078 and 10.130 MHz, including nominal 1 W configurations. The material supports field communication feasibility, temporal signal comparisons and deployment lessons. Reception counts are decoded records, not transmitted-attempt counts or acknowledged alarm deliveries. Thirty-day autonomy and the conditional ten-hour notification budget are system design targets.

The [original trial plan](field_documentation/Trial_Plan_original.pdf) records intended experiments. The [plan-to-implementation summary](field_documentation/trial_plan_and_implementation.md) explains their relationship to the actual trial. The later analysis protocol is explicitly retrospective.

## Earlier material

The existing `analysis/`, `generators/`, `automation/`, `core/`, `utilities/`, `system_monitoring/` and root-level spreadsheet/chart files are retained as earlier research material. Use the dated supplement above for the current manuscript's numerical results. The earlier reception release is preserved, with a [current-analysis pointer](data/reconstructed_trials_2026-10-05/CURRENT_ANALYSIS.txt).

The current manuscript is being edited separately in Overleaf; this update publishes supporting research material rather than an outdated manuscript copy. For an immutable reference, use a GitHub commit permalink for the supplement. The repository does not grant an additional licence over third-party source material; retain its attribution and applicable terms.
