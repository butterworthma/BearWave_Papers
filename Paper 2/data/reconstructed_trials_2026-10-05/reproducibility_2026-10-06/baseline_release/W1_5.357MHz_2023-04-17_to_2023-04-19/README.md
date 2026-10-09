# W1: 5.357 MHz field observations

Observed reception interval: **2023-04-17 06:31:30+00:00 to 2023-04-19 10:59:30+00:00 (UTC)**. These are the first and last recovered receptions, not verified operating start/stop times.

## Results

| Measure | Result |
| --- | ---: |
| Received rows | 230 |
| CQ / heartbeat / identifier-only | 228 / 0 / 2 |
| Earlier selection / additional recovered rows | 200 / 30 |
| SNR median [Q1, Q3], dB | -6 [-13, 3] |
| SNR range, dB | -21 to 23 |
| Timing offset median [Q1, Q3], seconds | 0.7 [0.5, 0.8] |
| CQ-only SNR median, dB | -6 |
| Most frequent observed CQ spacing, seconds | 615 |

The full statistics file includes all-row, CQ, heartbeat, identifier-only and earlier/additional-selection sensitivities. Empty statistics mean that a subset has no observations, not zero signal strength. Quartiles use linear interpolation (type 7); they are descriptive spreads, not confidence intervals.

## Configuration evidence

- Site: Report p.5: Blue Trail, first location, 17 April, 5.357 MHz; p.9: Ridge first location (RL1), 18 April, 5.357 MHz. Exact move time not supplied.
- Radio: Author identification from trial report/photos: QRP at 5 MHz on 18 April. Radio on 17 and 19 April not specified; no change times or date-clock basis supplied.
- Nominal power: 1 W documented for the 126-row chart subset only; other rows unassigned.
- Operational context: Receiving antenna relocated on 17 April; exact observation boundary unknown.
- Documentary source: Diary pp. 5-6, 9; chart 1

The log timestamps are confirmed UTC. This does not independently establish diary time zones or precise setting-change times. Radio/site/power descriptions apply only where documented; they are not assigned to every row by inference.

## Interpretation

This folder is an observation window from the retrospective protocol, not proof of a single constant-configuration experiment. Results describe recovered successful decodes. Complete transmission attempts and endpoint uptime are unavailable, so delivery probability, outage duration, causal band/power effects and an eight-hour service guarantee cannot be calculated. CQ gaps are reception spacings, not measured missed-message runs or application latency.

`received_records.csv` is a processed, deduplicated export with stable IDs and source-file/line provenance. Message text, encoded frames and station identifiers are omitted from this publication export; the measurement rows and traffic categories are unchanged. Original raw logs are not included. See the parent README and `verify_results.py` for validation.
