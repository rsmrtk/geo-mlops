package geocoder

import (
	"context"
	"errors"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

const schema = `
CREATE TABLE IF NOT EXISTS geocache (
	s2_cell_id    TEXT PRIMARY KEY,
	address       TEXT NOT NULL,
	location_type TEXT NOT NULL,
	confidence    REAL NOT NULL,
	fetched_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);`

// Cache is a Postgres-backed geocode result store keyed by S2 cell ID.
type Cache struct {
	pool *pgxpool.Pool
}

func NewCache(ctx context.Context, databaseURL string) (*Cache, error) {
	pool, err := pgxpool.New(ctx, databaseURL)
	if err != nil {
		return nil, err
	}
	if _, err := pool.Exec(ctx, schema); err != nil {
		pool.Close()
		return nil, err
	}
	return &Cache{pool: pool}, nil
}

func (c *Cache) Close() {
	c.pool.Close()
}

func (c *Cache) Get(ctx context.Context, cellID string) (*Location, error) {
	var loc Location
	err := c.pool.QueryRow(ctx,
		`SELECT address, location_type, confidence FROM geocache WHERE s2_cell_id = $1`,
		cellID,
	).Scan(&loc.Address, &loc.LocationType, &loc.Confidence)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	loc.S2CellID = cellID
	return &loc, nil
}

func (c *Cache) Set(ctx context.Context, cellID string, loc *Location) error {
	_, err := c.pool.Exec(ctx,
		`INSERT INTO geocache (s2_cell_id, address, location_type, confidence, fetched_at)
		 VALUES ($1, $2, $3, $4, $5)
		 ON CONFLICT (s2_cell_id) DO UPDATE
		   SET address = EXCLUDED.address,
		       location_type = EXCLUDED.location_type,
		       confidence = EXCLUDED.confidence,
		       fetched_at = EXCLUDED.fetched_at`,
		cellID, loc.Address, loc.LocationType, loc.Confidence, time.Now(),
	)
	return err
}
