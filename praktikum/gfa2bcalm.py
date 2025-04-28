import re #regular expressions
import argparse
import ast
from collections import defaultdict

def parse_gfa(input_path, num_of_samples):
    """
    Parse a GFA-like file and extract:
    - S lines (sequences and optional metadata)
    - L lines (edges between unitigs)
    Returns:
        sequences: dict of {unitig_id: sequence}
        metadata: dict of {unitig_id: metadata string}
        links: dict of {unitig_id: list of L: edge descriptors}
    """
    sequences = {} # here I create the keys myself, same for metadata
    metadata = {} 
    abundance = {}
    sums = {}
    links = defaultdict(list) # safety because otherwise I would have to check if key exists

    with open(input_path, 'r') as f:
        for line in f:
            if line.startswith('S'):
                # Sequence line
                # egal ob metadata in "" oder nicht, sie ist nur mit ' ' und bleibt so zusammen
                _, sid, seq, comment = line.strip().split('\t', 3)
                sequences[sid] = seq

                # Metadata: samples / tags rausfiltern
                # Suche nach dem ersten Vorkommen einer Liste in eckigen Klammern (z. B. ['a', 'b'])
                match = re.search(r'\[.*?\]', comment)

                if match:
                    list_str = match.group(0) # extracts as string
                    samples = ast.literal_eval(list_str) # wandelt ihn um in Liste
                else: samples = []

                samples_line = ','.join(samples) # you must not have spaces in the samplen names
                metadata[sid] = samples_line

                # etwas das sich sum zieht
                match = re.search(r"sum:\s*([\d\.]+)", comment)

                # den rechenschritt könnte man auch woanders machen
                if match:
                    sum_int = int(match.group(1))
                    sums[sid] = sum_int
                    abundance[sid]=sum_int/num_of_samples

            elif line.startswith('L'):
                # Link/edge line
                # Format: L <from_id> <from_orient> <to_id> <to_orient> <overlap>
                _, from_id, from_orient, to_id, to_orient, _ = line.strip().split('\t')

                # Store the link in "L:<from_strand>:<to_id>:<to_strand>" format
                links[from_id].append(f"L:{from_orient}:{to_id}:{to_orient}")
    
    return sequences, metadata, links, abundance, sums

def write_custom_fa(output_path, sequences, metadata, links, abundance, sums):
    """
    Write the converted output to custom .fa-like format.
    Header includes:
        >unitig_id metadata: ... L:... L:... km:f:...
    Followed by:
       sequence
    """

    with open(output_path, 'w') as out:
        for sid in sequences:
            # speicher erstmal einzelne felder in liste
            header_parts = [f">{sid}"]

            # Add metadata (if exists)
            # get gibt zwar den wert zum schlüssel ist hier aber nur als test, ob ein eintrag existiert
            if metadata.get(sid):
                header_parts.append(f"metadata: {metadata[sid]}") # metadata ist eine dict von strings

            # Add all edge descriptions (if any)
            # links ist ein dict von listen.
            # += hängt alle elemente einzeln an 
            # get(sid, []) gibt leere liste zurück, falls keine links existieren
            # rückgabe [] weil list += None Fehler geben würde
            header_parts += links.get(sid, []) 

            # add sums
            if sums.get(sid):
                header_parts.append(f"KC:i:{sums[sid]}")

            # add abundance
            if abundance.get(sid):
                header_parts.append(f"km:f:{abundance[sid]}")

            # Join all parts with space as separator
            header_line = ' '.join(header_parts)

            # Write header and sequence
            out.write(header_line + '\n')
            out.write(sequences[sid] + '\n')


# zur ausführung

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert GFA file to custom FASTA-like format.")
    parser.add_argument("input_gfa", help="Pfad zur Eingabe-GFA-Datei")
    parser.add_argument("output_fa", help="Pfad zur Ausgabedatei")
    parser.add_argument("num_of_samples", type=int, help="Anzahl der verwendeten Samples")

    args = parser.parse_args()

    # Parse and convert
    sequences, metadata, links, abundance, sums = parse_gfa(args.input_gfa, args.num_of_samples)

    write_custom_fa(args.output_fa, sequences, metadata, links, abundance, sums)
