import logging
import librosa
import fastdtw
from scipy.spatial.distance import euclidean

from datastructure.feature import Feature
from datastructure.distance import Distance
from util import sha256sum
from util import get_name


class Extractor:
    def __init__(self):
        """Constructor"""
        self.logger = logging.getLogger(__name__)

    def get_all_features(self, file):
        name = get_name(file)
        self.logger.info('Processing ', name)
        print('Processing ', name)
        y, sr = librosa.load(file)

        # Calculating mfcc feature
        mfcc = librosa.feature.mfcc(y, sr, n_mfcc=20)
        # Calculating chroma_cens feature
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        mel = librosa.feature.melspectrogram(y=y, sr=sr)
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        # Rhythm
        rhythm = librosa.feature.tempogram(y=y, sr=sr)

        hash = sha256sum(file)

        return Feature(hash=hash, name=name, mfcc=mfcc, chroma_cens=chroma_cens, chroma_stft=chroma_stft, mel=mel,
                       tonnetz=tonnetz, rhythm=rhythm)

    def get_distance(self, feature1, feature2):
        self.logger.info(feature1.name + ' <==> ' + feature2.name)
        print(feature1.name + ' <==> ' + feature2.name)
        dist_func = euclidean

        distance1, path1 = fastdtw.fastdtw(feature1.mfcc.T, feature2.mfcc.T, dist=dist_func)
        distance2, path2 = fastdtw.fastdtw(feature1.chroma_cens.T, feature2.chroma_cens.T, dist=dist_func)
        distance3, path3 = fastdtw.fastdtw(feature1.chroma_stft.T, feature2.chroma_stft.T, dist=dist_func)
        distance4, path4 = fastdtw.fastdtw(feature1.mel.T, feature2.mel.T, dist=dist_func)
        distance5, path5 = fastdtw.fastdtw(feature1.tonnetz.T, feature2.tonnetz.T, dist=dist_func)
        distance6, path6 = fastdtw.fastdtw(feature1.rhythm.T, feature2.rhythm.T, dist=dist_func)

        return Distance(hash1=feature1.hash, hash2=feature2.hash, name1=feature1.name, name2=feature2.name,
                        mfcc_dist=distance1, chroma_cens_dist=distance2, chroma_stft_dist=distance3,
                        mel_dist=distance4, tonnetz_dist=distance5, rhythm_dist=distance6)
