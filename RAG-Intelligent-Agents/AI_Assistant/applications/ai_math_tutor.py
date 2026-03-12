#!/usr/bin/env python3
"""
AI Math Tutor
An educational application that helps students with math problems,
unit conversions, and provides step-by-step explanations
"""

import streamlit as st
import sys
import os

# Add the parent directory to the Python path to import the agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import react_graph
from langchain_core.messages import HumanMessage

def main():
    st.set_page_config(
        page_title="AI Math Tutor",
        page_icon="🧮",
        layout="wide"
    )
    
    st.title("🧮 AI Math Tutor")
    st.markdown("### Your personal AI assistant for math, science, and problem-solving!")
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["🔢 Math Solver", "📏 Unit Converter", "📚 Study Helper", "🔬 Science Calculator"])
    
    with tab1:
        st.header("🔢 Mathematics Problem Solver")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Math problem input
            math_problem = st.text_area(
                "Enter your math problem:",
                height=100,
                placeholder="Examples:\n- Solve: x^2 + 5x + 6 = 0\n- Simplify: (x+2)(x+3)\n- Calculate: sqrt(144) + 2^3\n- Find derivative of: x^3 + 2x^2 + x",
                value=st.session_state.get('math_problem', '')
            )
            
            # Example problems
            st.subheader("📝 Example Problems:")
            examples = [
                "Solve the quadratic equation: x^2 - 4x + 3 = 0",
                "Simplify the expression: (2x + 3)(x - 1)",
                "Calculate the derivative of: 3x^2 + 2x + 1",
                "Find the integral of: x^2 + x",
                "What is the limit of (sin(x)/x) as x approaches 0?",
                "Calculate: sqrt(64) + log(100, 10)"
            ]
            
            example_cols = st.columns(2)
            for i, example in enumerate(examples):
                with example_cols[i % 2]:
                    if st.button(example, key=f"math_example_{i}", use_container_width=True):
                        st.session_state.math_problem = example
                        st.rerun()
                        
            if st.button("🧮 Solve Problem", type="primary") and (math_problem or st.session_state.get('math_problem')):
                current_problem = math_problem if math_problem else st.session_state.get('math_problem', '')
                with st.spinner("🤖 Solving your math problem..."):
                    try:
                        question = f"Solve this math problem step by step and explain your reasoning: {current_problem}"
                        
                        result = react_graph.invoke({
                            "messages": [HumanMessage(content=question)],
                            "input_file": None
                        })
                        
                        if result and "messages" in result:
                            final_message = result["messages"][-1]
                            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                            
                            st.subheader("✅ Solution:")
                            st.write(response)
                            
                    except Exception as e:
                        st.error(f"❌ Error solving problem: {str(e)}")
        
        with col2:
            st.subheader("📖 Math Topics Covered:")
            st.markdown("""
            **Algebra:**
            - Equations and inequalities
            - Polynomials
            - Factoring
            - Functions
            
            **Calculus:**
            - Derivatives
            - Integrals
            - Limits
            - Series
            
            **Geometry:**
            - Area and volume
            - Trigonometry
            - Coordinate geometry
            
            **Statistics:**
            - Basic calculations
            - Probability
            - Data analysis
            """)
    
    with tab2:
        st.header("📏 Unit Converter")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            conversion_query = st.text_input(
                "Enter conversion (format: 'value unit to target_unit'):",
                placeholder="Examples: 100 km/h to m/s, 32 fahrenheit to celsius, 5 feet to meters",
                value=st.session_state.get('conversion_query', '')
            )
            
            # Example conversions
            st.subheader("🔄 Example Conversions:")
            conversion_examples = [
                "90 km/h to m/s",
                "100 fahrenheit to celsius",
                "5 feet to meters",
                "2 hours to seconds",
                "500 grams to pounds",
                "1 mile to kilometers"
            ]
            
            conv_cols = st.columns(2)
            for i, example in enumerate(conversion_examples):
                with conv_cols[i % 2]:
                    if st.button(example, key=f"conv_example_{i}", use_container_width=True):
                        st.session_state.conversion_query = example
                        st.rerun()
            
            if st.button("🔄 Convert Units", type="primary") and (conversion_query or st.session_state.get('conversion_query')):
                current_query = conversion_query if conversion_query else st.session_state.get('conversion_query', '')
                with st.spinner("🔄 Converting units..."):
                    try:
                        question = f"Convert the following units and explain the conversion: {current_query}"
                        
                        result = react_graph.invoke({
                            "messages": [HumanMessage(content=question)],
                            "input_file": None
                        })
                        
                        if result and "messages" in result:
                            final_message = result["messages"][-1]
                            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                            
                            st.subheader("🎯 Conversion Result:")
                            st.write(response)
                            
                    except Exception as e:
                        st.error(f"❌ Error converting units: {str(e)}")
        
        with col2:
            st.subheader("📐 Supported Units:")
            st.markdown("""
            **Length:**
            - meters, feet, inches, miles, km
            
            **Weight:**
            - grams, pounds, kilograms, ounces
            
            **Temperature:**
            - celsius, fahrenheit, kelvin
            
            **Speed:**
            - m/s, km/h, mph, knots
            
            **Time:**
            - seconds, minutes, hours, days
            
            **And many more!**
            """)
    
    with tab3:
        st.header("📚 Study Helper")
        
        study_question = st.text_area(
            "Ask any academic question:",
            height=100,
            placeholder="Examples:\n- Explain photosynthesis\n- What is the Pythagorean theorem?\n- How does gravity work?\n- Explain the water cycle",
            value=st.session_state.get('study_question', '')
        )
        
        # Subject areas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🔬 Science Topics:")
            science_topics = [
                "Explain Newton's laws of motion",
                "What is photosynthesis?",
                "How do chemical bonds work?",
                "Explain the periodic table"
            ]
            for i, topic in enumerate(science_topics):
                if st.button(topic, key=f"science_{i}", use_container_width=True):
                    st.session_state.study_question = topic
                    st.rerun()
        
        with col2:
            st.subheader("📐 Math Concepts:")
            math_concepts = [
                "What is the Pythagorean theorem?",
                "Explain logarithms",
                "What are prime numbers?",
                "How do fractions work?"
            ]
            for i, concept in enumerate(math_concepts):
                if st.button(concept, key=f"concept_{i}", use_container_width=True):
                    st.session_state.study_question = concept
                    st.rerun()
        
        with col3:
            st.subheader("🌍 Other Subjects:")
            other_topics = [
                "Explain the water cycle",
                "What caused World War I?",
                "How does economics work?",
                "What is programming?"
            ]
            for i, topic in enumerate(other_topics):
                if st.button(topic, key=f"other_{i}", use_container_width=True):
                    st.session_state.study_question = topic
                    st.rerun()
        
        if st.button("📖 Get Explanation", type="primary") and (study_question or st.session_state.get('study_question')):
            current_question = study_question if study_question else st.session_state.get('study_question', '')
            with st.spinner("🤖 Researching and preparing explanation..."):
                try:
                    question = f"Explain this topic in a clear, educational way suitable for students: {current_question}"
                    
                    result = react_graph.invoke({
                        "messages": [HumanMessage(content=question)],
                        "input_file": None
                    })
                    
                    if result and "messages" in result:
                        final_message = result["messages"][-1]
                        response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                        
                        st.subheader("📚 Explanation:")
                        st.write(response)
                        
                except Exception as e:
                    st.error(f"❌ Error getting explanation: {str(e)}")
    
    with tab4:
        st.header("🔬 Science Calculator")
        
        st.write("Solve physics, chemistry, and engineering problems!")
        
        science_problem = st.text_area(
            "Enter your science problem:",
            height=100,
            placeholder="Examples:\n- Calculate the force: F = ma, where m = 10kg and a = 9.8 m/s²\n- Find the molarity of a solution with 2 moles in 0.5 L\n- What's the kinetic energy of a 5kg object moving at 10 m/s?",
            value=st.session_state.get('science_problem', '')
        )
        
        # Example science problems
        st.subheader("🧪 Example Problems:")
        science_examples = [
            "Calculate the force: F = ma, where m = 10kg and a = 9.8 m/s²",
            "Find the kinetic energy: KE = ½mv², where m = 5kg and v = 10 m/s",
            "Calculate the molarity: M = n/V, where n = 2 moles and V = 0.5 L",
            "Find the electrical power: P = VI, where V = 12V and I = 2A",
            "Calculate the wavelength: λ = c/f, where c = 3×10⁸ m/s and f = 1×10⁶ Hz"
        ]
        
        sci_cols = st.columns(2)
        for i, example in enumerate(science_examples):
            with sci_cols[i % 2]:
                if st.button(example, key=f"science_example_{i}", use_container_width=True):
                    st.session_state.science_problem = example
                    st.rerun()
        
        if st.button("🧪 Solve Science Problem", type="primary") and (science_problem or st.session_state.get('science_problem')):
            current_problem = science_problem if science_problem else st.session_state.get('science_problem', '')
            with st.spinner("🔬 Calculating..."):
                try:
                    question = f"Solve this science problem with step-by-step calculations and explanations: {current_problem}"
                    
                    result = react_graph.invoke({
                        "messages": [HumanMessage(content=question)],
                        "input_file": None
                    })
                    
                    if result and "messages" in result:
                        final_message = result["messages"][-1]
                        response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                        
                        st.subheader("🎯 Solution:")
                        st.write(response)
                        
                except Exception as e:
                    st.error(f"❌ Error solving problem: {str(e)}")

if __name__ == "__main__":
    # Initialize session state
    for key in ['math_problem', 'conversion_query', 'study_question', 'science_problem']:
        if key not in st.session_state:
            st.session_state[key] = ''
    
    main()
