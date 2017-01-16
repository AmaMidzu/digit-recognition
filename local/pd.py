from prep_data import PrepData

import os
import os.path
import sys

kaldi_dir=''
corpus_dir=''
output_dir=''

class PD(PrepData):
    def make_text(self, filenames):
        results = []
        for t in filenames:
            spk_id = t[0]
            transcript = t[1].replace('1', 'ONE ').replace('2', 'TWO ').replace('3', 'THREE ').replace('4', 'FOUR ').replace('5', 'FIVE ').replace('6', 'SIX ').replace('7', 'SEVEN ').replace('8', 'EIGHT ').replace('9', 'NINE ').replace('z', 'ZERO ').replace('o', 'OH ').replace('a', '').replace('b', '')
            results.append("{}-{} {}".format(spk_id, t[1], transcript))
        return '\n'.join(sorted(results))

    def make_spk2gender_map(self):
        pass

    def make_spk2utt(self, filenames):
        pass

    def make_utt2spk(self, filenames):
        results = []
        for filename in filenames:
            results.append("{} {}".format(filename[0]+'-'+filename[1], filename[0]))
        return '\n'.join(sorted(results))

    def make_wav_scp(self, filenames, path):
        results = []
        for filename in filenames:
            results.append("{} {}".format(filename[0]+'-'+filename[1], (kaldi_dir+'tools/sph2pipe_v2.5/sph2pipe -f wav '+path+'/'+filename[0]+'/'+filename[1]+'.wav'+' |')))
        return '\n'.join(sorted(results))

    def make_segments(self):
        pass

    def make_reco2file_and_channel(self):
        pass

    def get_uttid(wave_filename):
        return wave_filename.split('.')[0]

    def get_spkid(wave_filename):
        return wave_filename.split('-')[0]

    def get_fileid(wave_filename):
        return wave_filename.split('-')[1]

def main():
    man = corpus_dir+'tidigits_comp/data/adults/train/man'
    woman = corpus_dir+'tidigits_comp/data/adults/train/woman'
    man_filenames = []
    woman_filenames = []
    man_test = corpus_dir+'tidigits_comp/data/adults/test/man'
    woman_test = corpus_dir+'tidigits_comp/data/adults/test/woman'
    man_test_filenames = []
    woman_test_filenames = []

    pd = PD()

    for d in os.listdir(man):
        for f in os.listdir(os.path.join(man,d)):
            fn = f.split('/')[-1].split('.')[0]
            man_filenames.append((d, fn))
    for d in os.listdir(woman):
        for f in os.listdir(os.path.join(woman,d)):
            fn = f.split('/')[-1].split('.')[0]
            woman_filenames.append((d, fn))

    for d in os.listdir(man_test):
        for f in os.listdir(os.path.join(man_test,d)):
            fn = f.split('/')[-1].split('.')[0]
            man_test_filenames.append((d, fn))
    for d in os.listdir(woman_test):
        for f in os.listdir(os.path.join(woman_test,d)):
            fn = f.split('/')[-1].split('.')[0]
            woman_test_filenames.append((d, fn))

    with open(output_dir+'td_data/train_td/text', 'w') as train_text, open(output_dir+'td_data/test_td/text', 'w') as test_text:
        train_text.write(pd.make_text(man_filenames))
        train_text.write('\n')
        train_text.write(pd.make_text(woman_filenames))
        test_text.write(pd.make_text(man_test_filenames))
        test_text.write('\n')
        test_text.write(pd.make_text(woman_test_filenames))
    with open(output_dir+'td_data/train_td/wav.scp', 'w') as train_text, open(output_dir+'td_data/test_td/wav.scp', 'w') as test_text:
        train_text.write(pd.make_wav_scp(man_filenames, man))
        train_text.write('\n')
        train_text.write(pd.make_wav_scp(woman_filenames, woman))
        test_text.write(pd.make_wav_scp(man_test_filenames, man_test))
        test_text.write('\n')
        test_text.write(pd.make_wav_scp(woman_test_filenames, woman_test))
    with open(output_dir+'td_data/train_td/utt2spk', 'w') as train_text, open(output_dir+'td_data/test_td/utt2spk', 'w') as test_text:
        train_text.write(pd.make_utt2spk(man_filenames))
        train_text.write('\n')
        train_text.write(pd.make_utt2spk(woman_filenames))
        test_text.write(pd.make_utt2spk(man_test_filenames))
        test_text.write('\n')
        test_text.write(pd.make_utt2spk(woman_test_filenames))

if __name__ == '__main__':
    main()
