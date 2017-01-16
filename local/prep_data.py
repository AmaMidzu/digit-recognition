#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from abc import ABCMeta, abstractmethod

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = "YOURNAME"


class PrepData(object):
    """
    An abstract preprocessor class for 'data' part
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_text(self):
        """
        This file contains every utterance matched with its text transcription.
        formatted: utt_id transcript
        It is a good practice to have spk_id as prefix for utt_id.
        (e.g. utt_id = spk_id-utt_start-utt_end)
        In such a case, make sure all spk_ids have
        the same length to avoid sorting error.
        """
        raise NotImplementedError

    @abstractmethod
    def make_spk2gender_map(self):
        raise NotImplementedError

    @abstractmethod
    def make_spk2utt(self):
        """
        This file is a reverse index from utt2spk.
        formatted: spk_id utt_id#1 utt_id#2 utt_id#3 ...
        You can create this file using utils/utt2spk_to_spk2utt.pl .
        Or can implement yourself.
        Make sure the original file is sorted in C locale.
        """
        raise NotImplementedError

    @abstractmethod
    def make_utt2spk(self):
        """
        This file tells Kaldi which utterance belongs to particular speaker.
        formatted: utt_id spk_id
        Note that even if you already used spk_id as prefixes in utt_id,
        this file is still needed.
        NOTE: If you don't speaker identity annotations,
        do not use some 'global' id for all speakers,
        rather treat each utterance is spoken by different speakers
        """
        raise NotImplementedError

    @abstractmethod
    def make_wav_scp(self):
        """
        This file lets Kaldi know where to look for wave files.
        formatted: file_id filepath
        Filepath can be a absolute path or a bash command to get the wave file.
        (especially when dealing with sphere files.)
        If you are using a command that pipes out the conversion i.e. sph2pipe,
        you need to specifically pipe-out the command using '|' at the end
            e.g.
            /path/to/sph2pipe -f wav $filename |
        The files pointed by wav.scp must be single-channel (mono).
        If not, include extraction of the exact channel you want in the *command*

        """
        raise NotImplementedError

    @abstractmethod
    def make_segments(self):
        """
        This file have slicing points of wave files to get individual utterances.
        formatted: utt_id file_id start end
        start and end should be seconds formatted up to 2 decimal places.
        """
        raise NotImplementedError

    @abstractmethod
    def make_reco2file_and_channel(self):
        """
        This file is only required when you have "stm" index in the data.
        formatted: file_id file_basename side
        Only applicable to some data that have two-channel recordings.
        file_basename is file_id without channel_id, side is the channel_id.
        Used in sclite scoring.
        """
        raise NotImplementedError

    @abstractmethod
    def get_uttid(self, wave_filename):
        raise NotImplementedError

    @abstractmethod
    def get_spkid(self, wave_filename):
        raise NotImplementedError

    @abstractmethod
    def get_fileid(self, wave_filename):
        raise NotImplementedError


