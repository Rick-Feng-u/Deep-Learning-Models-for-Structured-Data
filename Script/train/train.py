import torch
import torch.nn as nn
from torch import optim

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,
          max_length):
    encoder_hidden = encoder.init_hidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for input_elem in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[input_elem], encoder_hidden)
        encoder_outputs[input_elem] = encoder_output[0, 0]

    decoder_input = torch.tensor([[0]], device=device)

    decoder_hidden = encoder_hidden

    for target in range(target_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        loss += criterion(decoder_output, target_tensor[target])
        decoder_input = target_tensor[target]

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length


def train_iters(training_pairs, max_length, encoder, decoder, print_every=1000, plot_every=100, learning_rate=0.01):
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    criterion = nn.NLLLoss()

    training_data_size = len(training_pairs)

    for i in range(training_data_size):
        training_pair = training_pairs[i]
        input_idx_seq = training_pair[0]
        target_idx_seq = training_pair[1]

        input_idx_seq.append(1)  # EOS
        target_idx_seq.append(1)

        # print(input_idx_seq)
        input_tensor = torch.tensor(input_idx_seq, dtype=torch.long, device=device).view(-1, 1)
        target_tensor = torch.tensor(target_idx_seq, dtype=torch.long, device=device).view(-1, 1)

        loss = train(input_tensor, target_tensor, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion, max_length + 1)
        print_loss_total += loss
        plot_loss_total += loss

        if i % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print("loss average" + str(print_loss_avg))

        if i % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

    show_plot(plot_losses)


def show_plot(points):
    plt.figure()
    fig, ax = plt.subplots()
    # this locator puts ticks at regular intervals
    loc = ticker.MultipleLocator(base=0.2)
    ax.yaxis.set_major_locator(loc)
    plt.plot(points)
    plt.show()