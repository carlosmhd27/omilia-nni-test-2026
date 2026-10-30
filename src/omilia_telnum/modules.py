from logging import getLogger
from re import match, search, findall

logger = getLogger(__name__)

def validate_phone(phone_number: int | str) -> bool:
    """
    Validates the input telephone number.
    Ensures it follows the expected format for 10-digit and 14-digit numbers.
    
    :input phone_number: The phone number to validate.
    :return: True if the phone number is valid, False otherwise.
    """
    if isinstance(phone_number, int):
        phone_number = str(phone_number)
    if not isinstance(phone_number, str):
        return False

    ## erase all spaces from the phone number string
    tel_str = "".join(phone_number.split())
    if len(tel_str) == 10:
        logger.info("Checking 10-digit number...")
        if not (tel_str.startswith(("2", "69"))):
            logger.error("Invalid telephone number.")
            return False
    elif len(tel_str) == 14:
        logger.info("Checking 14-digit number...")
        if not (tel_str.startswith(("00302", "003069"))):
            logger.error("Invalid telephone number.")
            return False
    else:
        logger.error("Invalid telephone number.")
        return False
    logger.info("Telephone number is valid.")
    return True

def is_phone_number(phone_number:str) -> bool:
    """
    Validates the input telephone number.
    Ensures it contains only digits and spaces.
    Raises a ValueError if the input is invalid.

    :input phone_number: The phone number string to validate.
    :return: True if the phone number is valid, False otherwise.
    """
    if isinstance(phone_number, int):
        phone_number = str(phone_number)
    if not phone_number:
        return False
    if not isinstance(phone_number, str):
        return False
    phone_number = phone_number.strip()
    if not match(r"^\d[\d\s]*\d$", phone_number):
        logger.error("Invalid input. Please enter a valid telephone number.")
        return False
    return True

def _check_0space_variances(phone_number: str | int) -> list[str]:
    """
    Checks for 0-space variances in the telephone number.
    0-space variances refer to occurrences where a '0' is followed
    by one or more spaces and then a digit.

    Example:
        Input: "1 2 30 4 5 60 7 8 9"
        Output: [
        "1 2 30 4 5 60 7 8 9",
        "1 2 3 4 5 60 7 8 9",
        "1 2 30 4 5 6 7 8 9",
        "1 2 3 4 5 6 7 8 9"
        ]
    
    :input phone_number: The phone number string to check for 0-space variances.
    :return: A list of phone number variants with 0-space variances resolved.
    """
    if not phone_number:
        raise TypeError("Phone number cannot be empty.")
    if isinstance(phone_number, int):
        phone_number = str(phone_number)
    if not isinstance(phone_number, str):
        raise TypeError("Phone number must be a string.")

    logger.info(f"Checking for 0-space variances phone number {phone_number}")
    variants = {phone_number}

    find_zero_space = search(r"\d0\s+\d[\s|$]+", phone_number)
    if not find_zero_space:
        logger.info("No 0-space variance detected after initial search.")
        return [phone_number]
    # i is set to prevent infinite loops in case of unexpected input patterns.
    logger.info(f"0-space variance detected: '0' followed by space and digit found at position \
                {find_zero_space.start()} till {find_zero_space.end()}")

    # Extract the prefix up to and including the '0' before the space and digit.
    # We want to separate the number as prefix and suffix and keep iteracting 
    # over the suffix to check for further 0-space variances.
    # Example:
    # Input: "1 2 30 4 5 60 7 8 9"
    # Prefix variants: ["1 2 30", "1 2 3"]
    # Suffix to check: "4 5 60 7 8 9"
    # the prefix starts from the beginning of the phone number up to
    # and including the '0' before the space and digit.
    prefix_variance = phone_number[:find_zero_space.start() + 2]
    # The suffix goes till the number after the '0' and space sequence.
    suffix_to_check = phone_number[find_zero_space.end()-2:]
    print(f"Prefix variance: {prefix_variance}")
    print(f"Suffix to check: {suffix_to_check}")

    # Create list of all possible prefixes
    # if prefix 10 -> ["10", "1"]
    # if prefix 100 -> ["100", "10", "1"] and so on.
    prefixes = [prefix_variance]
    while prefix_variance.endswith("0"):
        prefix_variance = prefix_variance[:-1]
        prefixes.append(prefix_variance)
    print(f"Prefixes generated: {prefixes}")
    # convert prefix into a set to remove duplicates.
    prefixes = set(prefixes)

    # we then check the suffix for further 0-space variances recursively.
    # Following the example:
    # New prefix to check: ["4 5 60", "4 5 6"]
    # New suffix to check: "7 8 9"
    suffix_variant = _check_0space_variances(suffix_to_check)
    for suffix in suffix_variant:
        for prefix in prefixes:
            new_variant = prefix + " " + suffix
            logger.info(f"New variant created: {new_variant}")
            print(f"New variant created: {new_variant}")
            variants.add(new_variant)

    # We combine the new variants with the existing ones
    # Following the example:
    # Existing variants (only by checking prefix):
    #       ["1 2 30 4 5 60 7 8 9", "1 2 3 4 5 60 7 8 9"]
    # New variants (after checking suffix for new iteractions):
    #       ["1 2 30 4 5 6 7 8 9", "1 2 3 4 5 6 7 8 9"]

    logger.info("0-space variance check complete.")
    return list(variants)



def _check_2digits_variances(phone_number: str) -> list[str]:
    """
    Checks for 2-digits variances in the phone number.

    Example:
        Input: "1 23 4"
        Output: ["1 23 4", "1 203 4"]

    :input phone_number: The phone number string to check for 2-digits variances.
    :return: A list of phone number variants with 2-digits replaced by 2-digits with
        a 0 inserted where applicable.
    """
    if not phone_number:
        raise TypeError("Phone number cannot be empty.")
    if not isinstance(phone_number, str):
        raise TypeError("Phone number must be a string.")
    if not is_phone_number(phone_number):
        raise ValueError("Invalid phone number.")

    
    variants = {phone_number}
    if search(r"\s\d\d\s", phone_number):
        print("2-digits variance detected.")
        for match in findall(r"\s(\d[1-9])\s", phone_number):
            print(f"2-digits match found: {match}")
            logger.info(f"Adding a 0 to the 2-digits match '{match}' in phone number.")
            replace = match[0] + "0" + match[1]
            variants.add(phone_number.replace(match, replace))

    return list(variants)

def check_ambiguities(phone_number: str) -> list[str]:

    """
    Checks for ambiguities in the phone number by considering international and national prefixes,
    as well as 0-space and 2-digits variances.

    Example:
        Input: "0030 69 10 2 3 45 6 7 8"
        Output: [
                "0030 69 10 2 3 45 6 7 8",
                "0030 69 1 2 3 45 6 7 8",
                "0030 69 10 2 3 405 6 7 8",
                "0030 69 1 2 3 405 6 7 8"
                ]

    :input phone_number: The phone number string to check for ambiguities.
    :return: A list of phone number variants with ambiguities resolved.
    """

    logger.info(f"Starting ambiguity check for phone number: {phone_number}")
    if not phone_number:
        logger.error("Phone number cannot be empty.")
        raise TypeError("Phone number cannot be empty.")
    if not isinstance(phone_number, str):
        logger.error("Phone number must be a string.")
        raise TypeError("Phone number must be a string.")
    if not is_phone_number(phone_number):
        logger.error("Invalid phone number.")
        raise ValueError("Invalid phone number.")

    logger.info("Checking for ambiguities in the telephone number...")
    prefix = ""
    number = phone_number
    ## find international prefix "0030"
    find_inter_prefix = search(r"^0\s*0\s*3\s*0", phone_number)
    if find_inter_prefix:
        logger.info(f"prefix detected: '0030' found in position {find_inter_prefix.start()} till {find_inter_prefix.end()}")
        prefix = find_inter_prefix.group() + " "
        number = phone_number[find_inter_prefix.end():].strip()

    ## find national prefix "69" and "2"
    find_nat_prefix = search(r"^(6\s*9|2)", number)
    if find_nat_prefix:
        logger.info(f"national prefix detected: '{find_nat_prefix.group()}' found in position {find_nat_prefix.start()} till {find_nat_prefix.end()}")
        prefix += find_nat_prefix.group() + " "
        number = number[find_nat_prefix.end():].strip()
    logger.info(f"Prefix: {prefix}")
    logger.info(f"Number after prefix removal: {number}")

    ## check for 0-space variances in the remaining number
    variants = _check_0space_variances(number)
    logger.info(f"Variants after 0-space variance check: {len(variants)}")

    ## Add 2-digits variances to the existing variants
    for variant in variants.copy():
            logger.info(f"Checking 2 digits variances for variant: {variant}")
            variants += _check_2digits_variances(variant)
    logger.info("Ambiguity check completed.")
    variants = list({prefix + variant for variant in variants})
    return variants


