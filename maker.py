# maker.py - Run this to create your massive test_ranges.py
all_tests = [
    "DLC", "RBCCount", "Eosinophil Count", "Platelet Count", "BT", "CT", "ESR", 
    "PCV Hematocrit", "Complete Hemogram", "PBF for Type of Anemia", "Blood Grouping",
    "PT INR", "APTT", "G6PD", "Reticulocyte count", "d-Dimer", "Urine Sugar", 
    "Urine ALBUMIN", "Bile Salts", "Bile Pigments", "Urinary pH", "SEMEN Analysis",
    "FNAC", "PAP Smear", "Bacterial Culture", "CRP", "WIDAL", "HCV Card", "HBsAg",
    "HIV card", "HbA1C", "TSH", "fT3", "fT4", "S. Creatinine", "S. Bilirubin Total",
    "Vitamin B12", "Vitamin D", "LFT", "RFT", "Lipid Profile" 
    # ... and all others from your list
]

content = "MASTER_TEST_DATA = {\n"
for test in all_tests:
    content += f'    "{test}": [{{"name": "{test}", "range": "See Lab Standard", "unit": "N/A"}}],\n'
content += "}"

with open("test_ranges.py", "w") as f:
    f.write(content)
print("File 'test_ranges.py' has been created with all tests!")