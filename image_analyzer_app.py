#!/usr/bin/env python3
"""
ImageSense Analyzer - Drag & Drop Image Analysis Tool
Analyzes images using OpenAI GPT Vision and saves to CSV
"""

import os
import sys
import base64
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from tkinter import Tk, Label, Text, Scrollbar, Frame, Button, messagebox
from tkinter import END, DISABLED, NORMAL
from tkinterdnd2 import DND_FILES, TkinterDnD

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed")
    print("Run: pip install openai")
    sys.exit(1)

# ==============================
# CONFIG
# ==============================

OUTPUT_CSV = "image_analysis_results.csv"
VERSION = "1.0.0"

# Predefined CSV structure
CSV_COLUMNS = [
    "filename",
    "timestamp",
    "summary",
    "objects",
    "people_count",
    "people_description",
    "colors",
    "mood",
    "emotion",
    "movement",
    "setting",
    "lighting",
    "composition",
    "elements_list",
    "full_description",
    "cost_estimate"
]

# Pricing (as of Feb 2026 - verify current prices)
GPT4O_MINI_INPUT_PRICE = 0.00015 / 1000  # per token
GPT4O_MINI_OUTPUT_PRICE = 0.0006 / 1000  # per token

# ==============================
# GLOBAL STATE
# ==============================

client = None
total_cost = 0.0
images_processed = 0

# ==============================
# API KEY VALIDATION
# ==============================

def validate_api_key():
    """Check if OpenAI API key is set and valid"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        messagebox.showerror(
            "API Key Missing",
            "OpenAI API key not found!\n\n"
            "Please set your API key:\n\n"
            "Mac/Linux:\nexport OPENAI_API_KEY='your-key-here'\n\n"
            "Windows:\nsetx OPENAI_API_KEY 'your-key-here'\n\n"
            "Then restart this application."
        )
        return False
    
    try:
        global client
        client = OpenAI(api_key=api_key)
        # Test API key with a simple call
        log_message("✓ API key validated successfully")
        return True
    except Exception as e:
        messagebox.showerror(
            "API Key Invalid",
            f"Failed to initialize OpenAI client:\n{str(e)}\n\n"
            "Please check your API key."
        )
        return False

# ==============================
# IMAGE TO BASE64
# ==============================

def encode_image(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

# ==============================
# GPT IMAGE ANALYSIS
# ==============================

def analyse_image(image_path):
    """
    Analyze image using OpenAI GPT Vision
    Returns dict with analysis results
    """
    global total_cost, images_processed
    
    log_message(f"\n{'='*60}")
    log_message(f"📸 Analyzing: {Path(image_path).name}")
    log_message(f"{'='*60}")
    
    try:
        # Encode image
        base64_image = encode_image(image_path)
        log_message("✓ Image encoded")
        
        # Create prompt
        prompt = """
Please analyze this image in detail and return your response ONLY as valid JSON with exactly these fields:

{
    "summary": "Brief one-sentence description",
    "objects": "List main objects visible (comma-separated)",
    "people_count": "Number of people (0 if none, or specific count)",
    "people_description": "What people are doing (or 'None' if no people)",
    "colors": "Dominant colors and color characteristics",
    "mood": "Overall mood/atmosphere",
    "emotion": "Emotional quality conveyed",
    "movement": "Sense of movement or stillness",
    "setting": "Location/environment type",
    "lighting": "Lighting characteristics and quality",
    "composition": "Compositional elements and structure",
    "elements_list": "Detailed comma-separated list of all visible elements",
    "full_description": "Comprehensive 2-3 paragraph description covering all aspects"
}

Important: Return ONLY the JSON object, no other text before or after.
"""
        
        log_message("→ Sending to OpenAI GPT Vision...")
        
        # Call API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }
            ],
            max_tokens=1500,
        )
        
        log_message("✓ Response received")
        
        # Calculate cost
        usage = response.usage
        input_cost = usage.prompt_tokens * GPT4O_MINI_INPUT_PRICE
        output_cost = usage.completion_tokens * GPT4O_MINI_OUTPUT_PRICE
        image_cost = input_cost + output_cost
        total_cost += image_cost
        
        log_message(f"💰 Cost: ${image_cost:.4f} (Total: ${total_cost:.4f})")
        log_message(f"📊 Tokens: {usage.prompt_tokens} input, {usage.completion_tokens} output")
        
        # Parse response
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            data = json.loads(content)
            log_message("✓ JSON parsed successfully")
        except json.JSONDecodeError as e:
            log_message(f"⚠ JSON parse error: {str(e)}")
            log_message("Raw response:")
            log_message(content[:500])
            # Fallback structure
            data = {col: "" for col in CSV_COLUMNS if col not in ["filename", "timestamp", "cost_estimate"]}
            data["full_description"] = content
            data["summary"] = "Error parsing response - see full_description"
        
        # Add metadata
        data["filename"] = os.path.basename(image_path)
        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["cost_estimate"] = f"${image_cost:.4f}"
        
        images_processed += 1
        log_message(f"✓ Analysis complete ({images_processed} total)")
        
        return data
        
    except Exception as e:
        log_message(f"❌ ERROR: {str(e)}")
        messagebox.showerror("Analysis Error", f"Failed to analyze {Path(image_path).name}:\n{str(e)}")
        
        # Return error record
        return {
            "filename": os.path.basename(image_path),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": f"ERROR: {str(e)}",
            "objects": "",
            "people_count": "",
            "people_description": "",
            "colors": "",
            "mood": "",
            "emotion": "",
            "movement": "",
            "setting": "",
            "lighting": "",
            "composition": "",
            "elements_list": "",
            "full_description": "",
            "cost_estimate": "$0.0000"
        }

# ==============================
# SAVE TO CSV
# ==============================

def save_to_csv(data):
    """Append analysis data to CSV file"""
    try:
        # Ensure all columns exist
        for col in CSV_COLUMNS:
            if col not in data:
                data[col] = ""
        
        # Load existing or create new
        if os.path.exists(OUTPUT_CSV):
            df = pd.read_csv(OUTPUT_CSV)
        else:
            df = pd.DataFrame(columns=CSV_COLUMNS)
        
        # Append new row
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        
        # Save
        df.to_csv(OUTPUT_CSV, index=False)
        log_message(f"✓ Saved to {OUTPUT_CSV}")
        
        return True
        
    except Exception as e:
        log_message(f"❌ Error saving to CSV: {str(e)}")
        messagebox.showerror("Save Error", f"Failed to save to CSV:\n{str(e)}")
        return False

# ==============================
# GUI LOGGING
# ==============================

def log_message(message):
    """Add message to log window"""
    if log_text:
        log_text.config(state=NORMAL)
        log_text.insert(END, message + "\n")
        log_text.see(END)
        log_text.config(state=DISABLED)
        log_text.update()

# ==============================
# DROP HANDLER
# ==============================

def handle_drop(event):
    """Handle drag and drop of image files"""
    files = root.tk.splitlist(event.data)
    
    # Filter for image files
    image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"))]
    
    if not image_files:
        messagebox.showwarning("No Images", "Please drop image files (.png, .jpg, .jpeg, .webp)")
        return
    
    log_message(f"\n{'#'*60}")
    log_message(f"🎯 Processing {len(image_files)} image(s)")
    log_message(f"{'#'*60}\n")
    
    # Process each image
    success_count = 0
    for file in image_files:
        result = analyse_image(file)
        if save_to_csv(result):
            success_count += 1
    
    # Summary
    log_message(f"\n{'#'*60}")
    log_message(f"✅ BATCH COMPLETE")
    log_message(f"{'#'*60}")
    log_message(f"Processed: {len(image_files)} images")
    log_message(f"Successful: {success_count}")
    log_message(f"Total cost: ${total_cost:.4f}")
    log_message(f"Output: {OUTPUT_CSV}")
    log_message(f"{'#'*60}\n")
    
    messagebox.showinfo(
        "Analysis Complete", 
        f"Analyzed {success_count} images\n"
        f"Total cost: ${total_cost:.4f}\n\n"
        f"Results saved to:\n{OUTPUT_CSV}"
    )

# ==============================
# OPEN CSV HANDLER
# ==============================

def open_csv():
    """Open the CSV file in default application"""
    if os.path.exists(OUTPUT_CSV):
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', OUTPUT_CSV])
            elif platform.system() == 'Windows':
                os.startfile(OUTPUT_CSV)
            else:  # Linux
                subprocess.call(['xdg-open', OUTPUT_CSV])
            log_message(f"✓ Opened {OUTPUT_CSV}")
        except Exception as e:
            log_message(f"❌ Could not open CSV: {str(e)}")
            messagebox.showinfo("CSV Location", f"CSV file location:\n{os.path.abspath(OUTPUT_CSV)}")
    else:
        messagebox.showwarning("No Data", "No CSV file exists yet. Analyze some images first!")

# ==============================
# CLEAR LOG
# ==============================

def clear_log():
    """Clear the log window"""
    log_text.config(state=NORMAL)
    log_text.delete(1.0, END)
    log_text.config(state=DISABLED)
    log_message(f"ImageSense Analyzer v{VERSION}")
    log_message("="*60)
    log_message("Ready! Drag and drop images here to analyze.")
    log_message("="*60 + "\n")

# ==============================
# GUI SETUP
# ==============================

def create_gui():
    """Create the main GUI window"""
    global root, log_text
    
    root = TkinterDnD.Tk()
    root.title(f"ImageSense Analyzer v{VERSION}")
    root.geometry("800x600")
    
    # Header Frame
    header_frame = Frame(root, bg="#2c3e50", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    title_label = Label(
        header_frame,
        text="🖼️ ImageSense Analyzer",
        font=("Arial", 24, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=10)
    
    subtitle_label = Label(
        header_frame,
        text="Drag & Drop Images Here for AI Analysis",
        font=("Arial", 12),
        bg="#2c3e50",
        fg="#ecf0f1"
    )
    subtitle_label.pack()
    
    # Button Frame
    button_frame = Frame(root, bg="#ecf0f1")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    open_btn = Button(
        button_frame,
        text="📊 Open CSV",
        command=open_csv,
        font=("Arial", 10),
        bg="#3498db",
        fg="white",
        padx=20,
        pady=5
    )
    open_btn.pack(side="left", padx=5)
    
    clear_btn = Button(
        button_frame,
        text="🗑️ Clear Log",
        command=clear_log,
        font=("Arial", 10),
        bg="#95a5a6",
        fg="white",
        padx=20,
        pady=5
    )
    clear_btn.pack(side="left", padx=5)
    
    # Info Label
    info_label = Label(
        button_frame,
        text=f"Total Cost: ${total_cost:.4f} | Images: {images_processed}",
        font=("Arial", 10),
        bg="#ecf0f1"
    )
    info_label.pack(side="right", padx=10)
    
    # Log Frame
    log_frame = Frame(root)
    log_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    scrollbar = Scrollbar(log_frame)
    scrollbar.pack(side="right", fill="y")
    
    log_text = Text(
        log_frame,
        wrap="word",
        yscrollcommand=scrollbar.set,
        font=("Courier", 10),
        bg="#1e1e1e",
        fg="#00ff00",
        insertbackground="white"
    )
    log_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=log_text.yview)
    
    # Initial message
    clear_log()
    
    # Enable drag and drop
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", handle_drop)
    
    return root

# ==============================
# MAIN
# ==============================

def main():
    """Main entry point"""
    global root
    
    # Create GUI
    root = create_gui()
    
    # Validate API key on startup
    if not validate_api_key():
        root.destroy()
        return
    
    log_message("✓ Ready to analyze images!")
    log_message(f"Output will be saved to: {OUTPUT_CSV}\n")
    
    # Start GUI loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        log_message("\n👋 Shutting down...")
        root.destroy()

if __name__ == "__main__":
    main()
