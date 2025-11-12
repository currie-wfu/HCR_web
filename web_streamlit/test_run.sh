#!/bin/bash
echo "Installing Streamlit..."
pip install streamlit pandas -q

echo ""
echo "Starting ProbeGenerator Web Interface..."
echo "Your browser will open automatically!"
echo ""
streamlit run app.py
