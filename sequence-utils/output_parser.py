import pandas as pd
import ntpath
import csv
import re

########################################################################
# This function parses the cspade-full output
########################################################################
def parse_cspadefull(path=''):
    fr = open(path,'r')
    fw = open(r'p_parse.txt','w')
    #ln = fr.readlines()[3:-2]
    for line in fr:
    #lne = re.sub('#SUPP: [a-zA-Z_0-9]*','',line)
        lnes = ' '.join(line.split('--')[:-1]) + '-1' + '\n'
        lne =lnes.replace('->','-1')
    #lnes = ' '.join(lnes.split(',')) + '\n'
    #lnej = re.sub('}',' -1',lnes).replace('{','')
        fw.write(lne)
    fw.close()
    fr.close()
    
########################################################################
# This function parses the java output
########################################################################    
def parse_java(path=''):
    fr = open(path,'r')
    fw = open(r'j_parse.txt','w')
    for line in fr:
    #lne = re.sub('#SUPP: [a-zA-Z_0-9]*','',line)
        lnes = ' '.join(line.split('#')[:-1]) + '\n'
    #lnes = ' '.join(lnes.split(',')) + '\n'
    #lnej = re.sub('}',' -1',lnes).replace('{','')
        fw.write(lnes)
    fw.close()
    fr.close()
    

########################################################################
# This function parses the R output
########################################################################    
def parse_r(path=''):
    fr = open(path,'r')
    fw = open(r'r_parse.txt','w')
    lines = fr. readlines()[1:]
    for line in lines:
        lne = re.sub('[><]','',line)
        lnes = ' '.join(lne.split(';')[:-1])
        lnes = ' '.join(lnes.split(',')) + '\n'
        lnej = re.sub('}',' -1',lnes).replace('{','')
    
        fw.write(lnej)
    fw.close()
    fr.close()


########################################################################
# This function parses the r output in modified way
########################################################################    
def parse_r2(path=''):
    fr = open(path,'r')
    fw = open(r'r_parse2.txt','w')
    lines = fr.readlines()[1:]
    for line in lines:
        lne = re.sub('[{<]','',line)    
        lne1 = re.sub('[,]',' ',lne)    
        lne2 = ' '.join(lne1.split('}>;')[:-1])    
        if '}' not in lne2:
            if ' ' not in lne2:
                lne3 = lne2
            else:
                lne3 = ' '.join(sorted(lne2.split(' '),key=int))            
        else:
            lnei = lne2.split('} ')
            lneie = []        
            for itm in lnei:
                if " " in itm:
                    itme = ' '.join(sorted(itm.split(' '),key=int))
                    lneie.append(itme)
                else:
                    lneie.append(itm)        
            lne3 = ' -1 '.join(lneie)
        lne4 = lne3 + ' -1\n'
        fw.write(lne4)
    fw.close()
    fr.close()
    
    
########################################################################
# This function compares the 2 outputs
########################################################################    
def compare(path1, path2):
    d1 = pd.read_csv(path1, sep=' ', names=[s for s in range(30)], header=None, engine="python")
    d2 = pd.read_csv(path2, sep=' ', names=[s for s in range(30)], header=None, engine="python")
    d1 = d1.fillna(-5)
    d2 = d2.fillna(-5)
    d1 = d1.astype(int)
    d2 = d2.astype(int)
    diff = pd.merge(d1, d2, how='outer', suffixes = ('','_y') ,indicator=True)
    dif = diff.loc[diff['_merge'] != 'both']
    dif.to_csv('comparison.csv', index=None)
    count = 0
    for i in diff['_merge']:
        if i == 'both':
            pass
        else:
            count += 1 
    print(count, ' diffs found!')
   
