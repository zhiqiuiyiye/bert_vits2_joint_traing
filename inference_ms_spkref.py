## VCTK
import torch
import os
import commons
import utils
from models_v1_spkref import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence, clean_ph_to_sequence
from utils import get_audio

import codecs
import time

from transformers import BertTokenizer, BertModel
import torch
punctuation = ["!", "?", "…", ",", ".", "-",";",":"]
import random
random.seed(123)

tokenizer = BertTokenizer.from_pretrained('/data_02/chuyinxue/upload/bert-vits2/text/bert-base-multilingual-cased')
model = BertModel.from_pretrained("/data_02/chuyinxue/upload/bert-vits2/text/bert-base-multilingual-cased")
# tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
# model = BertModel.from_pretrained("bert-base-multilingual-cased")

# for params in model.parameters():
#     params.requires_grad = False
# for params in model.encoder.layer[-2:].parameters():
#     params.requires_grad = True
# import pdb;pdb.set_trace()
# for name,param in model.named_parameters():
#     print(f"{name}: {param.requires_grad}")

def norm_text(data):
    data = data.strip().replace('/',' ').replace('%',' ')
    for punc in punctuation:
        data = data.replace(' '+punc,punc)
    return data
def process_data(line):
    subword_lengths =[]
    # import pdb;pdb.set_trace()
    id,text,phoneme = line.strip().split('|')
    text = text.replace('"','')
    phoneme = phoneme.replace('/ " /','/')
    # if spk not in ['haitian']:
    #     text = text.strip().replace('-',' ')
    text = norm_text(text)
    tokens = text.strip().split()
    subwords = list(map(tokenizer.tokenize,tokens))
    subword_lengths = [1]+list(map(len, subwords))+[1]
    subwords = ['[CLS]'] + [i for indices in subwords for i in indices] + ['[SEP]']
    tokenize_res = tokenizer.convert_tokens_to_ids(subwords)
    if len(tokens)+2 != len(subword_lengths):
        print(line)
    ph_list = phoneme.strip().replace('/ sil','').replace('sil /','').split('/')
    ph_len = []
    flag_list = []
    for ph in ph_list:
        flag = 0
        for punc in punctuation:
            if punc in ph:
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
    # import pdb;pdb.set_trace()
    if len(ph_len) != len(subword_lengths):
        import pdb;pdb.set_trace()
    if sum(ph_len) != len(phoneme.strip().split()):
        import pdb;pdb.set_trace()
 
    return tokenizer.convert_tokens_to_ids(subwords),subword_lengths,ph_len


# with codecs.open('/data_02/chuyinxue/research/Bert-VITS2/data/metadata.list','r','utf-8') as f:
#     with codecs.open('/data_02/chuyinxue/research/Bert-VITS2/data/metadata_new.list','w','utf-8') as f1:
#         for line in f:
#             sentences,subword_lengths,ph_len = process_data(line)
#             new_line = line.strip() + '|' + ' '.join(map(str,sentences)) + '|' + ' '.join(map(str,subword_lengths)) + '|' + ' '.join(map(str,ph_len)) + '\n'
#             f1.write(new_line)



from scipy.io.wavfile import write


# def get_text(text, hps):
#     text_norm = text_to_sequence(text, hps.data.text_cleaners)
#     if hps.data.add_blank:
#         text_norm = commons.intersperse(text_norm, 0)
#     text_norm = torch.LongTensor(text_norm)
#     return text_norm


CONFIG_PATH = "/data_02/chuyinxue/research/vits2_pytorch/logs/bert_idn_spkref/config.json"
MODEL_PATH = "/data_02/chuyinxue/research/vits2_pytorch/logs/bert_idn_spkref/G_204000.pth"
TEXT_PATH = "/data_02/chuyinxue/research/vits2_pytorch/test/test_cases_id.txt"
SPK = "Ajeng_CG"
refwav = '/data_02/chuyinxue/dataset/IND_data/finetune/Ajeng_CG/wavs_16k_nf1_add_sil/1.wav'
OUTPUT_WAV_PATH = "output/model_v1_ajeng_cg_refspk/"
devices = torch.device('cuda:0')

spk_name = ['haitian', 'ajeng', 'rifan', 'Iyok', 'Robert', 'Novinda', 'Natasha',
             'qio', 'Indry', 'Alifan', 'nadya', 'hani', 'panji', 'Robert_CG','Ajeng_CG','Nirmala']
spk=[spk_name.index(SPK)]
spec,audio_norm = get_audio(refwav)

hps = utils.get_hparams_from_file(CONFIG_PATH)

if (
    "use_mel_posterior_encoder" in hps.model.keys()
    and hps.model.use_mel_posterior_encoder == True
):
    print("Using mel posterior encoder for VITS2")
    posterior_channels = 80  # vits2
    hps.data.use_mel_posterior_encoder = True
else:
    print("Using lin posterior encoder for VITS1")
    posterior_channels = hps.data.filter_length // 2 + 1
    hps.data.use_mel_posterior_encoder = False

net_g = SynthesizerTrn(
    len(symbols),
    posterior_channels,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model
).to(devices)
_ = net_g.eval()

_ = utils.load_checkpoint(MODEL_PATH, net_g, None)

# stn_tst = get_text(TEXT, hps)
with codecs.open(TEXT_PATH,'r','utf-8') as f:
    data =f.readlines()
    start_time = time.time()
    audio_length = 0
    for line in data:
        print(line)
        id,text,phoneme = line.strip().split('|')
        # import pdb;pdb.set_trace()
        senten,subword_len,ph_len1 = process_data(line)
        sentences = torch.LongTensor(senten).unsqueeze(0).to(devices)
        token2word = torch.FloatTensor(1, len(subword_len), sentences.size(1)).to(devices)
        word2phone = torch.FloatTensor(1, len(ph_len1), len(phoneme.strip().split())).to(devices)
        token2word.zero_()
        word2phone.zero_()
        sum_len=0
        # import pdb;pdb.set_trace()
        for j in range(len(subword_len)):
            token2word[0,j,sum_len:sum_len+subword_len[j]]=1/(subword_len[j]+(1e-9))
            sum_len += subword_len[j]
        sum_len=0
        for j in range(len(ph_len1)):
            word2phone[0,j,sum_len:sum_len+ph_len1[j]]=1
            sum_len += ph_len1[j]
        # import pdb;pdb.set_trace()
        spec_len = torch.tensor(spec.size(1)).unsqueeze(0).to(devices)
        spec_tensor = spec.unsqueeze(0).to(devices)
        ph = clean_ph_to_sequence(phoneme)
        ph = torch.LongTensor(ph).unsqueeze(0).to(devices)
        ph_lengths = torch.LongTensor([ph.size(1)]).to(devices)
        sentences_lengths = torch.LongTensor([sentences.size(1)]).to(devices)
        # import pdb;pdb.set_trace()
        sid =torch.LongTensor(spk).to(devices)
        with torch.no_grad():
            audio = (
                net_g.infer(
                    ph,
                    ph_lengths,
                    spec_tensor,
                    spec_len,
                    sentences,
                    sentences_lengths,
                    token2word,
                    word2phone,
                    0,
                    sid=sid,
                    # noise_scale=1,
                    # noise_scale_w=1,
                    noise_scale=0.667,
                    noise_scale_w=0.8,
                    length_scale=1,
                )[0][0, 0]
                .data.cpu()
                .float()
                .numpy()
            )
        os.makedirs(OUTPUT_WAV_PATH,exist_ok=True)
        file_name = OUTPUT_WAV_PATH +id+".wav"
        write(data=audio, rate=hps.data.sampling_rate, filename=file_name)
        audio_length += len(audio)/hps.data.sampling_rate
    end_time = time.time()
    rtf = (end_time-start_time)/audio_length
    print(rtf)



        

        



# with torch.no_grad():
#     x_tst = stn_tst.to(devices).unsqueeze(0)
#     x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(devices)
#     sid = torch.LongTensor([SPK_ID]).to(devices)
#     audio = (
#         net_g.infer(
#             x_tst,
#             x_tst_lengths,
#             sid=sid,
#             noise_scale=0.667,
#             noise_scale_w=0.8,
#             length_scale=1,
#         )[0][0, 0]
#         .data.cpu()
#         .float()
#         .numpy()
#     )

# write(data=audio, rate=hps.data.sampling_rate, filename=OUTPUT_WAV_PATH)
