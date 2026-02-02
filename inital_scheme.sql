-- Brands
CREATE TABLE brands (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- drinks table
CREATE TABLE drinks (
  id SERIAL PRIMARY KEY,
  brand_id INT REFERENCES brands(id) ON DELETE RESTRICT,
  flavour VARCHAR(100) NOT NULL,
  size_ml INT NOT NULL,
  caffeine_mg INT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
-- calculate caffeine per 100ml
  caffeine_per_100ml DECIMAL(5,2) GENERATED ALWAYS AS 
    ((caffeine_mg::DECIMAL / size_ml) * 100) STORED,
  
  UNIQUE(brand_id, flavour, size_ml)
);

-- new version of transactions table now called consumptions
CREATE TABLE consumptions (
  id SERIAL PRIMARY KEY,
  drink_id INT REFERENCES drinks(id) ON DELETE RESTRICT,
  consumed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  price_paid DECIMAL(6,2),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- indexes for performance
CREATE INDEX idx_consumptions_drink ON consumptions(drink_id);
CREATE INDEX idx_consumptions_date ON consumptions(consumed_at DESC);

-- seeding initial brands
INSERT INTO brands (name) VALUES ('Red Bull'), ('Monster'), ('Purdeys');