from dotenv import load_dotenv
import UI.login as login
load_dotenv(dotenv_path="infomation.env")
login.create_login_window()


