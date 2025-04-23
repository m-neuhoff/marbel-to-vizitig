
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
