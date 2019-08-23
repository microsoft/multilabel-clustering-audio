import os
import re
import resampy
import numpy as np
import tensorflow as tf
import click
import h5py
import tqdm
import librosa
import soundfile as psf
import subprocess
import shutil
import glob
import tempfile

import audioset.vggish_params as vggish_params

MODEL_PARAMS = 'audioset/vggish_model.ckpt'
PCA_PARAMS = 'audioset/vggish_pca_params.npz'
HOP_SIZE_S = 0.5
vggish_params.EXAMPLE_HOP_SECONDS = HOP_SIZE_S
SAMPLE_LENGTH = 10
XDIM = int(SAMPLE_LENGTH / HOP_SIZE_S) - 1
YDIM = 128

import audioset.vggish_input as vggish_input
import audioset.vggish_slim as vggish_slim
import audioset.vggish_postprocess as vggish_postprocess


@click.group()
def cli():
    pass

def load_input(filename, mono=True):
    """
    Extract input features
    Parameters
    ----------
    filename : str
    Yields
    -------
    dict of str: np.array
    """
    y, sr = psf.read(filename)
    if mono:
        y = librosa.to_mono(y.T)
    y = resampy.resample(y, sr, vggish_params.SAMPLE_RATE, filter='kaiser_fast')
    y /= np.max(np.abs(y))

    print('{} features {}'.format(filename, y.shape[0] / vggish_params.SAMPLE_RATE))
    return vggish_input.waveform_to_examples(y, vggish_params.SAMPLE_RATE).astype(np.float32)


def extract_vggish_embeddings(input_filepaths,
                              output_file,
                              xdim=XDIM,
                              ydim=YDIM,
                              start_index=0):

    pproc = vggish_postprocess.Postprocessor(PCA_PARAMS)

    with tf.Graph().as_default(), tf.Session() as sess, tqdm.tqdm(total=len(input_filepaths)) as pbar, h5py.File(output_file, 'w') as h5:
        # create dataset
        d = h5.create_dataset('features', (len(input_filepaths),), dtype=[('identifier', 'S32'),
                                                                          ('features', 'f4', (xdim, ydim)),
                                                                          ('features_z', 'u1', (xdim, ydim))])

        # Define the model in inference mode, load the checkpoint, and
        # locate input and output tensors.


        vggish_slim.define_vggish_slim(training=False)
        vggish_slim.load_vggish_slim_checkpoint(sess, MODEL_PARAMS)
        features_tensor = sess.graph.get_tensor_by_name(vggish_params.INPUT_TENSOR_NAME)
        embedding_tensor = sess.graph.get_tensor_by_name(vggish_params.OUTPUT_TENSOR_NAME)

        update_interval = int(len(input_filepaths) / 5.)
        idx = start_index
        for input_filepath in input_filepaths[start_index:]:
            input_data = load_input(input_filepath)

            [embedding] = sess.run([embedding_tensor], feed_dict={features_tensor: input_data})

            emb_pca = pproc.postprocess(embedding)

            identifier = os.path.split(input_filepath)[1]
            try:
                d[idx] = (identifier, embedding.astype('f4'), emb_pca.astype('u1'))
            except ValueError as e:
                print(idx, e)
                if embedding.shape[0] > xdim:
                    print('Too much data. Only using first {} output frames. {}'.format(xdim, identifier))
                    embedding = embedding[:xdim, :]
                    emb_pca = emb_pca[:xdim, :]
                else:
                    # pad to size, using NaN as fill
                    # NOTE THAT uint8 can't represent NaN, so you'll have to mask from embedding.
                    print('Too little data. Padding with nan. {}'.format(identifier))
                    embedding = np.pad(embedding, ((0, xdim - embedding.shape[0]), (0, 0)), 'constant', constant_values=np.nan)
                    emb_pca = np.pad(emb_pca, ((0, xdim - emb_pca.shape[0]), (0, 0)), 'constant', constant_values=np.nan)

                d[idx] = (identifier, embedding.astype('f4'), emb_pca.astype('u1'))

            idx += 1
            if (idx % update_interval) == 0:
                pbar.update(update_interval)


@cli.command('compute_features')
@click.argument('input-directory', type=click.Path(exists=True))
@click.argument('output-directory', type=click.Path(exists=True))
@click.option('--limit', type=click.INT, default=-1)
def compute_features(input_directory,
                     output_directory,
                     limit,):
    if limit == -1:
       limit = None

    for partition in ['test', 'validate', 'train']:
        audio_directory = os.path.join(input_directory, partition)
        output_filepath = os.path.join(output_directory, '{}_features.h5'.format(partition))

        audio_filepaths = sorted(glob.glob(os.path.join(audio_directory, '*.wav')))
        if limit is not None:
            audio_filepaths = audio_filepaths[:limit]
        extract_vggish_embeddings(audio_filepaths, output_filepath)


if __name__ == '__main__':
    cli()

