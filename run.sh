#!/bin/bash

mkdir td_data td_data/train_td td_data/test_td
#preparing the data
python ./pd.py
#sorting the dirs
utils/fix_data_dir.sh td_data/train_td/
utils/fix_data_dir.sh td_data/test_td/
#preparing the dictionary
mkdir dict
echo -e "W\nAH\nN\nT\nUW\nTH\nR\nIY\nF\nAO\nAY\nV\nS\nIH\nK\nEH\nEY\nOW\nZ" > dict/phones.txt
echo -e "ONE W AH N\nTWO T UW\nTHREE TH R IY\nFOUR F AO R\nFIVE F AY V\nSIX S IH K S\nSEVEN S EH V EH N\nEIGHT EY T\nNINE N AY N\nTEN T EH N\nOH OW\nZERO Z IY R OW" > dict/lexicon.txt
echo "SIL" > dict/silence_phones.txt
echo "SIL" > dict/optional_silence.txt
mv dict/phones.txt dict/nonsilence_phones.txt
cp dict/lexicon.txt dict/lexicon_words.txt
echo "<SIL> SIL" >> dict/lexicon.txt
#preparing the lang portion
utils/prepare_lang.sh --position-dependent-phones false dict "<SIL>" tmp td_data/lang
#compiling the fst grammar
$KALDI_ROOT/tools/openfst/bin/fstcompile --isymbols=td_data/lang/words.txt --osymbols=td_data/lang/words.txt  output/G.txt output/td_data/lang/G.fst
#training
steps/make_mfcc.sh --nj 1 td_data/train_td/ exp/make_mfcc/train_td
steps/compute_cmvn_stats.sh td_data/train_td/ exp/make_mfcc/train_td
steps/train_mono.sh --nj 1 --cmd utils/run.pl td_data/train_td/ td_data/lang/ exp/mono
#building graphs
utils/mkgraph.sh --mono td_data/lang exp/mono exp/mono/graph_tgpr
#testing
steps/make_mfcc.sh --nj 1 td_data/test_td/ exp/make_mfcc/test_td
steps/compute_cmvn_stats.sh td_data/test_td/ exp/make_mfcc/test_td
#decoding
steps/decode.sh --nj 1 exp/mono/graph_tgpr td_data/test_td/ exp/mono/decode_test_td
