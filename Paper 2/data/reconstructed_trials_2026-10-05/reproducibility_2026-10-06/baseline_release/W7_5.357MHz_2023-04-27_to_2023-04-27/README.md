# W7: 5.357 MHz field observations

Observed reception interval: **2023-04-27 00:07:00+00:00 to 2023-04-27 20:59:00+00:00 (UTC)**. These are the first and last recovered receptions, not verified operating start/stop times.

## Results

| Measure | Result |
| --- | ---: |
| Received rows | 222 |
| CQ / heartbeat / identifier-only | 222 / 0 / 0 |
| Earlier selection / additional recovered rows | 0 / 222 |
| SNR median [Q1, Q3], dB | -2 [-6, 1] |
| SNR range, dB | -16 to 14 |
| Timing offset median [Q1, Q3], seconds | -0.8 [-0.9, -0.7] |
| CQ-only SNR median, dB | -2 |
| Most frequent observed CQ spacing, seconds | 315 |

The full statistics file includes all-row, CQ, heartbeat, identifier-only and earlier/additional-selection sensitivities. Empty statistics mean that a subset has no observations, not zero signal strength. Quartiles use linear interpolation (type 7); they are descriptive spreads, not confidence intervals.

## Configuration evidence

- Site: Latest dated site entry is Landing Location 2 on 25 April (report p.21); no dated 27 April location entry. Carry-forward not established.
- Radio: Radio identity on 27 April remains unknown; do not extend the 25 April Hermes Lite assignment without evidence.
- Nominal power: Do not automatically carry forward the 25 April 5 W setting.
- Operational context: Mostly 315-second CQ spacing; first 315-second pair 02:26:00-02:31:15. This is an observed change, not a verified scheduler transition time.
- Documentary source: Author recollection on 5 October 2026; raw logs

The log timestamps are confirmed UTC. This does not independently establish diary time zones or precise setting-change times. Radio/site/power descriptions apply only where documented; they are not assigned to every row by inference.

## Interpretation

This folder is an observation window from the retrospective protocol, not proof of a single constant-configuration experiment. Results describe recovered successful decodes. Complete transmission attempts and endpoint uptime are unavailable, so delivery probability, outage duration, causal band/power effects and an eight-hour service guarantee cannot be calculated. CQ gaps are reception spacings, not measured missed-message runs or application latency.

`received_records.csv` is a processed, deduplicated export with stable IDs and source-file/line provenance. Message text, encoded frames and station identifiers are omitted from this publication export; the measurement rows and traffic categories are unchanged. Original raw logs are not included. See the parent README and `verify_results.py` for validation.
