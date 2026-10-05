# W2: 7.078 MHz field observations

Observed reception interval: **2023-04-18 02:16:00+00:00 to 2023-04-18 22:51:15+00:00 (UTC)**. These are the first and last recovered receptions, not verified operating start/stop times.

## Results

| Measure | Result |
| --- | ---: |
| Received rows | 66 |
| CQ / heartbeat / identifier-only | 57 / 0 / 9 |
| Earlier selection / additional recovered rows | 66 / 0 |
| SNR median [Q1, Q3], dB | -4 [-10, 0] |
| SNR range, dB | -16 to 7 |
| Timing offset median [Q1, Q3], seconds | -0.7 [-1.8, -0.025] |
| CQ-only SNR median, dB | -5 |
| Most frequent observed CQ spacing, seconds | 915 |

The full statistics file includes all-row, CQ, heartbeat, identifier-only and earlier/additional-selection sensitivities. Empty statistics mean that a subset has no observations, not zero signal strength. Quartiles use linear interpolation (type 7); they are descriptive spreads, not confidence intervals.

## Configuration evidence

- Site: Report p.11: Ridge second location (RL2), 18 April, 7.078 MHz, dated photograph caption.
- Radio: Author identification from trial report/photos: Hermes Lite at 7 MHz on 18 April. Pi/controller identity and date-clock basis not specified.
- Nominal power: 5 W stated in the historical chart title; not independently calibrated.
- Operational context: Historical curve plots DT, not SNR; it cannot diagnose falling RF power.
- Documentary source: Diary pp. 11-13; chart 2

The log timestamps are confirmed UTC. This does not independently establish diary time zones or precise setting-change times. Radio/site/power descriptions apply only where documented; they are not assigned to every row by inference.

## Interpretation

This folder is an observation window from the retrospective protocol, not proof of a single constant-configuration experiment. Results describe recovered successful decodes. Complete transmission attempts and endpoint uptime are unavailable, so delivery probability, outage duration, causal band/power effects and an eight-hour service guarantee cannot be calculated. CQ gaps are reception spacings, not measured missed-message runs or application latency.

`received_records.csv` is a processed, deduplicated export with stable IDs and source-file/line provenance. Message text, encoded frames and station identifiers are omitted from this publication export; the measurement rows and traffic categories are unchanged. Original raw logs are not included. See the parent README and `verify_results.py` for validation.
