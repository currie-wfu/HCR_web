import os

# Use relative path for local execution, or /data/output for Docker
OUTPUT_BASE_DIR = os.path.join(os.getcwd(), 'output') if not os.path.exists('/data') else os.path.join('/data', 'output')
TEST_BASE_DIR="/c/Users/stein.davi/projects/probes/output"

# Default initiator sequences
# Format: [initiator_name, left_sequence, left_spacer, right_sequence, right_spacer]
DEFAULT_INITIATORS = [
    ['B1', 'GAGGAGGGCAGCAAACGG', 'aa', 'GAAGAGTCTTCCTTTACG', 'ta'],
    ['B2', 'CCTCGTAAATCCTCATCA', 'aa', 'ATCATCCAGTAAACCGCC', 'aa'],
    ['B3', 'GTCCCTGCCTCTATATCT', 'tt', 'CCACTCAACTTTAACCCG', 'tt'],
    ['B4', 'CCTCAACCTACCTCCAAC', 'aa', 'TCTCACCATATTCGCTTC', 'at']
]