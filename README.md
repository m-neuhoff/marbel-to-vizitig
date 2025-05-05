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
dos2unix -h # umwandeln
```

# Nutzung von vizitig

installiere vizitig 1.0.5 nur so (pip hat nicht das aktuelle):
```bash
git clone https://gitlab.inria.fr/pydisk/examples/vizitig
cd vizitig
make install
```
Es wird ein vizitig-Ordner kopiert. Gehe in den Order und 
```...vizitig$ source venv/bin/activate```

(vizitig info gibt Errors)

1) Baue Graph mit: ```vizitig build mini_bcalm.fa -n minibcalm_graph # -n ist wichtig weil vizitig info nicht funktioniert```
2) Indexe den Graph mit: ```vizitig index build minibcalm_graph -t RustIndex```
3a) Colorn nach Samples mit: ```vizitig color -f ./path/to/fastas/mini_sample1.fa -m sample1 minibcalm_graph```
3b) Colorn nach sample und abundance mit: ```vizitig color -f ./path/to/fastas/mini_sample1.fa -m sample1 -abundances minibcalm_graph```
3c) Colorn nach abundance mit: ```vizitig color -f ./path/to/fastas/mini_bcalm.fa -m allsamples -abundances minibcalm_graph```

Im webclient kann man das auch alles per Mouseklick machen außer -abundances
...genaue Anleitung
Nach klick auf den Graphen wird eine neue Seite geladen: in der queryzeile "all" ohne "" eintragen und "fetch nodes"-Button klicken
Query ins query feld schreiben z.B. Color(allsamples, A=1), und add as filter klicken
im Graphen fenster add action und den erstellen filter auswählen, dann kann entsprechend eingefärbt werden

um Filter aufzuheben "show action" und remove ggf. mehrfach klicken

bei 3c bin ich mir nicht sicher, es macht keine fehlermeldung, aber ich sehe die färbung nicht, was aber an der geringen größe des samples liegen könnte

! Query nimmt für A= nur integer
! es wird nur nach der km:f: Abundance gefiltert siehe https://gitlab.inria.fr/vizisoft/vizitig/-/blob/main/vizitig/parsing.py

# Troubles

Bei vizitig run kommt ERROR:    [Errno 98] error while attempting to bind on address ('::1', 4242, 0, 0): address already in use
Lösung: use another port, e.g. 8928 by typing: vizitig run -p 8928


"Query evaluation error: metadata.id is null " im webclient
weil color ohne -m genutzt wurde 
Lösung: neuen Graph bauen und mit -m colorn, nachträglich mit -m colorn geht nicht