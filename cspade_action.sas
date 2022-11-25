proc cas; 
loadactionset "sequence";
sequence.cspade / table="sequence", 
casout="seqout",  
itemID="basen", 
eventID="position", 
sequenceID="marker", 
support = 0.4; 
run;
quit;
