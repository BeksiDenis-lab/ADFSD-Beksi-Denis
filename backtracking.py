import hashlib
import string
import time


def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


class PasswordCracker:
    def __init__(self, target_hash):
        self.target_hash = target_hash
        self.password_length = 6
        self.uppercase_letters = list(string.ascii_uppercase)  # A-Z
        self.lowercase_letters = list(string.ascii_lowercase)  # a-z
        self.digits = list(string.digits)  # 0-9
        self.special_chars = ['!', '@', '#', '$']
        self.recursive_calls = 0
        self.solution_found = False
        self.solution = None

    def backtrack(self, current_password, uppercase_count, lowercase_count, digit_count, special_count):

        self.recursive_calls += 1


        if self.solution_found:
            return


        if len(current_password) == self.password_length:

            if (uppercase_count == 1 and lowercase_count == 3 and
                    digit_count == 1 and special_count == 1):

                password_str = ''.join(current_password)
                if get_hash(password_str) == self.target_hash:
                    self.solution_found = True
                    self.solution = password_str
            return


        if uppercase_count < 1:
            for char in self.uppercase_letters:
                current_password.append(char)
                self.backtrack(current_password, uppercase_count + 1, lowercase_count, digit_count, special_count)
                if self.solution_found:
                    return
                current_password.pop()

        # Try adding a lowercase letter
        if lowercase_count < 3:
            for char in self.lowercase_letters:
                current_password.append(char)
                self.backtrack(current_password, uppercase_count, lowercase_count + 1, digit_count, special_count)
                if self.solution_found:
                    return
                current_password.pop()


        if digit_count < 1:
            for char in self.digits:
                current_password.append(char)
                self.backtrack(current_password, uppercase_count, lowercase_count, digit_count + 1, special_count)
                if self.solution_found:
                    return
                current_password.pop()


        if special_count < 1:
            for char in self.special_chars:
                current_password.append(char)
                self.backtrack(current_password, uppercase_count, lowercase_count, digit_count, special_count + 1)
                if self.solution_found:
                    return
                current_password.pop()

    def find_password(self):
        start_time = time.time()
        self.backtrack([], 0, 0, 0, 0)
        end_time = time.time()

        if self.solution_found:
            print(f"Parola găsită: {self.solution}")
            print(f"Număr apeluri recursive: {self.recursive_calls}")
            print(f"Timp de execuție: {end_time - start_time:.2f} secunde")
        else:
            print("Parola nu a fost găsită.")



target_hash = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"


cracker = PasswordCracker(target_hash)
cracker.find_password()