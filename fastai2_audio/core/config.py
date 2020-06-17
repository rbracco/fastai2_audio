# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_Core_Config_Pipeline.ipynb (unless otherwise specified).

__all__ = ['AudioBlock', 'config_from_func', 'AudioConfig']

# Cell
from fastai2.data.all import *
from .signal import *
from .spectrogram import *
from ..augment.preprocess import Resample
from ..augment.signal import DownmixMono, CropSignal
import torchaudio.transforms as transforms
from inspect import signature
from dataclasses import make_dataclass

# Cell
def AudioBlock(sample_rate=16000, force_mono=True, crop_signal_to=None, cls=AudioTensor):
    tfms = [Resample(sample_rate)]
    if force_mono:
        tfms.append(DownmixMono())
    if crop_signal_to is not None:
        tfms.append(CropSignal(duration=crop_signal_to))
    return TransformBlock(type_tfms=cls.create, item_tfms=Pipeline(tfms), batch_tfms=IntToFloatTensor)

# Cell
def config_from_func(func, name, **kwargs):
    params = signature(func).parameters.items()
    namespace = {k:v.default for k, v in params}
    namespace.update(kwargs)
    return make_dataclass(name, namespace.keys(), namespace=namespace)

# Cell
class AudioConfig():
    #default configurations from the wrapped function
    #make sure to pass in mel=False as kwarg for non-mel spec, and to_db=False for non db spec
    BasicSpectrogram    = config_from_func(transforms.Spectrogram, "BasicSpectrogram", mel=False, to_db=True)
    BasicMelSpectrogram = config_from_func(transforms.MelSpectrogram, "BasicMelSpectrogram", mel=True, to_db=True)
    BasicMFCC           = config_from_func(transforms.MFCC, "BasicMFCC ")
    #special configs with domain-specific defaults

    Voice = config_from_func(transforms.MelSpectrogram, "Voice", mel="True", to_db="False", f_min=50., f_max=8000., n_fft=1024, n_mels=128, hop_length=128)