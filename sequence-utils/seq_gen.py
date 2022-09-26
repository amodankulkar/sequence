from random import seed
from random import randint
import pandas as pd

def sequence_generator(transactions=10, name = 'seq_generator.txt', customers=10, totalItems=20, events_per_customer = 5, items_per_event = 5, classID=0, classes = 2):
    fw = open(name, 'w')
    count = 0
    itemlist = []

    for i in range(1, customers):
        mod = randint(1,(classes))	
        for j in range(1, randint(2, events_per_customer)):            
            if count > transactions:
                break
            else:
                count += 1
                itemlist = []                
                itm = randint(1, items_per_event)
                for k in range(itm):
                    itemlist.append(str(randint(1,totalItems)))
                res = sorted(itemlist, key = int) 
                if classID == 0:
                    lne = str(i) + ' ' + str(j) + ' ' + str(itm) + ' ' + ' ' .join(res)  + '\n'
                else:
                    
                    lne = str(mod) + ' ' + str(i) + ' ' + str(j) + ' ' + str(itm) + ' ' + ' ' .join(res)  + '\n'
                fw.write(lne)

    fw.close()
    
def get_classfile(path_to_r, path_classfile,path_input):
    fw = open(path_classfile,'w')
    fw1 = open(path_input,'w')
    fr = open(path_to_r,'r')
    df = pd.read_csv(path_to_r, sep=' ',  usecols =[0,1], header = None)
    cardinality = len(pd.Index(df[0]).value_counts())
    dfu = df.drop_duplicates()
    lne =''
    for index, row in dfu.iterrows():
        lne = lne + ' ' + str(row[1]) + ' ' + str(row[0])
    lne = str(cardinality) + lne
    fw.write(lne.strip())
    fw.close()
    for line in fr:
        lne = line.split()
        lne1 = lne[1:]
        lne2 = ' '.join(lne1)
        lne3 = lne2 + '\n'
        fw1.write(lne3)
    fr.close()
    fw1.close()
    
'''
from converter import seq_gen as sg
sg.sequence_generator(transactions=50, name='meseq.txt',customers=5,
                      events_per_customer=6, items_per_event=10)
'''


