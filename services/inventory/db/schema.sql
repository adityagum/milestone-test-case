-- ===============================
-- INVENTORY EVENTS (SOURCE OF TRUTH)
-- ===============================
CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,

  total_stock INT NOT NULL
    CHECK (total_stock >= 0),

  available_stock INT NOT NULL
    CHECK (available_stock >= 0),

  reserved_count INT NOT NULL
    CHECK (reserved_count >= 0)
);

-- ===============================
-- PROCESSED EVENTS (IDEMPOTENCY)
-- ===============================
CREATE TABLE IF NOT EXISTS processed_events (
  order_id TEXT PRIMARY KEY,
  processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ===============================
-- OPTIONAL INDEX (PERFORMANCE)
-- ===============================
CREATE INDEX IF NOT EXISTS idx_events_available
  ON events (event_id)
  WHERE available_stock > 0;
