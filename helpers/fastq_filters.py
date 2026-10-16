"""Helper functions for reading, filtering, and writing FASTQ files."""


def gc_filter(sequence_line: str, gc_bounds: float | tuple[float, float]) -> bool:
    """
    Check whether GC content is within specified bounds.
    Args:
        sequence_line: a string containing the nucleotide sequence
        gc_bounds: GC content limits (%).
            A single number specifies the upper bound.
            A tuple specifies (lower_bound, upper_bound).
    """
    # Remove newline characters
    sequence_line = sequence_line.rstrip("\r\n").upper()

    # Calculate GC content
    gc_content = (
        (sequence_line.count("G") + sequence_line.count("C")) / len(sequence_line) * 100
    )

    # Check whether one or two bounds are provided
    if isinstance(gc_bounds, (int, float)):
        # If so, compare GC content with the specified value
        return gc_content <= gc_bounds
    # Otherwise, compare GC content with the specified range
    return gc_bounds[0] <= gc_content <= gc_bounds[1]


def length_filter(sequence_line: str, length_bounds: int | tuple[int, int]) -> bool:
    """
    Check whether sequence length is within specified bounds.
    Args:sequence length
        sequence_line: a string containing the nucleotide sequence
        length_bounds: length limits.
            A single number specifies the upper bound.
            A tuple specifies (lower_bound, upper_bound).
    """
    # Remove newline characters
    sequence_line = sequence_line.rstrip("\r\n")

    # Check whether one or two bounds are provided
    if isinstance(length_bounds, (int)):
        # If so, compare sequence length with the specified value
        return len(sequence_line) <= length_bounds
    # Otherwise, compare sequence length with the specified range
    return length_bounds[0] <= len(sequence_line) <= length_bounds[1]


def quality_filter(quality_line: str, quality_threshold: int) -> bool:
    """
    Convert Phred+33 quality scores to numeric Phred scores,
    calculate the mean quality, and compare it with the threshold.
    """
    # Remove newline characters
    quality_line = quality_line.rstrip("\r\n")  # Убирает концы у стоки
    # Convert ASCII characters to Phred scores
    phred_scores = [ord(char) - 33 for char in quality_line]
    # Calculate mean quality and compare with threshold
    return sum(phred_scores) / len(phred_scores) >= quality_threshold


def read_fastq(input_fastq: str):
    """Read FASTQ records one at a time."""

    with open(input_fastq, "r") as file:
        record_number = 0

        while True:
            header = file.readline()  # Read header

            if not header:  # Stop when the file ends
                break

            sequence = file.readline()  # Read sequence line
            separator = file.readline()  # Read separator
            quality = file.readline()  # Read quality line

            record_number += 1

            # Check for unexpected end of file
            if not (sequence and separator and quality):
                raise ValueError(f"Unexpected end of file in record {record_number}")

            # Validate header
            if not header.startswith("@"):
                raise ValueError(f"Invalid header in record {record_number}")

            # Validate separator
            if not separator.startswith("+"):
                raise ValueError(f"Invalid separator in record {record_number}")

            # Validate sequence and quality lengths
            if len(sequence.rstrip("\r\n")) != len(quality.rstrip("\r\n")):
                raise ValueError(f"Length mismatch in record {record_number}")

            # Pass the record to the next function
            yield header, sequence, separator, quality
