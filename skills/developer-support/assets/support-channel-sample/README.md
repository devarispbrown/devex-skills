# Widget SDK

The Widget SDK renders interactive widgets in any JavaScript application.

## Install

```bash
npm install widget-sdk
```

## Quickstart

```js
import { Widget } from "widget-sdk";

const widget = new Widget({ apiKey: process.env.WIDGET_API_KEY });
widget.render("#app");
```

## Usage

See the docs/ directory for the API reference, configuration guide, and examples.

## Development

Clone the repository and run `npm test` to run the test suite.

## Contributing

See CONTRIBUTING.md for contribution guidelines.

## License

MIT
