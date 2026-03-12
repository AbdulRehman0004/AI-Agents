#!/usr/bin/env python3
"""
Data Analysis Assistant
Upload spreadsheets and get insights, visualizations, and analysis
"""

import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path to import the agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import react_graph
from langchain_core.messages import HumanMessage

def main():
    st.set_page_config(
        page_title="Data Analysis Assistant",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Data Analysis Assistant")
    st.markdown("### Upload your data and get instant insights and analysis")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Data File")
        uploaded_data = st.file_uploader(
            "Choose a data file",
            type=['csv', 'xlsx', 'xls', 'json'],
            help="Supported formats: CSV, Excel, JSON"
        )
        
        if uploaded_data:
            st.success(f"✅ Data uploaded: {uploaded_data.name}")
            st.info(f"📊 File size: {uploaded_data.size / 1024:.2f} KB")
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if uploaded_data:
            st.header("🔍 Analysis Options")
            
            # Analysis type selection
            analysis_type = st.selectbox(
                "What type of analysis do you need?",
                [
                    "📈 Basic Data Overview",
                    "📊 Statistical Summary",
                    "🔍 Find Patterns & Trends",
                    "💰 Financial Analysis",
                    "👥 Customer Data Analysis",
                    "📉 Performance Metrics",
                    "🎯 Custom Analysis"
                ]
            )
            
            # Custom analysis question
            if analysis_type == "🎯 Custom Analysis":
                custom_analysis = st.text_area(
                    "What specific analysis do you need?",
                    placeholder="Examples:\n- Find the top 10 customers by revenue\n- Calculate monthly growth rates\n- Identify seasonal patterns\n- Compare performance across regions\n- Find correlations between variables"
                )
            
            # Quick insights buttons
            st.subheader("⚡ Quick Insights")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("📋 Data Summary"):
                    st.session_state.quick_question = "Provide a comprehensive summary of this dataset including the number of rows, columns, data types, and any missing values."
            
            with col_b:
                if st.button("📈 Top Insights"):
                    st.session_state.quick_question = "Analyze this data and provide the top 5 most interesting insights or findings."
            
            with col_c:
                if st.button("🎯 Key Metrics"):
                    st.session_state.quick_question = "Calculate and present the key metrics and KPIs from this dataset."
            
            # Process button
            if st.button("🔬 Analyze Data", type="primary"):
                with st.spinner("🤖 Analyzing your data..."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_data.name).suffix) as tmp_file:
                            tmp_file.write(uploaded_data.getvalue())
                            temp_file_path = tmp_file.name
                        
                        # Prepare analysis question based on type with file size consideration
                        file_size_mb = uploaded_data.size / (1024 * 1024)
                        
                        if file_size_mb > 5:  # Large file
                            size_note = f"This is a large data file ({file_size_mb:.2f} MB). Focus on summary-level insights and key patterns rather than detailed row-by-row analysis. "
                        else:
                            size_note = ""
                        
                        if analysis_type == "📈 Basic Data Overview":
                            question = size_note + "Analyze this dataset and provide: 1) Basic statistics and data structure, 2) Key insights and patterns, 3) Data quality assessment, 4) Recommendations for further analysis."
                        elif analysis_type == "📊 Statistical Summary":
                            question = size_note + "Provide a comprehensive statistical analysis including: descriptive statistics, distributions, correlations, and statistical significance of key findings."
                        elif analysis_type == "🔍 Find Patterns & Trends":
                            question = size_note + "Analyze this data to identify: 1) Trends over time, 2) Patterns and correlations, 3) Outliers and anomalies, 4) Seasonal or cyclical patterns."
                        elif analysis_type == "💰 Financial Analysis":
                            question = size_note + "Perform financial analysis including: revenue trends, profitability metrics, cost analysis, growth rates, and financial health indicators."
                        elif analysis_type == "👥 Customer Data Analysis":
                            question = size_note + "Analyze customer data to identify: customer segments, behavior patterns, lifetime value, churn indicators, and growth opportunities."
                        elif analysis_type == "📉 Performance Metrics":
                            question = size_note + "Calculate and analyze performance metrics including: KPIs, benchmarks, performance trends, areas for improvement, and recommendations."
                        elif analysis_type == "🎯 Custom Analysis":
                            question = size_note + f"Analyze this dataset and provide insights for: {custom_analysis}"
                        
                        # Check for quick question
                        if hasattr(st.session_state, 'quick_question'):
                            question = st.session_state.quick_question
                            delattr(st.session_state, 'quick_question')
                        
                        # Process with agent
                        result = react_graph.invoke({
                            "messages": [HumanMessage(content=question)],
                            "input_file": temp_file_path
                        })
                        
                        # Display results
                        if result and "messages" in result:
                            final_message = result["messages"][-1]
                            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                            
                            st.subheader("📊 Analysis Results:")
                            st.write(response)
                            
                            # Option to download analysis
                            st.download_button(
                                label="📥 Download Analysis Report",
                                data=response,
                                file_name=f"analysis_report_{uploaded_data.name}.txt",
                                mime="text/plain"
                            )
                        
                        # Clean up temp file
                        os.unlink(temp_file_path)
                        
                    except Exception as e:
                        st.error(f"❌ Error analyzing data: {str(e)}")
            
            # Additional analysis options
            st.subheader("🔄 Follow-up Questions")
            follow_up = st.text_input(
                "Ask a follow-up question about your data:",
                placeholder="e.g., 'What's the correlation between sales and marketing spend?'"
            )
            
            if st.button("❓ Ask Follow-up") and follow_up and uploaded_data:
                with st.spinner("🤖 Processing follow-up question..."):
                    try:
                        # Save file again for follow-up
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_data.name).suffix) as tmp_file:
                            tmp_file.write(uploaded_data.getvalue())
                            temp_file_path = tmp_file.name
                        
                        result = react_graph.invoke({
                            "messages": [HumanMessage(content=follow_up)],
                            "input_file": temp_file_path
                        })
                        
                        if result and "messages" in result:
                            final_message = result["messages"][-1]
                            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                            
                            st.subheader("💬 Follow-up Answer:")
                            st.write(response)
                        
                        os.unlink(temp_file_path)
                        
                    except Exception as e:
                        st.error(f"❌ Error processing follow-up: {str(e)}")
        
        else:
            st.header("📊 Welcome to Data Analysis Assistant")
            st.markdown("""
            **Transform your data into actionable insights!**
            
            Simply upload your data file and choose from our analysis options:
            
            ---
            
            ### 🎯 Analysis Types Available:
            
            **📈 Basic Data Overview**
            - Data structure and quality assessment
            - Basic statistics and summaries
            - Initial insights and recommendations
            
            **📊 Statistical Summary**
            - Descriptive statistics
            - Distribution analysis
            - Correlation analysis
            
            **🔍 Pattern & Trend Analysis**
            - Time series trends
            - Seasonal patterns
            - Outlier detection
            
            **💰 Financial Analysis**
            - Revenue and profit analysis
            - Growth rate calculations
            - Financial health metrics
            
            **👥 Customer Analysis**
            - Customer segmentation
            - Behavior patterns
            - Lifetime value analysis
            
            **📉 Performance Metrics**
            - KPI calculations
            - Benchmarking
            - Performance trends
            
            ---
            
            ### 💡 Example Use Cases:
            - Sales performance analysis
            - Customer behavior insights
            - Financial reporting
            - Marketing campaign analysis
            - Operational efficiency metrics
            - Inventory management
            """)
    
    with col2:
        st.header("🛠️ Features")
        st.markdown("""
        **📊 Data Processing**
        - CSV, Excel, JSON support
        - Automatic data type detection
        - Missing value handling
        
        **🔍 Smart Analysis**
        - Statistical computations
        - Pattern recognition
        - Trend identification
        
        **📈 Insights Generation**
        - Key metric calculation
        - Correlation analysis
        - Performance benchmarking
        
        **💬 Interactive Q&A**
        - Ask follow-up questions
        - Custom analysis requests
        - Detailed explanations
        """)
        
        st.header("📋 Supported Data Types")
        st.markdown("""
        **📁 File Formats:**
        - CSV files
        - Excel spreadsheets (.xlsx, .xls)
        - JSON data files
        
        **📊 Data Types:**
        - Sales and revenue data
        - Customer information
        - Financial records
        - Marketing metrics
        - Operational data
        - Survey responses
        - Time series data
        """)
        
        st.header("🎯 Sample Questions")
        st.markdown("""
        **📈 Trends:**
        - "What's the monthly growth trend?"
        - "Are there seasonal patterns?"
        
        **💰 Financial:**
        - "Which products are most profitable?"
        - "What's the revenue breakdown?"
        
        **👥 Customers:**
        - "Who are our top customers?"
        - "What's the customer churn rate?"
        
        **📊 Performance:**
        - "How are we performing vs targets?"
        - "Which regions are underperforming?"
        """)

if __name__ == "__main__":
    main()
