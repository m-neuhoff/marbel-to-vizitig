
# Aufbau des Bcalm Formats

## READme von vizitig - Graph Annotations:
"If you want to add abundances to the graph, use the --abundances parameter of the color command. In this case, provide a BCALM file. It needs to have the default parameters with regards to abundance in BCALM (no special formatting and no --all-abundance-counts)."

## das ist ein Beispieldatei von vizitig mini_bcalm.fa:
">165114 genes: SLCO3A1:NM_013272 L:+:376041:+ L:+:552932:- km:f:2.0
CTTTTTTTCTTTTTTTAAGAAAAA
>193397 genes: IL26:NM_018402 L:-:338447:- L:+:477844:+ L:-:626412:- L:+:655635:-
AAAAAAGAAAACAAAAAAGCA
>238173 genes: SVIP:NM_001320340,NM_001320342,NM_148893,NR_135213 metadata: SRR567114 L:-:238180:+ L:-:238181:+ L:-:407716:- L:-:993992:-
ATATATATATATAATTTTTTA
..."

- >165114	Unitig ID, keine feste Stellenzahl
- genes: Optional gene annotations
- L:[sign]:[nodeID]:[sign]	Edges to other unitigs with directionality
- km:f:2.0	Optional metadata tag (k-mer frequency), es taucht nur bei manchen zeilen auf
- ATGC...	Actual unitig DNA sequence
- metadata is free text or ?, can look like metadata: SRR567114,SRR567115,SRR567120 too
- leerzeichen als Trenner

# gfa von Elena:
"H	VN:Z:debruijn-rs
S	0	CTCGTCATATCACCACACCGAATTTATTTTT	"samples: ['C_s3'], counts: [1], sum: 1, p-value: 0.5, log2(fold change): -inf"
L	0	-	918	-	15M
L	0	+	279	+	15M"

- Header
- Link und node in eigenen Zeilen (L/S)
- ID hat keine feste stellenzahl
- sign node sign number of kmears
- sequence
- metainfo like "samples: ['M_s2'], counts: [1], sum: 1, p-value: 0.5, log2(fold change): inf"
- Tabstopp als Trenner

# bcalm Tool
dieses Tool heißt bcalm und wandelt x in ein gfa um, siehe convert2gfa script. vllt kann man es umkehren oder als inspiration verwenden
https://github.com/GATB/bcalm
" In the FASTA output file of BCALM 2, every FASTA entry corresponds to a node. An edge e is represented in the header of node e.from as L:<e.fromSign>:<e.to>:<e.toSign>. Note that BCALM 2 records all edges, even though, in principle, one could record only one edge per mirror type."

# aber es gibt auch eine extra abundance.fa:
">0 LN:i:122 KC:i:92 km:f:1.0   L:+:6:+  L:-:2:- 
ACTTCTTCTCAGGTTCTGTTTTTACAGCCTGTTTTTTGTGTTTTTTCTTGTTAGGAAGATGTGGTCCTTCCATCTGTTGGCTGACTGGAATGGCCTTGGTTTCTGTGGGATTCATACTGGAA
>1 LN:i:151 KC:i:242 km:f:2.0   L:+:6:-  
ACTCTCCGCGGCGCATTCCGGGAGGCAGCGGCCGCAGCGGCCTCGCCATGTCCCAGCCCGGCCAGAAGCCCGCCGCCTCCCCGCGGCCCCGGCGAGCAGCCGCCGCCCGCCGCACCCATGAGCATGTCAGTGAAAAAACCAGTGAATCGCC
>2 LN:i:45 KC:i:45 km:f:3.0   L:-:3:+ L:-:9:+  L:+:0:+ L:+:8:+ 
GCTTGGTTGACTGTGACTTCTTCTCAGGTTCTGTTTTTACAGCCT
>3 LN:i:57 KC:i:54 km:f:2.0   L:+:5:-  L:-:2:+ 
..."

Erklärung von chatgpt:
">0	Unitig ID (node 0)
LN:i:122	Length of the unitig = 122 bp
KC:i:92	K-mer count (number of k-mers in this unitig) = 92
km:f:1.0	K-mer abundance (average or normalized frequency) = 1.0
L:+:6:+	Edge from this unitig (strand +) to unitig 6 (strand +)
L:-:2:-	Edge from this unitig (strand -) to unitig 2 (strand -)"

# was wollen wir von vizitig nutzen?
es gibt color was mit abundaces und metadata arbeiten kann, wobei metadata in deren beispielen nur S-kennungen sind 

vizitig color -k my/awesome/file.fa -d "This contains some cure against the cancer somehow" -m "sample1" my_graph_name
After this, you will be able to fetch all the nodes of the graph that correspond to this sample by using the following query 

More complex options exist to add metadata to a graph. One is suited for transcriptomic references, the other for genomic references

### https://gitlab.inria.fr/vizisoft/vizitig/-/blob/main/vizitig/types/__init__.py?ref_type=heads
```
@dataclass
class Color:
    id: str
    description: str
    type: str = "Color"
    offset: int | None = None

    def set_offset(self, offset: int):
        self.offset = offset

    def __hash__(self):
        return hash((self.id, self.type, self.offset))

    def short_repr(self):
        return f"Color({self.id})"

    def as_dict(self):
        return dataclass.as_dict(self)
```
```
@dataclass
class Abundance:
    id: str
    value: float
    type: str = "Abundance"
    encoded_color_value: int | None = None
    offset: int | None = None

    def set_offset(self, offset: int):
        self.offset = offset

    def __hash__(self):
        return hash((self.id, self.value, self.offset))

    def short_repr(self):
        return f"Abundance({self.id}, {self.value})"
```
### Readme vizitig
positional arguments:
  {info,rename,add,rm,index,color,annotate,build,run}
    ...
    color               Color an existing graph. There are several ways to use this feature : -vizitig color -f file_name -m color_name ->                  Will color the graph with whatever is in the
                        provided file -vizitig color --folder folder_name -> Will color the graph with every file in the provided folder. The name of the color will be the name of the file
                        for each file -vizitig color --folder folder_name -m color_name -> Same, but the name of the color will be color_name for all files -vizitig color --csv file.csv ->
                        Will use a csv file to color the graph. Csv must respect the following format (tabèseparated): /path/to/file1 red "Sample 1 - control group" /path/to/file2 green
                        "Sample 2 - condition 1" /path/to/file3 blue "Sample 3 - condition 2"


vizitig color -h
usage: vizitig  [-h] -m name [-d description] [-k file [file ...]] [-b buffer] [-u url [url ...]] [-c color] graph

positional arguments:
  graph                 A graph name. List possible graph with python3 -m vizitig info

options:
  -h, --help            show this help message and exit
  -m name, --metadata-name name
                        A key to identify the metadata to add to the graph
  -d description, --metadata-description description
                        A description of the metadata
  -k file [file ...], --kmer-files file [file ...]
                        Path toward files containing kmers (fasta format)
  -b buffer, --buffer-size buffer
                        Maximum size of a buffer
  -u url [url ...], --kmer-urls url [url ...]
                        URLs toward files containing kmers (fasta format)
  -c color, --color color
                        Default color to use in the vizualisation. Default is None


# Vorhaben um webclient auf bcf zu sehen
1) commit git check out, danach freeze kontrollieren aber vermutlich altes paket entfernen erst
-e git+https://gitlab.inria.fr/pydisk/examples/vizitig@b9a7c9df5095c230a0867e2c2f8a3908d331ef24#egg=vizitig ist der richtige
2) dateien austauschen und nur den einen graph bauen
3) port forwarding x11. server muss auf maschine laufen und ich muss mich auf die maschine verbinden wo der server läuft.


# Meine Graphen
my_graph_ex2_swl: war test wegen kaputter gfa, mit vielen S ohne L, alt
graph_bcalm_web: im webclient erstellter graph mit vizitig dateien
ex_30_graph: mit ok kmeranzahl, aber -m vergessen
ex_30_newgraph: -m ohne abundance
ex_30_abdu: mit abundance aber -m vllt nicht ?
ex_30_abdu2: -m allsamples
ex_30_abdu3: -m sample1

# todo 
0. test mit graphaligner um gaf anzuschauen 
1. mit marbel reads und transcript generieren auf bcf
2. mit dbg aus reads graph bauen auf bcf
3. mit graphaligner transcripte an graph alignen -> in gaf steht für jede sequence ein pfad durch den graph (Pfad besteht aus NodeIDs) auf bcf
4. anhand eines pfades ein transcript zusammensetzen aus Nodesequences aus Datei der graphdatei gfa oder fasta. Muss mir dann nochmal jemand erklären

erst mit kleinem datensatz kennenlernen und verstehen 
dann mit größerem datensatz testen, ob mein converter und vizitig das schaffen

# Projektziele
timo baut an marbel, also simulierung von datensätzen. Zur Prüfung werden hier transcripte mitgeliefert.

elena macht de novo, d.h. es gibt keine transcripte (die sind wie refgenom bei RNA-Sequenzierung)

# marbel 
marbel --n-species 10 --n-orthogroups 2000 --library-size 100000 --n-samples 3 3 --seed 23

(marbel) mneuhoff@cli:~/git_projekte/marbel$ /vol/slurm/bin/seff 26342829
Job ID: 26342829
Cluster: bcf
User/Group: mneuhoff/bcf_users
State: COMPLETED (exit code 0)
Nodes: 1
Cores per node: 128
CPU Utilized: 00:18:52
CPU Efficiency: 2.75% of 11:26:56 core-walltime
Job Wall-clock time: 00:05:22
Memory Utilized: 9.38 GB
Memory Efficiency: 2.35% of 400.00 GB

# Rückmeldung für marbel
geht auch einfach mit conda
wie wird output aussehen, welche dateien werden generiert und wie kann ich den order dafür selbst wählen

# error bei dbg
(marbel) mneuhoff@cli:~/git_projekte$ cargo install --git git@github.com:jlab/dbg.git
error: invalid url `git@github.com:jlab/dbg.git`: relative URL without a base; try using `ssh://git@github.com/jlab/dbg.git` instead
(marbel) mneuhoff@cli:~/git_projekte$ cargo install --git ssh://git@github.com:jlab/dbg.git
error: invalid url `ssh://git@github.com:jlab/dbg.git`: invalid port number
(marbel) mneuhoff@cli:~/git_projekte$ cargo install --git https://github.com/jlab/dbg.git
    Updating git repository `https://github.com/jlab/dbg.git`
warning: spurious network error (3 tries remaining): failed to connect to github.com: Connection timed out; class=Os (2)
warning: spurious network error (2 tries remaining): failed to connect to github.com: Connection timed out; class=Os (2)
warning: spurious network error (1 tries remaining): failed to connect to github.com: Connection timed out; class=Os (2)
error: failed to clone into: /homes/mneuhoff/.cargo/git/db/dbg-2e1d9179a5be67f1

Caused by:
  failed to connect to github.com: Connection timed out; class=Os (2)
(marbel) mneuhoff@cli:~/git_projekte$ ssh-keygen -t rsa -b 4096
...
(base) mneuhoff@cli:~/git_projekte$ addkey() { eval "$(ssh-agent -s)"; ssh-add ~/.ssh/id_rsa; }
(base) mneuhoff@cli:~/git_projekte$ cargo install --git https://github.com/jlab/dbg.git
    Updating git repository `https://github.com/jlab/dbg.git`
client_loop: send disconnect: Connection reset by peer
client_loop: send disconnect: Broken pipe

(base) mneuhoff@sr3-r2-a2k-1-2:~/git_projekte$ /vol/slurm/bin/seff 26358585
Job ID: 26358585
Cluster: bcf
User/Group: mneuhoff/bcf_users
State: COMPLETED (exit code 0)
Nodes: 1
Cores per node: 4
CPU Utilized: 00:00:26
CPU Efficiency: 43.33% of 00:01:00 core-walltime
Job Wall-clock time: 00:00:15
Memory Utilized: 2.19 GB
Memory Efficiency: 54.84% of 4.00 GB

# Rückmeldung dbg
tippfehler csv für unpaired reads 2x
tippfehler csv "inpue files"
muss im folder der input data ausgeführt werden

# für dbg
arbeitsspeich häfte wie von job

# converter
(base) mneuhoff@sr3-r2-a2k-1-2:~/git_projekte$ /vol/slurm/bin/seff 26358600
Job ID: 26358600
Cluster: bcf
User/Group: mneuhoff/bcf_users
State: COMPLETED (exit code 0)
Nodes: 1
Cores per node: 2
CPU Utilized: 00:00:15
CPU Efficiency: 46.88% of 00:00:32 core-walltime
Job Wall-clock time: 00:00:16
Memory Utilized: 602.91 MB
Memory Efficiency: 14.72% of 4.00 GB