# Paper 2: separate Borneo trial results

This release partitions all **1,177 recovered trial-sender receive rows** into the seven observation windows used in Paper 2. It includes the **484 previously selected rows and 693 additional recovered rows**, without selecting on reception quality. The earlier outcome-favouring selection is disclosed in the manuscript; retaining the recovered archive does not eliminate decoding or archive-retention bias.

## Browse the tests

| Window | Frequency MHz | First–last reception dates (UTC) | Rows | Median decoded SNR dB |
| --- | ---: | --- | ---: | ---: |
| [W1](W1_5.357MHz_2023-04-17_to_2023-04-19/README.md) | 5.357 | 2023-04-17–2023-04-19 | 230 | -6 |
| [W2](W2_7.078MHz_2023-04-18_to_2023-04-18/README.md) | 7.078 | 2023-04-18–2023-04-18 | 66 | -4 |
| [W3](W3_7.078MHz_2023-04-20_to_2023-04-21/README.md) | 7.078 | 2023-04-20–2023-04-21 | 102 | -12 |
| [W4](W4_10.130MHz_2023-04-23_to_2023-04-24/README.md) | 10.13 | 2023-04-23–2023-04-24 | 120 | -7 |
| [W5](W5_5.357MHz_2023-04-25_to_2023-04-26/README.md) | 5.357 | 2023-04-25–2023-04-26 | 254 | 6 |
| [W6](W6_10.130MHz_2023-04-25_to_2023-04-27/README.md) | 10.13 | 2023-04-25–2023-04-27 | 183 | -9 |
| [W7](W7_5.357MHz_2023-04-27_to_2023-04-27/README.md) | 5.357 | 2023-04-27–2023-04-27 | 222 | -2 |

Each folder contains received records, descriptive statistics and traffic sensitivities, consecutive CQ reception intervals, a spacing summary, configuration evidence and a readable analysis. `test_index.csv` reconciles the seven windows; `campaign_statistics.csv` gives the full-inventory context.

## What “separate test” means

These are documented observation windows, not seven independent or necessarily unchanged experiments. Windows may overlap in time on different frequencies. W7 is separated by UTC calendar date to expose changed spacing; its start is not a verified configuration change. Missing change times prevent defensible further splitting by site, radio or power. Frequency comes from log contents rather than filenames. Neither absent 3.578/14.078 MHz trial-sender records nor gaps in these windows establish failed-transmission counts.

This release covers the April 2023 Borneo reception analysis. The separate October 2023 chamber diagnostic is not pooled into these field tests.

## Data and definitions

- One row is one retained decoded record, not necessarily a complete application message or independent transmission trial.
- Timestamps are UTC, confirmed by the author as GPS-set. This does not independently verify clock accuracy or incident time zones.
- SNR is the logged decoder estimate in dB; DT is logged timing offset in seconds; audio offset is Hz. Neither is calibrated received power.
- `record_id` is the stable reconstruction identifier; `source_locations` and `frequency_header_locations` preserve original filenames and line numbers. Exact duplicate log copies were consolidated during the earlier reconstruction.
- `in_previous_spreadsheets` marks the earlier selected subset. Categories are CQ, heartbeat and ID_only.
- Station/message text and encoded frames are omitted from this public export; every measurement row, category and source reference remains represented. No private absolute paths, coordinates, raw diary documents or original logs are uploaded.
- Statistics are descriptive: count, minimum, type-7 quartiles, median and maximum. An empty subset has count zero and blank statistics.
- Reception gaps do not identify missed attempts, equipment downtime, propagation failure or alarm-delivery latency. No delivery percentage or eight-hour guarantee is claimed.

## Reproducibility

Run `python3 verify_results.py` in this directory (Python standard library only). It checks file hashes, the exact row partition and counts, every per-window/campaign SNR and DT summary against the records, and the consecutive CQ intervals and spacing summaries. The frozen numerical analysis follows retrospective protocol v1.2, which retained v1.0 descriptive rules. The current paper's results are unchanged by this split.

`provenance.json` records the hashes of the analysed inputs used to prepare this release; `manifest.json` records release-file hashes. Original archive reconstruction remains a separate step: this package validates the split and reported analyses but does not reconstruct from unpublished raw logs.
