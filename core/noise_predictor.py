import torch
import torch.nn as nn

class FluxNoiseLSTM(nn.Module):
    def __init__(self, input_size=128, hidden_size=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return self.sigmoid(out)

if __name__ == "__main__":
    model = FluxNoiseLSTM()
    dummy = torch.randn(1, 10, 128)
    print(f"Prediction: {model(dummy).item():.3f}")
