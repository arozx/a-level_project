import os
import sqlite3
from datetime import datetime

import chess
import pandas as pd
import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from sklearn.model_selection import train_test_split
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset


class ChessDataset(Dataset):
    def __init__(self, df, moves_df):
        self.df = df
        self.moves_df = moves_df
        self.length = len(df)

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        game = self.df.iloc[idx]

        # Get the moves for this game
        game_moves = self.moves_df[self.moves_df["game_id"] == game["id"]]

        # Apply the moves to a chess board to get the game state
        board = chess.Board()
        for _, move_row in game_moves.iterrows():
            move = chess.Move.from_uci(move_row["move"])
            board.push(move)

        # Convert the game state to a tensor
        game_state = board.fen()
        x = self.game_to_tensor(game_state)

        y = game["result"]
        return x, y

    @staticmethod
    def game_to_tensor(fen):
        # Map each piece to a dimension in the tensor
        piece_to_dim = {
            "P": 0,
            "R": 1,
            "N": 2,
            "B": 3,
            "Q": 4,
            "K": 5,
            "p": 6,
            "r": 7,
            "n": 8,
            "b": 9,
            "q": 10,
            "k": 11,
        }

        # Parse the FEN string
        board, color, _, _, _, _ = fen.split(" ")

        # Initialize the tensor
        tensor = torch.zeros(13, 8, 8)

        # Set the last dimension to represent the active color
        tensor[12] = 1 if color == "w" else 0

        # Set the tensor elements corresponding to the pieces on the board
        for i, row in enumerate(board.split("/")):
            col = 0
            for char in row:
                if char.isdigit():
                    # Empty squares
                    col += int(char)
                else:
                    # There is a piece on this square
                    tensor[piece_to_dim[char]][i][col] = 1
                    col += 1

        return tensor


class ChessDataModule(pl.LightningDataModule):
    def __init__(self, db_path, batch_size):
        super().__init__()
        self.db_path = db_path
        self.batch_size = batch_size

    def setup(self, stage=None):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)

        # Fetch all data from the 'games' table
        games_query = "SELECT * FROM games;"
        games_data = pd.read_sql_query(games_query, conn)

        # Fetch all data from the 'moves' table
        moves_query = "SELECT * FROM moves;"
        moves_data = pd.read_sql_query(moves_query, conn)

        # Split the games data into training, validation, and testing sets
        train_data, temp_data = train_test_split(
            games_data, test_size=0.4, random_state=42
        )
        val_data, test_data = train_test_split(
            temp_data, test_size=0.5, random_state=42
        )

        # Create the datasets
        self.train_dataset = ChessDataset(train_data, moves_data)
        self.val_dataset = ChessDataset(val_data, moves_data)
        self.test_dataset = ChessDataset(test_data, moves_data)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset, batch_size=32, num_workers=4, pin_memory=True
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset, batch_size=32, num_workers=4, pin_memory=True
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset, batch_size=32, num_workers=4, pin_memory=True
        )


class ChessModel(pl.LightningModule):
    def __init__(self):
        super(ChessModel, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        # Fully connected layers
        self.fc1 = nn.Linear(256 * 8 * 8, 2048)
        self.fc2 = nn.Linear(2048, 512)
        self.fc3 = nn.Linear(512, 1)  # Output layer

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # Flatten the tensor
        x = x.view(-1, 256 * 8 * 8)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.tanh(self.fc3(x))  # Output between -1 and 1
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y.long())  # Convert y to long type
        self.log("train_loss", loss)

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y.long())  # Convert y to long type
        self.log("val_loss", loss)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y.long())  # Convert y to long type
        self.log("test_loss", loss)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
        return [optimizer], [scheduler]


def main():
    # Initialize the DataModule and Model
    datamodule = ChessDataModule("chess_games.db", batch_size=4096)
    model = ChessModel()

    if not os.path.exists("tb_logs/chess_ai"):
        os.makedirs("tb_logs/chess_ai")

    # Initialize the TensorBoard logger
    logger = TensorBoardLogger("tb_logs", name="chess_ai")

    # Initialize the early stopping callback
    early_stop_callback = EarlyStopping(
        monitor="val_loss", min_delta=0.00, patience=3, verbose=False, mode="min"
    )

    # Initialize the Trainer with the logger and the early stopping callback
    trainer = pl.Trainer(
        gpus=1,
        precision=16,
        accumulate_grad_batches=4,
        max_epochs=10,
        logger=logger,
        callbacks=[early_stop_callback],
    )

    # Train the model
    trainer.fit(model, datamodule)

    # Save the model

    trainer.save_checkpoint(
        f"chess_model_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.ckpt"
    )

    # Validate the model
    trainer.validate()

    # Test the model
    trainer.test()


if __name__ == "__main__":
    main()
