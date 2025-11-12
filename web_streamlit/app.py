"""
ProbeGenerator - Streamlit Web Interface
Simple, elegant interface for designing FISH probes
"""

import streamlit as st
import subprocess
import tempfile
import os
import shutil
from pathlib import Path
import zipfile

# Page configuration
st.set_page_config(
    page_title="ProbeGenerator",
    page_icon="🧬",
    layout="wide"
)

# Title and description
st.title("🧬 ProbeGenerator - FISH Probe Design")
st.markdown("""
Design FISH probes with HCR initiator sequences for your genes.
Upload your gene sequence and genome index, configure parameters, and download ready-to-order probes.
""")

# Sidebar for parameters
st.sidebar.header("⚙️ Probe Design Parameters")

with st.sidebar:
    st.subheader("Probe Length")
    min_length = st.slider("Minimum length (bp)", 20, 30, 25)
    max_length = st.slider("Maximum length (bp)", 20, 30, 25)

    st.subheader("GC Content")
    min_gc = st.slider("Minimum GC%", 0, 50, 20)
    max_gc = st.slider("Maximum GC%", 50, 100, 80)

    st.subheader("Melting Temperature")
    min_tm = st.slider("Minimum Tm (°C)", 30, 60, 37)
    max_tm = st.slider("Maximum Tm (°C)", 60, 80, 72)

    st.subheader("Advanced")
    spacing = st.number_input("Max spacing", 100, 2000, 1000)
    formamide = st.number_input("Formamide %", 0, 50, 30)
    desired_spaces = st.number_input("Spacer nucleotides", 1, 10, 3)

# Main content area - tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload Files", "🔬 Results", "ℹ️ Help"])

with tab1:
    st.header("Upload Your Files")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Gene Sequence (FASTA)")
        gene_file = st.file_uploader(
            "Upload your gene sequence in FASTA format",
            type=['fa', 'fasta', 'fna'],
            help="Single or multi-FASTA file with gene sequences"
        )

        if gene_file:
            st.success(f"✓ Uploaded: {gene_file.name}")
            # Show preview and detect multi-FASTA
            content = gene_file.getvalue().decode('utf-8')
            lines = content.split('\n')

            # Count number of sequences
            header_count = sum(1 for line in lines if line.startswith('>'))
            if header_count > 1:
                st.info(f"📊 **Batch mode detected:** {header_count} genes found in FASTA file")
            elif header_count == 1:
                st.info("📊 Single gene detected")

            st.text_area("Preview", '\n'.join(lines[:10]), height=150)

    with col2:
        st.subheader("2. HCR Initiators")

        # Toggle for using custom initiators
        use_custom_initiators = st.checkbox(
            "Use custom initiator sequences",
            value=False,
            help="Check this to upload your own initiator sequences. Uncheck to use default B1-B4 initiators."
        )

        initiator_file = None

        if use_custom_initiators:
            # Show file uploader for custom initiators
            initiator_file = st.file_uploader(
                "Upload custom initiators CSV file",
                type=['csv'],
                help="CSV file with initiator sequences"
            )

            if initiator_file:
                st.success(f"✓ Uploaded: {initiator_file.name}")
                # Show preview
                import pandas as pd
                df = pd.read_csv(initiator_file)
                st.dataframe(df)
        else:
            # Show default initiators table
            st.info("ℹ️ Using default HCR initiator sequences (B1-B4)")
            import pandas as pd

            # Create dataframe from default initiators
            default_initiators_data = {
                'initiator': ['B1', 'B2', 'B3', 'B4'],
                'left sequence': ['GAGGAGGGCAGCAAACGG', 'CCTCGTAAATCCTCATCA', 'GTCCCTGCCTCTATATCT', 'CCTCAACCTACCTCCAAC'],
                'left spacer': ['aa', 'aa', 'tt', 'aa'],
                'right sequence': ['GAAGAGTCTTCCTTTACG', 'ATCATCCAGTAAACCGCC', 'CCACTCAACTTTAACCCG', 'TCTCACCATATTCGCTTC'],
                'right spacer': ['ta', 'aa', 'tt', 'at']
            }
            df_default = pd.DataFrame(default_initiators_data)
            st.dataframe(df_default, use_container_width=True)

    st.subheader("3. Genome Index Location")

    # Auto-detect genome index in parent directory
    # Get the directory containing app.py (web_streamlit/)
    current_file = Path(__file__).resolve()
    web_streamlit_dir = current_file.parent
    # Go up one level to Probegenerator/
    probegenerator_dir = web_streamlit_dir.parent
    script_dir = probegenerator_dir

    # Debug info (expandable)
    with st.expander("🔍 Debug: Genome Index Detection"):
        st.code(f"""Script file: {current_file}
web_streamlit dir: {web_streamlit_dir}
Probegenerator dir: {probegenerator_dir}
Searching in: {script_dir}""")
        bt2l_files = list(script_dir.glob("*.1.bt2l"))
        st.write(f"Found {len(bt2l_files)} .1.bt2l files:")
        for f in bt2l_files:
            st.write(f"  - {f.name}")

    # Find .bt2l or .bt2 files in the directory
    # Look specifically for .1.bt2l or .1.bt2 files (the first index file)
    detected_indexes = []

    # Check for .1.bt2l files first (large genome indexes)
    for bt2_file in script_dir.glob("*.1.bt2l"):
        filename = bt2_file.name
        # Skip reverse index files
        if ".rev.1.bt2l" in filename:
            continue
        # Remove the .1.bt2l extension to get the basename
        basename = str(bt2_file)[:-7]  # Remove last 7 characters (.1.bt2l)
        if basename not in detected_indexes:
            detected_indexes.append(basename)

    # Also check for regular .1.bt2 files if no .bt2l found
    if not detected_indexes:
        for bt2_file in script_dir.glob("*.1.bt2"):
            filename = bt2_file.name
            # Skip reverse index files
            if ".rev.1.bt2" in filename:
                continue
            # Remove the .1.bt2 extension to get the basename
            basename = str(bt2_file)[:-6]  # Remove last 6 characters (.1.bt2)
            if basename not in detected_indexes:
                detected_indexes.append(basename)

    # Show auto-detected or custom input
    use_custom_path = st.checkbox("Use custom genome index path", value=False)

    if use_custom_path:
        genome_index = st.text_input(
            "Path to Bowtie2 genome index",
            placeholder=str(script_dir / "your_genome_index"),
            help="Full path to Bowtie2 index basename (without .bt2 extension)"
        )
    else:
        if detected_indexes:
            if len(detected_indexes) == 1:
                genome_index = detected_indexes[0]
                st.success(f"✓ Auto-detected genome index:\n`{Path(genome_index).name}`")
            else:
                genome_index = st.selectbox(
                    "Select genome index",
                    detected_indexes,
                    format_func=lambda x: Path(x).name
                )
                st.success(f"✓ Using: `{Path(genome_index).name}`")
        else:
            st.warning("⚠️ No genome index found in Probegenerator directory. Please check 'Use custom genome index path' above.")
            genome_index = ""

    # Validate path exists
    if genome_index:
        if os.path.exists(genome_index + ".1.bt2l") or os.path.exists(genome_index + ".1.bt2"):
            if use_custom_path:
                st.success("✓ Genome index found!")
        else:
            st.error(f"❌ Genome index files not found at:\n`{genome_index}.1.bt2l`")

    # Run button
    st.divider()

    if st.button("🚀 Generate Probes", type="primary", use_container_width=True):
        # Check if initiators are available (either custom upload or using defaults)
        initiators_available = (not use_custom_initiators) or (use_custom_initiators and initiator_file is not None)

        if not gene_file or not genome_index:
            st.error("❌ Please upload gene file and specify genome index path")
        elif use_custom_initiators and not initiator_file:
            st.error("❌ Please upload custom initiators CSV file or uncheck 'Use custom initiator sequences'")
        elif not os.path.exists(genome_index + ".1.bt2l") and not os.path.exists(genome_index + ".1.bt2"):
            st.error(f"❌ Genome index not found at: {genome_index}")
        else:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as tmpdir:
                st.info("🔄 Processing... This may take a few minutes.")
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # Save uploaded files
                    status_text.text("Step 1/7: Saving uploaded files...")
                    progress_bar.progress(10)

                    gene_path = os.path.join(tmpdir, gene_file.name)
                    with open(gene_path, 'wb') as f:
                        f.write(gene_file.getvalue())

                    # Extract gene names and detect multi-FASTA
                    gene_names = []
                    gene_name = "gene"  # Default fallback for zip naming
                    try:
                        with open(gene_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith('>'):
                                    # Remove '>', strip whitespace, and take first word
                                    header_parts = line[1:].strip().split()
                                    if header_parts:
                                        gene_names.append(header_parts[0])

                        if len(gene_names) == 1:
                            gene_name = gene_names[0]
                        elif len(gene_names) > 1:
                            # Multi-FASTA: use first gene name or generic name
                            gene_name = f"{gene_names[0]}_and_{len(gene_names)-1}_others"
                    except Exception as e:
                        st.warning(f"⚠️ Could not extract gene name from FASTA header: {e}. Using default name 'gene'.")

                    # Handle initiators - use custom or create default
                    if use_custom_initiators and initiator_file:
                        # Save custom initiator file
                        initiator_path = os.path.join(tmpdir, initiator_file.name)
                        with open(initiator_path, 'wb') as f:
                            f.write(initiator_file.getvalue())
                        initiator_filename = initiator_file.name
                    else:
                        # Create default initiators CSV file
                        import csv
                        initiator_filename = 'initiators.csv'
                        initiator_path = os.path.join(tmpdir, initiator_filename)
                        with open(initiator_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['initiator', 'left sequence', 'left spacer', 'right sequence', 'right spacer'])
                            writer.writerow(['B1', 'GAGGAGGGCAGCAAACGG', 'aa', 'GAAGAGTCTTCCTTTACG', 'ta'])
                            writer.writerow(['B2', 'CCTCGTAAATCCTCATCA', 'aa', 'ATCATCCAGTAAACCGCC', 'aa'])
                            writer.writerow(['B3', 'GTCCCTGCCTCTATATCT', 'tt', 'CCACTCAACTTTAACCCG', 'tt'])
                            writer.writerow(['B4', 'CCTCAACCTACCTCCAAC', 'aa', 'TCTCACCATATTCGCTTC', 'at'])

                    # Create config file
                    config_path = os.path.join(tmpdir, 'config.txt')
                    with open(config_path, 'w') as f:
                        f.write(f"SEQ_FILE=\"{gene_file.name}\"\n")
                        f.write(f"GENOME_INDEX=\"{genome_index}\"\n")
                        f.write(f"INITIATORS_FILE=\"{initiator_filename}\"\n")
                        f.write(f"L={min_length}\n")
                        f.write(f"U={max_length}\n")
                        f.write(f"G={min_gc}\n")
                        f.write(f"MAX_G={max_gc}\n")
                        f.write(f"T_MIN={min_tm}\n")
                        f.write(f"T_MAX={max_tm}\n")
                        f.write(f"S={spacing}\n")
                        f.write(f"F={formamide}\n")
                        f.write(f"DESIRED_SPACES={desired_spaces}\n")

                    # Run ProbeGenerator
                    if len(gene_names) > 1:
                        status_text.text(f"Step 2/7: Running probe design pipeline for {len(gene_names)} genes...")
                    else:
                        status_text.text("Step 2/7: Running probe design pipeline...")
                    progress_bar.progress(30)

                    # Get script directory - use absolute path
                    # app.py is in web_streamlit/, probegen is in parent directory
                    current_file = Path(__file__).resolve()
                    web_streamlit_dir = current_file.parent
                    probegenerator_dir = web_streamlit_dir.parent
                    probegen_script = probegenerator_dir / "probegen"

                    # Verify script exists
                    if not probegen_script.exists():
                        st.error(f"❌ probegen script not found at: {probegen_script}")
                        st.error(f"Debug info:")
                        st.code(f"__file__: {__file__}\ncurrent_file: {current_file}\nweb_streamlit_dir: {web_streamlit_dir}\nprobegenerator_dir: {probegenerator_dir}")
                        st.stop()

                    # Run in temporary directory
                    result = subprocess.run(
                        [str(probegen_script), config_path],
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=600  # 10 minute timeout
                    )

                    progress_bar.progress(80)

                    if result.returncode == 0:
                        status_text.text("Step 7/7: Packaging results...")
                        progress_bar.progress(90)

                        # Create zip of results
                        output_dir = os.path.join(tmpdir, 'output')
                        zip_filename = f'{gene_name}_probes_results.zip'
                        zip_path = os.path.join(tmpdir, zip_filename)

                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            for root, dirs, files in os.walk(output_dir):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, tmpdir)
                                    # Replace 'output' with '{gene_name}_probes' in the archive path
                                    arcname = arcname.replace('output', f'{gene_name}_probes', 1)
                                    zipf.write(file_path, arcname)

                        # Store in session state
                        with open(zip_path, 'rb') as f:
                            st.session_state['results_zip'] = f.read()
                        st.session_state['zip_filename'] = zip_filename
                        st.session_state['gene_count'] = len(gene_names)
                        st.session_state['gene_names'] = gene_names

                        # Store console output
                        st.session_state['console_output'] = result.stdout

                        progress_bar.progress(100)
                        status_text.text("✅ Complete!")

                        st.success("✅ Probe generation complete! Go to 'Results' tab to download.")
                        st.balloons()
                    else:
                        st.error("❌ Probe generation failed. See error below:")
                        st.code(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Process timed out. Your genome may be too large for web processing.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("Download Your Probes")

    if 'results_zip' in st.session_state:
        gene_count = st.session_state.get('gene_count', 1)
        gene_names = st.session_state.get('gene_names', [])

        if gene_count > 1:
            st.success(f"✅ Batch processing complete! Generated probes for {gene_count} genes.")
            with st.expander(f"📋 View all {gene_count} gene names"):
                for i, name in enumerate(gene_names, 1):
                    st.write(f"{i}. {name}")
        else:
            st.success("✅ Results are ready!")

        # Download button
        zip_filename = st.session_state.get('zip_filename', 'probegenerator_results.zip')
        st.download_button(
            label="📥 Download Probe Results (ZIP)",
            data=st.session_state['results_zip'],
            file_name=zip_filename,
            mime="application/zip",
            use_container_width=True
        )

        if gene_count > 1:
            st.info(f"""
            The ZIP file contains probe files for **{gene_count} genes** organized by initiator (B1, B2, B3, B4).
            Each gene has separate probe sets:
            - `final_orf_probes_*.csv` - Probes for coding region
            - `final_five_prime_probes_*.csv` - 5' UTR probes
            - `final_three_prime_probes_*.csv` - 3' UTR probes
            """)
        else:
            st.info("""
            The ZIP file contains probe files organized by initiator (B1, B2, B3, B4):
            - `final_orf_probes_*.csv` - Probes for coding region
            - `final_five_prime_probes_*.csv` - 5' UTR probes
            - `final_three_prime_probes_*.csv` - 3' UTR probes
            """)

        # Show console output
        with st.expander("📋 View Processing Log"):
            st.code(st.session_state.get('console_output', 'No output available'))
    else:
        st.info("👈 Upload files and click 'Generate Probes' to see results here")

with tab3:
    st.header("How to Use ProbeGenerator")

    st.markdown("""
    ### Quick Start

    1. **Upload Gene Sequence** - FASTA file with your gene(s) - **Multi-FASTA supported!**
    2. **Choose Initiators** - Use default B1-B4 initiators or upload custom CSV
    3. **Specify Genome Index** - Path to your Bowtie2 genome index
    4. **Adjust Parameters** (optional) - Use sidebar to customize probe design
    5. **Generate Probes** - Click the button and wait
    6. **Download Results** - Get your ready-to-order probes

    ### Required Files

    #### Gene Sequence (FASTA)
    **Single gene:**
    ```
    >MyGene
    ATCGATCGATCG...
    ```

    **Multiple genes (Batch mode):**
    ```
    >Gene1
    ATCGATCGATCG...
    >Gene2
    GCTAGCTAGCTA...
    >Gene3
    TTAATTAATTAA...
    ```
    The system will automatically detect and process all genes in the file!

    #### Initiators
    **Default:** B1-B4 HCR initiator sequences are built-in. Just use the checkbox!

    **Custom CSV format (optional):**
    ```
    initiator,left sequence,left spacer,right sequence,right spacer
    B1,gAggAgggCAgCAAACgg,AA,gAAgAgTCTTCCTTTACg,TA
    B2,CCTCgTAAATCCTCATCA,AA,ATCATCCAgTAAACCgCC,AA
    ```

    #### Genome Index
    Pre-built Bowtie2 index for your organism. Must be accessible from the server.

    ### Probe Design Parameters

    - **Length**: Typically 20-30 bp
    - **GC Content**: 20-80% for specificity
    - **Tm**: 37-72°C for hybridization
    - **Spacing**: Max distance between probe pairs
    - **Spacer nucleotides**: N's between probe halves (default: 3)

    ### Output Files

    **For each gene and initiator (B1-B4), you get:**
    - ORF probes (main coding region)
    - 5' UTR probes
    - 3' UTR probes

    **File organization:**
    - Single gene: `GeneName_probes_results.zip`
    - Multiple genes: `Gene1_and_N_others_probes_results.zip`
    - Inside: organized by initiator folders (B1/, B2/, B3/, B4/)
    - Each folder contains probes for all genes

    CSV format with columns: set, probe, sequence

    ### Troubleshooting

    - **Genome index not found**: Check the path and ensure all .bt2 files exist
    - **No probes generated**: Adjust parameters (relax GC% or Tm ranges)
    - **Timeout**: Large genomes may exceed web processing limits

    ### Citation

    Please cite:
    - OligoMiner (Beliveau et al., 2018, PNAS)
    - Bowtie2 (Langmead & Salzberg, 2012, Nature Methods)
    - HCR (Choi et al., 2018, Development)
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>ProbeGenerator v1.0 | Python 3 Compatible |
    <a href='https://github.com/beliveau-lab/OligoMiner'>OligoMiner</a> +
    <a href='http://bowtie-bio.sourceforge.net/bowtie2/'>Bowtie2</a>
    </p>
</div>
""", unsafe_allow_html=True)
