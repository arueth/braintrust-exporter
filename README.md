# braintrust-exporter

## Prerequisites

- Braintrust API Key
- Python 3.10+
- `uv`

  ```shell
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## Setup

- Clone the repository.

  ```shell
  git clone https://github.com/arueth/braintrust-exporter
  cd braintrust-exporter
  ```

- Change directory to the `src` folder.

  ```shell
  cd src
  ```

- Create a virtual environment.

  ```shell
  uv venv
  ```

- Activate the virtual environment.

  ```shell
  source .venv/bin/activate
  ```

- Install the required packages.

  ```shell
  uv pip install -r requirements.txt
  ```

## Run the exporter

- Set the environment variables.

  ```shell
  export BRAINTRUST_API_KEY=<your-api-key>
  export OUTPUT_DIR=<path-to-output-directory>
  export PROJECT_NAME=<braintrust-project-name>
  ```

- Run the `braintrust_exporter.py` script

  ```shell
  ./braintrust_exporter.py
  ```

- Deactivate the virtual environment.

  ```shell
  deactivate
  ```
