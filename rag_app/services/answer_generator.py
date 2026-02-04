# rag_app/services/answer_generator.py

def generate_answer(chunks, max_lines=10):
    """
    Generate a concise readable answer from retrieved chunks.
    
    Args:
        chunks (list of str): Retrieved text chunks
        max_lines (int): Maximum number of lines to include in final answer

    Returns:
        str: Clean, readable answer
    """
    seen = set()
    lines = []

    for chunk in chunks:
        for line in chunk.splitlines():
            line = line.strip()
            if not line or line in seen:
                continue
            seen.add(line)
            lines.append(line)
            if len(lines) >= max_lines:
                break
        if len(lines) >= max_lines:
            break

    return " ".join(lines)
