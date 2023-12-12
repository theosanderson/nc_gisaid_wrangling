import argparse
import pandas as pd
import tarfile
from Bio import SeqIO
import gzip
import sys, tqdm, io
import subprocess

# Set up argument parser
parser = argparse.ArgumentParser(description='Process sequences.')
parser.add_argument('nc_tsv_gz_path', type=str, help='Path to the nc.tsv.gz file')
parser.add_argument('sequences_tar_xz_path', type=str, help='Path to the sequences_fasta_2023_12_11.tar.xz file')

# Parse arguments
args = parser.parse_args()

# Print loading to stderr
print('Loading sequences from {}...'.format(args.nc_tsv_gz_path), file=sys.stderr)
df = pd.read_csv(args.nc_tsv_gz_path , sep='\t', usecols=['seqName'])

print('Loaded {} sequences.'.format(len(df)), file=sys.stderr)
seq_names = set(df['seqName'])
print('Loaded {} unique sequences.'.format(len(seq_names)), file=sys.stderr)

command = f"tar -xJf {args.sequences_tar_xz_path} --to-stdout sequences.fasta"
# stream from command

print('Loading sequences from {}...'.format(args.sequences_tar_xz_path), file=sys.stderr)

with subprocess.Popen(['tar', '-xJf', args.sequences_tar_xz_path, '--to-stdout', 'sequences.fasta'], stdout=subprocess.PIPE) as proc:
    # Use Bio.SeqIO to parse the fasta file from the stdout of the tar command
    # make a text stream
    with io.TextIOWrapper(proc.stdout, encoding='utf-8') as text_stream:
    
        for record in tqdm.tqdm(SeqIO.parse(text_stream, 'fasta'), total=len(seq_names)):
            # Check if the sequence name is not in the set
            if record.id not in seq_names:
                # Process or output the record as needed
                # For example, print the record (or you can write it to a file or do other processing)
                print(record.format('fasta'))
            else:
                # Optionally, handle the case where the sequence is already in the set
                pass

    # Check for errors in the subprocess
    if proc.returncode and proc.returncode != 0:
        print(f"Error in executing tar command: return code {proc.returncode}", file=sys.stderr)