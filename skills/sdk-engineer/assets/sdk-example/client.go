package widgets

// Client talks to the Widgets API.
type Client struct{}

// ListWidgets returns all widgets.
func (c *Client) ListWidgets() ([]Widget, error) { return nil, nil }

// GetWidget returns one widget by ID.
func (c *Client) GetWidget(id string) (*Widget, error) { return nil, nil }

type Widget struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}
