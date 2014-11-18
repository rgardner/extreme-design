def write_to_csv(filename, packets):
    """Append data to given file."""
    with open(filename, "a") as f:
        for packet in packets:
            f.write(packet.to_csv())
