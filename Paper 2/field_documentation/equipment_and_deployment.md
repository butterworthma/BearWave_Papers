# Equipment and deployment context

This summary reflects the current manuscript and author clarifications. It describes the 2023 trial, not the later low-power BearWave design.

| Component | Field configuration |
| --- | --- |
| Control node | Hermes Lite SDR and laptop; SparkSDR 2.0.33 with audio routed to JS8Call 2.2.0 |
| Remote nodes | Hermes Lite 2 SDR with Raspberry Pi 4; QRPGuys DSB2 radio with Raspberry Pi audio/control support |
| Modem operation | JS8Call Normal mode with multi-pass decoding; nominal 15-second transmission cycles |
| Timing | GPS2Time; GPS fix established during setup and GPS connected throughout testing; receiver logs in UTC |
| Antennas | Base fan dipole, initially covering nominal 3.5, 5 and 7 MHz bands, later modified to include 10 and 14 MHz; single-band dipoles at remote nodes |
| Installation | Inverted-V arrangement, longest-element endpoints approximately 1.5 m above ground and elements approximately 45 degrees; no measured centre height is inferred |
| RF checks | Coline DC1500A power meter into a 50-ohm dummy load before deployment; Daiwa CN-101 inline power/SWR meter in the field; settings are nominal transmitter output, not radiated power |
| Deployment reach | Blue Trail, ridge and landing locations at approximately 0.4–10 km from the control node; river and foot access |

The [configuration table](../data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/inputs/current_configuration.csv) associates documented radios, nominal powers and site context with W1–W7. Observation windows can span configuration changes. The 14 MHz radio is documented as the SDR on 24 April; the 23 April radio identity is not independently assigned here.

The [chronology](trial_chronology.csv) records the 25–27 April power changes and the author-corrected 26 April restart around 06:00 UTC. It does not assign precise power/site labels to every received record.

## Separate processor diagnostic

On 26 October 2023, a Raspberry Pi 4/Hermes Lite configuration ran SparkSDR and JS8Call in a professional environmental chamber. The author reports a 30 degrees C setpoint with approximately +/-0.1 degrees C stability. The fully charged battery was inside the chamber and the radio was connected to a dummy load, without live over-the-air reception.

The [original Pi text](../data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/inputs/chamber_pi_results.txt) supplies 1,930 processor records; the [analysis](../data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/reproduce.py) checks temperatures and health flags. The chamber's own logger file was not supplied, so its stability is author-provided context. This separate diagnostic informs power/thermal design; it does not establish the cause of individual field interruptions.
