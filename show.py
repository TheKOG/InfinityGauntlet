import torchaudio
import matplotlib.pyplot as plt

waveform,sample_rate = torchaudio.load("tmp/tmp_.wav")

plt.plot(waveform.numpy()[0])
print(waveform.numpy()[0].max())
plt.show()