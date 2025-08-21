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

if [[ -z "$PYTHON_BIN" || ! $(version_ge "$PYTHON_VERSION" "3.12") ]]; then
    echo "🐍 Installing Python 3.12+..."
    if [[ "$OS" == "linux" ]]; then
        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update
        sudo apt install -y python3.12 python3.12-venv python3.12-dev
        
        # Configure python3 to point to python3.12
        echo "🔧 Configuring python3 to use Python 3.12..."
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
        sudo update-alternatives --set python3 /usr/bin/python3.12
        
    elif [[ "$OS" == "mac" ]]; then
        brew install python@3.12
        
        # Configure python3 to point to python3.12
        echo "🔧 Configuring python3 to use Python 3.12..."
        # Create symlink or add to PATH
        if [[ -f "/opt/homebrew/bin/python3.12" ]]; then
            # Apple Silicon Mac
            sudo ln -sf /opt/homebrew/bin/python3.12 /usr/local/bin/python3
        elif [[ -f "/usr/local/bin/python3.12" ]]; then
            # Intel Mac
            sudo ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3
        fi
    fi
else
    echo "✅ Python $PYTHON_VERSION is already installed."
fi


PYTHON_BIN=$(command -v python3.12 || command -v python3)

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

    # -------- macOS-specific dependencies --------
    if [[ "$OS" == "mac" ]]; then
        # Check for wget
        if ! command -v wget &> /dev/null; then
            echo "📥 Installing wget for macOS..."
            brew install wget
        else
            echo "✅ wget is already installed."
        fi

        # Check for dlib
        if ! python3 -c "import dlib" &> /dev/null; then
            echo "🔧 Installing dlib for macOS..."
            brew install dlib
        else
            echo "✅ dlib is already installed."
        fi
    fi

    mkdir -p external
    git clone https://github.com/TadasBaltrusaitis/OpenFace.git "$OPENFACE_DIR"

    echo "📦 Installing OpenFace dependencies..."
    if [[ "$OS" == "linux" ]]; then
        # Check and install core build tools
        if ! command -v cmake &> /dev/null; then
            echo "🔨 Installing cmake..."
            sudo apt install -y cmake
        else
            echo "✅ cmake is already installed."
        fi

        if ! dpkg -l | grep -q "build-essential"; then
            echo "🔨 Installing build-essential..."
            sudo apt install -y build-essential
        else
            echo "✅ build-essential is already installed."
        fi

        # Check and install GCC-8
        if ! command -v gcc-8 &> /dev/null; then
            echo "🔨 Installing GCC-8..."
            # Try package manager first
            if ! sudo apt install -y gcc-8 g++-8 2>/dev/null; then
                echo "📥 GCC-8 not available in repos, installing manually..."
                # Download GCC-8 packages manually
                wget http://mirrors.kernel.org/ubuntu/pool/universe/g/gcc-8/gcc-8_8.4.0-3ubuntu2_amd64.deb
                wget http://mirrors.edge.kernel.org/ubuntu/pool/universe/g/gcc-8/gcc-8-base_8.4.0-3ubuntu2_amd64.deb
                wget http://mirrors.kernel.org/ubuntu/pool/universe/g/gcc-8/libgcc-8-dev_8.4.0-3ubuntu2_amd64.deb
                wget http://mirrors.kernel.org/ubuntu/pool/universe/g/gcc-8/cpp-8_8.4.0-3ubuntu2_amd64.deb
                wget http://mirrors.kernel.org/ubuntu/pool/universe/g/gcc-8/libmpx2_8.4.0-3ubuntu2_amd64.deb
                wget http://mirrors.kernel.org/ubuntu/pool/main/i/isl/libisl22_0.22.1-1_amd64.deb
                sudo apt install -y ./libisl22_0.22.1-1_amd64.deb ./libmpx2_8.4.0-3ubuntu2_amd64.deb ./cpp-8_8.4.0-3ubuntu2_amd64.deb ./libgcc-8-dev_8.4.0-3ubuntu2_amd64.deb ./gcc-8-base_8.4.0-3ubuntu2_amd64.deb ./gcc-8_8.4.0-3ubuntu2_amd64.deb
                # Clean up downloaded packages
                rm -f *.deb
            fi
        else
            echo "✅ GCC-8 is already installed."
        fi

        # Check and install OpenCV
        if ! pkg-config --exists opencv4 2>/dev/null && ! pkg-config --exists opencv 2>/dev/null; then
            echo "📹 Installing OpenCV..."
            sudo apt install -y libopencv-dev libopencv-contrib-dev
        else
            echo "✅ OpenCV is already installed."
        fi

        # Check and install Boost
        if ! dpkg -l | grep -q "libboost-all-dev"; then
            echo "🚀 Installing Boost libraries..."
            sudo apt install -y libboost-all-dev libboost-filesystem-dev libboost-system-dev
        else
            echo "✅ Boost libraries are already installed."
        fi

        # Check and install OpenBLAS
        if ! dpkg -l | grep -q "libopenblas-dev"; then
            echo "🧮 Installing OpenBLAS..."
            sudo apt install -y libopenblas-dev liblapack-dev libblas-dev
        else
            echo "✅ OpenBLAS is already installed."
        fi

        # Check and install dlib (minimum 19.13)
        DLIB_VERSION=""
        if dpkg -l | grep -q "libdlib-dev"; then
            # Try to get dlib version from pkg-config or dpkg
            DLIB_VERSION=$(dpkg -l | grep libdlib-dev | awk '{print $3}' | cut -d'-' -f1 2>/dev/null || echo "0.0.0")
        fi
        
        if [[ -z "$DLIB_VERSION" || ! $(version_ge "$DLIB_VERSION" "19.13") ]]; then
            echo "🤖 Installing dlib (minimum version 19.13)..."
            sudo apt install -y libdlib-dev
        else
            echo "✅ dlib version $DLIB_VERSION is already installed."
        fi

        # Check and install TBB
        if ! dpkg -l | grep -q "libtbb-dev"; then
            echo "🧵 Installing Threading Building Blocks..."
            sudo apt install -y libtbb-dev
        else
            echo "✅ TBB is already installed."
        fi

        # Check and install pkg-config
        if ! command -v pkg-config &> /dev/null; then
            echo "⚙️ Installing pkg-config..."
            sudo apt install -y pkg-config
        else
            echo "✅ pkg-config is already installed."
        fi

    elif [[ "$OS" == "mac" ]]; then
        # Check and install cmake
        if ! command -v cmake &> /dev/null; then
            echo "🔨 Installing cmake..."
            brew install cmake
        else
            echo "✅ cmake is already installed."
        fi

        # Check and install GCC
        if ! command -v gcc-11 &> /dev/null && ! command -v gcc-12 &> /dev/null; then
            echo "🔨 Installing GCC..."
            brew install gcc
        else
            echo "✅ GCC is already installed."
        fi

        # Check and install OpenCV
        if ! brew list opencv &> /dev/null; then
            echo "📹 Installing OpenCV..."
            brew install opencv
        else
            echo "✅ OpenCV is already installed."
        fi

        # Check and install Boost
        if ! brew list boost &> /dev/null; then
            echo "🚀 Installing Boost..."
            brew install boost
        else
            echo "✅ Boost is already installed."
        fi

        # Check and install OpenBLAS
        if ! brew list openblas &> /dev/null; then
            echo "🧮 Installing OpenBLAS..."
            brew install openblas lapack
        else
            echo "✅ OpenBLAS is already installed."
        fi

        # Check and install dlib (minimum 19.13)
        DLIB_VERSION=""
        if brew list dlib &> /dev/null; then
            # Get dlib version from brew
            DLIB_VERSION=$(brew list --versions dlib 2>/dev/null | awk '{print $2}' || echo "0.0.0")
        fi
        
        if [[ -z "$DLIB_VERSION" || ! $(version_ge "$DLIB_VERSION" "19.13") ]]; then
            echo "🤖 Installing dlib (minimum version 19.13)..."
            if brew list dlib &> /dev/null; then
                brew upgrade dlib
            else
                brew install dlib
            fi
        else
            echo "✅ dlib version $DLIB_VERSION is already installed."
        fi

        # Check and install TBB
        if ! brew list tbb &> /dev/null; then
            echo "🧵 Installing TBB..."
            brew install tbb
        else
            echo "✅ TBB is already installed."
        fi

        # Check and install pkg-config
        if ! command -v pkg-config &> /dev/null; then
            echo "⚙️ Installing pkg-config..."
            brew install pkg-config
        else
            echo "✅ pkg-config is already installed."
        fi
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
