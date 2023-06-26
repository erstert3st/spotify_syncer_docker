class captcha_solved_except(Exception):
    def __str__(self):
        return "Solved Captcha once, wait till next Execution"
    
class no_login_data(Exception):
    def __str__(self):
        return "add File or set ENV!"

class button_not_found(Exception):
    def __str__(self):
        return "element could not be found"