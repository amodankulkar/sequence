import pandas as pd
import ntpath
import csv

########################################
#This function converts any java input to SAS input
#########################################
def java_to_sas(path=''):
    fr = open(path,'r')
    head, tail = ntpath.split(path)
    head1 = 'java_to_sas_' + tail
    fw = open(head1,'w')
    sid = 0
    tme = 1
    for line in fr:
        sid += 1
        for elem in line.split(' '):
            if int(elem) == -2:
                tme = 1
            else:
                if int(elem) == -1:
                    tme += 1
                else:
                    lne = str(sid) + ' ' + str(tme) + ' ' + str(elem) + '\n'
                    fw.write(lne) 

    fr.close()
    fw.close()
    print('i am done!')
                    

########################################
#This function converts any SAS input to R input
#########################################
def sas_to_r(path='', sep=','):
    df = pd.read_csv(path,names=['transaction','time','item'])
    head, tail = ntpath.split(path)
    head1 = 'to_r_' + tail
    

    lst1 = list(df.item.unique())

    dkt = dict(zip(lst1, range(len(lst1))))

    df2 = df.applymap(lambda s: dkt.get(s) if s in dkt else s)

    df1 = df.groupby(['transaction', 'time'])['item'].apply(' '.join).reset_index()

    ls2 = [len(items.split(' ')) for items in list(df1['item'])]

    df1['count'] = ls2

    lis1 = list(df1['item'])
    lis2 = ''
    lis3 = list()
    lisp = ' '

    for qty in lis1:
        for i in qty.split(' '):
            lis2 = lis2 + lisp + str(dkt.get(i))
        lis3.append(lis2)
        lis2 = ''

    df1['numbers'] = lis3

    df5 = df1[['transaction','time','count','numbers']]

    listime = list(df5['time'])
    listimem = list()
    for ite in listime:
        ite = ite + 1
        listimem.append(ite)


    df5['time'] = listimem


    df5.to_csv(head1,sep=' ',index=False, header=False)
    fr = open(head1, 'r')
    head2 = 'sas_' + head1
    fw =open(head2,'w')
    for line in fr:
        ln = line.replace('" ','')
        fw.write(ln.replace('"',''))
    
    fw.close()
    print('i m done!')

########################################
#This function converts any R input to Java input
#########################################
def r_to_java(path, sep=';'): 
    head, tail = ntpath.split(path)
    
    fr = open(path,'r')
    cust = list()
    size = list()
    time = list()
    itms = list()
    for line in fr:
        ln = line.rstrip()
        lst1 = ln.split(sep)
        cust.append(lst1[0])
        time.append(lst1[1])
        size.append(lst1[2])
        itms.append(lst1[3:])

    df2 = pd.DataFrame({'cust': cust,'time':time,'size':size,'itms':itms})

    df2.loc[ df2.groupby('cust',as_index=False).nth(0).index, 'flag' ] = 1
    df2.loc[ df2.groupby('cust',as_index=False).nth(-1).index, 'flag1' ] = 2
    df2.flag = df2.flag.fillna(0).astype(int)
    df2.flag1 = df2.flag1.fillna(0).astype(int)

    lng = len(set(cust))
    print(lng)

    listOfLists = [[] for i in range(lng)]

    c = -1
    for index, row in df2.iterrows():
        if row['flag'] == 1 and row['flag1'] == 2:
            c += 1
            listOfLists[c].append(row['itms'])
            listOfLists[c].append('-1')
            listOfLists[c].append('-2')
        else:
            if row['flag'] == 1:
                c += 1
                listOfLists[c].append(row['itms'])
                listOfLists[c].append('-1')    
            else:
                if row['flag1'] == 2:
                    listOfLists[c].append(row['itms'])
                    listOfLists[c].append('-1')
                    listOfLists[c].append('-2')
                else:
                    listOfLists[c].append(row['itms'])
                    listOfLists[c].append('-1')

    for i in range(lng): 
        listOfLists[i] = [j for k in listOfLists[i] for j in k]

    oname = 'r_to_java_' + tail
    fw = open('{0}.txt'.format(oname),'w')
    for line in listOfLists:
        listToStr = ' '.join([str(elem) for elem in line])
        nStr = listToStr + '\n'
        fw.write(nStr.replace('- ','-'))
    fw.close()


########################################
#This another efficient function that converts any java input to R input
#########################################
def java_to_r(path="", sep=" "):
    head, tail = ntpath.split(path)
    head1 = 'java_to_r_' + tail
    itms = []
    index = 0
    fw = open(head1, 'w')
    fr = open(path,'r')
    reader = csv.reader(fr)
    
    for row in reader:
        time = 1
        index = index + 1
        for item in row[0].split(' '):
            if int(item) == -2.0:
                pass
            elif int(item) == -1.0:
                lnes = str(index) + ' ' + str(time) + ' ' + str(len(itms)) + ' ' + ' '.join(itms) + '\n'
                fw.write(lnes)
                time += 1
                itms = []
            else:
                itms.append(item)

    fr.close()
    fw.close()
    print('i m pretty much done!')

########################################
#This is a function that converts R input to the input required by our cas Action
#########################################
def r_to_action(path=''):
    fr = open(path,'r')
    head, tail = ntpath.split(path)
    head1 = 'r_to_action_' + tail
    fw = open(head1,'w')
    for line in fr:
        x = line.split(' ')
        #print(x)
        y = x[3:]
        #print(y)
        for ele in y:
            elem = ele.replace('\n','')
            lne = str(x[0]) + ' ' + str(x[1]) + ' ' + str(elem) + '\n'
            fw.write(lne)
    fr.close()
    fw.close

#Specimen to show how to use the functions
"""
java_to_sas(path=r'C:\myWork\CM_Spade\contextPrefixSpan.txt')
sas_to_r(path=r'C:\mywork\r_Project\seq_j.csv', sep=',')
r_to_java('fptree_cspade.txt')
java_to_r(path=r'C:\myWork\CM_Spade\data\contextPrefixSpan.txt')
"""







