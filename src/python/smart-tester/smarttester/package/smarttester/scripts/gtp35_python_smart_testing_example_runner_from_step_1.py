from smarttester.service.multi_prompt_python_smart_tester import unit_tests_from_function

if __name__ == "__main__":
    sum_function = """
    def sum(a: int, b: int) -> int:
        return a + b
    """

    unit_tests = unit_tests_from_function(
        sum_function,
        approx_min_cases_to_cover=10,
        print_text=True,
        continue_from_step=1,
        source_data_dir="1697881152460-sum"
    )
