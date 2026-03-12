#!/usr/bin/env python3
"""
Test file for the Gala Agent
This file imports the agent and tests various functionalities.
"""

import os
import sys
from langchain_core.messages import HumanMessage

# Import the agent and react_graph from our agent module
from agent import react_graph

def test_unit_conversion():
    """Test the unit conversion functionality"""
    print("🧪 Testing Unit Conversion...")
    print("=" * 50)
    
    # 1. Define the question
    question = "Convert 180 kilometers per hour to meters per second."
    
    # 2. Optional: specify a file path (or use None)
    file_path = None  # or something like "/content/sample.xlsx"
    
    # 3. Invoke the LangGraph agent
    result = react_graph.invoke({
        "messages": [HumanMessage(content=question)],
        "input_file": file_path
    })
    
    # 4. Print the final response
    print("📋 FINAL RESPONSE:")
    print("-" * 30)
    for msg in result["messages"]:
        print(msg.content)
        print()
    
    print("🔍 FULL MESSAGE TRACE:")
    print("-" * 30)
    for i, msg in enumerate(result["messages"], 1):
        print(f"Message {i}:")
        msg.pretty_print()
        print()

def test_math_calculation():
    """Test the math solving functionality"""
    print("\n🧪 Testing Math Calculation...")
    print("=" * 50)
    
    question = "What is the square root of 144?"
    
    result = react_graph.invoke({
        "messages": [HumanMessage(content=question)],
        "input_file": None
    })
    
    print("📋 FINAL RESPONSE:")
    print("-" * 30)
    for msg in result["messages"]:
        print(msg.content)
        print()

def test_search_query():
    """Test the search functionality"""
    print("\n🧪 Testing Search Query...")
    print("=" * 50)
    
    question = "Who is the current president of the United States in 2025?"
    
    result = react_graph.invoke({
        "messages": [HumanMessage(content=question)],
        "input_file": None
    })
    
    print("📋 FINAL RESPONSE:")
    print("-" * 30)
    for msg in result["messages"]:
        print(msg.content)
        print()

def test_wikipedia_query():
    """Test the Wikipedia functionality"""
    print("\n🧪 Testing Wikipedia Query...")
    print("=" * 50)
    
    question = "Tell me about artificial intelligence from Wikipedia."
    
    result = react_graph.invoke({
        "messages": [HumanMessage(content=question)],
        "input_file": None
    })
    
    print("📋 FINAL RESPONSE:")
    print("-" * 30)
    for msg in result["messages"]:
        print(msg.content)
        print()

def main():
    """Main function to run all tests"""
    print("🚀 Starting Gala Agent Tests")
    print("=" * 60)
    
    try:
        # Test 1: Unit Conversion (from your example)
        test_unit_conversion()
        
        # Test 2: Math Calculation
        test_math_calculation()
        
        # Test 3: Search Query
        test_search_query()
        
        # Test 4: Wikipedia Query
        test_wikipedia_query()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
