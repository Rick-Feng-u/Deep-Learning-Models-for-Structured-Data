import torch
from Script import Encoder, Decoder, train_iters

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

hidden_size = 256
#encoder_ = Encoder(input_seq_name.size_of_index, hidden_size).to(device)
#decoder_ = Decoder(hidden_size, out_seq_name.size_of_index).to(device)
#train_iters(pairs, input_seq_name, out_seq_name, input_seq_name.highest_length, encoder_, decoder_)