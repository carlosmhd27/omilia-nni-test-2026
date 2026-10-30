import streamlit as st

from src import check_ambiguities, is_phone_number, validate_phone

st.title("Omilia Telephone Number App")

phone_number = st.text_input("Enter your telephone number (only digits and spaces):").strip()
if phone_number and is_phone_number(phone_number):
    st.write(f"You entered: {phone_number}")
    table = {"Interpretation": [], "Clean": [], "Valid": []}
    variants = check_ambiguities(phone_number)
    for i, variant in enumerate(variants):
        clean_phone = "".join(variant.split())
        valid = "VALID" if validate_phone(clean_phone) else "INVALID"
        st.write(f"Variant {i + 1}: {variant} (Clean: {clean_phone}) - {valid}")
        table["Interpretation"].append(i + 1)
        table["Clean"].append(clean_phone)
        table["Valid"].append(valid)
    st.write("Summary Table:")
    st.table(table)

else:
    st.write("Invalid telephone number. Please enter a valid number with only digits and spaces.")
