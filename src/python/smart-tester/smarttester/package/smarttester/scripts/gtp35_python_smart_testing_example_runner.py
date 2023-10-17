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

    unit_tests = unit_tests_from_function(
        example_function,
        approx_min_cases_to_cover=10,
        print_text=True
    )
