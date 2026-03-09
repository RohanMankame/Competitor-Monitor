import streamlit as st
from crew import run_competitor_analysis

def main():
    st.set_page_config(page_title="Competitor Strategy Agent", page_icon="🏢", layout="wide")
    
    st.title("Competitor Strategy Agent")
    st.markdown("""
    Welcome to the **AI Competitor Strategy Dashboard**.
    
    Enter a product name, select target retailers, and internal company product infomation.
    
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
            currency = st.selectbox("Currency:", options=["USD", "GBP", "YEN", "INR", "RMB"], index=3) 
            
        col3, col4, col5 = st.columns(3)
        with col3:
            internal_promotion = st.text_input("Internal Promotion/Discount:", placeholder="e.g., 20% off")
        with col4:
            internal_sales = st.text_input("Internal Sales:", placeholder="e.g., 1000 units/mo")
        with col5:
            internal_rating = st.slider("Internal Star Rating:", min_value=1.0, max_value=5.0, value=4.5, step=0.1)
        
        submitted = st.form_submit_button("Run Strategic Analysis ")
        
    if submitted:
        if not product_name:
            st.error("Please provide a valid Product Name.")
        elif internal_price <= 0:
            st.warning("Please provide a valid Internal Base Price greater than 0.")
        else:
            st.info("Deploying the Researcher, Scout, and Strategist...")
            with st.spinner("Analyzing competitive market data... This process takes up to two minutes."):
                try:
                    analysis_result = run_competitor_analysis(
                        product_name, target_domains, internal_price, currency,
                        internal_promotion, internal_sales, internal_rating
                    )
                    
                    st.success("Analysis Complete!")
                    st.markdown("### Competitive Strategy Report")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
