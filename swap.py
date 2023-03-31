import argparse, enum, re, random
"""
Author: Emily Gao
About: Written for the purpose of classifying variable values and replacing them
NOTE: A portion of the identify code was written by Emily Gao for another open-source project
"""

class Data_Types(enum):

    def __init__():
        pass

    def identify(self, value):
        if value and value != '':
            split_by_dot = re.split('[./]', value) # splits by dots or slashes
            # check if it's valid CIDR or IP address
            if len(split_by_dot) <= 5 and not re.search('[a-zA-Z]', value) and all(0 <= int(i) and int(i) <= 255 for i in split_by_dot): # can cast to int because check for alpha has to pass first
                if value.count('/') == 1 and len(split_by_dot) == 5 and 0 <= int(split_by_dot[-1]) and int(split_by_dot[-1]) <= 32: # check if is CIDR range
                    return self.CIDR
                elif len(split_by_dot) == 4:
                    return self.IP
            # check if it's a valid CVE
            split_by_dash = value.split("-")
            if len(split_by_dash) == 3 and split_by_dash[0].upper() == "CVE" and (split_by_dash[1].isdigit() and len(split_by_dash[1]) == 4) and split_by_dash[2].isdigit(): # NOTE: assumes a valid year has exactly 4 digits due to overwehelming nature of currently known existing CVEs
                return self.CVE
            # check if it's a valid delimited integer (which is not a CIDR or IP address)
            # must have only digits and valid delimiters, and no alphabet characters
            contains_valid_delims = bool(re.search('[0-9.,-_:\/\{\}\|()\\]', value))
            does_not_contain_alpha = not bool(re.search('[a-zA-Z]', value))
            if contains_valid_delims and does_not_contain_alpha:
                return self.DELIMITED_INT
            # check if it's a valid id (TODO: need more input from Hava)
            # check if it's a valid hash (hexadecimal)
            try:
                test_hash = int(value, '16') # attempt converting to int (Python handles erroring)
                return self.HASH
            except ValueError:
                pass
        return self.MISMATCH

    def replace_ip(value):
        # TODO: Argue whether we need to generate a different random valid IP each time
        return "255.255.255.255"

    def replace_cidr(value):
        # TODO: Argue whether we need to generate a different random valid IP each time
        # NOTE: If so, need to randomize netmask as well
        pass
    
    def random_digits_generator(self, num_digits=None):
        digits = ""
        if num_digits == None:
            num_digits = random.randint(4, 7) # trailing digits of CVE can have more than 7 digits but we will set limit
        for i in range(num_digits):
            digits += str(random.randint(0, 9)) # unlike usual, this is inclusive of 9
        return digits
        
    def replace_cve(self, value): # TODO: Should this be a valid CVE? should length of it remain the same? should CVE stay capitalized or undercased?
        #return f"CVE-{self.random_digits_generator(4)}-{self.random_digits_generator()}"
        split_by_dash = value.split("-")
        return f"{split_by_dash[0]}-{self.random_digits_generator(len(split_by_dash[1]))}-{self.random_digits_generator(len(split_by_dash[2]))}"

    def replace_del_int(value):
        for i in range(len(value)):
            
        pass

    def replace_id(value):
        pass

    def replace_hash(value): # TODO: should length of hash remain the same?
        pass

    # ENUM to FUNC mappings
    IP = replace_ip
    CIDR = replace_cidr
    CVE = replace_cve
    DELIMITED_INT = replace_del_int # phone numbers and SSNs
    ID = replace_id
    HASH = replace_hash
    MISMATCH = None

def swap(to_swap):
    for value in to_swap:
        

def main(args):
    to_swap = []
    if args.input:
        with open(args.input, "r") as infile:
            to_swap = []
    if 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=None, help="Name of input file.")
    parser.add_argument("-o", "--output", default="swapped_values", help="Name of output file.")
    args = parser.parse_args()
    main(args)