# La Min Oo 6540039
# Set Kaung Lwin 6632017
# Sein Win Htut  6611040
import numpy as np
import librosa
import parselmouth
from parselmouth.praat import call

# extract audio features for SVM

# because of jupyter and multiprocessing library limitation
# this feature extraction was needed to split into another file
# for SVM training

def extract_features(file_path, sample_rate=22050):
    y, _ = librosa.load(file_path, sr=sample_rate, mono=True)

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

    rms = librosa.feature.rms(y=y)
    rms_features = np.array([rms.mean(), rms.std()])

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sample_rate)
    centroid_normalized = spectral_centroid / (sample_rate / 2)
    centroid_features = np.array([centroid_normalized.mean(), centroid_normalized.std()])

    mfcc = librosa.feature.mfcc(y=y, sr=sample_rate, n_mfcc=7)
    mfcc_features = mfcc.mean(axis=1)

    delta_mfcc = librosa.feature.delta(mfcc)
    delta_mfcc_features = delta_mfcc.mean(axis=1)

    snd = parselmouth.Sound(file_path)
    harmonicity = call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr_values = harmonicity.values[harmonicity.values > -199]
    hnr_mean = hnr_values.mean() if len(hnr_values) > 0 else 0.0

    chroma = librosa.feature.chroma_stft(
        S=np.abs(librosa.stft(y)), sr=sample_rate
    )
    chroma_features = chroma[:4].mean(axis=1)  

    features = np.hstack([
        f0_features,          
        rms_features,          
        centroid_features,     
        mfcc_features,         
        delta_mfcc_features,  
        [hnr_mean],            
        chroma_features,      
    ])

    return features 