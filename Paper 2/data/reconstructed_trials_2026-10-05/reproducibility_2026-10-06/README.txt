BearWave Paper 2 — reproducibility supplement
Prepared 6 October 2026; repository release assembled 7 October 2026
Retrospective protocol amendment v1.3

QUICK START

From this folder, run:
    python3 reproduce.py

Python 3.10 or later is recommended. The core analysis uses only the Python
standard library: no Excel, network connection, account, or original private
folder structure is required. Run without Python's -O option because the
historical baseline verifier uses assertions.

The command recomputes the results from the included inputs, compares them
against the numerical analysis used by the manuscript, checks the plotted
distribution coordinates, and writes results/validation.json. To leave the
provided results untouched, use:
    python3 reproduce.py --output /path/to/new/results

WHAT IS REPRODUCED

* All seven observation-window assignments from explicit frequency/date rules.
* Reception and traffic counts; type-7 SNR/DT summaries; traffic and original-
  selection sensitivity comparisons; consecutive test-message spacings.
* All four-hour local-time SNR bins, including both reported 7 MHz comparisons.
* The 126, 102 and 92 reception matches to the report's nominal-1-W charts.
* Map colour classification from original RGB pixels, three patch sizes,
  reception-to-map matching, hourly summaries and dawn/day/evening medians.
* The Darwin and Guam series used in the ionosonde figure.
* The original Pi diagnostic text, processor-temperature range and health flags.
* Every numerical coordinate in the manuscript's SNR/DT distribution figure.

The results reproduce the reported values. They do not supply missing
transmission-attempt counts or change the study into a reliability experiment.

STARTING POINTS AND SOURCE BOUNDARIES

The reception analysis starts from the processed records in the existing public
release. Message text and encoded frames are omitted. Original source filenames
and line references are retained. This supplement verifies the analysis from
those records, not the upstream raw-log parsing, sender classification or
deduplication. That distinction is explicit in ANALYSIS_PROTOCOL_v1.3.txt.

The map inputs contain every RGB pixel in the 7 x 7 patch around the study
location for each of 667 maps, plus the original legend colours, timestamps
and whole-image hashes. All nested 3 x 3 and 5 x 5 classifications can therefore
be recomputed without distributing the full third-party images. Original PNGs
are not included. extract_sources.py can repeat extraction from the originals.

The supplied ionosonde workbook is not included. Its exact 2023 columns are
included as numerical series; re-extraction from the unchanged workbook was
checked byte-for-byte during preparation. The original trial-report charts
likewise supply the included numerical points for nominal-power subset matching.
The power assignment is documentary; it is not a measured value for each row.

OPTIONAL UPSTREAM EXTRACTION

For map PNGs, install Pillow. For workbook reading, install openpyxl. The core
reproduction above needs neither. Example, using your own source paths:
    python3 extract_sources.py --maps "/path/to/Marks HF maps" --output extracted
    python3 extract_sources.py --workbook "/path/to/Complete (version 1).xlsx" --output extracted
    python3 extract_sources.py --trial-report "/path/to/DGFC Trials Results -v1.docx" --output extracted

Compare extracted files with their same-named counterparts in inputs/. Source
hashes and sheet/cell ranges are documented in provenance.json and the protocol.
Do not overwrite inputs while validating. No original source file is modified.

READING THE PACKAGE

ANALYSIS_PROTOCOL_v1.3.txt explains retrospective choices and interpretation.
DATA_DICTIONARY.txt defines units, categories, missing values and time bases.
claim_evidence.csv maps manuscript findings to their inputs and outputs.
PUBLICATION_STATUS.txt records the baseline snapshot and this repository release.
ATTRIBUTION.txt preserves external-data acknowledgments and provenance limits.
inputs/ contains the processed observations and explicit window rules.
expected/ freezes the earlier results for independent comparison, not calculation.
results/ contains the rerun results and validation report.
figures/ contains the reviewed editable plots and their numerical data.
baseline_release/ preserves the earlier publication export for reconciliation.

CURRENT VERSUS HISTORICAL DOCUMENTATION

Historical configuration notes and eight-hour target references in
baseline_release/ are preserved for provenance. They are superseded by the
current protocol and inputs/current_configuration.csv, not silently rewritten.
The present design scenario uses a ten-hour notification budget, conditional
on the animal-care protocol and the assumed two-hour staff-response allowance.
Neither ten-hour delivery nor 30-day autonomy is a measured outcome here.

The original publication manifest referenced .gitignore, which was absent from
the checked GitHub commit. Its exact hash-matching local-release copy has been
restored inside baseline_release/. No published measurement was changed.

This directory is the repository release of the validated supplement. Its
original numerical inputs and calculation rules are unchanged. The companion
field-documentation folder provides the historical trial plan, an implementation
summary, a dated chronology and a selected photo gallery. See the Paper 2
landing page for links. The paper itself is being edited separately in Overleaf.

OPTIONAL FIGURE PREVIEW
From this folder, run pdflatex figures_preview.tex using a TeX installation
with PGFPlots. The data and distribution coordinates are checked by reproduce.py.
No changes to the article layout are required.
