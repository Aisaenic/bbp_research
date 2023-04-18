# import string, random

# def random_hex_generator(num_digits=None, start_with_0x=False, contains_upcase=False):
#         digits = ""
#         hex_alphabet = "1234567890abcdef"
#         if start_with_0x:
#             digits += "0x"
#         if num_digits < 1:
#             return ValueError("Must generate at least one random digit.")
#         for i in range(num_digits):
#             digits += hex_alphabet[random.randint(0,15)]
#         if contains_upcase:
#              return digits.upper()
#         return digits

value = "0c:eb:c3:d4:eZ:56"
# split_by_colon = value.split(":")
# hex_digits = set(string.hexdigits)
# split_digits = "".join(split_by_colon)
# if len(split_by_colon) == 6 and all(dig in hex_digits for dig in split_digits):
#     self.random_hex_generator(12, False, bool(re.match('[A-F]')))
import re
one_case_or_other = (value.upper() == value) or (value.lower() == value)
print(one_case_or_other)