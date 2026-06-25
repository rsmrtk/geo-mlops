package geocoder

import (
	"context"
	"fmt"
	"time"
)

// Location is the result of a geocode lookup.
type Location struct {
	Lat          float64 `json:"lat"`
	Lng          float64 `json:"lng"`
	Address      string  `json:"address"`
	S2CellID     string  `json:"s2_cell_id"`
	S2Level      int     `json:"s2_level"`
	LocationType string  `json:"location_type"`
	Confidence   float64 `json:"confidence"`
	LatencyMS    int64   `json:"latency_ms"`
}

// Geocoder resolves coordinates to a full Location.
type Geocoder struct {
	nominatim *NominatimClient
	mlClient  *MLClient
}

func New(nominatimURL, mlURL string) *Geocoder {
	return &Geocoder{
		nominatim: NewNominatimClient(nominatimURL),
		mlClient:  NewMLClient(mlURL),
	}
}

func (g *Geocoder) Lookup(ctx context.Context, lat, lng float64) (*Location, error) {
	start := time.Now()

	cellID, level := S2CellFromLatLng(lat, lng)

	address, err := g.nominatim.ReverseGeocode(ctx, lat, lng)
	if err != nil {
		return nil, fmt.Errorf("nominatim: %w", err)
	}

	locType, confidence, err := g.mlClient.Classify(ctx, lat, lng)
	if err != nil {
		// ML failure is non-fatal — return result without classification
		locType = "unknown"
		confidence = 0
	}

	return &Location{
		Lat:          lat,
		Lng:          lng,
		Address:      address,
		S2CellID:     cellID,
		S2Level:      level,
		LocationType: locType,
		Confidence:   confidence,
		LatencyMS:    time.Since(start).Milliseconds(),
	}, nil
}
