import codecs

with codecs.open('test_en.txt','r','utf-8') as f1:
    with codecs.open('en.all.txt.cleaned','r','utf-8') as f2:
        with codecs.open('test_en_text_ph.txt','w','utf-8') as f3: 
            data1 = f1.readlines()
            data2 = f2.readlines()
            for i in range(len(data1)):
                id1,text = data1[i].strip().split('|')
                id2,phoneme = data2[i].strip().split('|')
                if id1 == id2:
                    new_line = id1 + '|' + text + '|' + phoneme + '\r\n'
                    f3.write(new_line)
                    #print(new_line)

with codecs.open('test_my.txt','r','utf-8') as f1:
    with codecs.open('my.all.txt.cleaned','r','utf-8') as f2:
        with codecs.open('test_my_text_ph.txt','w','utf-8') as f3: 
            data1 = f1.readlines()
            data2 = f2.readlines()
            for i in range(len(data1)):
                id1,text = data1[i].strip().split('|')
                id2,phoneme = data2[i].strip().split('|')
                if id1 == id2:
                    new_line = id1 + '|' + text + '|' + phoneme + '\r\n'
                    f3.write(new_line)
                    #print(new_line)                   
                 
