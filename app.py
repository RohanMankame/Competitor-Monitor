import streamlit as st
from crew import run_competitor_analysis

def main():
    st.set_page_config(page_title="Competitor Strategy Agent", page_icon="🏢", layout="wide")
    
    st.title("🏢 Competitor Strategy Agent")
    st.markdown("""
    Welcome to the **AI Competitor Strategy Dashboard**.
    
    Enter a product name, select target retailers, your internal price, and currency.
    1. The **Researcher** will find top product pages across your selected domains.
    2. The **Scout** will extract pricing and promotional data from all found pages.
    3. The **Strategist** will compare the aggregated market data to your internal price to recommend a tactical move.
    """)
    
    with st.form("strategy_form"):
        product_name = st.text_input("Product Name / Search Query:", placeholder="e.g., Apple AirPods Pro 2")
        
        target_domains = st.multiselect(
            "Target Domains (Optional - Leave blank to search universally):", 
            options=["amazon.in", "flipkart.com", "croma.com", "reliance-digital.com", "myntra.com"],
            default=["amazon.in", "flipkart.com"]
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            internal_price = st.number_input("Internal Base Price:", min_value=0.0, value=0.0, step=0.01)
        with col2:
            currency = st.selectbox("Currency:", options=["USD", "GBP", "YEN", "INR", "RMB"], index=3) # Default to INR given .in domains
        
        internal_promotions = st.text_area("Internal Promotions / Discounts (Optional):", placeholder="e.g., 10% off with code SAVE10, Buy 1 Get 1 Free", help="Include any current offers you are running on this product to factor into the competitive analysis.")
        
        submitted = st.form_submit_button("Run Strategic Analysis 📊")
        
    if submitted:
        if not product_name:
            st.error("Please provide a valid Product Name.")
        elif internal_price <= 0:
            st.warning("Please provide a valid Internal Base Price greater than 0.")
        else:
            st.info("Deploying the Researcher, Scout, and Strategist...")
            with st.spinner("Analyzing competitive market data... This process takes up to two minutes."):
                try:
                    analysis_result = run_competitor_analysis(product_name, target_domains, internal_price, currency, internal_promotions)
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 🗺️ Competitive Strategy Report")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
