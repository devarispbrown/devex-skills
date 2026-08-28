// Minimal fixture client for the Widgets API (subset only).
export interface Widget {
  id: string;
  name: string;
}
export class WidgetsClient {
  constructor(private readonly baseUrl: string, private readonly apiKey: string) {}
  async listWidgets(): Promise<Widget[]> {
    return [{ id: "w-1", name: "alpha" }];
  }
  async getWidget(id: string): Promise<Widget> {
    return { id, name: "alpha" };
  }
}
