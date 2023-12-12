Helper to run Nextclade on the previous unprocessed data

```
python get_prev_unprocessed_data.py ~/Desktop/nc.tsv.gz ~/Desktop/sequences_fasta_2023_12_11.tar.xz | ~/nextclade run --dataset-name sars-cov-2 --output-tsv nc2.tsv.gz
```