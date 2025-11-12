#!/bin/bash
# ProbeGenerator Launcher for Mac

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the web_streamlit directory
cd "$DIR/web_streamlit"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit is not installed. Installing required packages..."
    pip install -r requirements.txt
fi

# Launch Streamlit
echo "Starting ProbeGenerator..."
echo "The app will open in your browser automatically"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --browser.gatherUsageStats false

# Keep terminal open if there's an error
read -p "Press Enter to exit..."
