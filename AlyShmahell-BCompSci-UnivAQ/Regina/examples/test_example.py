import os

if __name__ == '__main__':
    os.system(f"cd {os.path.dirname(os.path.realpath(__file__))} && cd .. && composer install")
    os.system(f"cd {os.path.dirname(os.path.realpath(__file__))} && php example.php")