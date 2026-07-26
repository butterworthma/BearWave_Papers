# Evaluating NVIS for Remote Wildlife Monitoring: A Field Trial in the Borneo Rainforest

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/butterworthma/BearWave-Paper2)

## 📊 Overview
This repository contains the complete analysis code for **"Evaluating NVIS for Remote Wildlife Monitoring: A Field Trial in the Borneo Rainforest"** - a comprehensive study of Near Vertical Incidence Skywave (NVIS) communication for wildlife monitoring applications. The code includes ionospheric foF2 (critical frequency) analysis, field test results, and NVIS propagation modeling with data from Guam and Darwin monitoring stations.

**GitHub Repository:** [https://github.com/butterworthma/BearWave-Paper2](https://github.com/butterworthma/BearWave-Paper2)

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
# Generate all 6 standardized charts
python generators/generate_corrected_charts.py

# Run individual analysis
python analysis/guam_april15-28_fof2_7years.py

# Batch process all analyses
python automation/run_all_2x2_charts.py
```

## 📁 Repository Structure
- `core/` - Core layout and formatting modules
- `analysis/` - Main foF2 analysis scripts (6 scripts)
- `generators/` - Chart generation utilities
- `automation/` - Batch processing scripts
- `utilities/` - Display and viewing tools
- `docs/` - Documentation and guides
- `data/` - Place NVIS_data.xlsx here (not tracked by git)
- `output/` - Generated charts will be saved here

## 📋 Data Requirements
- NVIS_data.xlsx with Guam and Darwin sheets
- Place in the `data/` directory
- Update file paths in scripts if needed

## 📊 Generated Charts & Figures
- **Field Test Results**: Figs 10, 14, 15 (5 GHz, 7.078 MHz, 10.130 MHz)
- **Ionospheric Analysis**: Figs 22-27 (foF2 critical frequency analysis)
- **Standardized 2x2 layouts** with consistent positioning
- **NVIS frequency band analysis** for wildlife monitoring optimization
- **Professional formatting** ready for scientific publication

## 🔧 Key Features
- **Field-Tested NVIS Communication**: Real-world Borneo rainforest deployment
- **Ionospheric foF2 Analysis**: Multi-year comparative studies (2017-2023)
- **Wildlife Monitoring Focus**: Optimized for remote conservation applications
- **Standardized Layout Enforcer**: Ensures consistent chart positioning
- **Multi-Station Analysis**: Guam and Darwin ionospheric monitoring
- **Portable Codebase**: Relative paths work on any system

See `SCRIPT_DEPENDENCY_MAP.md` for detailed file relationships.

## 🌍 Research Context
This work supports remote wildlife monitoring in the Borneo rainforest at the Danau Girang Field Centre (DGFC), Malaysia. The study evaluates NVIS communication effectiveness for conservation applications in challenging tropical environments.

## 📞 Support
For issues or questions:
- Open an issue on [GitHub](https://github.com/butterworthma/BearWave-Paper2/issues)
- Refer to the documentation in the `docs/` directory

## 🔗 Repository Links
- **GitHub Repository:** [https://github.com/butterworthma/BearWave-Paper2](https://github.com/butterworthma/BearWave-Paper2)
- **Clone Repository:** `git clone https://github.com/butterworthma/BearWave-Paper2.git`

## 📄 Citation
**"Evaluating NVIS for Remote Wildlife Monitoring: A Field Trial in the Borneo Rainforest"**
*PhD Research - Cardiff University*
