proc cas; 
loadactionset "sequence";
sequence.cspade / table="sequence", 
casout="seqout",  
itemID="basen", 
eventID="position", 
sequenceID="genotype", 
support = 0.4; 
run;
quit;
