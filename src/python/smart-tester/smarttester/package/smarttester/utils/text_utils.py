import re


def _get_bullets_number(text: str) -> int:
    bullet_characters = ["-", "•", "*"]

    lines = text.splitlines()
    bullets = []
    
    # get first matching bullet character
    for line in lines:
        bullet_character = None
        for char in line:
            if char in bullet_characters:
                bullet_character = char
                break

        if bullet_character:
            bullet_line = line.split(bullet_character)[0] + bullet_character
            # if doesn't contain characters like letters or numbers
            if not re.search(r'[a-zA-Z0-9]', bullet_line):
                bullets.append(bullet_line)

    if len(bullets) == 0:
        return 0

    # group bullets by format
    _grouped_bullets: dict[str, int] = {}
    for bullet in bullets:
        if bullet not in _grouped_bullets:
            _grouped_bullets[bullet] = 0
        _grouped_bullets[bullet] += 1

    # count bullets number as the most frequent format
    bullets_number = max(_grouped_bullets.values())

    return bullets_number


if __name__ == "__main__":
    sentence = """
    Scenarios to consider for unit testing the `_get_bullets_number` function:

1. Basic scenario:
   - Input text contains a single bullet point.
     - Example: `' - Bullet point'`
   - Input text contains multiple bullet points.
     - Example: `' - Bullet point 1\n - Bullet point 2'`

2. Nested bullet points:
   - Input text contains nested bullet points.
     - Example: `' - Bullet point 1\n   - Nested bullet point 1\n   - Nested bullet point 2\n - Bullet point 2'`
   - Input text contains nested bullet points with different indentation levels.
     - Example: `' - Bullet point 1\n     - Nested bullet point 1\n   - Nested bullet point 2\n - Bullet point 2'`

3. Different bullet point characters:
   - Input text contains bullet points with different characters (`-`, `•`, `*`).
     - Example: `'- Bullet point 1\n • Bullet point 2\n * Bullet point 3'`

4. Empty input text:
   - Input text is an empty string.
     - Example: `''`

5. No bullet points:
   - Input text does not contain any bullet points.
     - Example: `'This is a regular sentence.'`

6. Leading and trailing whitespace:
   - Input text contains leading and/or trailing whitespace.
     - Example: `'   - Bullet point   \n'`

7. Special characters:
   - Input text contains special characters.
     - Example: `' - Bullet point with special character: @#$%'`

8. Newline characters:
   - Input text contains newline characters (`\n`).
     - Example: `' - Bullet point 1\n\n - Bullet point 2\n\n\n - Bullet point 3'`

9. Windows-style line endings:
   - Input text contains Windows-style line endings (`\r\n`).
     - Example: `' - Bullet point 1\r\n - Bullet point 2\r\n\r\n - Bullet point 3'`

10. Mixed line endings:
    - Input text contains a mix of different line endings (Windows-style and Unix-style).
      - Example: `' - Bullet point 1\r\n - Bullet point 2\n\n - Bullet point 3\r\n\r\n'`
      """

    result = (_get_bullets_number(sentence))
