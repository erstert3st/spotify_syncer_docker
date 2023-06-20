class captcha_solved_Except(Exception):
    def __str__(self):
        return "Solved Captcha once, wait till next Execution"