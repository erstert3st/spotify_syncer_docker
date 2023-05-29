class captchaSolvedExcept(Exception):
    def __str__(self):
        return "Solved Captcha wait till next Execution"