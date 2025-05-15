import re  # regular expressions
import argparse
import ast  # string to list umwandeln
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
    abundance = {}  # dieses Dict ist aktuell ohne Nutzen, da es später ein Feld befüllt, dass vizitig gar nicht verarbeitet

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
                # alternativ nach samples: wenn das immer so heißt
                match = re.search(r'\[.*?\]', comment)

                if match:
                    list_str = match.group(0) # gibt vollständigen Treffer zurück, also mit []
                    samples = ast.literal_eval(list_str) # wandelt ihn um in Liste
                else: samples = []

                samples_line = ','.join(samples) # you must not have spaces in the samplen names
                metadata[sid] = samples_line

                # etwas das sich sum zieht
                match = re.search(r"sum:\s*([\d\.]+)", comment)

                # den rechenschritt könnte man auch auslagern
                if match:
                    sum_int = int(match.group(1))  # gibt nur den Teil des Treffers der in den Klammern des re-Ausdrucks steht
                    sums[sid] = sum_int
                    abundance[sid]=sum_int/num_of_samples  # dieses Dict ist aktuell ohne Nutzen, da es später ein Feld befüllt, dass vizitig gar nicht verarbeitet

            elif line.startswith('L'):
                # Link/edge line
                # Format: L <from_id> <from_orient> <to_id> <to_orient> <overlap>
                _, from_id, from_orient, to_id, to_orient, _ = line.strip().split('\t')

                # Store the link in "L:<from_strand>:<to_id>:<to_strand>" format
                links[from_id].append(f"L:{from_orient}:{to_id}:{to_orient}")
    
    return sequences, metadata, links, abundance, sums


def parse_gaf(gaf_path):
    """
    Liest eine GAF-Datei ein und extrahiert die Zuordnung von Transkript-IDs zu Node-IDs.
    
    Rückgabe: Dict[str, List[int]]
    """
    transcript_to_sids = {}
    with open(gaf_path, 'r') as gaf_file:
        for line in gaf_file:
            transcript_id, _, _, _, _, path, _ = line.strip().split('\t', 6) # transcriptId und Path extrahieren
            sids = re.findall(r'\d+', path) # Path von einem String mit >< zu einer Liste von Integers
            transcript_to_sids[transcript_id] = sids # dict befüllen
    return transcript_to_sids



def write_transcript_fasta(transcript_to_sids, sequences, output_path):
    """
    Schreibt eine FASTA-Datei basierend auf Transkript-zu-NodeID-Zuordnung und gegebenen Sequenzen.
    """
    with open(output_path, 'w') as out_fasta:
        for transcript_id, sids in transcript_to_sids.items():
            for sid in sids:
                if sequences.get(sid):  # wird None wenn Schlüssel nicht existiert
                    out_fasta.write(f'>{transcript_id}\n{sequences[sid]}\n')
                else: print(f"{sid} existiert in sequences nicht")


def write_fasta_unitig(out, sid, sequences, metadata, links, abundance, sums):
    """
    Schreibt eine FASTA-Einheit (Header + Sequenz) für einen Unitig
    """
    header_parts = [f">{sid} genes: GENE0"]  # Header beginnt mit ID + Gene-Info

    if metadata.get(sid):  # falls Metadaten vorhanden
        header_parts.append(f"metadata: {metadata[sid]}")  # z. B. metadata: A_1,B_2

    header_parts += links.get(sid, [])  # alle "L:"-Einträge (Kanten)

    if sums.get(sid):  
        # dieses Feld ist aktuell ein Platzhalter ohne Funktion, denn:
        # der KC:i:-Eintrag (absolut abundance) wird vom vizitig parser nicht gelesen (optional)
        # hier wird aktuell die mean abundance eingetragen, da sie ebenfalls Probleme hat s.u.
        header_parts.append(f"KC:i:{abundance[sid]}")

    if abundance.get(sid):  
        # eigentlich sollte hier der (mean) Abundance-Wert eingetragen werden (optional)
        # Aber im webclient ist Filtern nur nach Werten >= 1 möglich 
        # daher verwende ich hier die absolut Abundance aus sums
        header_parts.append(f"km:f:{sums[sid]}")

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
            # hänge neue sid an die Listen an, die zu den jeweiligen Samples gehören
            sample_to_unitigs[sample].append(sid)

    # Für jedes Sample wird eine eigene Datei geschrieben
    for sample, sids in sample_to_unitigs.items():
        # for ... in dict bringt liste von Tupeln von key und value
        # das tupel wird direkt entpackt
        output_path = join(output_dir, f"Sample_{sample}.fa")

        # Datei öffnen zum Schreiben
        with open(output_path, 'w') as out:
            # Alle zugehörigen Unitigs für dieses Sample schreiben
            for sid in sids:
                # Verwende die Hilfsfunktion, um Header + Sequenz zu schreiben
                write_fasta_unitig(out, sid, sequences, metadata, links, abundance, sums)



def write_bcalm_fa(output_path, sequences, metadata, links, abundance, sums):
    """
    Writes a bcalm style fasta-file, using the information stored in dictionaries

    ><id> metadata: <sample1, sample2, ...> KC:i:<abundance> km:f:<abundance> L:<+/->:<other id>:<+/->/n
    <sequence>
    """
    with open(output_path, 'w') as out:
        for sid in sequences:
            write_fasta_unitig(out, sid, sequences, metadata, links, abundance, sums)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert GFA file to bcalm FASTA-like format.")
    parser.add_argument("input_gfa", help="Pfad zur Eingabe-GFA-Datei")
    parser.add_argument("output_fa", help="Pfad zur Ausgabedatei")
    parser.add_argument("num_of_samples", type=int, help="Anzahl der verwendeten Samples")
    parser.add_argument("--sample_dir", default="sample_fas", help="Ordner für pro-Sample FASTA-Dateien")
    parser.add_argument("output_transcript")
    parser.add_argument("gaf_path")

    args = parser.parse_args()

    # Parsen and konvertieren
    sequences, metadata, links, abundance, sums = parse_gfa(args.input_gfa, args.num_of_samples)
    
    write_bcalm_fa(args.output_fa, sequences, metadata, links, abundance, sums)
    write_sample_fas(args.sample_dir, sequences, metadata, links, abundance, sums)

    transcript_to_sids = parse_gaf(args.gaf_path)

    write_transcript_fasta(transcript_to_sids, sequences, args.output_transcript)

    # nur zur Kontrolle
    if not transcript_to_sids:
        print("transcript_to_sids is an empty dict")
    # schlüssel_typen = {type(key) for key in sequences.keys()}
    # print(f"Die Schlüssel im Dict haben den Typ {schlüssel_typen}")