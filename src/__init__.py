from omilia_telnum import check_ambiguities, is_phone_number, validate_phone

if __name__ == "__main__":
    import sys
    from logging import INFO, basicConfig, getLogger
    from time import time
    basicConfig(level=INFO)
    logger = getLogger(__name__)
    check_phone = "0030 69 10 2 3 4 5 60 7 8"
    if not is_phone_number(check_phone):
        logger.error("Invalid phone number format.")
        sys.exit(1)
    tic = time()
    variants = check_ambiguities(check_phone)
    print(f"Original telephone number: {check_phone}")
    for i, variant in enumerate(variants):
        clean_phone = "".join(variant.split())
        valid = "VALID" if validate_phone(clean_phone) else "INVALID"
        print(f"Variant {i+1}: {variant} (Clean: {clean_phone}) - {valid}")
    toc = time()
    print(f"Time taken: {toc - tic} seconds")