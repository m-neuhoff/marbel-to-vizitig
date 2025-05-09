# gfa-to-bcalm

Die erzeugte fasta-Datei enthält ID, die Namen der Samples als metadata, die Links, Abundance und die Sequence;
in der Art wie bcalm es erzeugen würde: 
```
><id> metadata: <sample1, sample2, ...> KC:i:<abundance> km:f:<abundance> L:<+/->:<other id>:<+/->/n
<sequence>
```

Das script lässt sich so aus dem Terminal verwenden:

`python gfa2bcalm.py input.gfa output.fa num_of_samples`

num_of_samples ist dabei die Anzahl aller untersuchter samples. Aber die Rechnung stimmt noch nicht und daher auch die mean abundance noch nicht

# Hinweis bei Windows->Linux 

```bash
file my_ex_data/output_ex_sampl_kc_km.fa # überprüfen ob die fasta files Windows-Endung (ACII text, with CRLF line terminators) haben
dos2unix -h # umwandeln oder in VS code unten rechts auf CRLF zu LF wechseln und speichern
```

# Nutzung von vizitig CLI

installiere vizitig 1.0.5 nur so (pip hat nicht das aktuelle):
```bash
git clone https://gitlab.inria.fr/pydisk/examples/vizitig
cd vizitig
make install
```
Es wird ein vizitig-Ordner kopiert. Gehe in den Order und 
```...vizitig$ source venv/bin/activate```

(vizitig info gibt Errors)

0) Prüfe, ob die gfa eine AvailableKmerSize verwendet
1) Baue Graph mit: ```vizitig build mini_bcalm.fa -n minibcalm_graph # -n ist wichtig```
2) Indexe den Graph mit: ```vizitig index build minibcalm_graph -t RustIndex```
3) Colorn
    * Colorn nach Samples mit: ```vizitig color -f ./path/to/fastas/mini_sample1.fa -m sample1 minibcalm_graph```
    * Colorn nach sample und abundance mit: ```vizitig color -f ./path/to/fastas/mini_sample1.fa -m sample1 -abundances minibcalm_graph```
    * Colorn nach abundance mit: ```vizitig color -f ./path/to/fastas/mini_bcalm.fa -m allsamples -abundances minibcalm_graph```

(bei 3c bin ich mir nicht sicher, es macht keine fehlermeldung, aber ich sehe die färbung nicht, was aber an der geringen größe des samples liegen könnte)

vgl. vizitig example:
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

# Nutzung des webclients

Im webclient kann man das auch alles per Mouseklick machen außer -abundances
...genaue Anleitung
In der Tabelle sieht man Infos über die Graphen, Index, Größe, ...
Nach klick auf den Graphen wird eine neue Seite geladen: in der queryzeile "all" ohne "" eintragen und "fetch nodes"-Button klicken
Query ins query feld schreiben z.B. Color(allsamples, A=1), und add as filter klicken 
im Graphen fenster add action und den erstellen filter auswählen, dann kann entsprechend eingefärbt werden
um Filter aufzuheben "show action" und remove ggf. mehrfach klicken

! Query nimmt für A= nur integer
! es wird nur nach der km:f: Abundance gefiltert siehe https://gitlab.inria.fr/vizisoft/vizitig/-/blob/main/vizitig/parsing.py
! Query nimmt auch Color(A=1) ?

# vizitig annotate erkunden als Schritt 4)

For the transcripts reference sequence, it will tag the graph with the a generic metadata that has the header of the reference sequence and later add the additional data of the annotation file. The later is therefore optional

Wenn eine annot.file eingegeben wird, wird das genes: Feld befüllt, das mit Gene(X) gefiltert werden kann

If transcript references are provided alone, every sequence will be added. Transcripts will be named after their name in the reference sequence. Possible Query: Transcript(NM_010111)

look at metadata explorer enthält als Metadata types: Exons, Color, Transcripts, Gene

# Export

When using classic selection, you can type "Selection" in the query field to export the current selection as a list of nodes. Users can then create a filter that saves this list of nodes. ? überprüfen

# Troubles

Bei vizitig run kommt ERROR:    [Errno 98] error while attempting to bind on address ('::1', 4242, 0, 0): address already in use
Lösung: use another port, e.g. 8928 by typing: vizitig run -p 8928


"Query evaluation error: metadata.id is null " im webclient
weil color ohne -m genutzt wurde 
Lösung: neuen Graph bauen und mit -m colorn, nachträglich mit -m colorn geht nicht