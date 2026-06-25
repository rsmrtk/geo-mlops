package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/rsmrtk/geo-mlops/internal/geocoder"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintf(os.Stderr, "usage: geocoder <lat> <lng>\n")
		os.Exit(1)
	}

	lat, lng, err := geocoder.ParseLatLng(os.Args[1], os.Args[2])
	if err != nil {
		log.Fatal(err)
	}

	nominatimURL := envOrDefault("NOMINATIM_URL", "https://nominatim.openstreetmap.org")
	mlURL := envOrDefault("ML_SVC_URL", "http://localhost:5001")

	g := geocoder.New(nominatimURL, mlURL)

	loc, err := g.Lookup(context.Background(), lat, lng)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Address:  %s\n", loc.Address)
	fmt.Printf("S2 Cell:  %s (level %d)\n", loc.S2CellID, loc.S2Level)
	fmt.Printf("Type:     %s (confidence: %.2f)\n", loc.LocationType, loc.Confidence)
	fmt.Printf("Latency:  %dms\n", loc.LatencyMS)
}

func envOrDefault(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}
