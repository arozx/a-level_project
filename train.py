import gc
import multiprocessing
import os
import shutil
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
from torch.utils.tensorboard import SummaryWriter


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

        # Convert the game result to a numerical value
        result = game["result"]
        if result == "1-0":
            y_value = 1.0
        elif result == "0-1":
            y_value = 0.0
        else:  # "1/2-1/2"
            y_value = 0.5

        y = torch.tensor(y_value, dtype=torch.float32)  # Ensure y is a tensor
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
        # * number of CPU cores available
        self.num_workers = multiprocessing.cpu_count() - 1

    def setup(self, stage=None):
        assert os.path.exists(
            self.db_path
        ), f"Database file not found at {os.path.abspath(self.db_path)}"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        assert ("games",) in tables, "Table 'games' not found in the database"
        assert ("moves",) in tables, "Table 'moves' not found in the database"

        cursor.execute("SELECT COUNT(*) FROM games")
        rows = cursor.fetchone()
        print(f"Number of rows in 'games' table: {rows[0]:,}")
        assert rows[0] > 0, "No data found in 'games' table"

        cursor.execute("SELECT COUNT(*) FROM moves")
        rows = cursor.fetchone()
        print(f"Number of rows in 'moves' table: {rows[0]:,}")
        assert rows[0] > 0, "No data found in 'moves' table"

        data = pd.read_sql_query("SELECT * FROM games", conn)
        print(f"Number of rows in 'data' DataFrame: {len(data):,}")
        assert len(data) > 0, "No data loaded into DataFrame"

        train_data, temp_data = train_test_split(data, test_size=0.4, random_state=42)
        val_data, test_data = train_test_split(
            temp_data, test_size=0.5, random_state=42
        )
        assert (
            len(train_data) > 0 and len(val_data) > 0 and len(test_data) > 0
        ), "Data splitting failed"

        moves_data = pd.read_sql_query("SELECT * FROM moves", conn)

        self.train_dataset = ChessDataset(train_data, moves_data)
        self.val_dataset = ChessDataset(val_data, moves_data)
        self.test_dataset = ChessDataset(test_data, moves_data)
        assert (
            len(self.train_dataset) > 0
            and len(self.val_dataset) > 0
            and len(self.test_dataset) > 0
        ), "Dataset creation failed"

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, num_workers=7)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=7)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=7)


class ChessModel(pl.LightningModule):
    def __init__(self):
        super(ChessModel, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(
            in_channels=13, out_channels=64, kernel_size=3, stride=1, padding=1
        )
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        # Fully connected layers
        self.fc1 = nn.Linear(256 * 8 * 8, 2048)
        self.fc2 = nn.Linear(2048, 512)
        self.fc3 = nn.Linear(512, 1)  # Output layer

    def forward(self, x):
        x = x.view(
            -1, 13, 8, 8
        )  # Reshape from (batch_size, 832) to (batch_size, 13, 8, 8)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # Flatten the tensor
        x = x.view(-1, 256 * 8 * 8)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)  # No activation function
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        y = y.view(y_hat.shape)  # Add this line to reshape y
        loss = F.mse_loss(y_hat, y)  # Use MSE loss for regression
        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )

    def validation_step(self, batch, batch_idx):
        x, y = batch  # Unpack the batch into input and target tensors
        x = x.view(x.size(0), -1)  # Flatten the input tensor
        y_hat = self(x)  # Pass the input tensor through the model
        loss = F.mse_loss(y_hat, y)  # Use MSE loss for regression
        self.log(
            "val_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )  # Log the loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)  # Use MSE loss for regression
        self.log(
            "test_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


def main():
    # Initialize the DataModule and Model
    datamodule = ChessDataModule(
        "/home/user/repos/a-level_project/chess_games.db", batch_size=4096
    )
    model = ChessModel()

    # remove old logs
    if os.path.exists("tb_logs/chess_ai"):
        print("removing old logs...")
        shutil.rmtree("tb_logs/chess_ai")

    # create the directory for the TensorBoard logs
    os.makedirs("tb_logs/chess_ai")

    # Initialize the TensorBoard logger
    logger = TensorBoardLogger("tb_logs", name="chess_ai")

    # Initialize the early stopping callback
    early_stop_callback = EarlyStopping(
        monitor="val_loss", min_delta=0.00, patience=3, verbose=False, mode="min"
    )

    # Initialize the Trainer with the logger and the early stopping callback
    trainer = pl.Trainer(
        max_epochs=10,
        logger=logger,
        callbacks=[early_stop_callback],
        log_every_n_steps=10,
    )

    # Train the model
    trainer.fit(model, datamodule)

    # Save the model
    trainer.save_checkpoint(
        f"checkpoints/chess_model_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.ckpt"
    )

    # Validate the model
    trainer.validate()

    # Test the model
    trainer.test()

    # Initialize the TensorBoard writer and add the model graph
    writer = SummaryWriter(log_dir="tb_logs/chess_ai")
    x, _ = next(iter(datamodule.train_dataloader()))
    writer.add_graph(model, x)

    # Get a batch of data
    x, y = next(iter(datamodule.train_dataloader()))

    # Forward pass through the model
    y_pred = model(x)

    # Compute the loss
    loss = F.cross_entropy(y_pred, y)

    # Compute the accuracy
    accuracy = (y_pred.argmax(dim=1) == y).float().mean()

    # Log the loss and accuracy
    writer.add_scalar("Loss/train", loss, global_step=470)
    writer.add_scalar("Accuracy/train", accuracy, global_step=470)

    # Log the gradients and model parameters
    for name, param in model.named_parameters():
        writer.add_histogram(f"{name}/grad", param.grad, global_step=470)
        writer.add_histogram(f"{name}/param", param, global_step=470)

    # Delete unnecessary variables
    del x, y, y_pred, loss, accuracy

    # Force garbage collection
    gc.collect()


if __name__ == "__main__":
    main()
