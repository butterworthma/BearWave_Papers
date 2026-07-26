# 📊 BearWave Paper 2 - Figures and Plots

**"Ionospheric foF2 Analysis and System Performance"**

**GitHub Repository:** [https://github.com/butterworthma/BearWave-Paper2](https://github.com/butterworthma/BearWave-Paper2)

This document showcases all the figures and analysis plots generated for Paper 2, presenting comprehensive ionospheric analysis, multi-frequency performance evaluation, and system monitoring results from the BearWave deployment.

---

## 🎯 **Paper Overview**

Paper 2 provides in-depth analysis of ionospheric conditions affecting NVIS propagation, multi-frequency system performance, and comprehensive system monitoring data from the BearWave deployment in Borneo. The analysis spans 7 years of ionospheric data (2017-2023) and includes detailed system performance metrics.

---

## 🛰️ **Ionospheric Analysis Figures**

### **Darwin Station Analysis (Southern Hemisphere)**

#### **Darwin April 15-28 (7 Years)**
**Script:** `analysis/darwin_april15-28_fof2_7years.py`
**Data:** `data/NVIS_data.xlsx` (Darwin sheet)

```bash
python analysis/darwin_april15-28_fof2_7years.py
```

**Generated Charts:**
- Darwin foF2 April 15-28 24-hour 7-Year Comparison
- Darwin foF2 April 15-28 Statistical Comparison
- Darwin foF2 April 15-28 Peak Timing Analysis
- Darwin foF2 April 15-28 Combined Overview

**Key Findings:**
- Average foF2: 9.6±0.2 MHz across 7 years
- Peak timing: ~04:00 local time
- Excellent NVIS conditions for 7.078 MHz and 10.130 MHz

#### **Darwin April 15th Single Day Analysis**
**Script:** `analysis/darwin_april15_fof2_7years.py`
**Data:** `data/NVIS_data.xlsx` (Darwin sheet)

```bash
python analysis/darwin_april15_fof2_7years.py
```

**Generated Charts:**
- Darwin foF2 April 15th 24-hour 7-Year Comparison
- Darwin foF2 April 15th Statistical Comparison  
- Darwin foF2 April 15th Peak Timing Analysis
- Darwin foF2 April 15th Combined Overview

**Key Results:**
- Consistent ionospheric patterns across years
- 7-year average: 9.6 MHz
- MUF (3×foF2): 28.7 MHz, OWF: 24.4 MHz

#### **Darwin Full April Analysis**
**Script:** `analysis/darwin_fof2_april.py`
**Data:** `data/NVIS_data.xlsx` (Darwin sheet)

```bash
python analysis/darwin_fof2_april.py
```

**Generated Charts:**
- Darwin foF2 Full April 7-Year Statistical Analysis
- Darwin foF2 Full April Temporal Variations
- Darwin foF2 Full April Distribution Analysis

---

### **Guam Station Analysis (Northern Hemisphere)**

#### **Guam April 15-28 (7 Years)**
**Script:** `analysis/guam_april15-28_fof2_7years.py`
**Data:** `data/NVIS_data.xlsx` (Guam sheet)

```bash
python analysis/guam_april15-28_fof2_7years.py
```

**Generated Charts:**
- Guam foF2 April 15-28 24-hour 7-Year Comparison
- Guam foF2 April 15-28 Statistical Comparison
- Guam foF2 April 15-28 Peak Timing Analysis
- Guam foF2 April 15-28 Combined Overview

#### **Guam April 15th Single Day Analysis**
**Script:** `analysis/guam_april15_fof2_7years.py`
**Data:** `data/NVIS_data.xlsx` (Guam sheet)

```bash
python analysis/guam_april15_fof2_7years.py
```

#### **Guam Full April Analysis**
**Script:** `analysis/guam_fof2_april.py`
**Data:** `data/NVIS_data.xlsx` (Guam sheet)

```bash
python analysis/guam_fof2_april.py
```

---

## 📡 **Multi-Frequency Analysis Figures**

### **Figure 10: 5 GHz Performance Analysis**
**Script:** `generators/fig10_5mhz_generator.py`
**Data:** `data/5_GHZ_Standardized_data_preview__first_200_rows_.csv`

```bash
python generators/fig10_5mhz_generator.py
```

**Description:** Comprehensive 5 GHz system performance including:
- Signal strength analysis over 32+ hour period
- Day/night performance variations
- Statistical distribution analysis
- Optimal transmission windows

**Key Findings:**
- Longest continuous operation period: 32:52:30
- Consistent performance across extended deployment
- Validated for long-term conservation monitoring

---

### **Figure 14: 7.1 MHz NVIS Analysis**
**Script:** `generators/fig14_7_1mhz_generator.py`
**Data:** `data/7_1_MHz_Standardized_data.xlsx`

```bash
python generators/fig14_7_1mhz_generator.py
```

**Generated Charts:**
- 7.078 MHz 24-hour SNR Analysis
- 7.078 MHz Best Period Analysis (20:35:15 duration)
- Day vs Night performance comparison

**Key Results:**
- Operating frequency: 7.078 MHz @ 5W
- Best continuous period: 20:35:15 on 2023-04-18
- Excellent day/night performance differential

---

### **Figure 15: 10.130 MHz NVIS Analysis**
**Script:** `generators/fig15_10_130mhz_generator.py`
**Data:** `data/10_130_MHz_Standardized_data.xlsx`

```bash
python generators/fig15_10_130mhz_generator.py
```

**Generated Charts:**
- 10.130 MHz 24-hour SNR Analysis
- 10.130 MHz Best Period Analysis (15:10:45 duration)
- 10.130 MHz Power Efficiency Analysis

**Key Results:**
- Operating frequency: 10.130 MHz @ 1W
- Best continuous period: 15:10:45 on 2023-04-20
- Superior power efficiency: High SNR/Watt ratio

---

## 🌡️ **System Monitoring Figures**

### **Figure 28: Raspberry Pi CPU Throttling Temperature**
**Script:** `generators/fig28_raspberry_pi_cpu_throttling.py`
**Data:** `data/cpu_temperature_data.xlsx`

```bash
python generators/fig28_raspberry_pi_cpu_throttling.py
```

**Generated Charts:**
- CPU Temperature Timeline with Throttling Thresholds
- Temperature vs CPU Speed Correlation
- Thermal Performance Summary
- System Health Assessment

**Key Results:**
- **Total samples:** 1,930 temperature measurements
- **Average temperature:** 69.4°C
- **Maximum temperature:** 75.0°C
- **Time above warning (70°C):** 57.7%
- **Time above throttling (80°C):** 0.0% ✅
- **System status:** GOOD - No throttling occurred

**Thermal Thresholds:**
- **Warning:** 70°C (Orange)
- **Throttling:** 80°C (Red)
- **Critical:** 85°C (Dark Red)
- **Ambient:** 30°C (Borneo environment)

---

### **Figure 29: CPU Temperature Analysis (Three Charts)**
**Script:** `system_monitoring/cpu_temperature_analysis.py`
**Data:** `data/cpu_temperature_data.xlsx`

```bash
python system_monitoring/cpu_temperature_analysis.py
```

**Generated Charts:**
- Comprehensive CPU Temperature Timeline Analysis
- Thermal Performance Summary (2x2 layout)
- System Health Status Dashboard

**Key Features:**
- **Timeline Analysis:** Temperature progression with moving averages
- **Statistical Breakdown:** Temperature metrics and threshold analysis
- **Performance Summary:** Time in temperature zones analysis
- **Health Dashboard:** Overall system status assessment

**Analysis Results:**
- **Duration:** Extended monitoring period
- **Thermal Management:** Effective cooling performance
- **Reliability:** No thermal throttling events
- **Operational Status:** Validated for field deployment

---

## 📊 **Comprehensive Analysis Figures**

### **2x2 Comparison Charts**
**Script:** `generators/generate_2x2_charts.py`
**Data:** `data/Complete_NVIS_data.xlsx`

```bash
python generators/generate_2x2_charts.py
```

**Generated Charts:**
- Complete NVIS 2x2 Comparison (Guam vs Darwin)
- Annual foF2 Trends (Both Stations)
- Station Correlation Analysis
- Distribution Comparison Analysis

**Data Coverage:**
- **Guam:** 1,363 records, 42 columns (2016-2023+)
- **Darwin:** 1,363 records, 19 columns (2017-2023+)
- **Complete temporal analysis** across multiple years

---

### **Corrected Charts Generator**
**Script:** `generators/generate_corrected_charts.py`
**Data:** `data/NVIS_data.xlsx`

```bash
python generators/generate_corrected_charts.py
```

**Generated Charts (6 total):**
1. Guam April 15-28 Corrected Analysis
2. Guam April 15th Corrected Analysis
3. Guam Full April Corrected Analysis
4. Darwin April 15-28 Corrected Analysis
5. Darwin April 15th Corrected Analysis
6. Darwin Full April Corrected Analysis

**Features:**
- Exact foF2 calculations matching original scripts
- Standardized formatting across all charts
- Timestamp-based file naming for version control

---

### **Six Standardized Charts Generator**
**Script:** `generators/generate_six_standardized_charts.py`
**Data:** `data/NVIS_data.xlsx`

```bash
python generators/generate_six_standardized_charts.py
```

**Generated Charts:**
- All 6 core ionospheric analysis charts with standardized layout
- Consistent formatting and color schemes
- Professional publication-ready quality

**Features:**
- Standardized 2x2 panel layout for each chart
- Consistent color coding across all analyses
- Automated file naming and organization

---

### **Less Cluttered April 15th Charts**
**Script:** `generators/generate_less_cluttered_april15th.py`
**Data:** `data/NVIS_data.xlsx`

```bash
python generators/generate_less_cluttered_april15th.py
```

**Generated Charts:**
- Simplified April 15th visualizations
- Reduced visual clutter for clearer presentation
- Alternative visualization options (heatmap, reduced lines)

**Features:**
- Interactive visualization type selection
- Cleaner temporal progression displays
- Enhanced readability for presentations

---

## 🤖 **Automation and Batch Processing**

### **Run All 2x2 Charts**
**Script:** `automation/run_all_2x2_charts.py`
**Data:** `data/NVIS_data.xlsx`

```bash
python automation/run_all_2x2_charts.py
```

**Features:**
- Executes all 6 core foF2 analysis scripts automatically
- Generates comprehensive 2x2 chart comparisons
- Displays generated charts interactively
- Progress tracking and error handling

---

### **Apply Standardized Format to All**
**Script:** `automation/apply_standardized_format_to_all.py`
**Data:** `data/NVIS_data.xlsx`

```bash
python automation/apply_standardized_format_to_all.py
```

**Features:**
- Applies consistent formatting to all analysis scripts
- Ensures standardized output across all charts
- Batch processing with progress indicators

---

### **Generate All Charts to Test Folder**
**Script:** `automation/generate_all_charts_to_test_folder.py`
**Data:** `data/NVIS_data.xlsx`

```bash
python automation/generate_all_charts_to_test_folder.py
```

**Features:**
- Generates all charts to organized test directory
- Comprehensive batch processing of all analysis types
- Detailed progress reporting and file organization

---

## 🖥️ **Interactive Display and Utilities**

### **Show All 2x2 Charts**
**Script:** `utilities/show_all_2x2_charts.py`

```bash
python utilities/show_all_2x2_charts.py
```

**Features:**
- Interactive display of all generated 2x2 charts
- Navigation between different analysis results
- Zoom and pan capabilities for detailed examination

---

### **Display Charts Interactive**
**Script:** `utilities/display_charts_interactive.py`

```bash
python utilities/display_charts_interactive.py
```

**Features:**
- Interactive chart viewer with advanced controls
- Side-by-side comparison capabilities
- Export and annotation tools

---

### **Simple Run and Show**
**Script:** `utilities/simple_run_and_show.py`

```bash
python utilities/simple_run_and_show.py
```

**Features:**
- One-click execution and display
- Simplified interface for quick analysis
- Automatic chart generation and viewing

---

## 🔧 **Analysis Tools and Scripts**

### **Core Analysis Scripts:**
```
📁 analysis/ (6 core ionospheric analysis scripts)
├── darwin_april15-28_fof2_7years.py    # Darwin 2-week analysis
├── darwin_april15_fof2_7years.py       # Darwin single day
├── darwin_fof2_april.py                # Darwin full month
├── guam_april15-28_fof2_7years.py      # Guam 2-week analysis
├── guam_april15_fof2_7years.py         # Guam single day
└── guam_fof2_april.py                  # Guam full month

📁 generators/ (Figure generators - LATEST VERSIONS)
├── fig10_5mhz_generator.py             # Figure 10: 5 GHz (Sep 21 21:40)
├── fig14_7_1mhz_generator.py           # Figure 14: 7.1 MHz (Sep 21 23:04) ⭐
├── fig15_10_130mhz_generator.py        # Figure 15: 10.130 MHz (Sep 21 23:05) ⭐
├── fig28_raspberry_pi_cpu_throttling.py # Figure 28: CPU temp (Sep 21 23:18) ⭐
├── generate_2x2_charts.py              # 2x2 comparisons (Sep 21 23:23) ⭐
├── generate_corrected_charts.py        # Corrected analysis (outputs "new_standard_")
├── generate_six_standardized_charts.py # Batch generator (6 charts)
├── generate_less_cluttered_april15th.py # Simplified April 15th charts
└── field_test_results_generator.py     # Field test results

📁 system_monitoring/
└── cpu_temperature_analysis.py         # Figure 29: CPU analysis (Sep 21 23:13) ⭐

📁 automation/ (Batch processing tools)
├── run_all_2x2_charts.py              # Execute all 6 analysis scripts
├── apply_standardized_format_to_all.py # Apply consistent formatting
└── generate_all_charts_to_test_folder.py # Generate all to test directory

📁 utilities/ (Interactive tools)
├── show_all_2x2_charts.py             # Display generated charts
├── display_charts_interactive.py       # Interactive chart viewer
└── simple_run_and_show.py             # One-click execution
```

### **Data Files:**
```
📁 data/
├── NVIS_data.xlsx                      # Core ionospheric data
├── Complete_NVIS_data.xlsx             # Complete dataset (2x2 plots)
├── cpu_temperature_data.xlsx           # System temperature monitoring
├── 5_GHZ_Standardized_data_preview__first_200_rows_.csv
├── 7_1_MHz_Standardized_data.xlsx      # 7.1 MHz measurements
└── 10_130_MHz_Standardized_data.xlsx   # 10.130 MHz measurements
```

---

## 🚀 **Running the Complete Analysis**

### **Prerequisites:**
```bash
pip install pandas matplotlib numpy openpyxl seaborn
```

### **Generate All Figures:**
```bash
# Ionospheric Analysis
python analysis/darwin_april15-28_fof2_7years.py
python analysis/guam_april15-28_fof2_7years.py

# Multi-frequency Analysis  
python generators/fig10_5mhz_generator.py
python generators/fig14_7_1mhz_generator.py
python generators/fig15_10_130mhz_generator.py

# System Monitoring
python generators/fig28_raspberry_pi_cpu_throttling.py
python system_monitoring/cpu_temperature_analysis.py  # Figure 29

# Comprehensive Analysis
python generators/generate_2x2_charts.py
python generators/generate_corrected_charts.py
python generators/generate_six_standardized_charts.py
python generators/generate_less_cluttered_april15th.py

# Automation Tools
python automation/run_all_2x2_charts.py
```

### **Batch Processing:**
```bash
# Run all analysis scripts
for script in analysis/*.py; do python "$script"; done
for script in generators/*.py; do python "$script"; done
```

---

## 📈 **Key Scientific Findings**

### **Ionospheric Conditions:**
- **7-year foF2 baseline** established for both hemispheres
- **Seasonal variations** quantified and characterized
- **Optimal NVIS frequencies** validated (7-10 MHz range)
- **Propagation reliability** confirmed for conservation applications

### **Multi-frequency Performance:**
- **5 GHz:** Extended operation capability (32+ hours)
- **7.1 MHz @ 5W:** Excellent NVIS performance (20+ hours)
- **10.130 MHz @ 1W:** Superior power efficiency
- **Frequency diversity** provides operational redundancy

### **System Reliability:**
- **Thermal management:** No CPU throttling under field conditions
- **Continuous operation:** Validated for extended deployments
- **Environmental resilience:** Maintained performance in tropical conditions
- **Power efficiency:** Optimized for remote solar/battery operation

---

## 🌿 **Conservation Applications**

The comprehensive analysis validates BearWave system capabilities for:

- **Real-time Wildlife Monitoring:** Continuous data transmission
- **Anti-poaching Networks:** Reliable communication infrastructure  
- **Research Data Collection:** Long-term environmental monitoring
- **Emergency Communications:** Backup systems for remote areas

---

## 📚 **Technical Documentation**

- **[README.md](README.md)** - Repository overview
- **[Installation Guide](docs/INSTALLATION.md)** - Setup instructions
- **[Data Formats](docs/DATA_FORMATS.md)** - File specifications
- **[API Reference](docs/API.md)** - Programming interface

---

*This comprehensive analysis demonstrates the scientific rigor and practical validation of the BearWave system for conservation technology applications in challenging remote environments.*
