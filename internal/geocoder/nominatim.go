package geocoder

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"time"
)

type NominatimClient struct {
	baseURL string
	http    *http.Client
}

func NewNominatimClient(baseURL string) *NominatimClient {
	return &NominatimClient{
		baseURL: baseURL,
		http:    &http.Client{Timeout: 5 * time.Second},
	}
}

type nominatimResponse struct {
	DisplayName string `json:"display_name"`
	Error       string `json:"error"`
}

func (c *NominatimClient) ReverseGeocode(ctx context.Context, lat, lng float64) (string, error) {
	u := fmt.Sprintf("%s/reverse?lat=%f&lon=%f&format=json",
		c.baseURL, lat, lng)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
	if err != nil {
		return "", err
	}
	req.Header.Set("User-Agent", "geo-mlops/1.0")

	resp, err := c.http.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("nominatim returned %d", resp.StatusCode)
	}

	var result nominatimResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}
	if result.Error != "" {
		return "", fmt.Errorf("nominatim error: %s", result.Error)
	}
	if result.DisplayName == "" {
		return "", fmt.Errorf("no address found for %f,%f", lat, lng)
	}

	return result.DisplayName, nil
}

// BaseURL returns the configured Nominatim base URL.
func (c *NominatimClient) BaseURL() string {
	return c.baseURL
}

// ParseLatLng validates latitude and longitude values.
func ParseLatLng(latStr, lngStr string) (float64, float64, error) {
	var lat, lng float64
	if _, err := fmt.Sscanf(latStr, "%f", &lat); err != nil {
		return 0, 0, fmt.Errorf("invalid lat %q", latStr)
	}
	if _, err := fmt.Sscanf(lngStr, "%f", &lng); err != nil {
		return 0, 0, fmt.Errorf("invalid lng %q", lngStr)
	}
	if lat < -90 || lat > 90 {
		return 0, 0, fmt.Errorf("lat %f out of range [-90, 90]", lat)
	}
	if lng < -180 || lng > 180 {
		return 0, 0, fmt.Errorf("lng %f out of range [-180, 180]", lng)
	}
	return lat, lng, nil
}

// NominatimURL builds a validated Nominatim URL from a raw string.
func NominatimURL(raw string) (string, error) {
	u, err := url.ParseRequestURI(raw)
	if err != nil {
		return "", fmt.Errorf("invalid nominatim URL: %w", err)
	}
	return u.String(), nil
}
