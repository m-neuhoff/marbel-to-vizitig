# gfa-to-bcalm

Die erzeugte fasta-Datei enthält ID, die Namen der Samples als metadata, die Links, Abundance und die Sequence;
in der Art wie bcalm es erzeugen würde.

Das script lässt sich so aus dem Terminal verwenden:

`python gfa2bcalm.py input.gfa output.fa num_of_samples`

num_of_samples ist dabei die Anzahl aller untersuchter samples. Aber die Rechnung stimmt noch nicht und daher auch die mean abundance noch nicht
