#!/usr/bin/env bash

# Probe generator local run script
# Uses --mm flag for memory-mapped Bowtie2 index access

set -e

# Configuration from env_file.txt
SEQ_PATH="Sp8.fa"
PATH_TO_BOWTIE_INDEX="."
BOWTIE_INDEX_BASENAME="GCF_040938575.1_UKY_AmexF1_1_genomic_long.fna"
INITIATOR="initiators.csv"
DESIRED_SPACES=3
L=25
U=25
G=20
MAX_G=80
T_MIN=37
T_MAX=72
S=1000
F=30

# Paths
WORK_DIR="/Users/curriej/Wake Forest University Dropbox/Joshua Currie/Claude/Probegenerator"
OLIGOMINER_DIR="$WORK_DIR/OligoMiner"
PROBEGEN_DIR="$WORK_DIR/probegenerator_src/probegenerator"

cd "$WORK_DIR"

# Remove existing output
if [ -d "output" ]; then
    echo "Removing existing output directory..."
    rm -rf output
fi

echo "Creating output directory..."
mkdir -p output

# Step 1: Parse multifasta
echo "Step 1: Parsing input FASTA..."
python3 "$PROBEGEN_DIR/parseMultifasta.py" -f "$SEQ_PATH"

# Read gene names
while read -r fasta; do
    echo "Processing gene: $fasta"

    # Extract gene name
    gene_name=(${fasta//\// })

    # Step 2: Run OligoMiner blockParse
    echo "  Step 2: Running OligoMiner blockParse..."
    python3 "$OLIGOMINER_DIR/blockParse.py" \
        -f "${fasta}.fa" \
        -l $L \
        -L $U \
        -g $G \
        -G $MAX_G \
        -t $T_MIN \
        -T $T_MAX \
        -s $S \
        -F $F \
        -O \
        -b \
        -o output/output

    # Step 3: Generate probes
    echo "  Step 3: Generating probes..."
    python3 "$PROBEGEN_DIR/probeGenerator.py" \
        -p output/output.bed \
        -f "${fasta}.fa" \
        -s $DESIRED_SPACES \
        -if "$INITIATOR"

    # Step 4: Run Bowtie2 alignment with --mm flag
    echo "  Step 4: Running Bowtie2 alignment (memory-mapped mode)..."
    bowtie2 --mm \
        -x "$PATH_TO_BOWTIE_INDEX/$BOWTIE_INDEX_BASENAME" \
        -U probes_for_alignment.fastq \
        -t \
        -k 100 \
        --very-sensitive-local \
        -S "${gene_name[1]}".sam

    # Step 5: Clean output
    echo "  Step 5: Cleaning output..."
    python3 "$OLIGOMINER_DIR/outputClean.py" \
        -u \
        -f "${gene_name[1]}".sam \
        -o "${gene_name[1]}"

    # Step 6: Copy files to initiator directories
    echo "  Step 6: Organizing output files..."
    python3 "$PROBEGEN_DIR/utils/file_copy_utils.py" \
        -i "$INITIATOR" \
        -n "${gene_name[1]}"

    # Step 7: Parse BAM and generate final probe files
    echo "  Step 7: Parsing alignments and generating final probes..."
    python3 "$PROBEGEN_DIR/parseBam.py" \
        -p "${gene_name[1]}/${gene_name[1]}_probes.csv" \
        -p2 "${gene_name[1]}/${gene_name[1]}" \
        -i "$INITIATOR"

    echo "  Complete!"
done < names.txt

echo ""
echo "==================================="
echo "Probe generation complete!"
echo "==================================="
echo "Results are in the 'output' directory"
