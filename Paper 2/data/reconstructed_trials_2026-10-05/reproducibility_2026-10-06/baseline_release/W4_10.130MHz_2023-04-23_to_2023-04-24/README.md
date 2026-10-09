# W4: 10.130 MHz field observations

Observed reception interval: **2023-04-23 00:02:00+00:00 to 2023-04-24 23:31:00+00:00 (UTC)**. These are the first and last recovered receptions, not verified operating start/stop times.

## Results

| Measure | Result |
| --- | ---: |
| Received rows | 120 |
| CQ / heartbeat / identifier-only | 90 / 24 / 6 |
| Earlier selection / additional recovered rows | 116 / 4 |
| SNR median [Q1, Q3], dB | -7 [-12.25, -3] |
| SNR range, dB | -23 to 14 |
| Timing offset median [Q1, Q3], seconds | 0.4 [0.3, 0.5] |
| CQ-only SNR median, dB | -8 |
| Most frequent observed CQ spacing, seconds | 615 |

The full statistics file includes all-row, CQ, heartbeat, identifier-only and earlier/additional-selection sensitivities. Empty statistics mean that a subset has no observations, not zero signal strength. Quartiles use linear interpolation (type 7); they are descriptive spreads, not confidence intervals.

## Configuration evidence

- Site: Report pp.18-21: ridge antenna changes on 23 April and battery-change photograph on 24 April for 10.130/14.078 MHz. Exact numbered positions unspecified.
- Radio: Author identification from trial report/photos: QRP at 10 MHz on 23 and 24 April; corroborates diary assignment on 24 April. Exact date-clock alignment and controller identity unresolved.
- Nominal power: 1 W stated for the 92-row chart subset; remaining rows need configuration continuity.
- Operational context: PC reset, antenna damage/repair and CQ/heartbeat changes occur in this diary period; exact affected rows unassigned.
- Documentary source: Diary pp. 18-21; chart 4

The log timestamps are confirmed UTC. This does not independently establish diary time zones or precise setting-change times. Radio/site/power descriptions apply only where documented; they are not assigned to every row by inference.

## Interpretation

This folder is an observation window from the retrospective protocol, not proof of a single constant-configuration experiment. Results describe recovered successful decodes. Complete transmission attempts and endpoint uptime are unavailable, so delivery probability, outage duration, causal band/power effects and an eight-hour service guarantee cannot be calculated. CQ gaps are reception spacings, not measured missed-message runs or application latency.

`received_records.csv` is a processed, deduplicated export with stable IDs and source-file/line provenance. Message text, encoded frames and station identifiers are omitted from this publication export; the measurement rows and traffic categories are unchanged. Original raw logs are not included. See the parent README and `verify_results.py` for validation.
