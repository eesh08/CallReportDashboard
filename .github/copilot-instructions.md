# Copilot Instructions for CallReportDashboard

## Repository Overview

This repository contains a **Streamlit-based dashboard** application for generating insights on representatives' meetings with doctors across divisions. The dashboard provides interactive visualizations and filtering capabilities for call activity data.

## Technology Stack

- **Python 3.x**: Primary programming language
- **Streamlit**: Web framework for the interactive dashboard
- **Pandas**: Data manipulation and analysis
- **Plotly Express**: Interactive data visualizations
- **openpyxl**: Excel file handling support

## Project Structure

```
CallReportDashboard/
├── Dashboard.py           # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Key Application Features

The dashboard (`Dashboard.py`) provides:

1. **Data Upload**: CSV file upload functionality
2. **Filtering System**: Multi-level filters (Month, Employee, Division, Territory, Product)
3. **KPI Metrics**: Total calls, unique customers, products discussed, CLM calls
4. **Visualizations**:
   - Monthly call trends (line chart)
   - Top products discussed (bar chart)
   - Employee productivity analysis (bar chart)
   - Product × Speciality heatmap
5. **Raw Data View**: Expandable data table for detailed inspection

## Running the Application

### Installation
```bash
pip install -r requirements.txt
```

### Running the Dashboard
```bash
streamlit run Dashboard.py
```

The application will launch in your default web browser at `http://localhost:8501`.

## Code Style and Conventions

### General Guidelines
- Follow **PEP 8** Python style guidelines
- Use **descriptive variable names** that reflect the business domain
- Add **comments** for complex logic or non-obvious code sections
- Maintain **consistent indentation** (4 spaces)

### Streamlit-Specific Conventions
- Use `@st.cache_data` decorator for data loading functions to optimize performance
- Organize UI components logically (filters in sidebar, main content in main area)
- Use Streamlit columns (`st.columns()`) for side-by-side layouts
- Provide user feedback with `st.success()`, `st.info()`, `st.warning()`, etc.

### Data Handling
- Always strip column names (`df.columns.str.strip()`) after loading data
- Use `.dropna()` appropriately to handle missing values
- Apply filters in a logical order (time → person → geography → product)
- Avoid row duplication when filtering by products (P1-P4)

## Key Data Columns

The application expects CSV files with the following key columns:
- `Month`: Month of the call activity
- `Year Month`: Combined year-month for trend analysis
- `In-Field Activity: Owner Name`: Employee/representative name
- `Division`: Division identifier
- `Territory Code`: Territory identifier
- `Customer ID`: Unique customer identifier
- `Speciality`: Doctor/customer speciality
- `P1`, `P2`, `P3`, `P4`: Product columns (up to 4 products per call)
- `Call with CLM`: Whether CLM (Closed Loop Marketing) was used

## Testing

### Manual Testing
Since this is a Streamlit dashboard application, testing primarily involves:

1. **Start the application**: `streamlit run Dashboard.py`
2. **Upload test CSV**: Prepare a CSV file with the required columns
3. **Test filters**: Verify each filter works correctly
4. **Check visualizations**: Ensure all charts render properly
5. **Verify calculations**: Confirm KPI metrics are accurate

### Validation Checklist
- [ ] Data loads without errors
- [ ] All filters function correctly
- [ ] Charts display expected data
- [ ] KPI metrics calculate correctly
- [ ] Product filtering handles multiple product columns (P1-P4) properly
- [ ] No duplicate rows appear after filtering

## Common Patterns and Functions

### Data Loading
```python
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df
```

### Product Filtering
The application handles products across 4 columns (P1-P4). Use the `filter_by_product()` function to filter without duplicating rows:
```python
def filter_by_product(df, product):
    if product == "All":
        return df
    return df[
        (df['P1'] == product) |
        (df['P2'] == product) |
        (df['P3'] == product) |
        (df['P4'] == product)
    ]
```

## Making Changes

### When Adding New Features
1. **Maintain existing functionality**: Don't break current filters or visualizations
2. **Follow the existing layout pattern**: Filters in sidebar, content in main area
3. **Use appropriate Streamlit components**: Select the right widget for the interaction
4. **Optimize with caching**: Use `@st.cache_data` for expensive operations
5. **Test thoroughly**: Manually verify with sample data

### When Modifying Filters
1. **Preserve filter order**: Time → Person → Geography → Product
2. **Include "All" option**: Always provide an "All" selection for flexibility
3. **Handle missing values**: Use `.dropna()` before creating filter options
4. **Sort filter options**: Keep filter lists sorted for better UX

### When Adding Visualizations
1. **Use Plotly Express**: Consistent with existing charts
2. **Add meaningful titles**: Clearly describe what the chart shows
3. **Use `use_container_width=True`**: Ensures responsive layout
4. **Consider color schemes**: Maintain visual consistency

## Dependencies

All dependencies are listed in `requirements.txt`. When adding new dependencies:
1. **Add to requirements.txt**: Include the package name (version optional)
2. **Use common packages**: Prefer well-maintained, popular libraries
3. **Test compatibility**: Ensure new packages work with existing ones

## Troubleshooting

### Common Issues
- **Column name mismatches**: Always strip whitespace from column names
- **Missing data**: Handle with `.dropna()` or default values
- **Filter interactions**: Apply filters in the correct order to avoid unexpected results
- **Performance**: Use caching (`@st.cache_data`) for data loading and expensive operations

## Additional Notes

- The dashboard is designed for pharmaceutical/medical sales representatives tracking doctor visits
- Data privacy: Ensure any sample or test data doesn't contain real customer information
- The application expects clean, structured CSV data with consistent column names
- Product discussions are recorded in up to 4 columns (P1-P4) per call record
