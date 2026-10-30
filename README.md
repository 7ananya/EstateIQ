# EstateIQ Mumbai — Property Intelligence Website

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.

## Website sections
- Home page with warm ivory/beige styling and a layered 3D property-card showcase.
- Explore Listings with locality, BHK and rent filters.
- Investment Lab with assumption-based rental-yield and payback comparisons.
- Market Insights with descriptive statistics and charts styled to match the beige/sage palette.

## Dataset and methodology
The supplied Mumbai listing dataset is in `data/Mumbai_property_details.csv`. Listings are not verified sale transactions. Purchase prices are estimated as parsed area × the user's assumed price per square foot. Yield and payback values are scenario estimates, not investment advice. The Area field may contain multiple numbers; the app uses the first numeric value.

## Credit
Built by **Ananya Terwadkar** as a university project.

The hero and card-preview photos and Google Fonts are loaded from external sources and may require an internet connection. The 3D cards are CSS-based interface mockups; they are not screenshots of separate deployed pages.
