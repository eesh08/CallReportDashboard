# Quick Start Guide

## Running the Dashboard in 3 Simple Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Dashboard
```bash
streamlit run dashboard.py
```

### Step 3: Upload Your Data
1. The dashboard will open in your browser at `http://localhost:8501`
2. Click "Browse files" in the sidebar
3. Upload your CSV or Excel file
4. View automatic insights and visualizations!

## Try It With Sample Data

Want to see the dashboard in action? Use the included `sample_data.csv`:

1. Start the dashboard (see Step 2 above)
2. Upload `sample_data.csv` from the sidebar
3. Explore all the features!

## Expected Data Format

Your file should include these columns:
- `representative` - Sales rep name
- `doctor` - Doctor name  
- `division` - Medical division/specialty
- `date` - Visit date (YYYY-MM-DD format)

Optional columns for more insights:
- `call_type` - Visit type (In-person, Virtual, Phone)
- `outcome` - Result (Positive, Neutral, Follow-up needed)
- `product` - Product discussed
- `location` - Visit location

## What You'll Get

📊 **Key Metrics**
- Total calls count
- Number of representatives
- Number of doctors
- Number of divisions

💡 **Automatic Insights**
- Performance averages
- Top performers
- Engagement patterns
- Trend analysis

📈 **5 Interactive Visualizations**
1. Representative performance chart
2. Division distribution pie chart
3. Time trend line chart
4. Doctor engagement rankings
5. Cross-dimensional heatmap

💾 **Export Options**
- Download summary statistics
- Download processed data

## Troubleshooting

**Dashboard won't start?**
- Make sure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`

**File upload fails?**
- Check file format is CSV or Excel (.xlsx, .xls)
- Ensure file contains the required columns
- Check for special characters in column names

**Missing visualizations?**
- Some charts require specific columns (e.g., time trend needs 'date')
- Upload a file with all recommended columns for best results

## Need Help?

Check the main [README.md](README.md) for detailed documentation or open an issue on GitHub.
