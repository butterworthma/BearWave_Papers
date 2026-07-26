# GitHub Repository Setup

## Repository Information

**Repository URL:** https://github.com/butterworthma/BearWave-Paper2.git

**Clone Command:**
```bash
git clone https://github.com/butterworthma/BearWave-Paper2.git
```

## Git Configuration

**Current Remote:**
```bash
origin  https://github.com/butterworthma/BearWave-Paper2.git (fetch)
origin  https://github.com/butterworthma/BearWave-Paper2.git (push)
```

**User Configuration:**
- Name: Apollopog
- Email: sbutterworth77@gmail.com

## Files Updated with GitHub Links

1. **README.md** - Added GitHub repository badge and links
2. **SCRIPT_DEPENDENCY_MAP.md** - Added repository link at the top
3. **FIGURES.md** - Added repository link at the top
4. **.gitignore** - Updated to include the comprehensive stacked charts PNG

## Ready to Push

### New Files to Add:
- `generators/display_all_charts_side_by_side.py` - Side-by-side chart generator
- `utilities/foF2_summary_statistics.py` - Summary statistics script

### Modified Files:
- `README.md` - Added GitHub links and repository information
- `SCRIPT_DEPENDENCY_MAP.md` - Added repository link
- `FIGURES.md` - Added repository link
- `.gitignore` - Updated to include stacked charts PNG

## Push Commands

```bash
# Stage all changes
git add README.md SCRIPT_DEPENDENCY_MAP.md FIGURES.md .gitignore
git add generators/display_all_charts_side_by_side.py
git add utilities/foF2_summary_statistics.py

# Commit changes
git commit -m "Update GitHub links and add new chart generation scripts"

# Push to GitHub
git push origin main
```

Or if using master branch:
```bash
git push origin master
```

## Repository Structure

The repository is configured to push to:
- **Owner:** butterworthma
- **Repository:** BearWave-Paper2
- **Full URL:** https://github.com/butterworthma/BearWave-Paper2

## Notes

- The virtual environment (`venv/`) is excluded from git (in .gitignore)
- Generated PNG files are excluded except for the comprehensive stacked charts
- Data files are excluded except for essential ones needed for repository functionality
