

import torch
import torch.nn as nn

words = ["happiness", "is", "my", "goal"]
word2idx = {w: i for i, w in enumerate(words)}
idx2word = {i: w for i, w in enumerate(words)}

x_input = torch.tensor([word2idx[w] for w in ["happiness", "is", "my"]]).unsqueeze(0)
y_target = torch.tensor([word2idx["goal"]])

vocab_size = len(words)
embed_size = 10
hidden_size = 20

embedding = nn.Embedding(vocab_size, embed_size)

Wxh = torch.randn(embed_size, hidden_size, requires_grad=True)
Whh = torch.randn(hidden_size, hidden_size, requires_grad=True)
bh = torch.randn(hidden_size, requires_grad=True)
Why = torch.randn(hidden_size, vocab_size, requires_grad=True)
by = torch.randn(vocab_size, requires_grad=True)

optimizer = torch.optim.Adam([Wxh, Whh, bh, Why, by] + list(embedding.parameters()), lr=0.01)
criterion = nn.CrossEntropyLoss()

for epoch in range(300):
    optimizer.zero_grad()
    x = embedding(x_input)
    h = torch.zeros(x.size(0), hidden_size)
    for t in range(x.size(1)):
        h = torch.tanh(x[:, t] @ Wxh + h @ Whh + bh)
    y_pred = h @ Why + by
    loss = criterion(y_pred, y_target)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 50 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

with torch.no_grad():
    x = embedding(x_input)
    h = torch.zeros(x.size(0), hidden_size)
    for t in range(x.size(1)):
        h = torch.tanh(x[:, t] @ Wxh + h @ Whh + bh)
    y_pred = h @ Why + by
    pred_idx = torch.argmax(y_pred, dim=1).item()
    print("Predicted word:", idx2word[pred_idx])
