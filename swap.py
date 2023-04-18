import argparse, re, random, os, string
"""
Author: Emily Gao
About: Written for the purpose of classifying variable values and replacing them
NOTE: A portion of the identify code was written by Emily Gao for another open-source project
"""

class Data_Types():

    def identify(self, value):
        if value and value != '':
            split_by_dot = re.split('[./]', value) # splits by dots or slashes
            # check if it's valid CIDR or IP address
            try:
                if len(split_by_dot) <= 5 and not re.search('[a-zA-Z]', value) and all(0 <= int(i) and int(i) <= 255 for i in split_by_dot): # can cast to int because check for alpha has to pass first
                    if value.count('/') == 1 and len(split_by_dot) == 5 and 0 <= int(split_by_dot[-1]) and int(split_by_dot[-1]) <= 32: # check if is CIDR range
                        return self.CIDR(value)
                    elif len(split_by_dot) == 4:
                        return self.IP(value)
            except:
                pass # continue on, try-except counters issues with parsing delimited integers
            # check if it's a valid CVE
            split_by_dash = value.split("-")
            if len(split_by_dash) == 3 and split_by_dash[0].upper() == "CVE" and (split_by_dash[1].isdigit() and len(split_by_dash[1]) == 4) and split_by_dash[2].isdigit(): # NOTE: assumes a valid year has exactly 4 digits due to overwehelming nature of currently known existing CVEs
                return self.CVE(value)
            # check if it's a valid delimited integer (which is not a CIDR or IP address)
            # must have only digits and valid delimiters, and no alphabet characters
            contains_valid_delims = re.search('[\.,-_:\/\{\}\|\(\)\[\]\\\]', value)
            one_case_or_other = (value.upper() == value) or (value.lower() == value) # we cannot allow mixed case, that is invalid hex
            not_contain_invalid_alpha = not re.search('[g-zG-Z]', value) # cannot fall within valid definition of delimited numbers
            if one_case_or_other and not_contain_invalid_alpha: # and contains_valid_delims: TODO: Do we even need to check for delimiters?
                return self.DELIMITED_NUM(value)
            # check if it's a valid hash (hexadecimal)
            try:
                test_hash = int(value, 16) # attempt converting to int (Python handles erroring)
                return self.HASH(value)
            except ValueError:
                pass
        return self.MISMATCH

    def replace_ip(self, value):
        # TODO: Argue whether we need to generate a different random valid IP each time
        return "255.255.255.255"

    def replace_cidr(self, value):
        # TODO: Argue whether we need to generate a different random valid IP each time
        # NOTE: If so, need to randomize netmask as well
        return "255.255.255.255/0"

    def random_hex_generator(self, num_digits=None, start_with_0x=False, contains_upcase=False):
        digits = ""
        hex_alphabet = "1234567890abcdef"
        if start_with_0x:
            digits += "0x"
        if num_digits < 1:
            return ValueError("Must generate at least one random digit.")
        for i in range(num_digits):
            digits += hex_alphabet[random.randint(0,15)]
        if contains_upcase:
            return digits.upper()
        return digits
    
    def random_digits_generator(self, num_digits=None):
        digits = ""
        if num_digits == None:
            num_digits = random.randint(4, 7) # trailing digits of CVE can have more than 7 digits but we will set limit
        if num_digits < 1:
            return ValueError("Must generate at least one random digit.")
        for i in range(num_digits):
            digits += str(random.randint(0, 9)) # unlike usual, this is inclusive of 9
        return digits
        
    def replace_cve(self, value): # TODO: Should this be a valid CVE? should length of it remain the same? should CVE stay capitalized or undercased?
        #return f"CVE-{self.random_digits_generator(4)}-{self.random_digits_generator()}"
        split_by_dash = value.split("-")
        return f"{split_by_dash[0]}-{self.random_digits_generator(len(split_by_dash[1]))}-{self.random_digits_generator(len(split_by_dash[2]))}"

    def replace_del_num(self, value):
        new_val = ""
        hex_alpha_present = re.search('[a-fA-F]', value) # strong indicator value contains hex (but still chance its an int, cannot tell 100%)
        for i in range(len(value)):
            if re.search('[0-9a-fA-F]', value[i]): # is a numeric digit
                if hex_alpha_present:
                    new_val += self.random_hex_generator(1) # can include a-fA-F
                else:
                    new_val += self.random_digits_generator(1) # cannot include a-fA-F
            else: # is a delimiter
                new_val += value[i]
        return new_val

    def replace_hash(self, value): # TODO: should length of hash remain the same? Yes. if non-zero, stay non-zero?
        if len(value) > 2 and value.startswith("0x"):
            return self.random_hex_generator(len(value[2:]), True)
        else:
            return self.random_hex_generator(len(value))

    # ENUM to FUNC mappings
    IP = replace_ip
    CIDR = replace_cidr
    CVE = replace_cve
    DELIMITED_NUM = replace_del_num # phone numbers and SSNs
    HASH = replace_hash
    MISMATCH = None

    def main(self):
        #print(self.identify("1-\555")) # make sure to test 1-\\555\-555-5555 vs 1-\555\-555-5555
        #print(self.identify("2500995745"))
        pass

def swap(to_swap):
    types = Data_Types()
    swapped = []
    for value in to_swap:
        swap = types.identify(value.strip())
        if swap == Data_Types.MISMATCH:
            swapped.append(value)
        else:
            swapped.append(swap)
    return swapped

# def file_precheck(name):
#     invalid = True
#     while invalid:
#         if os.path.exists(f"{os.getcwd()}/{name}"):
#             delete = input("Output file already exists, delete file first? [Y/n]")
#             if delete.lower() == "y":
#                 os.remove(f"{os.getcwd()}/{name}")
#                 invalid = False
#             else:
#                 name = input(f"{'Input invalid. ' if delete.lower() != 'n' else ''}Please specify alternative filename.")
#         else:
#             return None

def main(args):
    to_swap = []
    if args.infile:
        if args.infile.endswith(".csv"):
            with open(args.infile, "r") as infile:
                to_swap = infile.readlines()
        else:
            print("Input file must be of type csv, please try again.")
            return

    outfile_name = f"{args.infile[:-4]}_swapped.csv"

    if len(to_swap) > 0:
        swapped = swap(to_swap)
        #file_precheck(args.outfile) # TODO
        os.remove(f"{os.getcwd()}/{outfile_name}")
        with open(outfile_name, "a") as outfile:
            for swapped_val in swapped:
                outfile.write(f"{swapped_val}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", help="Name of input csv file.")
    #parser.add_argument("-o", "--outfile", default=None, help="Name of output csv file.")
    args = parser.parse_args()
    main(args)