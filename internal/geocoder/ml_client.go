package geocoder

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type MLClient struct {
	baseURL string
	http    *http.Client
}

func NewMLClient(baseURL string) *MLClient {
	return &MLClient{
		baseURL: baseURL,
		http:    &http.Client{Timeout: 3 * time.Second},
	}
}

type classifyRequest struct {
	Lat float64 `json:"lat"`
	Lng float64 `json:"lng"`
}

type classifyResponse struct {
	LocationType string  `json:"location_type"`
	Confidence   float64 `json:"confidence"`
}

func (c *MLClient) Classify(ctx context.Context, lat, lng float64) (locType string, confidence float64, err error) {
	body, _ := json.Marshal(classifyRequest{Lat: lat, Lng: lng})

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.baseURL+"/classify", bytes.NewReader(body))
	if err != nil {
		return "", 0, err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.http.Do(req)
	if err != nil {
		return "", 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", 0, fmt.Errorf("ml-svc returned %d", resp.StatusCode)
	}

	var result classifyResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", 0, err
	}

	return result.LocationType, result.Confidence, nil
}
