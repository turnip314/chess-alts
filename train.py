import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader

class ChessDataset(Dataset):
    def __init__(self, board_states, target_values):
        self.board_states = board_states
        self.target_values = target_values

    def __len__(self):
        return len(self.board_states)

    def __getitem__(self, idx):
        return torch.tensor(self.board_states[idx], dtype=torch.float32), torch.tensor(self.target_values[idx], dtype=torch.float32)

class Trainer:
    def __init__(self, model):
        self.model = model

    def load(self, filename: str):
        pass

    def train_model(self, train_loader, epochs=10, save_path=None):
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for board_states, target_values in train_loader:
                board_states, target_values = board_states.to(device), target_values.to(device)

                # Forward pass
                predictions = self.model(board_states)

                # Compute loss
                loss = criterion(predictions, target_values)
                total_loss += loss.item()

                # Backward pass and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader)}")

        if save_path is not None:
            torch.save(self.model.state_dict(), save_path)
