# W5: 5.357 MHz field observations

Observed reception interval: **2023-04-25 04:42:30+00:00 to 2023-04-26 23:56:45+00:00 (UTC)**. These are the first and last recovered receptions, not verified operating start/stop times.

## Results

| Measure | Result |
| --- | ---: |
| Received rows | 254 |
| CQ / heartbeat / identifier-only | 246 / 0 / 8 |
| Earlier selection / additional recovered rows | 0 / 254 |
| SNR median [Q1, Q3], dB | 6 [-0.75, 12] |
| SNR range, dB | -20 to 21 |
| Timing offset median [Q1, Q3], seconds | -0.4 [-0.5, -0.2] |
| CQ-only SNR median, dB | 6 |
| Most frequent observed CQ spacing, seconds | 615 |

The full statistics file includes all-row, CQ, heartbeat, identifier-only and earlier/additional-selection sensitivities. Empty statistics mean that a subset has no observations, not zero signal strength. Quartiles use linear interpolation (type 7); they are descriptive spreads, not confidence intervals.

## Configuration evidence

- Site: Report pp.21-22: Landing Location 2, 25 April, 5.357/10.130 MHz. Exact move time and continuity on 26 April not supplied.
- Radio: Author identification from trial report/photos: Hermes Lite at 5 MHz on 25 April. Continuation on 26 April and exact date-clock alignment unresolved.
- Nominal power: 5 W marked in second-location table on 25 April; continuity unverified.
- Operational context: Receiver retuning logged at 04:38:16 on 25 April; first target RX at 04:42:30.
- Documentary source: Diary pp. 21-22

The log timestamps are confirmed UTC. This does not independently establish diary time zones or precise setting-change times. Radio/site/power descriptions apply only where documented; they are not assigned to every row by inference.

## Interpretation

This folder is an observation window from the retrospective protocol, not proof of a single constant-configuration experiment. Results describe recovered successful decodes. Complete transmission attempts and endpoint uptime are unavailable, so delivery probability, outage duration, causal band/power effects and an eight-hour service guarantee cannot be calculated. CQ gaps are reception spacings, not measured missed-message runs or application latency.

`received_records.csv` is a processed, deduplicated export with stable IDs and source-file/line provenance. Message text, encoded frames and station identifiers are omitted from this publication export; the measurement rows and traffic categories are unchanged. Original raw logs are not included. See the parent README and `verify_results.py` for validation.
