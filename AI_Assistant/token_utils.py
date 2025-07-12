#!/usr/bin/env python3
"""
Token Counter Utility
Helps estimate tokens in text to avoid rate limits
"""

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    
    Rough estimation: 1 token ≈ 4 characters for English text
    This is an approximation - actual tokenization may vary
    """
    if not text:
        return 0
    
    # Simple estimation: average 4 characters per token
    return len(text) // 4

def check_token_limit(text: str, max_tokens: int = 25000) -> tuple[bool, int]:
    """
    Check if text is within token limits.
    
    Args:
        text: Text to check
        max_tokens: Maximum allowed tokens (default: 25000, safe for 30k limit)
    
    Returns:
        (is_within_limit, estimated_tokens)
    """
    estimated_tokens = estimate_tokens(text)
    return estimated_tokens <= max_tokens, estimated_tokens

def truncate_text_smart(text: str, max_tokens: int = 25000) -> str:
    """
    Intelligently truncate text to fit within token limits.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum allowed tokens
    
    Returns:
        Truncated text with summary note
    """
    estimated_tokens = estimate_tokens(text)
    
    if estimated_tokens <= max_tokens:
        return text
    
    # Calculate how much text to keep (with buffer)
    target_chars = max_tokens * 4 * 0.8  # 80% of limit for safety
    
    if len(text) <= target_chars:
        return text
    
    # Smart truncation: keep beginning and end
    keep_start = int(target_chars * 0.7)  # 70% from start
    keep_end = int(target_chars * 0.3)    # 30% from end
    
    truncated = (
        text[:keep_start] + 
        f"\n\n[... CONTENT TRUNCATED - Original: {len(text)} chars, Truncated: {int(target_chars)} chars ...]\n\n" + 
        text[-keep_end:]
    )
    
    return truncated

def get_safe_prompt(base_prompt: str, file_content: str, max_tokens: int = 25000) -> str:
    """
    Create a safe prompt that fits within token limits.
    
    Args:
        base_prompt: The instruction/question
        file_content: Content to analyze
        max_tokens: Maximum allowed tokens
    
    Returns:
        Safe prompt that fits within limits
    """
    prompt_tokens = estimate_tokens(base_prompt)
    available_tokens = max_tokens - prompt_tokens - 500  # Buffer for response
    
    if available_tokens <= 0:
        return "The prompt is too long. Please simplify your request."
    
    # Check if file content fits
    content_tokens = estimate_tokens(file_content)
    
    if content_tokens <= available_tokens:
        return f"{base_prompt}\n\nFile content:\n{file_content}"
    
    # Truncate file content
    safe_content = truncate_text_smart(file_content, available_tokens)
    
    return f"{base_prompt}\n\nFile content (truncated for processing):\n{safe_content}"

if __name__ == "__main__":
    # Test the utility
    sample_text = "This is a sample text. " * 1000
    is_safe, tokens = check_token_limit(sample_text)
    print(f"Sample text: {tokens} tokens, Safe: {is_safe}")
    
    if not is_safe:
        truncated = truncate_text_smart(sample_text, 5000)
        print(f"Truncated to: {estimate_tokens(truncated)} tokens")
