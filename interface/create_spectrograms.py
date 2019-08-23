import os
import librosa
import matplotlib.pyplot as plt
import glob
import numpy as np
import librosa.display
import matplotlib.ticker as ticker


def create_spectrogram(recording_group_dir, filename, spectrogram_dir, sr, amin=1e-4):
    """
    * Calculates spectrogram and add those to an image `<group_id>` directory.
    
    Parameters
    ----------
    recording_group_dir : str
        directory where recordings are located.
    filename : str
        name of file
    spectrogram_group_dir : str
        directory where spectrograms will be saved.
    sr : int
        sampling rate.
    amin : float
        Minimum value for spectogram display.

    Returns
    -------
    None
    """
    y, sr = librosa.load(os.path.join(recording_group_dir, filename) + '.wav', sr)

    D = librosa.power_to_db(librosa.stft(y, n_fft=512, hop_length=256), ref=np.max, amin=amin)

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 1, 1)

    librosa.display.specshow(D, y_axis='linear', sr=sr, hop_length=256, )

    plt.tight_layout()

    plt.axis('off')
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())

    plt.savefig(os.path.join(spectrogram_dir, filename) + '.jpg', bbox_inches='tight',
                pad_inches=-0.3)


print('hello')

audio_folder = 'C:/Users/t-anmend/Documents/interface/src/assets/SONYC/train/'
audio_paths = sorted(glob.glob(os.path.join(audio_folder, '*.wav')))

filenames = [os.path.splitext(os.path.split(audio_path)[1])[0].replace("\\","/") for audio_path in audio_paths]

spectrogram_dir = 'C:/Users/t-anmend/Documents/interface/src/assets/SONYC/images/train'

for i in range(2138,len(filenames)):
    print(filenames[i])
    create_spectrogram(audio_folder, filenames[i], spectrogram_dir, sr=44100)