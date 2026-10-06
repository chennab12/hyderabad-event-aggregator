import streamlit as st
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Schema for Structured Hyderabad Event Intelligence ---
class HyderabadEventItem(BaseModel):
    event_title: str = Field(description="Name of the event")
    venue_area: str = Field(description="Neighborhood or venue in Hyderabad e.g., Gachibowli, Hitec City, Jubilee Hills")
    category: str = Field(description="Category e.g., Stand-up Comedy, Tech Meetup, Music Concert, Cultural Festival")
    target_age: str = Field(description="Target age group suitability")
    current_cost_inr: float = Field(description="Current ticket price in INR or 0 for free")
    deal_offers: str = Field(description="Available deals, credit card discounts, or free admission notes")
    why_its_best: str = Field(description="Why this ranks in the top 20% ROI events")
    personal_benefit: str = Field(description="How attending benefits the person professionally or personally")
    price_worth_verdict: str = Field(description="Verdict: 🔥 Absolute Worth It, 🟡 Fair Value, ❌ Overpriced")
    roi_score: float = Field(description="Calculated value score out of 100")
    source_link: str = Field(description="Direct URL to BookMyShow or Insider event page")

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Hyderabad Event Recommendation Aggregator",
    page_icon="🌆",
    layout="wide"
)

st.title("🌆 Hyderabad Agentic Event Intelligence & Recommendation Hub")
st.markdown("Discover the top 20% high-ROI events in **Hyderabad, Telangana** tailored to your age, neighborhood, and interests. Compare ticket costs in INR, view deal offers, and access direct booking links.")

# --- Sidebar Search & Dynamic Criteria ---
st.sidebar.header("Hyderabad Event Criteria")
user_area = st.sidebar.selectbox("Preferred Hub / Area", ["All Hyderabad", "Gachibowli / Hitec City", "Jubilee Hills / Banjara Hills", "Madhapur / Kondapur"])
user_age_group = st.sidebar.selectbox("Age Group Suitability", ["Adults (21+)", "All Ages / Family", "Young Professionals & Students"])

selected_interests = st.sidebar.multiselect(
    "Interests & Categories",
    ["Stand-up Comedy", "Tech & AI Meetups", "Music Concerts & Live Gigs", "Food & Cultural Fests", "Networking & Startup Mixers"],
    default=["Stand-up Comedy", "Tech & AI Meetups", "Music Concerts & Live Gigs", "Food & Cultural Fests"]
)

max_budget_inr = st.sidebar.slider("Maximum Budget (₹ INR)", min_value=0, max_value=5000, value=1500, step=100)

sort_by = st.sidebar.selectbox(
    "Sort Recommendations By",
    ["Highest ROI / Best Value Score", "Lowest Ticket Cost (INR)"]
)

if st.button("Run Hyderabad Event Aggregator", type="primary"):
    with st.spinner(f"Agents aggregating top-rated events across Hyderabad under ₹{max_budget_inr}..."):
        
        # Mock database of top-tier Hyderabad events validated via Pydantic v2
        mock_events = [
            HyderabadEventItem(
                event_title="Hyderabad AI & Generative Tech Summit 2026",
                venue_area="Hitec City (HITEX Exhibition Center)",
                category="Tech & AI Meetups",
                target_age="Young Professionals & Students",
                current_cost_inr=750.00,
                deal_offers="Early bird 20% discount code using HET20 on Insider.",
                why_its_best="Premier regional gathering of AI researchers, founders, and machine learning practitioners.",
                personal_benefit="Directly accelerates professional networking, technical knowledge acquisition, and career growth in AI/ML.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=96.0,
                source_link="https://insider.in"
            ),
            HyderabadEventItem(
                event_title="Zakir Khan Live - Stand-up Comedy Special",
                venue_area="Gachibowli Indoor Stadium",
                category="Stand-up Comedy",
                target_age="Adults (21+)",
                current_cost_inr=999.00,
                deal_offers="ICICI Bank credit card net-banking 10% cashback.",
                why_its_best="Sold-out national comedy tour stop featuring premium relatable storytelling and elite entertainment.",
                personal_benefit="Provides vital stress relief, weekend relaxation, and an enjoyable evening out with friends.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=91.5,
                source_link="https://bookmyshow.com"
            ),
            HyderabadEventItem(
                event_title="Dakkhan Food & Craft Street Festival",
                venue_area="Jubilee Hills Public Gardens",
                category="Food & Cultural Fests",
                target_age="All Ages / Family",
                current_cost_inr=0.00,
                deal_offers="Free entry pass via district cultural portal registration.",
                why_its_best="Celebration of authentic Hyderabadi cuisine, Nizami heritage, and regional artisan crafts.",
                personal_benefit="Immersive cultural experience and wonderful weekend food tasting exploration with family.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=94.0,
                source_link="https://bookmyshow.com"
            ),
            HyderabadEventItem(
                event_title="Indie Rock Night ft. Local Underground Bands",
                venue_area="Madhapur (Heart Cup Coffee / Amphitheatre)",
                category="Music Concerts & Live Gigs",
                target_age="Adults (21+)",
                current_cost_inr=499.00,
                deal_offers="Includes one complimentary beverage voucher.",
                why_its_best="Showcases the best emerging independent musical talent in Hyderabad's vibrant indie scene.",
                personal_benefit="Supports local artists and offers an energetic, vibrant atmosphere for music enthusiasts.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=88.5,
                source_link="https://insider.in"
            ),
            HyderabadEventItem(
                event_title="Hyderabad Startup Founders & Investors Networking Mixer",
                venue_area="Kondapur (Daspalla Hotel)",
                category="Networking & Startup Mixers",
                target_age="Young Professionals & Students",
                current_cost_inr=1200.00,
                deal_offers="Includes high tea and curated speed-networking sessions.",
                why_its_best="High-density professional networking event connecting tech founders with venture partners.",
                personal_benefit="Unlocks potential co-founder partnerships, mentorship, and high-value business connections.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=95.0,
                source_link="https://insider.in"
            )
        ]
        
        # Convert models using Pydantic v2 model_dump()
        df = pd.DataFrame([event.model_dump() for event in mock_events])
        
        # Filter based on user criteria
        filtered_df = df[
            (df["current_cost_inr"] <= max_budget_inr) &
            (df["category"].isin(selected_interests))
        ]
        
        if sort_by == "Highest ROI / Best Value Score":
            filtered_df = filtered_df.sort_values(by="roi_score", ascending=False)
        elif sort_by == "Lowest Ticket Cost (INR)":
            filtered_df = filtered_df.sort_values(by="current_cost_inr", ascending=True)
            
        st.success(f"Aggregated {len(filtered_df)} top-tier recommended events across Hyderabad matching your criteria!")
        
        # --- Top Summary Metrics ---
        col1, col2, col3 = st.columns(3)
        if not filtered_df.empty:
            free_events_count = len(filtered_df[filtered_df["current_cost_inr"] == 0])
            avg_cost = filtered_df["current_cost_inr"].mean()
            col1.metric("Top Recommended Events", len(filtered_df))
            col2.metric("Free / Low-Cost Events", free_events_count)
            col3.metric("Average Ticket Cost", f"₹{avg_cost:.2f}")
        
        # --- Main Tabular Display ---
        st.subheader("📊 Top 20% High-ROI Hyderabad Event Intelligence Table")
        
        if not filtered_df.empty:
            display_df = filtered_df[[
                "event_title", "venue_area", "category", "current_cost_inr", 
                "deal_offers", "price_worth_verdict", "roi_score"
            ]].copy()
            
            display_df.columns = [
                "Event Title", "Hyderabad Venue / Area", "Category", "Cost (₹)", 
                "Deals & Offers", "Worth It Verdict", "ROI Score"
            ]
            
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("### 🔍 Detailed Breakdown, Personal Benefits & Suggested Next Steps")
            for _, row in filtered_df.iterrows():
                with st.expander(f"📍 {row['event_title']} ({row['venue_area']}) — Cost: ₹{row['current_cost_inr']} [{row['price_worth_verdict']}]"):
                    c_left, c_right = st.columns([2, 1])
                    with c_left:
                        st.markdown(f"* **Category & Target Audience:** {row['category']} | Suitable for: `{row['target_age']}`")
                        st.markdown(f"* **Why It's a Top Recommendation:** {row['why_its_best']}")
                        st.markdown(f"* **Personal Benefit:** {row['personal_benefit']}")
                        st.markdown(f"* **Deals & Offers Available:** {row['deal_offers']}")
                        st.markdown(f"* **Suggested Next Steps:** Check date availability, apply promo codes on BookMyShow/Insider, and add reminder to calendar.")
                    with c_right:
                        st.link_button("🔗 Book Tickets on Source Site", row["source_link"])
        else:
            st.warning("No events matched your exact category and budget filters in Hyderabad. Try expanding your interest selections or increasing your maximum budget.")
else:
    st.info("Configure your Hyderabad search criteria in the sidebar and click **Run Hyderabad Event Aggregator** to view recommended events.")
