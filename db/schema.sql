CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY,
  total_stock INT NOT NULL CHECK (total_stock >= 0),
  available_stock INT NOT NULL CHECK (available_stock >= 0),
  reserved_count INT NOT NULL CHECK (reserved_count >= 0)
);
