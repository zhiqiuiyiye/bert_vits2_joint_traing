import numpy as np
import os
import codecs
with codecs.open('/data_02/chuyinxue/research/vits2_pytorch/data/myen_data/metadata_new_train.list','r','utf-8') as f:
    for line in f:
        audio = line.strip().split('|')[0]
        assert os.path.exists(audio)
        mel = audio.replace(".wav", ".mel.pt")
        if os.path.exists(mel):
            print(mel)
            melnpy = np.load(mel)