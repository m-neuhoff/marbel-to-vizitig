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

# Nutzung von vizitig

installiere vizitig 1.0.5 nur so (pip hat nicht das aktuelle):
```bash
git clone https://gitlab.inria.fr/pydisk/examples/vizitig
cd vizitig
make install
```
Es wird ein vizitig-Ordner kopiert. Gehe in den Order und 
```...vizitig$ source venv/bin/activate```

(vizitig info und vizitig run geben Errors bzw. funktionieren scheinbar nicht)

1) Baue Graph mit: ```vizitg build mini_bcalm.fa -n minibcalm_graph #wichtig weil vizitig info nicht funktioniert```
2) Indexe den Graph mit: ```vizitig index build minibcalm_graph -t RustIndex```
3) Colorn nach Samples mit: ```vizitig color -f ./path/to/fastas/mini_bcalm.fa minibcalm_graph```
