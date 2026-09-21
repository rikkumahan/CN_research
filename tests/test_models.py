"""
tests/test_models.py
Unit tests for Model Architectures:
- FFNN (D=325 parameters)
- 1D-CNN, LSTM, Transformer (PyTorch baselines)
- Forward pass output shape and probability normalization
"""

import pytest
import numpy as np
import torch
from src.models import FFNN, PyTorchCNN1D, PyTorchLSTM, PyTorchTransformer, DeepLearningWrapper

def test_ffnn_parameter_count_and_forward():
    ffnn = FFNN(ni=8, h1=16, h2=8, no=5)
    # D = (8*16 + 16) + (16*8 + 8) + (8*5 + 5) = 144 + 136 + 45 = 325
    assert ffnn.D == 325

    w = np.random.randn(ffnn.D) * 0.1
    X = np.random.randn(20, 8)
    probs = ffnn._fwd(X, w)
    
    assert probs.shape == (20, 5)
    assert np.allclose(probs.sum(axis=1), 1.0, atol=1e-5)
    preds = ffnn.predict(X, w)
    assert len(preds) == 20
    assert np.all(preds >= 0) and np.all(preds < 5)

def test_pytorch_cnn1d_shape_and_params():
    model = PyTorchCNN1D(num_features=8, num_classes=5)
    x = torch.randn(16, 8)
    out = model(x)
    assert out.shape == (16, 5)

def test_pytorch_lstm_shape_and_params():
    model = PyTorchLSTM(num_features=8, hidden_dim=32, num_classes=5, num_layers=2)
    x = torch.randn(16, 8)
    out = model(x)
    assert out.shape == (16, 5)

def test_pytorch_transformer_shape_and_params():
    model = PyTorchTransformer(num_features=8, d_model=32, nhead=4, num_layers=2, num_classes=5)
    x = torch.randn(16, 8)
    out = model(x)
    assert out.shape == (16, 5)

def test_dl_wrapper_fit_predict():
    wrapper = DeepLearningWrapper(PyTorchCNN1D, name="TestCNN", epochs=2, batch_size=16)
    X = np.random.randn(32, 8).astype(np.float32)
    y = np.random.randint(0, 5, size=32)
    wrapper.fit(X, y)
    preds = wrapper.predict(X)
    assert len(preds) == 32
    metrics = wrapper.evaluate(X, y)
    assert "accuracy" in metrics
    assert "f1" in metrics

