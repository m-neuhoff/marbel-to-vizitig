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


def write_fasta_unitig(out, sid, sequences, metadata, links, abundance, sums):
    """
    Schreibt eine FASTA-Einheit (Header + Sequenz) für einen Unitig in einen offenen Datei-Handle.
    """
    header_parts = [f">{sid} genes: GENE0"]  # Header beginnt mit ID + Gene-Info

    if metadata.get(sid):  # falls Metadaten vorhanden
        header_parts.append(f"metadata: {metadata[sid]}")  # z. B. metadata: A_1,B_2

    header_parts += links.get(sid, [])  # alle "L:"-Einträge (Kanten)

    if sums.get(sid):  # Sum-Wert hinzufügen (optional)
        header_parts.append(f"KC:i:{sums[sid]}")

    if abundance.get(sid):  # Abundance-Wert hinzufügen (optional)
        header_parts.append(f"km:f:{abundance[sid]}")

    # Alle Teile mit Leerzeichen verbinden und schreiben
    header_line = ' '.join(header_parts)
    out.write(header_line + '\n')

    # Sequenzzeile schreiben
    out.write(sequences[sid] + '\n')



def write_sample_fas(output_dir, sequences, metadata, links, abundance, sums):
    """
    Schreibt für jedes vorkommende Sample eine eigene FASTA-Datei.
    Jede Datei enthält alle Unitigs, in deren Metadaten dieses Sample enthalten ist.
    """

    from os import makedirs  # zum Erstellen von Verzeichnissen
    from os.path import join, exists  # um Pfade zu bauen und Existenz zu prüfen

    # Falls der Ausgabepfad nicht existiert, erstelle das Verzeichnis
    if not exists(output_dir):
        makedirs(output_dir)

    # sample_to_unitigs sammelt pro Sample alle zugehörigen Unitig-IDs
    sample_to_unitigs = defaultdict(list)

    # Durchlaufe alle Unitigs und ihre Metadaten
    for sid, samples_str in metadata.items():
        # Die Metadaten enthalten Samples als kommaseparierte Strings -> in Liste umwandeln
        for sample in samples_str.split(','):
            # Jeder Sample-Name bekommt die aktuelle Unitig-ID zugewiesen
            sample_to_unitigs[sample].append(sid)

    # Für jedes Sample wird eine eigene Datei geschrieben
    for sample, sids in sample_to_unitigs.items():
        # Dateiname im Stil "Sample_A_1.fa"
        output_path = join(output_dir, f"Sample_{sample}.fa")

        # Datei öffnen zum Schreiben
        with open(output_path, 'w') as out:
            # Alle zugehörigen Unitigs für dieses Sample schreiben
            for sid in sids:
                # Verwende die Hilfsfunktion, um Header + Sequenz zu schreiben
                write_fasta_unitig(out, sid, sequences, metadata, links, abundance, sums)



def write_custom_fa(output_path, sequences, metadata, links, abundance, sums):
    with open(output_path, 'w') as out:
        for sid in sequences:
            write_fasta_unitig(out, sid, sequences, metadata, links, abundance, sums)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert GFA file to custom FASTA-like format.")
    parser.add_argument("input_gfa", help="Pfad zur Eingabe-GFA-Datei")
    parser.add_argument("output_fa", help="Pfad zur Ausgabedatei")
    parser.add_argument("num_of_samples", type=int, help="Anzahl der verwendeten Samples")
    parser.add_argument("--sample_dir", default="sample_fas", help="Ordner für pro-Sample FASTA-Dateien")

    args = parser.parse_args()

    # Parse and convert
    sequences, metadata, links, abundance, sums = parse_gfa(args.input_gfa, args.num_of_samples)

    write_custom_fa(args.output_fa, sequences, metadata, links, abundance, sums)
    write_sample_fas(args.sample_dir, sequences, metadata, links, abundance, sums)