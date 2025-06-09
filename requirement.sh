#!/bin/bash

echo "🔧 Checking system dependencies..."

# Install ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Installing ffmpeg..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo "⚠️ Please install ffmpeg manually"
    fi
else
    echo "✅ ffmpeg already installed."
fi

# i create a virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📄 Creating dependencies.txt..."
cat <<EOF > dependencies.txt
fastapi
uvicorn[standard]
python-multipart
srt
vosk
EOF

# install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r dependencies.txt

echo "✅ All set! To run the API:"
echo "source venv/bin/activate && uvicorn your_script_name:app --reload"
