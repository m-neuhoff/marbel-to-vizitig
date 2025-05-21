# Praktikum: Vom Marbel-Datensatz zum colored debruijn-Graph

Dieses Repository zeigt, wie man von einem Marbel-Datensatz zu einem colored De-Bruijn-Graphen gelangt und diesen im Webclient von Vizitig visualisieren kann. Es enthält neben Slurm-Skripten zur Verwendung der verschiedenen Programme mein Skript zur Konvertierung von Graphen im GFA-Format in ein bcalm-style FASTA-Format. Außerdem macht es den ersten Schritt zu einem Vergleich der Ergebnisse beim Alignen von Transkripten mit GraphAligner vs Vizitig.

## Dependencies & Installation

Folgende Programme müssen installiert sein (die von mir verwendeten Versionen stehen in Klammern):

- marbel
- dbg
- GraphAligner
- vizitig

Ich habe Marbel in einer Conda-Umgebung installiert, dbg durch Klonen des Repositories (die Installation dann nach Elenas mündl. Anleitung), GraphAligner ebenfalls über Conda (außerhalb einer Umgebung) und Vizitig durch Klonen des Repositories und Installation gemäß der Anleitung im entsprechenden Repository.

## Inhalt und Verwendung dieses Repos

Im Repository befinden sich Bash- und SBATCH-Skripte für die einzelnen Teilaufgaben. Sie sind nummeriert in der Reihenfolge, in der sie ausgeführt werden sollen. Die Skripte müssen aus dem Hauptverzeichnis des Repositories gestartet werden. Skript 1 und 3 sind Bash-Skripte, die übrigen SBATCH-Skripte.

Die Pfade zu Marbel, dbg und GraphAligner in den jeweiligen Skripten müssen individuell angepasst werden und ggf. die entsprechenden Umgebungen aktiviert werden.

Beim Start jedes Skripts muss der Name des Datensatzes als Argument angegeben werden (im script wird er auf die Variable main_folder geschrieben). Ein Ordner mit diesem Namen wird durch das erste Skript erstellt und alle weiteren Skripte arbeiten mit relativen Pfaden basierend auf diesem Namen.

Beispiel:

`bash 1_make_folders.sh my_test`
`sbatch 2_marbel.sh my_test`

Im Ordner scripts befinden sich zwei Versionen meines Python-Skripts:

    Gfa2bcalm konvertiert lediglich GFA zu FASTA.

    Gfa2vizitig konvertiert GFA zu FASTA, erzeugt die für das Einfärben benötigten Sample-Dateien und generiert eine Transkriptdatei mit den Informationen aus dem Alignment mit GraphAligner. Im bash-Skript wird letzteres verwendet.

how2vizitig.sh ist ein Beispiel, wie die Vizitig-CLI verwendet werden kann.

Der Ordner bigger_example zeigt das Ergebnis, wenn alle Skripte (außer how2vizitig.sh) ausgeführt wurden. Der Datensatz wurde mit 4000 orthogroups, 10 spezies, 100000 library size und 3 samples pro Gruppe erstellt. Der kleinere Datensatz smaller_example ist besser geeignet für die Demonstration von vizitig auf meinem PC und wurde mit 200 orthogroups, 5 spezies, 10000 library size und 3 samples pro Gruppe erstellt.

Die Datei in file_list_csv wird von dbg verwendet. 

### Was macht gfa2vizitig?

Das script enthält neben dem Argument-Parser im main, als Funktionen einen Datei-Parser für gaf und einen für gfa. In diesen Datei-Parsern werden die relevanten Informationen in Dictionaries gelegt, i.d.R. mit der Segment bzw. Node-ID als Schlüssel. Auf diese Dictionaries greifen die verschiedenen write-Funktionen zu: 
- Eine schreibt den Graph als fasta, das Input-Format für vizitig.
- Eine andere generiert die Sample-Dateien, mit denen vizitig später den Graphen colort. Dazu kopiert sie alle Unitig-Zeilen, bei denen Sample x in den metadaten steht, in eine eigene Datei Sample_x.fa. 
- Eine dritte Funktion zieht aus dem gaf-Graph die Info, über welche Nodes ein Transcript läuft, um daraus eine Transcript-fasta-Datei zu generieren. 

## Über vizitig

### Input-Formate

Der Graph als fasta-Datei enthält ID, die Namen der Samples als metadata, die Links, Abundance und die Sequence;
in der Art wie bcalm es erzeugen würde: 
```
><id> metadata: <sample1, sample2, ...> KC:i:<abundance> km:f:<abundance> L:<+/->:<other id>:<+/->/n
<sequence>
```
Vizitig ließt allerdings nur das km:f: Feld ein. KC:i: wird ignoriert.
Vizitig erstellt aus dem fasta-Graph einen db-Graph. 
Um nach Samples zu filtern, müssen die samples als eigene fasta-Dateien vorliegen, die metadata-Spalte reicht nicht aus.

Die fasta-files von Exons müssen bestimmte header lines haben: `>|XX_DY220_RS02960|:0-0(unknown)`
fasta-files von Transcripten haben im header nur die TranscriptID stehen: `>DY220_RS02960`


### Nutzung von vizitig CLI

installiere vizitig 1.0.5 nur so (um zu überprüfen, ob pip mittlerweile auch 1.0.5 hat: `pip index versions vizitig`):
```bash
git clone https://gitlab.inria.fr/pydisk/examples/vizitig
cd vizitig
make install
```
Es wird ein vizitig-Ordner kopiert. Um vizitig zu verwenden, gehe in den Order und 
```...vizitig$ source venv/bin/activate```

Anschließend wird ein Graph wie unten beschrieben erstellt. Das kann anhand von bigger_example auch in how2vizitig.sh nachgeschaut werden. 
Colorn und annotieren ermöglichen beide das später der Graph anhand der jeweils hinterlegten Information gefiltert und gefärbt werden kann. Der Color-Begriff ist hier nur etwas verwirrend, weil damit in vizitig immer nur die Samples gemeint sind (eine Color = ein Sample). Wenn später nach mehreren Samples gefiltert werden können soll, müssen sie nacheinander mit dem color-Befehl eingebracht werden. Annotate bezieht sich auf Transcripte und Exons.

In Punkt 3 habe ich versucht aufzuzeigen, wie die abundance eingebracht werden kann, die nur als Option des color-Befehls existiert. 

0) Prüfe, ob die gfa eine AvailableKmerSize verwendet
1) Baue Graph mit: ```vizitig build mini_bcalm.fa -n minibcalm_graph # -n ist wichtig```
2) Indexe den Graph mit: ```vizitig index build minibcalm_graph -t RustIndex```
3) Colorn
    * Colorn nach Samples mit: ```vizitig color -f ./path/to/fastas/mini_sample1.fa -m sample1 minibcalm_graph```
    * Colorn nach sample und abundance mit: ```vizitig color -f ./path/to/fastas/mini_sample1.fa -m sample1 -abundances minibcalm_graph```
    * Colorn nach abundance mit: ```vizitig color -f ./path/to/fastas/mini_bcalm.fa -m allsamples -abundances minibcalm_graph```

(bei 3c bin ich mir nicht sicher, es macht keine fehlermeldung, aber ich sehe die färbung nicht, was aber an der geringen größe des samples liegen könnte)

Zum Vergleich: Es gibt mini_bcalm als kleinen Beispiel-Graph von vizitig, das wie im vizitig-Repo beschrieben mit vizitig erstellt werden kann. Dabei wird folgender Code ausgeführt.
```bash
small_ex:
	bash -c "source venv/bin/activate;python3 -m vizitig build examples/mini_bcalm.fa -n mini_bcalm"
	bash -c "source venv/bin/activate;python3 -m vizitig index build mini_bcalm"
	bash -c "source venv/bin/activate;python3 -m vizitig index build mini_bcalm --small-k 2"
	bash -c "source venv/bin/activate;python3 -m vizitig annotate mini_bcalm -e examples/mini_exons.fa"
	bash -c "source venv/bin/activate;python3 -m vizitig annotate mini_bcalm --transcripts examples/mini_ref.fa -m examples/mini_annot.gtf"
	bash -c "source venv/bin/activate;python3 -m vizitig color -f examples/mini_sample1.fa -d sample -m sample1 mini_bcalm"
	bash -c "source venv/bin/activate;python3 -m vizitig color -f examples/mini_sample2.fa.gz -d sample -m sample2 mini_bcalm"
	bash -c "source venv/bin/activate;python3 -m vizitig color -f examples/abundances.fa -d sample -m sample3 -abundances mini_bcalm"
```

sample-files können auch fna oder normales fasta sein (und natürlich bcalm fasta für abundancen) aber keine fastq

### Nutzung des webclients

Im webclient kann man die obigen Schritte auch per Mouseklick machen außer -abundances. Dazu läd man im webclient einen neuen Graph hoch im fasta-Format und kann mit klick auf den Stift alle weiteren Schritte erledigen.

In der Tabelle auf der Startseite sieht man Infos über die Graphen: Index, Größe, ...

Nach klick auf den Graphen wird eine neue Seite geladen. Folgender Ablauf ist sinnvoll:
1. in der queryzeile "all" ohne "" eintragen und "fetch nodes"-Button klicken, läd den gesamten Graphen, daher nur bei kleinen Graphen so vorgehen
2. Query ins query feld schreiben z.B. Color(allsamples, A=1), und add as filter klicken 
3. im Graphen fenster add action und den erstellen filter auswählen, dann kann entsprechend eingefärbt werden
4. um Filter aufzuheben "show action" und remove ggf. mehrfach klicken

! Query nimmt für A= nur integer
! es wird nur nach der km:f: Abundance gefiltert siehe https://gitlab.inria.fr/vizisoft/vizitig/-/blob/main/vizitig/parsing.py

In der Query können logische Ausdrücke verwendet werden, wie im Repo beschrieben. Es können mehrere Actions übereinander liegen, wenn sie dieselben Nodes betreffen, ist nur die zuletzt getätigte sichtbar. Transparency war bei mir oft nicht sichtbar.

Der Metadata-Explorer (rechts) zeigt die Metadata-Typen, die in dem aktuellen Graph enthalten sind: z.B. Color, Transcripts, Gene und Exon. Bei großen Graphen kann das Laden länger dauern. Der Explorer zeigt die unique values der Metadaten. Durch anklicken werden sie in das Query-Feld geschrieben. Wenn eine annot.file eingegeben wird, wird das genes: Feld befüllt, das mit Gene(X) gefiltert werden kann. Wenn Transcript-Files ohne annotations-file verwendet wurden wie bei mir, kann nach der TranscriptID gefiltert werden. 


### Troubles

Bei vizitig run kommt ERROR:    [Errno 98] error while attempting to bind on address ('::1', 4242, 0, 0): address already in use
Lösung: use another port, e.g. 8928 by typing: vizitig run -p 8928


"Query evaluation error: metadata.id is null " im webclient
Das passiert sobald man auf den Graph mit color ohne -m bearbeitet hat. Das lässt sich nicht rückgängig machen.
Lösung: neuen Graph bauen und mit -m colorn, denn nachträglich mit -m colorn geht nicht


unexpected symbols: 
```bash
file my_ex_data/output_ex_sampl_kc_km.fa # überprüfen ob die fasta files Windows-Endung (ACII text, with CRLF line terminators) haben
dos2unix -h # umwandeln oder in VS code unten rechts auf CRLF zu LF wechseln und speichern
```
