# bioinf-tools

A collection of Python command-line utilities for processing bioinformatics data.

## Available Tools

### 1. FASTQ Filter

Filter FASTQ sequencing reads based on:

- GC content (%).
- Sequence length (bp).
- Mean Phred quality.

### 2. FASTA Multiline to Oneline Converter

Convert a multiline FASTA file into a single-line FASTA format.


## Dependencies

- No third-party Python packages are required.

## Limitations

- Only uncompressed FASTQ and FASTA files are supported.
- FASTQ quality scores are assumed to use Phred+33 encoding.

## Project Structure

- `bioinf_tools.py` — main functions and program entry point.
- `fastq_filters.py` — functions for reading FASTQ records and applying filters.
- `bioinf_tools_utils.py` — command-line argument parsing, output path preparation, and FASTA record writing.

## Usage

The program provides two subcommands:

```bash
python bioinf_tools.py filter_fastq [options]
```

```bash
python bioinf_tools.py fasta_oneline [options]
```

## FASTQ Filter

### Command-Line Arguments

| Argument | Description | Default |
|---|---|---|
| `-i`, `--input-fastq` | Path to the input FASTQ file | Required |
| `-o`, `--output-fastq` | Output FASTQ filename | Required |
| `-g`, `--gc-bounds` | GC content limits (%) | `(0, 100)` |
| `-l`, `--length-bounds` | Read length limits (bp) | `(0, 2**32)` |
| `-q`, `--quality-threshold` | Minimum mean Phred quality | `0` |
| `-h`, `--help` | Display help information | — |

### GC Content Filter

A single number specifies the maximum allowed GC content:

```bash
-g 50
```

Two numbers specify the lower and upper bounds:

```bash
-g 20 80
```

Both boundaries are inclusive.

### Read Length Filter

A single number specifies the maximum read length:

```bash
-l 250
```

Two numbers specify a length range:

```bash
-l 100 250
```

Both boundaries are inclusive.

### Quality Filter

Use `-q` to specify the minimum average Phred quality:

```bash
-q 30
```

A read is retained if its mean Phred quality is greater than or equal to the threshold.

The program assumes Phred+33 quality encoding.

### Examples

**1. Filter by GC content**

```bash
python bioinf_tools.py filter_fastq -i reads.fastq -o result.fastq -g 30 70
```

Retain reads with GC content between 30% and 70%.

**2. Filter by read length**

```bash
python bioinf_tools.py filter_fastq -i reads.fastq -o result.fastq -l 100 250
```

Retain reads containing 100–250 nucleotides.

**3. Filter by mean quality**

```bash
python bioinf_tools.py filter_fastq -i reads.fastq -o result.fastq -q 25
```

Retain reads with mean Phred quality of at least 25.

**4. Apply all filters**

```bash
python bioinf_tools.py filter_fastq -i reads.fastq -o result.fastq -g 30 70 -l 100 250 -q 25
```

A read is retained only if it passes all three filters.

### Output

The program automatically creates a directory named `filtered` in the same directory as the input FASTQ file.

The output file contains FASTQ records that satisfy all selected filtering criteria.

## FASTA Multiline to Oneline Converter

The `fasta_oneline` command converts multiline FASTA sequences into single-line format.

### Command-Line Arguments

| Argument | Description | Default |
|---|---|---|
| `-i`, `--input-fasta` | Path to the input FASTA file | Required |
| `-o`, `--output-fasta` | Output FASTA filename or path | Optional |
| `-h`, `--help` | Display help information | — |

### Examples

**Convert FASTA with an automatically generated filename**

```bash
python bioinf_tools.py fasta_oneline -i data/sequences.fasta
```

The output file will be:

```text
data/sequences_oneline.fasta
```

---

## Useful Resources

- [FASTA format — NCBI](https://www.ncbi.nlm.nih.gov/genbank/fastaformat/) -- FASTA file format specification.
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html) -- command-line argument parsing.
- [Python os.path documentation](https://docs.python.org/3/library/os.path.html) -- common pathname manipulations.
- [Python file handling](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files) -- reading and writing files.
- [The ultimate bioinformatics survival guide](https://www.youtube.com/watch?v=vx2u5uUu3DE) -- essential tips for surviving long debugging sessions.