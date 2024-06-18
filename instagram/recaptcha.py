from twocaptcha import TwoCaptcha
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# 105.29.165.242

api_key = "33b2bba01bbbfaa76c0d9e7f7b47f3c3"
server = "http://www.botmasterlabs.net/"

solver = TwoCaptcha(api_key, server=server)

try:
    result = solver.recaptcha(
        sitekey='6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u',
        url='https://2captcha.com/demo/recaptcha-v2',
    )

except Exception as e:
    sys.exit(e)

else:
    sys.exit('solved: ' + str(result))
