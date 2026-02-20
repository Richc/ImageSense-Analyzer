# 🖼️ ImageSense Analyzer - Installation & Setup Guide

**Version:** 1.0.0  
**Date:** 20 February 2026

---

## 📋 What This Application Does

ImageSense Analyzer is a drag-and-drop desktop tool that:

✅ Analyzes images using OpenAI GPT Vision  
✅ Extracts detailed information (objects, colors, mood, people, etc.)  
✅ Saves results to a structured CSV file  
✅ Works with multiple images at once  
✅ Provides cost tracking  
✅ Ready for Excel/Google Sheets  

---

## 🎯 Prerequisites

### 1. Python 3.9 or Higher

**Check your Python version:**
```bash
python3 --version
```

**If you don't have Python or need to upgrade:**
- **Mac**: Install from [python.org](https://www.python.org/downloads/) or use Homebrew: `brew install python3`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### 2. OpenAI API Key

You need an OpenAI API key with access to GPT-4 Vision models.

**Get your API key:**
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new key
5. Copy it (you'll need it in step 3)

---

## 🚀 Installation Steps

### Step 1: Download the Application Files

You should have these files:
```
image_analyzer_app.py     # Main application
requirements.txt          # Dependencies list
INSTALLATION_GUIDE.md     # This file
```

### Step 2: Install Dependencies

Open Terminal (Mac/Linux) or Command Prompt (Windows) and navigate to the folder:

```bash
cd /path/to/PR
```

**Install required packages:**

```bash
pip3 install -r requirements.txt
```

**Or install individually:**

```bash
pip3 install openai pandas pillow tkinterdnd2
```

### Step 3: Set Your OpenAI API Key

**Mac/Linux:**

**Option A - Temporary (current terminal session only):**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Option B - Permanent (add to shell profile):**
```bash
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

For bash users, use `~/.bashrc` instead of `~/.zshrc`

**Windows:**

**Command Prompt:**
```bash
setx OPENAI_API_KEY "sk-your-api-key-here"
```

**PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-your-api-key-here', 'User')
```

**⚠️ Important:** After setting the API key on Windows, restart your terminal/command prompt.

### Step 4: Run the Application

```bash
python3 image_analyzer_app.py
```

---

## 🎮 How to Use

### Basic Workflow

1. **Launch the app** - Run the command above
2. **Drag images** - Drop one or multiple images into the window
3. **Wait for analysis** - Watch the progress in the log window
4. **View results** - Click "📊 Open CSV" button or open `image_analysis_results.csv`

### Supported Image Formats

- ✅ PNG (.png)
- ✅ JPEG (.jpg, .jpeg)
- ✅ WebP (.webp)
- ✅ GIF (.gif)
- ✅ BMP (.bmp)

### Understanding the Output

The CSV file contains these columns:

| Column | Description |
|--------|-------------|
| `filename` | Original image filename |
| `timestamp` | When analysis was performed |
| `summary` | Brief one-sentence description |
| `objects` | Main objects identified |
| `people_count` | Number of people (or 0) |
| `people_description` | What people are doing |
| `colors` | Dominant colors and characteristics |
| `mood` | Overall mood/atmosphere |
| `emotion` | Emotional quality |
| `movement` | Sense of motion or stillness |
| `setting` | Location/environment |
| `lighting` | Lighting characteristics |
| `composition` | Compositional elements |
| `elements_list` | Detailed comma-separated list |
| `full_description` | Comprehensive 2-3 paragraph analysis |
| `cost_estimate` | Cost for this image analysis |

---

## 💰 Cost Information

### Pricing (as of February 2026)

Using **GPT-4o-mini** vision model:
- **~$0.001 - $0.003 per image** (typical)
- Varies based on image complexity and response length

### Cost Tracking

- Real-time cost display in the app
- Per-image cost in CSV
- Cumulative total shown after each batch

### Example Costs

- 10 images: ~$0.02
- 100 images: ~$0.20
- 1,000 images: ~$2.00

**Note:** Always verify current OpenAI pricing at [openai.com/pricing](https://openai.com/pricing)

---

## 🔧 Troubleshooting

### Problem: "openai package not installed"

**Solution:**
```bash
pip3 install openai --upgrade
```

### Problem: "API Key Missing" error

**Solution:** 
1. Make sure you set the `OPENAI_API_KEY` environment variable
2. Restart your terminal after setting it
3. Verify it's set: 
   - Mac/Linux: `echo $OPENAI_API_KEY`
   - Windows: `echo %OPENAI_API_KEY%`

### Problem: "tkinterdnd2" installation fails

**Mac:**
```bash
brew install tcl-tk
pip3 install tkinterdnd2
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
pip3 install tkinterdnd2
```

**Windows:**
- Usually installs fine with pip
- If issues, try: `pip3 install --upgrade tkinterdnd2`

### Problem: Window doesn't accept drops

**Solution:**
- Make sure the image files have proper extensions
- Try dragging from a different application (Finder/Explorer)
- On macOS, you may need to grant Terminal permissions to access files

### Problem: JSON parsing errors

**Solution:**
- This is usually temporary - the app will still save the raw response
- Try analyzing the image again
- Check your API key has vision model access

### Problem: Image format not supported

**Solution:**
- Convert your images to PNG or JPEG
- Use online converters or:
  ```bash
  # Using ImageMagick (install first)
  convert input.tiff output.jpg
  ```

---

## 📊 Opening the CSV File

### In Excel (Windows/Mac)

1. Open Excel
2. File → Open
3. Select `image_analysis_results.csv`
4. Choose "Delimited" → "Comma"

### In Google Sheets

1. Go to sheets.google.com
2. File → Import
3. Upload tab → Select file
4. Import data

### In Numbers (Mac)

1. Open Numbers
2. File → Open
3. Select the CSV file

---

## 🎨 Example Use Cases

### 1. Photo Collection Analysis
Analyze your photo library to:
- Catalog objects and scenes
- Identify mood and atmosphere
- Find specific colors or themes
- Track people in photos

### 2. Art Collection Documentation
Document artwork with:
- Detailed descriptions
- Color analysis
- Compositional notes
- Mood and theme tracking

### 3. Stock Photo Tagging
Generate comprehensive tags for:
- Objects and elements
- Color schemes
- Emotional qualities
- Use case categories

### 4. Research Projects
Analyze images for:
- Historical documentation
- Visual pattern recognition
- Comparative studies
- Data visualization

---

## 🚀 Advanced Features

### Batch Processing Large Collections

For processing hundreds of images efficiently, you can modify the script or run it multiple times with subsets.

**Tips:**
- Process in batches of 50-100 images
- Monitor costs as you go
- Back up your CSV periodically

### Custom Prompts

To customize what information is extracted, edit the `prompt` variable in the code (line ~150):

```python
prompt = """
Your custom prompt here...
Include the fields you want analyzed...
"""
```

### Integration with Other Tools

The CSV output can be imported into:
- Airtable
- Notion databases
- Power BI
- Tableau
- Custom databases

---

## 🐛 Known Limitations

1. **Rate Limits:** OpenAI has rate limits - if processing large batches, you may need to add delays
2. **Image Size:** Very large images may need longer processing time
3. **Network Required:** Requires internet connection for API calls
4. **API Costs:** Each analysis costs money (though minimal)
5. **Accuracy:** AI analysis may not be 100% accurate - always review results

---

## 📝 FAQ

**Q: Can I use this offline?**  
A: No, it requires internet to call OpenAI API.

**Q: Is my data private?**  
A: Images are sent to OpenAI for analysis. Review OpenAI's data policy.

**Q: Can I analyze videos?**  
A: Not directly, but you can extract frames and analyze those.

**Q: What's the maximum image size?**  
A: GPT-4 Vision can handle most reasonable image sizes. Very large files may be automatically resized.

**Q: Can I run this on a server?**  
A: Yes, but you'd need to remove the GUI and create a command-line version.

**Q: Is there a free tier?**  
A: OpenAI offers initial credits for new accounts. Check their website for current offers.

---

## 🆘 Getting Help

### If you encounter issues:

1. **Check the log window** - Error messages often explain the problem
2. **Verify API key** - Most issues are API key related
3. **Check internet connection** - Required for API calls
4. **Review error messages** - They usually point to the solution

### For bugs or feature requests:

Create an issue in the project repository or contact support.

---

## 📄 License & Credits

**ImageSense Analyzer**  
Built for the ImageSense project  
Uses OpenAI GPT-4 Vision API  

---

## ✅ Quick Start Checklist

Before first use, verify:

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] OpenAI API key obtained
- [ ] API key set as environment variable
- [ ] Terminal/Command Prompt restarted (if needed)
- [ ] Application launches without errors
- [ ] Test with 1 image first

---

## 🎉 You're Ready!

Run the application:
```bash
python3 image_analyzer_app.py
```

Drag some images and watch the magic happen! 🚀

---

*Last updated: 20 February 2026*
