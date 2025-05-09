#!/bin/bash

cd ~/git_projekte/marbel/simulated_reads

# CSV-Datei vorbereiten
echo -n > ./summary/samples.csv

# Alle passenden FASTQ-Dateien finden
for r1 in sample_*_group*_R1.fastq.gz; do
    # Entsprechende R2-Datei
    r2="${r1/_R1.fastq.gz/_R2.fastq.gz}"

    # Prüfe, ob R2 existiert
    if [[ -f "$r2" ]]; then
        # Sample-Nummer extrahieren
        sample_num=$(echo "$r1" | grep -oP 'sample_\K[0-9]+')

        # Gruppe extrahieren (1 oder 2)
        group=$(echo "$r1" | grep -oP 'group\K[12]')

        # Gruppencode A oder B
        if [[ "$group" == "1" ]]; then
            group_code="A"
        else
            group_code="B"
        fi

        # Schreibe Zeile in CSV
        echo "$r1,$r2,$group_code,$sample_num" >> ./summary/samples.csv
    fi
done
