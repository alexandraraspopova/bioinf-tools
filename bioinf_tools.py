import os

from helpers.bioinf_tools_utils import (
    parse_arguments,
    prepare_fasta_output_path,
    prepare_output_path,
    write_fasta_record,
)
from helpers.fastq_filters import (
    gc_filter,
    length_filter,
    quality_filter,
    read_fastq,
)


def main() -> None:
    """Run the selected bioinformatics utility."""
    args = parse_arguments()

    if args.task == "filter_fastq":
        filter_fastq(
            args.input_fastq,
            args.output_fastq,
            args.gc_bounds,
            args.length_bounds,
            args.quality_threshold,
        )

    elif args.task == "fasta_oneline":
        convert_multiline_fasta_to_oneline(
            args.input_fasta,
            args.output_fasta,
        )


# filter function
def filter_fastq(
    input_fastq: str,
    output_fastq: str,
    gc_bounds: float | tuple[float, float] = (0, 100),
    length_bounds: int | tuple[int, int] = (0, 2**32),
    quality_threshold: float = 0,
):
    """
    Filter FASTQ reads.
    Args:
        input_fastq: Path to the input FASTQ file.
        output_fastq: Name to the output FASTQ file.
        gc_bounds: GC content limits (%).
            A single number specifies the upper bound.
            A tuple specifies (lower_bound, upper_bound).
        length_bounds: Read length limits (bp).
            A single number specifies the upper bound.
            A tuple specifies (lower_bound, upper_bound).
        quality_threshold: Minimum mean Phred quality.
    """

    # Prepare output path
    output_path = prepare_output_path(input_fastq, output_fastq)

    # Open output file
    with open(output_path, "w") as output:
        # Read input file
        for record in read_fastq(input_fastq):
            # Apply filters
            if (
                length_filter(record[1], length_bounds)
                and gc_filter(record[1], gc_bounds)
                and quality_filter(record[3], quality_threshold)
            ):
                # Write the filtered record
                output.writelines(record)
    print(f"FASTQ file saved to: {os.path.abspath(output_path)}")


# converter function
def convert_multiline_fasta_to_oneline(
    input_fasta: str,
    output_fasta: str | None = None,
) -> None:
    """Convert multiline FASTA file to single-line format."""

    # Prepare the output file path
    output_fasta = prepare_fasta_output_path(input_fasta, output_fasta)

    # Open input and output files
    with open(input_fasta, "r") as input_file, open(output_fasta, "w") as output_file:
        header = None
        seq_parts = []

        # Read the input file
        for line in input_file:
            line = line.strip()

            # Check for a new header
            if line.startswith(">"):
                # If True - write the previous record
                if header is not None:
                    write_fasta_record(output_file, header, seq_parts)
                # And start a new record
                header = line
                seq_parts = []

            else:
                # Add sequence to the list
                seq_parts.append(line)

        # Write the last record because > will not appear again.
        if header is not None:
            write_fasta_record(output_file, header, seq_parts)
    print(f"FASTA file saved to: {os.path.abspath(output_fasta)}")


# Parse arguments from command line and pass to filter_fastq()

if __name__ == "__main__":
    main()
