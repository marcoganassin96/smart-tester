from smarttester.service.multi_prompt_python_smart_tester import unit_tests_from_function

if __name__ == "__main__":
    example_function = """def pig_latin(text):
        def translate(word):
            vowels = 'aeiou'
            if word[0] in vowels:
                return word + 'way'
            else:
                consonants = ''
                for letter in word:
                    if letter not in vowels:
                        consonants += letter
                    else:
                        break
                return word[len(consonants):] + consonants + 'ay'

        words = text.lower().split()
        translated_words = [translate(word) for word in words]
        return ' '.join(translated_words)
    """

    get_bullets_number_function = """
    def _get_bullets_number(text: str) -> int:
        bullet_characters = ["-", "•", "*"]
    
        lines = text.splitlines()
        bullets = []
        # get first matching bullet character
        for line in lines:
            bullet_character = next((c for c in bullet_characters if c in line), None)
            if bullet_character:
                bullet_line = line.split(bullet_character)[0]
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
    """

    unit_tests = unit_tests_from_function(
        get_bullets_number_function,
        approx_min_cases_to_cover=10,
        print_text=True
    )
