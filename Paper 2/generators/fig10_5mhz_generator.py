#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from math import sin, cos, asin, acos, atan2, pi, floor
from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo

# ========= USER SETTINGS =========
FILE_PATH = 'data/5_GHZ_Standardized_data_preview__first_200_rows_.csv'
SITE_NAME = 'Danau Girang Field Centre (DGFC) 5 MHz'
LAT = 5.4139
LON = 118.0385                 # East positive
LOCAL_TZ = ZoneInfo("Asia/Kuching")
WINDOW_SIZE = 10               # moving average window
LINE_COLOR = 'black'
SAVE_ENRICHED_EXCEL = False    # set True to save sunrise/sunset columns alongside your data
ENRICHED_OUT = 'output/5_GHZ_with_sun_dgfc.xlsx'
# =================================

# ---- NOAA-style solar utilities ----
def deg2rad(d): return d * pi / 180.0
def rad2deg(r): return r * 180.0 / pi

def julian_day(d: date) -> float:
    y, m, D = d.year, d.month, d.day
    if m <= 2:
        y -= 1; m += 12
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
    Z = int(J)
    F = J - Z
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
    lw = deg2rad(-lon_deg)  # west negative
    H = hour_angle(deg2rad(lat_deg), dec, altitude=-0.833)
    Jtransit = solar_transit_jd(jd, lw)
    Jrise = Jtransit - rad2deg(H)/360.0
    Jset  = Jtransit + rad2deg(H)/360.0
    sr = jd_to_utc_datetime(Jrise).astimezone(tz).replace(tzinfo=None)
    ss = jd_to_utc_datetime(Jset ).astimezone(tz).replace(tzinfo=None)
    return sr, ss

# ---- Data loading + prep ----
def load_and_standardize(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Light auto-mapping if needed
    if 'SNR_DB' not in df.columns:
        snr_col = None
        for c in df.columns:
            lc = str(c).strip().lower()
            if lc in ('snr', 'snr(db)', 'snr (db)', 'snr (dbm)', 'snr_db', 'snr (dbm)'):
                snr_col = c; break
        if snr_col is None:
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            snr_col = num_cols[0] if num_cols else df.columns[2]
        date_col = 'Date' if 'Date' in df.columns else df.columns[0]
        time_col = 'Time' if 'Time' in df.columns else df.columns[1]
        df = df.rename(columns={date_col: 'Date', time_col: 'Time', snr_col: 'SNR_DB'})

    # ---- DROP SECONDS: keep only HH:MM ----
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

    # Try common time formats; fallback flexible
    t_try = None
    for fmt in ('%H:%M:%S', '%H:%M', '%I:%M:%S %p', '%I:%M %p'):
        try:
            tt = pd.to_datetime(df['Time'], format=fmt, errors='coerce')
            if tt.notna().sum() >= int(0.8 * len(df)):  # accept if most rows parse
                t_try = tt
                break
        except Exception:
            pass
    if t_try is None:
        t_try = pd.to_datetime(df['Time'], errors='coerce')

    df['Time'] = np.where(t_try.notna(), t_try.dt.strftime("%H:%M"), df['Time'].astype(str))

    # Build DateTime from date + HH:MM (now deterministic)
    df['DateTime'] = pd.to_datetime(
        df['Date'].astype(str) + ' ' + df['Time'],
        format="%Y-%m-%d %H:%M",
        errors="coerce"
    )
    df['SNR_DB'] = pd.to_numeric(df['SNR_DB'], errors='coerce')
    return df

def compute_sun_map(unique_days, lat, lon, tz):
    sun = {}
    for d in unique_days:
        try:
            sr, ss = sunrise_sunset_local(d, lat, lon, tz)
        except Exception:
            sr, ss = (None, None)
        sun[d] = (sr, ss)
    return sun

def main():
    df = load_and_standardize(FILE_PATH)
    df['SNR_DB_Smoothed'] = df['SNR_DB'].rolling(WINDOW_SIZE).mean()

    unique_days = pd.to_datetime(df['Date']).dt.date.unique()
    sun_map = compute_sun_map(unique_days, LAT, LON, LOCAL_TZ)

    start_date = df['DateTime'].min() - timedelta(hours=1)
    end_date   = df['DateTime'].max() + timedelta(hours=1)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(df['DateTime'], df['SNR_DB_Smoothed'],
            label=f'Smoothed SNR DB ({WINDOW_SIZE}-pt MA)', color=LINE_COLOR)

    # Shade each night (sunset(d) -> sunrise(d+1))
    dates_sorted = sorted(unique_days)
    for i, d in enumerate(dates_sorted):
        ss = sun_map.get(d, (None, None))[1]
        sr_next = sun_map.get(dates_sorted[i+1], (None, None))[0] if i+1 < len(dates_sorted) else None
        if ss is not None and sr_next is not None:
            left = max(ss, start_date)
            right = min(sr_next, end_date)
            if pd.notna(left) and pd.notna(right) and left < right:
                ax.axvspan(left, right, color='gray', alpha=0.3, zorder=0)

    import matplotlib.patches as mpatches
    night_patch = mpatches.Patch(color='gray', alpha=0.3, label="Night (sunset → next sunrise, local time)")
    ax.legend(handles=[night_patch, ax.lines[0]], loc='upper left')
    ax.set_xlim([start_date, end_date])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M'))
    ax.xaxis.set_major_locator(MaxNLocator(8))
    plt.xticks(rotation=45, fontsize=6.7)
    plt.xlabel('Date and Time'); plt.ylabel('SNR DB')
    plt.title(SITE_NAME)
    plt.grid(True, color='gray')
    plt.tight_layout(); plt.subplots_adjust(top=0.88, bottom=0.2)
    plt.show()

    if SAVE_ENRICHED_EXCEL:
        sun_rows = []
        for d in dates_sorted:
            sr, ss = sun_map[d]
            sun_rows.append({'Date': pd.Timestamp(d), 'Sunrise': sr, 'Sunset': ss})
        sun_df = pd.DataFrame(sun_rows)
        merged = pd.merge(df, sun_df, on='Date', how='left')
        merged.to_excel(ENRICHED_OUT, index=False)
        print(f"Enriched Excel written to: {ENRICHED_OUT}")

if __name__ == '__main__':
    main()