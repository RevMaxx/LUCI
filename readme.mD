## LUCI 

The first AI-based medical agent designed to automate all medical processes.

## Installation

```bash
pip install LuciAI
```

## Usage

```python
from Luci.Agents import Search

query = "Revmaxx LLC"
search_instance = Search(query)

results = search_instance.search_text(max_results=5)
search_instance.print_text_result(results)
```

## Contributing

We welcome contributions to LuciAI! If you're interested in improving the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Create a pull request.

## License

[![License: RevMaxx LLC Software License](https://img.shields.io/badge/license-RevMaxx%20LLC-blue.svg)](LICENSE)


