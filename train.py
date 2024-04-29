import sqlite3
import time

import pandas as pd
import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset


# Step 2: Define a PyTorch Lightning Dataset class
class ChessDataset(Dataset):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM games")
        self.length = self.cursor.fetchone()[0]

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        query = "SELECT * FROM games LIMIT 1 OFFSET ?"
        self.cursor.execute(query, (idx,))
        game = self.cursor.fetchone()

        # Preprocess the game data
        game_data = {
            "white_elo": game[10],
            "black_elo": game[11],
            "white_rating_diff": game[12],
            "black_rating_diff": game[13],
        }

        # Convert the game data to a PyTorch tensor
        game_tensor = torch.tensor(list(game_data.values()), dtype=torch.float32)

        return game_tensor


class ChessDataModule(pl.LightningDataModule):
    def __init__(self, db_path, batch_size):
        super().__init__()
        self.db_path = db_path
        self.batch_size = batch_size

    def setup(self, stage=None):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)

        # Fetch all data from the 'games' table
        query = "SELECT * FROM games;"
        data = pd.read_sql_query(query, conn)

        # Split the data into training, validation, and testing sets
        train_data, temp_data = train_test_split(data, test_size=0.4, random_state=42)
        val_data, test_data = train_test_split(
            temp_data, test_size=0.5, random_state=42
        )

        # Create datasets from the dataframes
        self.train_dataset = ChessDataset(train_data)
        self.val_dataset = ChessDataset(val_data)
        self.test_dataset = ChessDataset(test_data)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size)


# Step 4: Define a PyTorch Lightning Module class
class ChessModel(pl.LightningModule):
    # ...
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("train_loss", loss)

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("val_loss", loss)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log("test_loss", loss)


def main():
    # Initialize the DataModule and Model
    datamodule = ChessDataModule("chess_games.db", batch_size=128)
    model = ChessModel()

    # Initialize the TensorBoard logger
    logger = TensorBoardLogger("tb_logs", name="chess_ai")

    # Initialize the early stopping callback
    early_stop_callback = EarlyStopping(
        monitor="val_loss", min_delta=0.00, patience=3, verbose=False, mode="min"
    )

    # Initialize the Trainer with the logger and the early stopping callback
    trainer = pl.Trainer(max_epochs=10, logger=logger, callbacks=[early_stop_callback])

    # Train the model
    trainer.fit(model, datamodule)

    # Save the model

    trainer.save_checkpoint(f"chess_model_{time}.ckpt")

    # Validate the model
    trainer.validate()

    # Test the model
    trainer.test()


if __name__ == "__main__":
    main()
