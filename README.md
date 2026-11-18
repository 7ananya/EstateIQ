# EstateIQ Mumbai – Property Intelligence Website

## Overview

EstateIQ Mumbai is an interactive property intelligence platform built using Streamlit. It provides an interface to explore Mumbai property listings, compare rental opportunities, and analyze property market trends through interactive visualizations.

The platform combines property data exploration, rental yield estimation, and descriptive market analysis to help users understand different aspects of the Mumbai residential real estate market.

## Key Features

- **Home:** Property-focused landing page with a layered card showcase and custom visual design.
- **Explore Listings:** Filter property listings by locality, BHK configuration, and rent.
- **Investment Lab:** Compare rental yield and estimated payback periods using customizable assumptions.
- **Market Insights:** Explore descriptive statistics and interactive charts to understand listing patterns and market trends.
- **Interactive Visualizations:** Charts and analytical views designed with a consistent ivory, beige, and sage colour palette.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Data Visualization | Plotly |
| Frontend Styling | CSS |
| Dataset Format | CSV |

## Project Structure

```text
EstateIQ-Mumbai/
│
├── app.py
├── requirements.txt
├── data/
│   └── Mumbai_property_details.csv
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/7ananya/EstateIQ.git
```

### 2. Navigate to the Project Directory

```bash
cd EstateIQ
```

### 3. Install Dependencies

Python 3.10 or later is required.

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Dataset and Methodology

The application uses the Mumbai property listing dataset stored at:

`data/Mumbai_property_details.csv`

The analytical methodology includes:

- Property listing exploration and filtering.
- Locality-based comparisons.
- Descriptive statistical analysis.
- Rental yield estimation.
- Estimated investment payback calculations.

### Important Assumptions and Limitations

- The dataset contains property listings, not verified sale transactions.
- Purchase prices are estimated using the parsed property area multiplied by a user-defined assumed price per square foot.
- Rental yield and payback calculations are scenario-based estimates and should not be interpreted as financial or investment advice.
- Where the Area field contains multiple numerical values, the application uses the first numerical value.
- Property listing information may not reflect current market prices or actual transaction values.

## Design and Interface

The application uses a warm ivory and beige visual theme with sage accents.

The interface includes layered CSS-based 3D property-card mockups, custom styling, and externally sourced property photographs and Google Fonts.

An internet connection may be required to load external images and fonts. The 3D cards are interface design elements rather than screenshots of separately deployed pages.

## Live Demo

[Explore EstateIQ Mumbai](https://estateiq-mumbai.streamlit.app/)

## Author

**Ananya Terwadkar**

[GitHub Profile](https://github.com/7ananya)
