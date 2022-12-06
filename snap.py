import torch
import torchaudio
import numpy as np
from IPython.display import display,Audio
import matplotlib.pyplot as plt
from torch import nn
from transformers import Wav2Vec2FeatureExtractor, WavLMForXVector

class CFG:
    device='cpu'
    RATE=16000
    percent=0.9
    batch_size=1
    epoches=80
    lr=1e-6
    load_pth='pth/best.pth'
    debug=114514
    save_steps=20
    length=15360

def Load_Snap(filename = "./audios/snaps/snap0.wav"):
    waveform,sample_rate = torchaudio.load(filename)
    # print("Shape of waveform:{}".format(waveform.size())) #音频大小
    # print("sample rate of waveform:{}".format(sample_rate))#采样率
    resampler = torchaudio.transforms.Resample(sample_rate, CFG.RATE)
    if(sample_rate!=CFG.RATE):
        waveform=resampler(waveform)
    for channel in waveform:
        return channel

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("microsoft/wavlm-base-plus")

class Snap(nn.Module):
    def __init__(self):
        super(Snap,self).__init__()
        sample_snap=Load_Snap('audios/snaps/snap0.wav')
        self.sample_inputs=feature_extractor(sample_snap, padding=True, return_tensors="pt",sampling_rate=CFG.RATE).to(CFG.device)
        # print(self.sample_inputs['input_values'].shape)

    def forward(self, x):
        x=x.reshape(CFG.batch_size,-1).cpu().numpy()
        tmp=[]
        for a in x:
            tmp.append(a)
        x=feature_extractor(tmp, padding=True, return_tensors="pt",sampling_rate=CFG.RATE).to(CFG.device)
        self.sample=pretrained(**self.sample_inputs).embeddings[0]
        x=pretrained(**x).embeddings
        cosine_sim = torch.nn.CosineSimilarity(dim=-1)
        similarity = cosine_sim(self.sample, x)
        return similarity

model=Snap()
model=model.to(CFG.device)

def Load(pth=CFG.load_pth):
    global pretrained
    pretrained=WavLMForXVector.from_pretrained(pth)

def is_Snap(filename):
    x=Load_Snap(filename)
    y=model(x)
    return y

if __name__=='__main__':
    Load('pth/best_pth')
    print(is_Snap('tmp/tmp.wav'))