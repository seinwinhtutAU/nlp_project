import numpy as np
import librosa
import parselmouth
from parselmouth.praat import call

sample_rate = 22050

def extract_features(file_path):
    y, _ = librosa.load(file_path, sr=sample_rate, mono=True)

    mfcc = librosa.feature.mfcc(y=y, sr=sample_rate, n_mfcc=13)
    delta_mfcc = librosa.feature.delta(mfcc)
    delta_mfcc_features = delta_mfcc.mean(axis=1)

    chroma = librosa.feature.chroma_stft(
        S=np.abs(librosa.stft(y)), sr=sample_rate
    )
    chroma_features = chroma.mean(axis=1)

    rms = librosa.feature.rms(y=y)
    rms_features = np.array([rms.mean(), rms.std()])

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sample_rate)
    centroid_normalized = spectral_centroid / (sample_rate / 2)
    centroid_features = np.array([centroid_normalized.mean(), centroid_normalized.std()])

    f0 = librosa.yin(y, fmin=80, fmax=300)
    f0_clean = f0[f0 > 0]
    if len(f0_clean) > 0:
        f0_features = np.array([
            f0_clean.mean(),
            f0_clean.std(),
            f0_clean.max() - f0_clean.min()
        ])
    else:
        f0_features = np.zeros(3)

    snd = parselmouth.Sound(file_path)
    harmonicity = call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr_values = harmonicity.values[harmonicity.values > -199]
    hnr_mean = hnr_values.mean() if len(hnr_values) > 0 else 0.0

    mel = librosa.feature.melspectrogram(y=y, sr=sample_rate, n_mels=40)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_features = np.hstack([mel_db.mean(axis=1), mel_db.std(axis=1)])

    features = np.hstack([
        delta_mfcc_features,  # 13
        chroma_features,      # 12
        rms_features,         # 2
        centroid_features,    # 2
        f0_features,          # 3
        [hnr_mean],           # 1
        mel_features,         # 80
    ])

    return features  # shape: (113,)