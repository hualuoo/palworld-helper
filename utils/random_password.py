import string
import random


def random_string():
    data = string.ascii_letters + string.digits
    random_length = random.randint(12, 16)
    new_password = ''.join(random.sample(data, random_length))
    return new_password
