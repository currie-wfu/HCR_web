# ProbeGenerator - FISH Probe Design Tool

**Version 1.0** - Python 3 Compatible

A tool for designing FISH (Fluorescence In Situ Hybridization) probes with HCR (Hybridization Chain Reaction) initiator sequences. This version has been updated from Python 2 to Python 3 and includes memory-mapped Bowtie2 support for large genomes.

## 🤝 Contributing
- This iteration of the HCR Probe generator is directly adapted from David Stein’s probe generator (https://github.com/davidfstein/probegenerator), which was built and supported in James Monaghan’s lab at Northeastern University.
- Bowtie index files for the axolotl genome (UKY_AmexF1_1, https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_040938575.1/) that were used to test this tool were created and contributed by Sean Keeley and Rita Aires from Tatiana Sandoval-Guzmán’s lab at the CRTD Dresden. Axoltol bowtie indices are large (>50GB) and can be provided upon request.
- This tool was built with AI-assisted coding.

## 🔬 Scientific Background

This tool implements the probe design workflow from:
- **OligoMiner** - Beliveau et al. (2018) PNAS
- **HCR** - Choi et al. (2018) Development

### Probe Design Parameters

Default values are optimized for standard HCR-FISH:

| Parameter | Default | Description |
|-----------|---------|-------------|
| L/U | 25/25 | Probe length range (bp) |
| G/MAX_G | 20/80 | GC content range (%) |
| T_MIN/T_MAX | 37/72 | Melting temperature (°C) |
| S | 1000 | Max spacing between pairs |
| DESIRED_SPACES | 3 | Spacer nucleotides |

## 🔧 What's New in This Version

### Python 3 Compatibility
- ✅ Converted all Python 2 print statements to Python 3 syntax
- ✅ Fixed deprecated file modes (`'rU'` → `'r'`)
- ✅ Updated Biopython imports (removed `Bio.Alphabet`, updated `GC` function)
- ✅ Fixed `exec()` scoping issues with `getattr()`

### Memory-Mapped Bowtie2
- ✅ Added `--mm` flag for large genome indexes (e.g., 52GB Axolotl genome)
- ✅ No longer requires loading entire genome into RAM
- ✅ Works with limited memory systems

### User-Friendly Packaging
- ✅ Simple configuration file (no command-line args needed)
- ✅ Single-command execution
- ✅ Comprehensive error messages
- ✅ Beginner-friendly documentation

## 📊 Features

- Design FISH probes for any gene sequence
- Automatic filtering by:
  - GC content (20-80% default)
  - Melting temperature (37-72°C default)
  - Probe length (25bp default)
  - Genome-wide specificity
- HCR initiator sequences (B1, B2, B3, B4)
- Separate probes for:
  - Open reading frame (ORF)
  - 5' UTR
  - 3' UTR
- Ready-to-order CSV output
- Batch processing for multiple genes

## 🚀 Quick Start Web Interface - Easy Launch Guide

### For Mac Users
1. **Double-click** `launch_probegenerator.command`
2. The app will open in your browser automatically
3. That's it!

**First time only:** You may need to right-click → "Open" to allow the script to run.

### For Windows Users
1. **Double-click** `launch_probegenerator.bat`
2. The app will open in your browser automatically
3. That's it!

## How It Works

These launchers:
- ✅ Auto-detect the genome index in the Probegenerator folder
- ✅ Check if dependencies are installed
- ✅ Start the web server
- ✅ Open your browser to http://localhost:8501


### Simple Install
**Using the entire Probegenerator folder:**

1. Copy the `Probegenerator` folder to your preferred location
2. Install prerequisites:
   - **Python 3.8+** ([python.org/downloads](https://www.python.org/downloads/))
   - **Bowtie2** ([Installation guide](http://bowtie-bio.sourceforge.net/bowtie2/))
   - **OligoMiner tools** (instructions in main README)
3. Double-click the launcher for your OS (*.command for MacOS and *.bat for Windows)
4. Done!

The launcher automatically:
- Finds the probegen script
- Detects genome indexes if they are in the same Probegenerator folder
- Installs Python packages if needed

### Dependency installs

**Mac:**
```bash
# Install Python (if not already installed)
brew install python3

# Install Bowtie2
brew install bowtie2

# Install OligoMiner (once)
pip3 install biopython
```
# Install Streamlit (once)
pip install streamlit
```

**Windows:**
```batch
# Install Python from python.org
# Install Bowtie2 from the official website

# Install OligoMiner (in Command Prompt)
pip install biopython
```
# Install Streamlit (once)
pip install streamlit
```

## Customization

### Change Default Port
Edit the launcher script and change:
```bash
streamlit run app.py --server.port 8502
```

### Auto-Open Browser
Remove `--server.headless true` from the launcher.

### Add Custom Genome Paths
Edit `app.py` line ~90 to add your lab's genome locations.

**Tip:** For lab-wide deployment, consider setting up on a shared computer and giving colleagues the IP address (e.g., `http://192.168.1.100:8501`). Only one installation needed!

## Troubleshooting

### "Command not found: streamlit"
Install dependencies:
```bash
cd Probegenerator/web_streamlit
pip install -r requirements.txt
```

### Port 8501 Already in Use
Another instance is running. Either:
- Close the other instance
- Change port in launcher script

### Genome Index Not Found
- Ensure `.bt2l` or `.bt2` files are in the `Probegenerator` folder
- Check the debug output in the web interface

### Mac Won't Run .command File
Right-click → "Open" the first time to grant permission.

### Windows "Not Recognized as Command"
Python or pip not in PATH. Reinstall Python and check "Add to PATH".

## 📧 Citation

If you use this tool in your research, please cite:

1. **OligoMiner:**
   Beliveau, B.J. et al. (2018) "OligoMiner provides a rapid, flexible environment for the design of genome-scale oligonucleotide in situ hybridization probes." PNAS.

2. **Bowtie2:**
   Langmead, B. & Salzberg, S.L. (2012) "Fast gapped-read alignment with Bowtie 2." Nature Methods.

3. **HCR (if using initiators):**
   Choi, H.M.T. et al. (2018) "Third-generation in situ hybridization chain reaction: multiplexed, quantitative, sensitive, versatile, robust." Development.

---
