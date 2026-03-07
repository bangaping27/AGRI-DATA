from fake_useragent import UserAgent

ua = UserAgent()

def get_random_user_agent():
    return ua.random
