import torch

from models.decoder import Decoder
from models.encoder import Encoder
from models.seq2seq import Seq2Seq
from utils.utils import IGNORE_ID

if __name__ == "__main__":
    # Encoder
    D, H, Li, B, R = 8, 2, 2, True, 'lstm'
    N, Ti, To = 4, 10, 5
    padded_input = torch.randn(N, Ti, D)
    input_lengths = torch.tensor([Ti]*N, dtype=torch.int)
    padded_input[-2, -2:, ] = 0
    input_lengths[-2] = Ti - 2
    padded_input[-1, -3:, ] = 0
    input_lengths[-1] = Ti - 3

    encoder = Encoder(D, H, Li,
                      bidirectional=B,
                      rnn_type=R)

    # Decoder
    VOC, EMB, SOS, EOS, L = 10, 3, 8, 9, 2
    H = H * 2 if B else H
    padded_target = torch.randint(10, (N, To), dtype=torch.long)  # N x To
    padded_target[-1, -3:] = IGNORE_ID

    decoder = Decoder(VOC, EMB, SOS, EOS, H, L)

    # Seq2Seq
    seq2seq = Seq2Seq(encoder, decoder)
    loss = seq2seq(padded_input, input_lengths, padded_target)
    print(loss)
    # print(decoder_outputs)
    # print("To+1 =", len(decoder_outputs))
    # print("N, V =", decoder_outputs[0].size())

    import argparse
    beam_size = 5
    nbest = 5
    defaults = dict(beam_size=beam_size,
                    nbest=nbest,
                    decode_max_len=0)
    args = argparse.Namespace(**defaults)
    char_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    for i in range(3):
        print("\n***** Utt", i+1)
        Ti = i + 20
        input = torch.randn(Ti, D)
        length = torch.tensor([Ti], dtype=torch.int)
        nbest_hyps = seq2seq.recognize(input, length, char_list, args)
