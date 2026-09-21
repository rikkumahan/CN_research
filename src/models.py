"""
src/models.py
Core Classification Architectures for SDWN Traffic Classification:
1. FFNN (8 -> 16 -> 8 -> 5, D=325) for PSO & MOPSO (Pradhan et al. & Senior)
2. 1D-CNN (PyTorch Baseline)
3. LSTM (PyTorch Baseline)
4. Transformer Encoder (PyTorch Baseline)

All models adhere to a unified interface and provide composite overhead (F) estimation.
"""

import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Default operator fitness weights (Claim 2)
DEFAULT_WEIGHTS = {
    'alpha': 0.45,   # Classification error (1 - Acc)
    'beta': 0.20,    # Flow-Rule Update Rate (FRUR)
    'gamma': 0.15,   # Active weight density (CPU overhead)
    'delta': 0.10,   # Mean weight magnitude (Flow setup delay)
    'epsilon': 0.10  # Sparse weight threshold (Southbound bandwidth)
}

# ----------------------------------------------------------------------
# 1. FFNN Architecture (8 -> 16 -> 8 -> 5, D=325)
# ----------------------------------------------------------------------
class FFNN:
    def __init__(self, ni=8, h1=16, h2=8, no=5):
        self.ni, self.h1, self.h2, self.no = ni, h1, h2, no
        self.D = ni * h1 + h1 + h1 * h2 + h2 + h2 * no + no  # 325

    def _unpack(self, w):
        ni, h1, h2, no = self.ni, self.h1, self.h2, self.no
        i = 0
        W1 = w[i:i + ni * h1].reshape(ni, h1); i += ni * h1; b1 = w[i:i + h1]; i += h1
        W2 = w[i:i + h1 * h2].reshape(h1, h2); i += h1 * h2; b2 = w[i:i + h2]; i += h2
        W3 = w[i:i + h2 * no].reshape(h2, no); i += h2 * no; b3 = w[i:i + no]
        return W1, b1, W2, b2, W3, b3

    def _fwd(self, X, w):
        W1, b1, W2, b2, W3, b3 = self._unpack(w)
        h1 = np.maximum(0, X @ W1 + b1)
        h2 = np.maximum(0, h1 @ W2 + b2)
        z = h2 @ W3 + b3
        e = np.exp(z - z.max(axis=1, keepdims=True))
        return e / e.sum(axis=1, keepdims=True)

    def predict(self, X, w):
        return np.argmax(self._fwd(X, w), axis=1)

    def acc(self, X, y, w):
        return accuracy_score(y, self.predict(X, w))

    def ce(self, X, y, w):
        p = self._fwd(X, w)
        return -np.log(p[np.arange(len(y)), y] + 1e-12).mean()

    # Fitness components
    def f1_err(self, X, y, w):
        return 1.0 - self.acc(X, y, w)

    def f2_frur(self, X, w, sigma=0.10, trials=5):
        base = self.predict(X, w)
        rates = [np.mean(base != self.predict(X + np.random.randn(*X.shape) * sigma, w))
                 for _ in range(trials)]
        return float(np.mean(rates))

    def f3_cpu(self, w):
        return float(np.mean(np.abs(w) > 0.3))

    def f4_fsd(self, w):
        return min(float(np.mean(np.abs(w))) / 3.0, 1.0)

    def f5_bw(self, w):
        return float(np.mean(np.abs(w) > 0.05))

    def composite(self, X, y, w, weights=DEFAULT_WEIGHTS):
        f1 = self.f1_err(X, y, w)
        f2 = self.f2_frur(X, w)
        f3 = self.f3_cpu(w)
        f4 = self.f4_fsd(w)
        f5 = self.f5_bw(w)
        F = (weights['alpha'] * f1 +
             weights['beta'] * f2 +
             weights['gamma'] * f3 +
             weights['delta'] * f4 +
             weights['epsilon'] * f5)
        return F, f1, f2, f3, f4, f5


# ----------------------------------------------------------------------
# 2. PyTorch 1D-CNN Baseline
# ----------------------------------------------------------------------
class PyTorchCNN1D(nn.Module):
    def __init__(self, num_features=8, num_classes=5):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(16)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        self.pool = nn.AdaptiveAvgPool1d(4)
        self.fc = nn.Linear(32 * 4, num_classes)

    def forward(self, x):
        # x shape: (batch_size, 8) -> (batch_size, 1, 8)
        x = x.unsqueeze(1)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


# ----------------------------------------------------------------------
# 3. PyTorch LSTM Baseline
# ----------------------------------------------------------------------
class PyTorchLSTM(nn.Module):
    def __init__(self, num_features=8, hidden_dim=32, num_classes=5, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_dim,
                            num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        # x shape: (batch_size, 8) -> (batch_size, 8, 1)
        x = x.unsqueeze(2)
        out, _ = self.lstm(x)
        last_out = out[:, -1, :]
        return self.fc(last_out)


# ----------------------------------------------------------------------
# 4. PyTorch Transformer Encoder Baseline
# ----------------------------------------------------------------------
class PyTorchTransformer(nn.Module):
    def __init__(self, num_features=8, d_model=32, nhead=4, num_layers=2, num_classes=5):
        super().__init__()
        self.embedding = nn.Linear(1, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead,
                                                   dim_feedforward=64, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(d_model * num_features, num_classes)

    def forward(self, x):
        # x shape: (batch_size, 8) -> (batch_size, 8, 1) -> (batch_size, 8, d_model)
        x = x.unsqueeze(2)
        x = self.embedding(x)
        x = self.transformer_encoder(x)
        x = x.reshape(x.size(0), -1)
        return self.fc(x)


# ----------------------------------------------------------------------
# 5. Generic DL Model Wrapper & Evaluator
# ----------------------------------------------------------------------
class DeepLearningWrapper:
    def __init__(self, model_class, name="DL_Model", epochs=40, lr=0.005, batch_size=64, num_classes=5):
        self.name = name
        self.epochs = epochs
        self.lr = lr
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model_class(num_features=8, num_classes=num_classes).to(self.device)
        self.train_time = 0.0

    def count_parameters(self):
        return sum(p.numel() for p in self.model.parameters() if p.requires_grad)

    def fit(self, X_train, y_train):
        start_time = time.time()
        self.model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr, weight_decay=1e-4)

        X_t = torch.tensor(X_train, dtype=torch.float32)
        y_t = torch.tensor(y_train, dtype=torch.long)
        dataset = torch.utils.data.TensorDataset(X_t, y_t)
        loader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        for epoch in range(self.epochs):
            for bx, by in loader:
                bx, by = bx.to(self.device), by.to(self.device)
                optimizer.zero_grad()
                out = self.model(bx)
                loss = criterion(out, by)
                loss.backward()
                optimizer.step()

        self.train_time = time.time() - start_time
        return self

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            X_t = torch.tensor(X, dtype=torch.float32).to(self.device)
            out = self.model(X_t)
            preds = torch.argmax(out, dim=1).cpu().numpy()
        return preds

    def evaluate(self, X_test, y_test):
        preds = self.predict(X_test)
        acc = accuracy_score(y_test, preds)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, preds, average="macro", zero_division=0)
        return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}

    def compute_composite_overhead(self, X_test, y_test, weights=DEFAULT_WEIGHTS, sigma=0.10):
        """
        Computes comparable F proxy for Deep Learning models based on weights and noise robustness.
        """
        preds = self.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = 1.0 - acc

        # FRUR under input feature jitter
        perturbed_X = X_test + np.random.randn(*X_test.shape) * sigma
        pert_preds = self.predict(perturbed_X)
        f2_frur = float(np.mean(preds != pert_preds))

        # Flatten all model parameters
        all_weights = np.concatenate([p.detach().cpu().numpy().flatten() for p in self.model.parameters()])
        f3_cpu = float(np.mean(np.abs(all_weights) > 0.3))
        f4_fsd = min(float(np.mean(np.abs(all_weights))) / 3.0, 1.0)
        f5_bw = float(np.mean(np.abs(all_weights) > 0.05))

        F = (weights['alpha'] * f1 +
             weights['beta'] * f2_frur +
             weights['gamma'] * f3_cpu +
             weights['delta'] * f4_fsd +
             weights['epsilon'] * f5_bw)
        return F, f1, f2_frur, f3_cpu, f4_fsd, f5_bw

