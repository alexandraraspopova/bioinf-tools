"""Utils for fastq_filter"""

import os
import argparse


def prepare_output_path(input_fastq: str, output_fastq: str) -> str:
    """Create the directory "filtered" and return the output file path."""

    # Get the input file directory
    input_dir = os.path.dirname(os.path.abspath(input_fastq))

    # Create the directory "filtered"
    output_dir = os.path.join(input_dir, "filtered")
    os.makedirs(output_dir, exist_ok=True)

    # Return the output file path
    return os.path.join(output_dir, output_fastq)


def prepare_fasta_output_path(
    input_fasta: str,
    output_fasta: str | None = None,
) -> str:
    """Generate the output FASTA file path."""

    # Get the input file directory
    input_dir = os.path.dirname(os.path.abspath(input_fasta))

    # Generate the output filename
    if output_fasta is None:
        name, extension = os.path.splitext(os.path.basename(input_fasta))
        output_fasta = f"{name}_oneline{extension or '.fasta'}"

    else:
        name, extension = os.path.splitext(output_fasta)
        if not extension:
            output_fasta += ".fasta"

    # Save the output near the input file
    if not os.path.dirname(output_fasta):
        output_fasta = os.path.join(input_dir, output_fasta)

    return output_fasta


def write_fasta_record(output_file, header: str, seq_parts: list[str]) -> None:
    output_file.write(header + "\n")
    output_file.write("".join(seq_parts) + "\n")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Bioinformatics utilities")

    # Create tasks
    subparsers = parser.add_subparsers(
        dest="task",
        required=True,
    )

    # FASTQ filtering command
    fastq_parser = subparsers.add_parser(
        "filter_fastq",
        help="Filter FASTQ reads",
        description="Filter FASTQ reads by GC content, length, and quality",
    )

    fastq_parser.add_argument(
        "-i", "--input-fastq", help="Input FASTQ path", required=True
    )
    fastq_parser.add_argument(
        "-o", "--output-fastq", help="Output filename", required=True
    )
    fastq_parser.add_argument(
        "-g",
        "--gc-bounds",
        nargs="+",
        type=float,
        help="One upper bound or two GC bounds (%%)",
    )
    fastq_parser.add_argument(
        "-l",
        "--length-bounds",
        nargs="+",
        type=int,
        help="One upper bound or two read length bounds",
    )
    fastq_parser.add_argument(
        "-q",
        "--quality-threshold",
        type=float,
        default=0,
        help="Minimum mean Phred quality (default: 0)",
    )

    # FASTA conversion task
    fasta_parser = subparsers.add_parser(
        "fasta_oneline",
        help="Convert multiline FASTA to single-line format",
    )

    fasta_parser.add_argument(
        "-i",
        "--input-fasta",
        help="Input FASTA path",
        required=True,
    )

    fasta_parser.add_argument(
        "-o",
        "--output-fasta",
        help="Output FASTA path (optional)",
        default=None,
    )

    args = parser.parse_args()

    if args.task == "filter_fastq":
        # Process GC bounds
        gc_bounds = (0, 100)
        # Check whether the argument was provided
        if args.gc_bounds is not None:
            # Raise an error if more than two values were provided
            if len(args.gc_bounds) > 2:
                fastq_parser.error("GC bounds must contain one or two numbers")
            # If one value was provided, assign it directly
            if len(args.gc_bounds) == 1:
                gc_bounds = args.gc_bounds[0]
            # If two values were provided, convert them to a tuple
            else:
                gc_bounds = tuple(args.gc_bounds)

        # Process length bounds
        length_bounds = (0, 2**32)
        if args.length_bounds is not None:
            if len(args.length_bounds) > 2:
                fastq_parser.error("Length bounds must contain one or two numbers")
            if len(args.length_bounds) == 1:
                length_bounds = args.length_bounds[0]
            else:
                length_bounds = tuple(args.length_bounds)

        args.gc_bounds = gc_bounds
        args.length_bounds = length_bounds

    return args
