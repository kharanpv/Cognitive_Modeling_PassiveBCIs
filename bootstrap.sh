#!/usr/bin/env bash

set -e

echo "🧪 Bootstrapping environment..."

# -------- OS Detection --------
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

# -------- 1. Check Python --------
PYTHON_BIN="$(command -v python3 || true)"
PYTHON_VERSION="$($PYTHON_BIN --version 2>/dev/null | cut -d' ' -f2 || echo "0.0.0")"

version_ge() {
    printf '%s\n%s\n' "$1" "$2" | sort -V -C
}

if [[ -z "$PYTHON_BIN" || ! $(version_ge "$PYTHON_VERSION" "3.11") ]]; then
    echo "🐍 Installing Python 3.11+..."
    if [[ "$OS" == "linux" ]]; then
        sudo apt update && sudo apt install -y python3.11 python3.11-venv python3.11-dev
    elif [[ "$OS" == "mac" ]]; then
        brew install python@3.11
    fi
else
    echo "✅ Python $PYTHON_VERSION is already installed."
fi

PYTHON_BIN=$(command -v python3.11 || command -v python3)

# -------- 2. Check Poetry --------
if ! command -v poetry &> /dev/null; then
    echo "🎼 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | "$PYTHON_BIN" -
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✅ Poetry is already installed."
fi

# -------- 3. Check FFmpeg --------
if ! command -v ffmpeg &> /dev/null; then
    echo "🎞️ Installing FFmpeg..."
    if [[ "$OS" == "linux" ]]; then
        sudo apt install -y ffmpeg
    elif [[ "$OS" == "mac" ]]; then
        brew install ffmpeg
    fi
else
    echo "✅ FFmpeg is already installed."
fi

# -------- 4. Poetry Install --------
echo "📦 Installing Python dependencies with Poetry..."
poetry install

# -------- 5. OpenFace Install --------
OPENFACE_DIR="external/OpenFace"
FEATURE_EXE="$OPENFACE_DIR/build/bin/FeatureExtraction"

if [[ -f "$FEATURE_EXE" ]]; then
    echo "✅ OpenFace already built."
else
    echo "🧠 Installing OpenFace..."

    mkdir -p external
    git clone https://github.com/TadasBaltrusaitis/OpenFace.git "$OPENFACE_DIR"

    echo "📦 Installing OpenFace dependencies..."
    if [[ "$OS" == "linux" ]]; then
        sudo apt install -y cmake g++ libopencv-dev libboost-all-dev libtbb-dev
    elif [[ "$OS" == "mac" ]]; then
        brew install cmake boost tbb opencv
    fi

    echo "📥 Downloading models..."
    pushd "$OPENFACE_DIR"
    bash download_models.sh

    echo "🔧 Building OpenFace..."
    mkdir -p build
    cd build
    cmake ..  # Use root-level CMakeLists.txt
    make -j$(nproc || sysctl -n hw.ncpu)

    popd
fi

echo "✅ All setup complete!"
