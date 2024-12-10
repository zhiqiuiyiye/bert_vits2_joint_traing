import codecs
import random
random.seed(123)

with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/metadata_new_train.list','r','utf-8') as f1:
    with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/metadata_new_test.list','r','utf-8') as f2:
        data = f1.readlines()
        data += f2.readlines()

finetune_data = []
with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/finetune_ajeng_cg_as_ajeng_train.list','w','utf-8') as f:
    with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/finetune_ajeng_cg_as_ajeng_val.list','w','utf-8') as f_cg:
        for line in data:
            speaker = line.strip().split('|')[1]
            if speaker in ['Ajeng_CG']:
                line = line.replace('|Ajeng_CG|','|ajeng|')
                finetune_data.append(line)
        random.shuffle(finetune_data)
        val_data = finetune_data[-10:]
        train_data = finetune_data[:-10]
        f.write(''.join(train_data))
        f_cg.write(''.join(val_data))
    
