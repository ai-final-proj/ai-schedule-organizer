#!/bin/bash
# Bootstrap the Flask + Angular app for local (non-Docker) development.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${ROOT_DIR}/.venv"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "error: ${PYTHON_BIN} not found on PATH. Set PYTHON_BIN to your python3 executable." >&2
  exit 1
fi

echo "==> Ensuring virtual environment exists at ${VENV_DIR}"
if [ ! -d "${VENV_DIR}" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

echo "==> Activating virtual environment"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "==> Upgrading pip"
pip install --upgrade pip >/dev/null

echo "==> Installing backend requirements"
pip install -r "${ROOT_DIR}/requirements.txt"

echo "==> Installing frontend dependencies"
pushd "${ROOT_DIR}/frontend" >/dev/null
npm install

echo "==> Building Angular frontend (production configuration)"
npm run build
popd >/dev/null

cat <<'EOF'

Local setup complete.

To run the backend:
  source .venv/bin/activate
  export DATABASE_URL="postgresql+psycopg://user:pass@host:5432/db"
  export SECRET_KEY="dev"
  export PORT=7860
  flask --app app run --debug --port "${PORT}"

Frontend assets are already built into frontend/dist; Flask will serve them automatically.

EOF
