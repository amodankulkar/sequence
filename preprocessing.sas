
options validvarname=any;


caslib mylib task=add type=path path="/tstgen/wky/tst/largeio/testwsio/dnt/deepforest" subdirs desc="My library" ;
caslib _all_ assign;


PROC CASUTIL  ;
  LOAD CASDATA="journal.pone.0243185.s005.csv" INCASLIB="Mylib"  CASOUT="genes";

RUN;
quit;

data geneseq;
set mylib.genes;
genotype = _N_;
len = length(sequence);
seq1=find(sequence,"[");
seq2=find(sequence,"]");
len2 = len - seq2;
len3 = seq2 - seq1;
sub1 = substr(sequence,1,(seq1 - 1));
sub3 = compress(substr(sequence,(seq1 + 1), (seq2 - seq1 - 1)),"/");
sub2 = substr(sequence, (seq2 + 1), len2);
run;



data mylib.seqgene (keep= genotype position base sequence);
set geneseq;
n1= length(sub1);
n2= length(sub2);
n3= length(sub3);
n0 = 1;
do until(n0 > n1);
   put n0=;
   base=substr(sub1,n0,1);
   position = n0;
   output;
   n0 +1;
end;
n000 = 1;
do until(n000 > n3);
   put n000=;
   base=substr(sub3,n000,1);
   position = n0;
   output;
   n000 +1;
end;
n00 = 1;
do until(n00 > n2);
   put n00=;
   base=substr(sub2,n00,1);
   position = n0 + n00;
   output;
   n00 +1;
end;
run;

proc sql;
create table sequence as 
SELECT genotype, CASE
    WHEN base eq 'A' THEN 1
    WHEN base eq 'C' THEN 2
WHEN base eq 'G' THEN 3
WHEN base eq 'K' THEN 4
WHEN base eq 'N' THEN 5
WHEN base eq 'R' THEN 6
WHEN base eq 'S' THEN 7
WHEN base eq 'T' THEN 8
WHEN base eq 'W' THEN 9
WHEN base eq 'Y' THEN 10
    ELSE 0
END AS basen, position 
FROM mylib.seqgene;
run;
quit;

data mylib.sequence;
set sequence;
run;
