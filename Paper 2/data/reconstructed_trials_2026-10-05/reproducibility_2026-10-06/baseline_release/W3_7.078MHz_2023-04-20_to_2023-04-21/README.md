# W3: 7.078 MHz field observations

Observed reception interval: **2023-04-20 02:15:00+00:00 to 2023-04-21 00:17:30+00:00 (UTC)**. These are the first and last recovered receptions, not verified operating start/stop times.

## Results

| Measure | Result |
| --- | ---: |
| Received rows | 102 |
| CQ / heartbeat / identifier-only | 100 / 0 / 2 |
| Earlier selection / additional recovered rows | 102 / 0 |
| SNR median [Q1, Q3], dB | -12 [-15, -7.25] |
| SNR range, dB | -20 to 2 |
| Timing offset median [Q1, Q3], seconds | 0.7 [0.7, 0.8] |
| CQ-only SNR median, dB | -12 |
| Most frequent observed CQ spacing, seconds | 615 |

The full statistics file includes all-row, CQ, heartbeat, identifier-only and earlier/additional-selection sensitivities. Empty statistics mean that a subset has no observations, not zero signal strength. Quartiles use linear interpolation (type 7); they are descriptive spreads, not confidence intervals.

## Configuration evidence

- Site: Report p.15: ridge deployment, 20 April, with RL1/RL2/RL3 panorama and 3.5/7 MHz settings; exact numbered position for 7 MHz not assigned in text/caption.
- Radio: Author identification from trial report/photos: QRP at 7 MHz on 20 April. Continuation into 21 April and exact date-clock alignment unresolved.
- Nominal power: 1 W stated for the matched chart; diary reports 0.5 W on 21 April without a change time.
- Operational context: 102 rows were stored in the nominal 10 MHz workbook. Do not automatically label the three 21 April UTC rows as 0.5 W.
- Documentary source: Diary pp. 15-16; chart 3

The log timestamps are confirmed UTC. This does not independently establish diary time zones or precise setting-change times. Radio/site/power descriptions apply only where documented; they are not assigned to every row by inference.

## Interpretation

This folder is an observation window from the retrospective protocol, not proof of a single constant-configuration experiment. Results describe recovered successful decodes. Complete transmission attempts and endpoint uptime are unavailable, so delivery probability, outage duration, causal band/power effects and an eight-hour service guarantee cannot be calculated. CQ gaps are reception spacings, not measured missed-message runs or application latency.

`received_records.csv` is a processed, deduplicated export with stable IDs and source-file/line provenance. Message text, encoded frames and station identifiers are omitted from this publication export; the measurement rows and traffic categories are unchanged. Original raw logs are not included. See the parent README and `verify_results.py` for validation.
