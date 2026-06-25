package geocoder

import (
	"fmt"

	"github.com/golang/geo/s2"
)

const defaultS2Level = 14

// S2CellFromLatLng returns the S2 cell token and level for the given coordinates.
func S2CellFromLatLng(lat, lng float64) (cellID string, level int) {
	ll := s2.LatLngFromDegrees(lat, lng)
	cell := s2.CellIDFromLatLng(ll).Parent(defaultS2Level)
	return fmt.Sprintf("%x", uint64(cell)), defaultS2Level
}
