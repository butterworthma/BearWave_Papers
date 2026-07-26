#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from math import sin, cos, asin, acos, atan2, pi, floor
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('MacOSX')  # Use native macOS backend for plot display
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator

# ============ CONFIG ============
FILES = [
    "output/final7.1_new.xlsx",
    "output/final_10.130.xlsx",
    "output/5_GHZ_Standardized_data_preview__first_200_rows_.csv",
    # add more files here...
]

# BEST QUALITY PERIODS (no data loss, highest quality scores)
BEST_QUALITY_PERIODS = {
    'final_7.1.xlsx': {
        'start': '2023-04-18 02:16:00',
        'end': '2023-04-18 11:25:00',
        'duration': '9h 9m',
        'records': 35,
        'quality_score': 0.456,
        'description': 'Morning period - excellent SNR stability'
    },
    'final_10.130.xlsx': {
        'start': '2023-04-20 02:25:00',
        'end': '2023-04-20 17:35:45',
        'duration': '15h 10m',
        'records': 82,
        'quality_score': 0.622,
        'description': 'Full day coverage - best continuous period'
    },
    '5_GHZ_Standardized_data_preview__first_200_rows_.csv': {
        'start': '2023-04-18 01:25:00',
        'end': '2023-04-19 05:41:00',
        'duration': '28h 16m',
        'records': 145,
        'quality_score': 0.741,
        'description': 'Multi-day period - highest quality score'
    }
}

# Danau Girang Field Centre
LAT = 5.4139
LON = 118.0385
LOCAL_TZ = ZoneInfo("Asia/Kuching")

GENERATE_PLOTS = True     # set False if you only want the enriched files
DISPLAY_PLOTS = True      # set False to save plots without displaying them
MA_WINDOW = 5             # smaller window for higher quality data
USE_BEST_QUALITY_ONLY = True  # Filter to best quality periods only
# ===============================


# ---------- Solar utils (NOAA-ish) ----------
def deg2rad(d): return d * pi / 180.0
def rad2deg(r): return r * 180.0 / pi

def julian_day(d: date) -> float:
    y, m, D = d.year, d.month, d.day
    if m <= 2: y -= 1; m += 12
    A = floor(y/100)
    B = 2 - A + floor(A/4)
    return floor(365.25*(y + 4716)) + floor(30.6001*(m + 1)) + D + B - 1524.5

def jd_to_jcent(jd): return (jd - 2451545.0) / 36525.0

def solar_coords(jc):
    M = deg2rad((357.52911 + jc*(35999.05029 - 0.0001537*jc)) % 360.0)
    L0 = (280.46646 + jc*(36000.76983 + jc*0.0003032)) % 360.0
    C = (deg2rad(1.914602 - jc*(0.004817 + 0.000014*jc))*sin(M)
         + deg2rad(0.019993 - 0.000101*jc)*sin(2*M)
         + deg2rad(0.000289)*sin(3*M))
    lam = deg2rad((L0 + rad2deg(C)) % 360.0)
    eps = deg2rad(23.439291 - jc*(0.0130042 + jc*(1.64e-7 - 5.04e-7*jc)))
    delta = asin(sin(eps)*sin(lam))
    alpha = atan2(cos(eps)*sin(lam), cos(lam))
    return M, lam, delta, alpha, eps

def hour_angle(lat_rad, dec, altitude=-0.833):
    alt = deg2rad(altitude)
    cosH = (sin(alt) - sin(lat_rad)*sin(dec)) / (cos(lat_rad)*cos(dec))
    cosH = min(1.0, max(-1.0, cosH))
    return acos(cosH)

def solar_transit_jd(jd, lw):
    n = round(jd - 2451545.0009 - lw/(2*pi))
    Japprox = 2451545.0009 + lw/(2*pi) + n
    M_ = deg2rad((357.5291 + 0.98560028*(Japprox - 2451545)) % 360.0)
    lam_ = deg2rad((280.160 + 1.915*sin(M_) + 0.020*sin(2*M_) + 0.0003*sin(3*M_)) % 360.0)
    return 2451545.0009 + lw/(2*pi) + n + 0.0053*sin(M_) - 0.0069*sin(2*lam_)

def jd_to_utc_datetime(jd):
    J = jd + 0.5
    Z = int(J); F = J - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25)/36524.25)
        A = Z + 1 + alpha - int(alpha/4)
    B = A + 1524
    C = int((B - 122.1)/365.25)
    D = int(365.25 * C)
    E = int((B - D)/30.6001)
    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715
    day_int = int(day)
    frac = day - day_int
    seconds = int(round(frac * 86400))
    return datetime(year, month, day_int, tzinfo=timezone.utc) + timedelta(seconds=seconds)

def sunrise_sunset_local(d: date, lat_deg: float, lon_deg: float, tz: ZoneInfo):
    jd = julian_day(d)
    jc = jd_to_jcent(jd)
    _, _, dec, _, _ = solar_coords(jc)
    lw = deg2rad(-lon_deg)  # west negative; lon_deg>0 (east) => negative lw
    H = hour_angle(deg2rad(lat_deg), dec, altitude=-0.833)
    Jtransit = solar_transit_jd(jd, lw)
    Jrise = Jtransit - rad2deg(H)/360.0
    Jset  = Jtransit + rad2deg(H)/360.0
    sr = jd_to_utc_datetime(Jrise).astimezone(tz).replace(tzinfo=None)
    ss = jd_to_utc_datetime(Jset ).astimezone(tz).replace(tzinfo=None)
    return sr, ss
# -----------------------------------------


def read_table_any(p: Path) -> pd.DataFrame:
    ext = p.suffix.lower()
    if ext in {".csv", ".txt"}:
        return pd.read_csv(p)
    if ext in {".xlsx", ".xlsm"}:
        import openpyxl  # ensure installed
        df = pd.read_excel(p, engine="openpyxl")
        # Check if first row looks like data instead of headers
        import datetime
        if len(df.columns) > 2 and isinstance(df.columns[0], (pd.Timestamp, datetime.datetime)):
            # Likely no headers, reload with header=None and assign column names
            df = pd.read_excel(p, engine="openpyxl", header=None)
            # Assign generic column names, we'll map them later
            df.columns = [f"Col_{i}" for i in range(len(df.columns))]
            # Try to identify Date, Time, SNR columns by position and content
            if len(df.columns) >= 3:
                df = df.rename(columns={"Col_0": "Date", "Col_1": "Time", "Col_2": "SNR_DB"})
        return df
    if ext == ".xls":
        import xlrd
        return pd.read_excel(p, engine="xlrd")
    if ext == ".xlsb":
        import pyxlsb
        return pd.read_excel(p, engine="pyxlsb")
    # fallback try as Excel
    import openpyxl
    return pd.read_excel(p, engine="openpyxl")


def ensure_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure a proper Date column of dtype datetime64[ns] normalized to midnight."""
    if "Date" in df.columns:
        out = df.copy()
        out["Date"] = pd.to_datetime(out["Date"], errors="coerce").dt.normalize()
        return out

    # Try detect a DateTime-like column
    dt_col = None
    for c in df.columns:
        name = str(c).lower()
        if name in ("datetime", "timestamp", "date_time", "datetime_local", "datetime_utc"):
            dt_col = c; break
        if "date" in name and "time" in name:
            dt_col = c; break
    if dt_col is None:
        dt_col = df.columns[0]  # last resort

    out = df.copy()
    dt = pd.to_datetime(out[dt_col], errors="coerce")
    out["Date"] = dt.dt.normalize()
    return out


def compute_sun_table(dates, lat, lon, tz):
    recs = []
    for d in sorted({d for d in pd.to_datetime(dates).dt.date if pd.notna(d)}):
        sr, ss = sunrise_sunset_local(d, lat, lon, tz)
        recs.append({"Date": pd.Timestamp(d), "Sunrise": sr, "Sunset": ss})
    sun = pd.DataFrame(recs)
    if not sun.empty:
        sun["Date"] = pd.to_datetime(sun["Date"]).dt.normalize()
    return sun


def filter_to_best_quality_period(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    """Filter dataframe to the best quality period for this file"""

    if not USE_BEST_QUALITY_ONLY:
        return df

    # Get the filename without path
    file_key = Path(filename).name

    if file_key not in BEST_QUALITY_PERIODS:
        print(f"Warning: No best quality period defined for {file_key}")
        return df

    period_info = BEST_QUALITY_PERIODS[file_key]

    # Create DateTime column if it doesn't exist
    if 'DateTime' not in df.columns:
        if 'Date' in df.columns and 'Time' in df.columns:
            df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))
        else:
            print(f"Warning: Cannot create DateTime column for {file_key}")
            return df

    # Filter to best quality period
    start_time = pd.to_datetime(period_info['start'])
    end_time = pd.to_datetime(period_info['end'])

    print(f"Filtering {file_key} to best quality period:")
    print(f"  Period: {start_time} to {end_time}")
    print(f"  Duration: {period_info['duration']} ({period_info['records']} expected records)")
    print(f"  Quality Score: {period_info['quality_score']:.3f}")
    print(f"  Description: {period_info['description']}")

    # Apply filter
    filtered_df = df[(df['DateTime'] >= start_time) & (df['DateTime'] <= end_time)].copy()

    print(f"  Result: {len(filtered_df)} records (was {len(df)})")

    if filtered_df.empty:
        print(f"  Warning: No data found in best quality period for {file_key}")

    return filtered_df

def enrich_file(in_path: Path, lat, lon, tz) -> Path:
    print(f"\nProcessing: {in_path.name}")

    df = read_table_any(in_path)
    df = ensure_date_column(df)

    # Filter to best quality period if enabled
    df = filter_to_best_quality_period(df, str(in_path))

    if df.empty:
        print(f"  Skipping {in_path.name} - no data after filtering")
        return None

    sun_df = compute_sun_table(df["Date"], lat, lon, tz)
    merged = pd.merge(df, sun_df, on="Date", how="left")

    # Ensure Sunrise and Sunset columns are datetime objects for plotting
    if 'Sunrise' in merged.columns:
        merged['Sunrise'] = pd.to_datetime(merged['Sunrise'], errors='coerce')
    if 'Sunset' in merged.columns:
        merged['Sunset'] = pd.to_datetime(merged['Sunset'], errors='coerce')

    # Save alongside input with appropriate suffix
    suffix = "_best_quality_with_sun" if USE_BEST_QUALITY_ONLY else "_with_sun"

    if in_path.suffix.lower() in {".csv", ".txt"}:
        out_path = in_path.with_name(in_path.stem + suffix + ".csv")
        merged.to_csv(out_path, index=False)
    else:
        out_path = in_path.with_name(in_path.stem + suffix + ".xlsx")
        try:
            import openpyxl  # ensure writer available
            merged.to_excel(out_path, index=False)
        except Exception:
            out_path = in_path.with_name(in_path.stem + suffix + ".csv")
            merged.to_csv(out_path, index=False)

    print(f"  Saved: {out_path.name}")
    return out_path


def optional_plot(in_or_enriched_path: Path, site_name: str, window: int):
    """Make a night-shaded SNR plot if columns allow. Saves PNG next to file."""
    try:
        df = read_table_any(in_or_enriched_path)
    except Exception:
        # Try reading enriched xlsx if input was csv and vice versa
        alt = in_or_enriched_path.with_suffix(".xlsx")
        df = read_table_any(alt) if alt.exists() else read_table_any(in_or_enriched_path)

    # We need Date + either DateTime or (Date+Time). And SNR_DB.
    if "DateTime" not in df.columns:
        if "Time" in df.columns:
            # Normalize Time to HH:MM for consistency
            t_try = None
            for fmt in ("%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p"):
                tt = pd.to_datetime(df["Time"], format=fmt, errors="coerce")
                if tt.notna().sum() >= int(0.8 * len(df)):
                    t_try = tt; break
            if t_try is None:
                t_try = pd.to_datetime(df["Time"], errors="coerce")
            df["Time"] = np.where(t_try.notna(), t_try.dt.strftime("%H:%M"), df["Time"].astype(str))
            df["DateTime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"],
                                            format="%Y-%m-%d %H:%M", errors="coerce")
        else:
            # Without Time, plotting over hours won't make sense
            return
    else:
        # Ensure DateTime column is datetime type (might be string from CSV)
        df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")

    # Ensure Date column is datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Ensure Sunrise/Sunset columns are datetime if they exist (might be strings from CSV)
    if "Sunrise" in df.columns:
        df["Sunrise"] = pd.to_datetime(df["Sunrise"], errors="coerce")
    if "Sunset" in df.columns:
        df["Sunset"] = pd.to_datetime(df["Sunset"], errors="coerce")

    if "SNR_DB" not in df.columns:
        # Try to guess SNR column
        snr_col = None
        lowers = {str(c).strip().lower(): c for c in df.columns}
        for key in ("snr_db", "snr (dbm)", "snr (db)", "snr(db)", "snr"):
            if key in lowers:
                snr_col = lowers[key]; break
        if snr_col is None:
            return  # no SNR to plot
        df = df.rename(columns={snr_col: "SNR_DB"})

    # Make sun_map from Sunrise/Sunset if present; otherwise compute per date
    if {"Sunrise", "Sunset"}.issubset(df.columns):
        sun_map = {}
        for d, row in df.drop_duplicates("Date")[["Date", "Sunrise", "Sunset"]].iterrows():
            # Convert string timestamps to datetime objects if needed
            sunrise = pd.to_datetime(row["Sunrise"], errors='coerce') if pd.notna(row["Sunrise"]) else None
            sunset = pd.to_datetime(row["Sunset"], errors='coerce') if pd.notna(row["Sunset"]) else None
            sun_map[pd.to_datetime(row["Date"]).date()] = (sunrise, sunset)
    else:
        unique_days = pd.to_datetime(df["Date"]).dt.date.unique()
        sun_map = {}
        for d in unique_days:
            try:
                sr, ss = sunrise_sunset_local(d, LAT, LON, LOCAL_TZ)
            except Exception:
                sr, ss = (None, None)
            sun_map[d] = (sr, ss)

    # Plot
    df["SNR_DB"] = pd.to_numeric(df["SNR_DB"], errors="coerce")
    df["SNR_DB_Smoothed"] = df["SNR_DB"].rolling(window).mean()

    start_dt = df["DateTime"].min() - timedelta(hours=1)
    end_dt   = df["DateTime"].max() + timedelta(hours=1)

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.plot(df["DateTime"], df["SNR_DB_Smoothed"], label=f"SNR_DB ({window}-pt MA)")

    dates_sorted = sorted([d for d in sun_map.keys() if d is not None])
    for i, d in enumerate(dates_sorted):
        sr = sun_map[d][0] if d in sun_map else None  # sunrise of current day
        ss = sun_map[d][1] if d in sun_map else None  # sunset of current day
        sr_next = sun_map[dates_sorted[i+1]][0] if i+1 < len(dates_sorted) else None  # sunrise of next day

        # Shade night period: sunset → next sunrise (but only for consecutive days)
        if ss is not None and sr_next is not None:
            # Check if the days are consecutive (within 2 days)
            current_date = d
            next_date = dates_sorted[i+1]
            day_gap = (next_date - current_date).days

            if day_gap <= 1:  # Only shade if days are consecutive or same day
                left = max(ss, start_dt)
                right = min(sr_next, end_dt)
                if pd.notna(left) and pd.notna(right) and left < right:
                    ax.axvspan(left, right, color="gray", alpha=0.3, zorder=0)
            else:
                # For non-consecutive days, only shade the evening of current day
                left = max(ss, start_dt)
                # Shade until midnight or end of data, whichever comes first
                midnight = pd.Timestamp(current_date) + pd.Timedelta(days=1)
                right = min(midnight, end_dt)
                if pd.notna(left) and pd.notna(right) and left < right:
                    ax.axvspan(left, right, color="gray", alpha=0.3, zorder=0)

                # Also shade the morning of the next day if it has data
                if next_date in dates_sorted:
                    next_midnight = pd.Timestamp(next_date)
                    left = max(next_midnight, start_dt)
                    right = min(sr_next, end_dt)
                    if pd.notna(left) and pd.notna(right) and left < right:
                        ax.axvspan(left, right, color="gray", alpha=0.3, zorder=0)

        # For single day data, also shade before sunrise and after sunset
        if len(dates_sorted) == 1:
            # Shade before sunrise (start of data → sunrise)
            if sr is not None:
                left = start_dt
                right = min(sr, end_dt)
                if pd.notna(left) and pd.notna(right) and left < right:
                    ax.axvspan(left, right, color="gray", alpha=0.3, zorder=0)

            # Shade after sunset (sunset → end of data)
            if ss is not None:
                left = max(ss, start_dt)
                right = end_dt
                if pd.notna(left) and pd.notna(right) and left < right:
                    ax.axvspan(left, right, color="gray", alpha=0.3, zorder=0)

    night_patch = mpatches.Patch(color="gray", alpha=0.3, label="Night (sunset → next sunrise)")
    ax.legend(handles=[night_patch, ax.lines[0]], loc="upper left")
    ax.set_xlim([start_dt, end_dt])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d %H:%M"))
    ax.xaxis.set_major_locator(MaxNLocator(8))
    plt.xticks(rotation=45, fontsize=7)
    # Extract frequency from filename for title
    filename = in_or_enriched_path.name.lower()
    frequency = ""
    if "7.1" in filename:
        frequency = "7.078 MHz"
    elif "10.130" in filename:
        frequency = "10.130 MHz"
    elif "5_ghz" in filename or "5ghz" in filename:
        frequency = "5 GHz"

    # Calculate statistics and duration
    mean_snr = df["SNR_DB"].mean()
    std_snr = df["SNR_DB"].std()

    # Calculate duration from DateTime column
    start_time = df["DateTime"].min()
    end_time = df["DateTime"].max()
    duration = end_time - start_time

    # Convert duration to hours and minutes
    total_minutes = int(duration.total_seconds() / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours > 0:
        duration_str = f"{hours}h {minutes}m"
    else:
        duration_str = f"{minutes}m"

    # Format dates for title
    start_date = start_time.strftime("%Y-%m-%d")
    end_date = end_time.strftime("%Y-%m-%d")

    if start_date == end_date:
        # Same day
        date_str = f"{start_date} ({duration_str})"
    else:
        # Multi-day
        date_str = f"{start_date} to {end_date} ({duration_str})"

    # Create title: Frequency (Power), Mean SNR (±Std), Date (Duration)
    # Add power specifications for specific frequencies
    if "7.078" in frequency:
        frequency_with_power = f"{frequency} (5 W)"
    elif "5 GHz" in frequency:
        frequency_with_power = f"{frequency} (1 W)"
    else:
        frequency_with_power = frequency

    title = f"{frequency_with_power}, {mean_snr:.1f} dB (±{std_snr:.1f}), {date_str}"

    plt.xlabel("Date and Time"); plt.ylabel("SNR DB")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

    # Create filename from title (sanitize for filesystem)
    safe_title = title.replace(":", "-").replace("/", "-").replace("±", "+-").replace(" ", "_")
    safe_title = safe_title.replace("(", "").replace(")", "").replace(",", "")

    # Save to current working directory (Mark_paper_2)
    import os
    current_dir = Path(os.getcwd())
    out_png = current_dir / f"{safe_title}.png"

    print(f"💾 Saving plot to: {out_png}")
    fig.savefig(out_png, dpi=160)
    print(f"✅ Plot saved successfully: {out_png.name}")

    # Display the plot if enabled
    if DISPLAY_PLOTS:
        print(f"🖼️  Displaying plot: {out_png.name}")
        plt.ion()  # Turn on interactive mode
        plt.show(block=True)  # Show plot and wait for user to close it
        plt.ioff()  # Turn off interactive mode
        print(f"✅ Plot displayed and saved: {out_png.name}")
        print("Close the plot window to continue...")
        print("-" * 50)
    else:
        plt.close(fig)  # Close figure to free memory
        print(f"✅ Plot saved: {out_png.name}")


def main():
    print("=== COMBINED ANALYSIS WITH BEST QUALITY DATA ===")
    if USE_BEST_QUALITY_ONLY:
        print("Using BEST QUALITY PERIODS ONLY (no data loss)")
        print("Quality periods defined:")
        for filename, period in BEST_QUALITY_PERIODS.items():
            print(f"  {filename}: {period['start']} to {period['end']} ({period['duration']})")
    else:
        print("Using ALL available data")
    print()

    processed_files = 0

    for f in FILES:
        in_path = Path(f).expanduser()
        if not in_path.exists():
            print(f"[skip] Not found: {in_path}")
            continue

        out_path = enrich_file(in_path, LAT, LON, LOCAL_TZ)

        if out_path is None:
            print(f"[skip] No data after filtering: {in_path.name}")
            continue

        print(f"[ok] Enriched → {out_path.name}")
        processed_files += 1

        if GENERATE_PLOTS:
            # You can plot from enriched to reuse Sunrise/Sunset columns
            src_for_plot = out_path if out_path.exists() else in_path

            # Extract frequency for display
            filename = src_for_plot.name.lower()
            if "7.1" in filename:
                freq_info = "7.078 MHz"
            elif "10.130" in filename:
                freq_info = "10.130 MHz"
            elif "5_ghz" in filename or "5ghz" in filename:
                freq_info = "5 GHz"
            else:
                freq_info = "Unknown frequency"

            print(f"\n📊 Generating plot for {freq_info}...")

            try:
                optional_plot(Path(src_for_plot), site_name=f"DGFC {LAT:.3f}°, {LON:.3f}°", window=MA_WINDOW)
                expected_png = Path(src_for_plot).with_suffix("").with_name(Path(src_for_plot).stem + "_plot.png")
                if expected_png.exists():
                    print(f"[ok] Plot saved → {expected_png.name}")
            except Exception as e:
                print(f"[error] Plot failed for {src_for_plot}: {e}")

    print(f"\n=== SUMMARY ===")
    print(f"Processed {processed_files}/{len(FILES)} files")
    if USE_BEST_QUALITY_ONLY:
        print("Used best quality periods with no data loss")
        print("Files created have '_best_quality_with_sun' suffix")
    else:
        print("Used all available data")
        print("Files created have '_with_sun' suffix")

    if GENERATE_PLOTS and processed_files > 0:
        print(f"\n📊 PLOTTING BEHAVIOR:")
        if DISPLAY_PLOTS:
            print("• Each plot is displayed automatically when generated")
            print("• Close each plot window to continue to the next one")
            print("• All plots are also saved as PNG files")
        else:
            print("• Plots are saved as PNG files (display disabled)")
        print("• Plots show best quality periods with nighttime shading")
        print(f"• Display setting: DISPLAY_PLOTS = {DISPLAY_PLOTS}")

    print(f"\n🎯 BEST QUALITY DATA ANALYSIS COMPLETE!")
    print("All files and plots ready for scientific analysis.")

if __name__ == "__main__":
    main()