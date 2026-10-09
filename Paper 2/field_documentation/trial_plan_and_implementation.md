# Trial plan and implementation

Prepared 7 October 2026 from Mark Butterworth's original trial plan, April 2023 field report, later author clarifications and the current numerical analysis. Page numbers below refer to the printed page numbers in [the original plan](Trial_Plan_original.pdf), which are one less than PDF viewer page numbers.

## Purpose and intended experiments

The plan proposed low-power, low-bandwidth remote sensor messaging through an NVIS-oriented HF link, motivated by trap-status monitoring and reducing servicing visits. It set out three experiments (printed p. 5, with methods on pp. 20–24):

| Planned experiment | Intended design | April 2023 implementation and reported evidence |
| --- | --- | --- |
| Frequency and time-of-day behaviour | Approximately 3.5, 5 and 7 MHz bands; nominal 15-minute transmissions over 24 hours; GPS synchronisation; comparison with ionospheric conditions | Frequencies and antennas were adjusted during the trial, adding 10 and 14 MHz. Repeated decoding occurred at 5.357, 7.078 and 10.130 MHz. The analysis reports seven reception windows, observed cadence, within-window SNR comparisons and contextual foF2 data. |
| Transmitter power and link margin | Proposed levels from 10 mW to 5 W, with alternative schedules depending on access and time | Documented nominal settings include 0.5, 1 and 5 W. Exact chart-to-record matches support the 1 W subsets. The trial demonstrates modest-output reception; it does not execute the whole planned controlled power sweep or identify a minimum reliable power. |
| Deployment reach | A fixed control node, remote relocation in approximately 1 km steps, and additional difficult terrain locations | Accessible Blue Trail, ridge and landing deployments span approximately 0.4–10 km. These support practical deployment experience; they do not form a systematic spatial coverage survey. |

The plan considered several implementation options: separate single-band nodes, sequential single-band trials and a tuned multi-band arrangement. It also proposed a month between battery changes. The current paper reports the implemented field configuration and retains 30-day autonomy as a later system target.

## Planned logging and actual analysis

Printed pp. 19–20 describe recording start/end times, frequency, power, mode, location and configuration changes; pp. 20–21 describe receiver logs and GPS synchronisation. The analysed receiver timestamps are UTC, as confirmed by the author. Explicitly local diary times convert using UTC+8.

The current window boundaries are reception-based analysis rules, not precise hardware operating periods. Approximately timed transitions are preserved as such. The first and last reception in a window are not assumed to be switch-on and switch-off times. The [current configuration table](../data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/inputs/current_configuration.csv) and [chronology](trial_chronology.csv) provide their context.

The raw-message archive is not redistributed in this release. Public processed records retain source references but omit radio-message text and encoded frames. The [protocol](../data/reconstructed_trials_2026-10-05/reproducibility_2026-10-06/ANALYSIS_PROTOCOL_v1.3.txt) specifies the complete identified reception inventory, earlier-selection comparisons and analysis methods.

## Reading the historical plan

The original document is preserved unchanged. References to FT8, candidate equipment, provisional frequencies, coverage ambitions and predicted outcomes describe the planning stage. The field implementation used JS8Call 2.2.0 in Normal mode, with Hermes Lite and QRPGuys DSB2 radio configurations. The paper's reported reception frequencies follow receiver logs.

GPS synchronisation supports decoding; it does not by itself identify the propagation path. The measured temporal patterns support an ionospheric contribution but do not separate pure NVIS from mixed propagation. Planned reserve-wide coverage, delivery reliability and a month of unattended operation are not converted into measured results by publishing the plan.

## Supporting records

The dated field report documents antenna relocation to reduce charging interference, connector/audio/coax problems, a power-related base-station reset, antenna retuning and later equipment recovery. These are included alongside the successful reception results in the chronology. The separate chamber diagnostic was conducted on 26 October 2023 and is not an April field measurement.

The current analysis has no decoded trial-sender messages at 3.578 or 14.078 MHz; the report notes that automatic test-message repetition was not enabled for the SDR configuration on 24 April. Thus an empty decoded record set alone is not a measured propagation failure rate.
