# Script Dependency Map for Git Repository
## 📋 Complete Analysis of Python Scripts and Dependencies

**GitHub Repository:** [https://github.com/butterworthma/BearWave-Paper2](https://github.com/butterworthma/BearWave-Paper2)

### 🎯 KEY FILES FOR GIT REPOSITORY

## 🔧 CORE MODULES (MUST INCLUDE)

### **1. Standardized Layout System**
```
📁 standardized_layout_enforcer.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, os, datetime
├── Used by: generate_corrected_charts.py, generate_six_standardized_charts.py
└── Purpose: Enforces consistent 2x2 chart layout with correct foF2 calculations
```

### **2. Alternative Standardized Format**
```
📁 standardized_report_format.py ⭐ CORE
├── Dependencies: matplotlib, numpy
├── Used by: guam_april15-28_fof2_7years.py (tries to import)
└── Purpose: Alternative standardized formatting (older version)
```

## 📊 MAIN foF2 ANALYSIS SCRIPTS (CORE DATA ANALYSIS)

### **3. Guam Analysis Scripts**
```
📁 guam_april15-28_fof2_7years.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Imports: standardized_report_format (optional)
├── Data: NVIS_data.xlsx (Guam sheet)
└── Generates: Individual charts + 2x2 combined overview

📁 guam_april15_fof2_7years.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Data: NVIS_data.xlsx (Guam sheet, April 15th only)
└── Generates: Single day analysis charts

📁 guam_fof2_april.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Data: NVIS_data.xlsx (Guam sheet, full April)
└── Generates: Full month analysis charts
```

### **4. Darwin Analysis Scripts**
```
📁 darwin_april15-28_fof2_7years.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Data: NVIS_data.xlsx (Darwin sheet)
└── Generates: Individual charts + 2x2 combined overview

📁 darwin_april15_fof2_7years.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Data: NVIS_data.xlsx (Darwin sheet, April 15th only)
└── Generates: Single day analysis charts

📁 darwin_fof2_april.py ⭐ CORE
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Data: NVIS_data.xlsx (Darwin sheet, full April)
└── Generates: Full month analysis charts
```

## 🎨 CHART GENERATION UTILITIES

### **5. Corrected Chart Generators**
```
📁 generate_corrected_charts.py ⭐ IMPORTANT
├── Dependencies: pandas, numpy, matplotlib, datetime, os, sys
├── Imports: None (self-contained)
├── Purpose: Generates charts with correct foF2 calculations
└── Output: ~/Desktop/test/test2/corrected/

📁 generate_six_standardized_charts.py ⭐ IMPORTANT
├── Dependencies: pandas, numpy, matplotlib, datetime, os, sys
├── Imports: standardized_layout_enforcer
├── Purpose: Generates all 6 standardized charts
└── Output: ~/Desktop/test/

📁 generate_less_cluttered_april15th.py
├── Dependencies: pandas, numpy, matplotlib, datetime, os, sys
├── Imports: standardized_layout_enforcer
├── Purpose: Less cluttered April 15th visualizations
└── Output: ~/Desktop/test/test2/
```

## 🚀 AUTOMATION & ORCHESTRATION SCRIPTS

### **6. Batch Processing Scripts**
```
📁 run_all_2x2_charts.py
├── Dependencies: subprocess, os, datetime, matplotlib, glob
├── Calls: All 6 foF2 analysis scripts
├── Purpose: Run all scripts and generate 2x2 charts
└── Output: Shows generated charts

📁 apply_standardized_format_to_all.py
├── Dependencies: os, subprocess, datetime
├── Calls: All 6 foF2 analysis scripts
├── Purpose: Apply standardized formatting to all scripts
└── Lists: FOF2_SCRIPTS array

📁 generate_all_charts_to_test_folder.py
├── Dependencies: subprocess, os, sys, datetime
├── Calls: All foF2 scripts + test chart generators
├── Purpose: Generate all charts to test folder
└── Output: ~/Desktop/test/
```

## 📈 SPECIALIZED ANALYSIS SCRIPTS

### **7. NVIS & Ionospheric Analysis**
```
📁 nvis_ionospheric_analysis.py
├── Dependencies: pandas, numpy, matplotlib, requests, datetime, os
├── External APIs: NOAA space weather APIs
├── Purpose: Real ionospheric data analysis
└── Output: NVIS ionospheric analysis charts

📁 nvis_propagation_model.py
├── Dependencies: pandas, numpy, matplotlib, datetime, os
├── Purpose: NVIS propagation modeling
└── Output: Propagation model charts

📁 Combined.py ⭐ IMPORTANT
├── Dependencies: pandas, numpy, matplotlib, pathlib, datetime
├── Purpose: Combined analysis with best quality data
└── Config: BEST_QUALITY_PERIODS
```

## 🔧 UTILITY & HELPER SCRIPTS

### **8. File Management**
```
📁 add_new_standard_prefix.py
├── Dependencies: os, shutil, glob, datetime
├── Purpose: Add "new_standard_" prefix to files
└── Modifies: Existing PNG files

📁 rename_to_combined_script_format.py
├── Dependencies: os, shutil, glob, datetime
├── Purpose: Rename files to combined script format
└── Modifies: Existing PNG files
```

### **9. Display & Viewing Scripts**
```
📁 show_all_2x2_charts.py
├── Dependencies: subprocess, os, glob, datetime
├── Purpose: Display all existing 2x2 charts
└── Opens: PNG files in system viewer

📁 display_charts_interactive.py
├── Dependencies: matplotlib, os, glob
├── Purpose: Interactive chart viewer with menu
└── Shows: Best quality charts

📁 simple_run_and_show.py
├── Dependencies: subprocess, os, glob
├── Purpose: Run one script at a time and show results
└── Interactive: Menu-driven script execution
```

## 📋 CONFIGURATION & DOCUMENTATION

### **10. Configuration Files**
```
📁 requirements.txt ⭐ ESSENTIAL
├── Lists: All Python package dependencies
├── Core: pandas, numpy, matplotlib, openpyxl, psutil
└── Optional: scipy, seaborn, plotly, statsmodels

📁 config_template.py
├── Purpose: Configuration template for analysis scripts
└── Contains: File paths, parameters, settings
```

### **11. Documentation**
```
📁 README_github.md ⭐ ESSENTIAL
├── Purpose: Main documentation for GitHub
├── Contains: Setup instructions, usage examples
└── Audience: GitHub repository users

📁 README_chart_display.md
├── Purpose: Chart display troubleshooting guide
└── Contains: Display issues, solutions, script references

📁 README_combined_analysis.md
├── Purpose: Combined analysis documentation
└── Contains: Best quality periods, analysis methods
```

## 🧪 TESTING & DIAGNOSTICS

### **12. Test Scripts**
```
📁 test_chart_display.py
├── Dependencies: matplotlib, numpy
├── Purpose: Test chart display functionality
└── Diagnostic: Matplotlib backend testing

📁 test_matplotlib_display.py
├── Dependencies: matplotlib, numpy
├── Purpose: Test matplotlib display system
└── Diagnostic: Display system verification
```

## 🎯 RECOMMENDED GIT REPOSITORY STRUCTURE

### **ESSENTIAL FILES (MUST INCLUDE):**
```
📦 ionospheric-fof2-analysis/
├── 📁 core/
│   ├── standardized_layout_enforcer.py ⭐
│   ├── standardized_report_format.py ⭐
│   └── Combined.py ⭐
├── 📁 analysis/
│   ├── guam_april15-28_fof2_7years.py ⭐
│   ├── guam_april15_fof2_7years.py ⭐
│   ├── guam_fof2_april.py ⭐
│   ├── darwin_april15-28_fof2_7years.py ⭐
│   ├── darwin_april15_fof2_7years.py ⭐
│   └── darwin_fof2_april.py ⭐
├── 📁 generators/
│   ├── generate_corrected_charts.py ⭐
│   ├── generate_six_standardized_charts.py ⭐
│   └── generate_less_cluttered_april15th.py
├── 📁 automation/
│   ├── run_all_2x2_charts.py
│   ├── apply_standardized_format_to_all.py
│   └── generate_all_charts_to_test_folder.py
├── 📁 specialized/
│   ├── nvis_ionospheric_analysis.py
│   └── nvis_propagation_model.py
├── 📁 utilities/
│   ├── show_all_2x2_charts.py
│   ├── display_charts_interactive.py
│   └── simple_run_and_show.py
├── 📁 docs/
│   ├── README.md ⭐
│   ├── README_chart_display.md
│   └── SCRIPT_DEPENDENCY_MAP.md ⭐
├── requirements.txt ⭐
└── .gitignore
```

### **OPTIONAL FILES (NICE TO HAVE):**
- File management utilities
- Additional test scripts
- Legacy analysis scripts
- Specialized display scripts

### **EXCLUDE FROM GIT:**
- Generated PNG files
- Data files (NVIS_data.xlsx)
- Output directories
- Temporary files
- User-specific paths

## 🔗 DEPENDENCY SUMMARY

### **External Dependencies:**
- pandas, numpy, matplotlib (core)
- openpyxl (Excel file support)
- requests (for NVIS API calls)
- psutil (for system monitoring)

### **Internal Dependencies:**
- standardized_layout_enforcer.py → Used by chart generators
- standardized_report_format.py → Used by foF2 analysis scripts
- NVIS_data.xlsx → Required by all foF2 analysis scripts

### **Data Dependencies:**
- NVIS_data.xlsx (Guam and Darwin sheets)
- Best quality period definitions
- Ionospheric parameter configurations
