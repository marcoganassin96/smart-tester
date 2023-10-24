color_prefix_by_role = {
            "system": "\033[0m",  # gray
            "user": "\033[0m",  # gray
            "assistant": "\033[92m",  # green
        }

def print_messages(messages, color_prefix_by_role=color_prefix_by_role) -> None:
    """Prints messages sent to or from GPT."""
    for message in messages:
        role = message["role"]
        color_prefix = color_prefix_by_role[role]
        content = message["content"]
        print(f"{color_prefix}\n[{role}]\n{content}")

def print_message_delta(delta, color_prefix_by_role=color_prefix_by_role) -> None:
    """Prints a chunk of messages streamed back from GPT."""
    if "role" in delta:
        role = delta["role"]
        color_prefix = color_prefix_by_role[role]
        print(f"{color_prefix}\n[{role}]\n", end="")
    elif "content" in delta:
        content = delta["content"]
        print(content, end="")
    else:
        pass
