package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/rsmrtk/geo-mlops/internal/geocoder"
)

func main() {
	nominatimURL := envOrDefault("NOMINATIM_URL", "https://nominatim.openstreetmap.org")
	mlURL := envOrDefault("ML_SVC_URL", "http://ml-svc:5001")
	addr := envOrDefault("ADDR", ":8080")

	g := geocoder.New(nominatimURL, mlURL)

	mux := http.NewServeMux()
	mux.HandleFunc("/geocode", handleGeocode(g))
	mux.HandleFunc("/health", handleHealth)

	log.Printf("server listening on %s", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatal(err)
	}
}

func handleGeocode(g *geocoder.Geocoder) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		q := r.URL.Query()
		lat, lng, err := geocoder.ParseLatLng(q.Get("lat"), q.Get("lng"))
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		loc, err := g.Lookup(r.Context(), lat, lng)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(loc)
	}
}

func handleHealth(w http.ResponseWriter, _ *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"ok"}`))
}

func envOrDefault(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

