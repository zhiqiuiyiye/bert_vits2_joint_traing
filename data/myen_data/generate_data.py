import codecs

from transformers import BertTokenizer, BertModel
import torch
punctuation = ["!", "?", "…", ",", ".", "-",";",":"]
import random
upper_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
random.seed(123)

tokenizer = BertTokenizer.from_pretrained('/data_02/chuyinxue/research/Bert-VITS2/data/bert-base-multilingual-cased')
model = BertModel.from_pretrained("/data_02/chuyinxue/research/Bert-VITS2/data/bert-base-multilingual-cased")
# tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
# model = BertModel.from_pretrained("bert-base-multilingual-cased")
def norm_text(data):
    data = data.strip().replace('/',' ').replace('%',' ').replace('&','').replace('#','').replace('@','').replace('"',' " ')
    data = data.strip().replace('(',' ( ').replace(')',' ) ').replace(" '"," ").replace("' "," ")
    data = (data+'\t').replace("'\t","").replace('\t','')
    for punc in punctuation:
        data = data.replace('  '+punc,punc).replace(' '+punc,punc)
        data = data.replace(punc,punc+' ').replace('  ',' ').strip()
    return data

def is_upper(token):
    if len(token) > 1 and token[0] in upper_letter and token[1] in upper_letter:
        return True
    return False
def process_data(line):
    subword_lengths =[]
    # import pdb;pdb.set_trace()
    id,text,ph,wav,spk = line.strip().split('|')
    wav = wav.strip().split('=')[1].replace('24k','16k').replace('24K','16K')
    spk = spk
    lang = 'MyEn'
    text = text.strip().split('=')[1]
    phoneme = ph.strip().split('=')[1]
    new_line = wav +'|'+spk+'|'+lang+'|'+text+'|'+phoneme
    # wav,spk,lang,text,phoneme = line.strip().split('|')
    # text = text.replace('"','')
    # phoneme = phoneme.replace('/ " /','/')
    # if spk not in ['haitian']:
    text = text.strip().replace('-','- ')
    text = norm_text(text)
    tokens = text.strip().split()
    token_list = []
    for token in tokens:
        if is_upper(token):
            new_token = ' '.join([i for i in token])
            token_list += new_token.split()
        else:
            token_list.append(token)
    text = ' '.join(token_list)
    text = norm_text(text)
    tokens = text.strip().split()
     
    # import pdb;pdb.set_trace()
    subwords = list(map(tokenizer.tokenize,tokens))
    subword_lengths = [1]+list(map(len, subwords))+[1]
    subwords = ['[CLS]'] + [i for indices in subwords for i in indices] + ['[SEP]']
    tokenize_res = tokenizer.convert_tokens_to_ids(subwords)
    if len(tokens)+2 != len(subword_lengths):
        print(line)
    ph_list = phoneme.strip().replace('* /','').replace('/ &','').split('/')
    ph_len = []
    flag_list = []
    # if line.startswith('MY-F100174.wav'):
    #     import pdb;pdb.set_trace()
    for ph in ph_list:
        flag = 0
        for punc in punctuation:
            if punc in ph.strip()[-1]:
                flag = 1
                break
        flag_list.append(flag)
        if flag==0:
            ph_len.append(len(ph.strip().split())+1)
            if len(flag_list) > 1 and flag_list[-2] ==1:
                ph_len[-1] += 1
        else:
            ph_len[-1] += 1
    ph_len = [2] + ph_len + [2]
    if text[-1] not in punctuation:
        ph_len[-2] -= 1
    # if text[-1] in punctuation:
    #     ph_len[-2] += 1
     # import pdb;pdb.set_trace()
    # assert len(ph_len) == len(subword_lengths)
    if len(ph_len) != len(subword_lengths):
        import pdb;pdb.set_trace()
    if sum(ph_len) != len(phoneme.strip().split()):
        import pdb;pdb.set_trace()
    # assert sum(ph_len) == len(phoneme.strip().split())

    # sentences.append(tokenizer.convert_tokens_to_ids(subwords))

    # import pdb;pdb.set_trace()
    return new_line,tokenizer.convert_tokens_to_ids(subwords),subword_lengths,ph_len


# with codecs.open('/data_02/chuyinxue/research/Bert-VITS2/data/metadata.list','r','utf-8') as f:
#     with codecs.open('/data_02/chuyinxue/research/Bert-VITS2/data/metadata_new.list','w','utf-8') as f1:
#         for line in f:
#             sentences,subword_lengths,ph_len = process_data(line)
#             new_line = line.strip() + '|' + ' '.join(map(str,sentences)) + '|' + ' '.join(map(str,subword_lengths)) + '|' + ' '.join(map(str,ph_len)) + '\n'
#             f1.write(new_line)

with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/myen_data/train_data_my_mg_add_luna_text.txt','r','utf-8') as f1:
    train_data = f1.readlines()
with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/myen_data/val_data_my_mg_add_luna_text.txt','r','utf-8') as f1:
    test_data = f1.readlines()

# test_data = random.sample(data,100)
# train_data = list(set(data) - set(test_data))

with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/myen_data/metadata_new_train.list','w','utf-8') as f1:
    for line in train_data:
        new_line,sentences,subword_lengths,ph_len = process_data(line)
        new_line1 = new_line.strip() + '|' + ' '.join(map(str,sentences)) + '|' + ' '.join(map(str,subword_lengths)) + '|' + ' '.join(map(str,ph_len)) + '\n'
        f1.write(new_line1)

        
with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/myen_data/metadata_new_test.list','w','utf-8') as f1:
    for line in test_data:
        new_line,sentences,subword_lengths,ph_len = process_data(line)
        new_line1 = new_line.strip() + '|' + ' '.join(map(str,sentences)) + '|' + ' '.join(map(str,subword_lengths)) + '|' + ' '.join(map(str,ph_len)) + '\n'
        f1.write(new_line1)