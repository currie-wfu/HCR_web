# ProbeGenerator - Streamlit Web Interface

Beautiful, user-friendly web interface for ProbeGenerator.

## Quick Start

### Local Testing

```bash
# Install Streamlit
pip install streamlit pandas

# Run the app
cd web_streamlit
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Deploy to Streamlit Cloud (Free!)

1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Deploy!

**Note:** Streamlit Cloud has limited resources. For large genomes, deploy locally or use a server.

## Features

- ✨ Drag-and-drop file upload
- 📊 Interactive parameter sliders
- 📈 Real-time progress tracking
- 💾 One-click download of results
- 📱 Mobile-friendly
- 🎨 Beautiful, intuitive interface

## Limitations

- Genome index must be accessible from server (can't upload 50GB files)
- 10-minute timeout for processing
- Best for small-medium genomes

## Customization

Edit `app.py` to:
- Change default parameters
- Add more visualization
- Customize branding
- Add authentication

## Alternative: Run on Your Server

```bash
# Install dependencies
pip install streamlit pandas

# Run on custom port
streamlit run app.py --server.port 8080

# Run on all interfaces (accessible from network)
streamlit run app.py --server.address 0.0.0.0
```

Access from any computer on your network!
