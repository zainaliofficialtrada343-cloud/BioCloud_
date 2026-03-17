from fpdf import FPDF
from settings_config import LAB_DETAILS
import base64

# --- 1. THERMAL RECEIPT GENERATOR (Small Size) ---
def generate_receipt_pdf(v):
    """
    v: List of patient data [ID, Invoice, Date, Name, Mobile, Age, Gender, Collected, Test, Total, Paid, Rem, ...]
    """
    pdf = FPDF(format=(80, 150)) # Thermal Printer Size
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 6, f"{LAB_DETAILS['name']}", ln=True, align='C')
    pdf.set_font("Arial", '', 7)
    pdf.cell(0, 4, f"{LAB_DETAILS['address']}", ln=True, align='C')
    pdf.cell(0, 4, f"Contact: {LAB_DETAILS['phone']}", ln=True, align='C')
    
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(0, 5, "PATIENT RECEIPT", border='TB', ln=True, align='C')
    
    # Patient Info
    pdf.ln(2)
    pdf.set_font("Arial", '', 7)
    pdf.cell(30, 4, f"Inv #: {v[1]}")
    pdf.cell(0, 4, f"Date: {v[2]}", align='R', ln=True)
    pdf.cell(30, 4, f"Name: {v[3]}")
    pdf.cell(0, 4, f"Age/Sex: {v[5]}/{v[6]}", align='R', ln=True)
    
    # Tests Table
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 7)
    pdf.cell(45, 5, "Test Description", border='B')
    pdf.cell(15, 5, "Rate", border='B', align='R', ln=True)
    
    pdf.set_font("Arial", '', 7)
    tests_list = str(v[8]).split(", ")
    total_bill = float(v[9])
    rate_per = total_bill / len(tests_list) if len(tests_list) > 0 else 0
    
    for t in tests_list:
        pdf.cell(45, 5, t)
        pdf.cell(15, 5, f"{rate_per:.0f}", align='R', ln=True)
    
    # Totals
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(45, 5, "TOTAL BILL:")
    pdf.cell(15, 5, f"Rs. {v[9]}", align='R', ln=True)
    pdf.cell(45, 5, "PAID AMOUNT:")
    pdf.cell(15, 5, f"Rs. {v[10]}", align='R', ln=True)
    pdf.cell(45, 5, "BALANCE DUES:", border='T')
    pdf.cell(15, 5, f"Rs. {v[11]}", border='T', align='R', ln=True)
    
    # Footer
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 6)
    pdf.cell(0, 3, f"Developed by {LAB_DETAILS['developer']}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 2. PROFESSIONAL LAB REPORT (A4 Size) ---
def generate_lab_report_pdf(p_data, results_list):
    """
    p_data: Dataframe row of patient
    results_list: List of dicts [{'name': 'Hb', 'val': '12', 'range': '13-17', 'unit': 'g/dL'}]
    """
    pdf = FPDF() # Default A4
    pdf.add_page()
    
    # Professional Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(20, 80, 160) # Blue color
    pdf.cell(0, 12, f"{LAB_DETAILS['name']}", ln=True, align='C')
    
    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"{LAB_DETAILS['address']} | {LAB_DETAILS['phone']}", ln=True, align='C')
    pdf.line(10, 35, 200, 35)
    
    # Patient Summary Box
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Patient Name:")
    pdf.set_font("Arial", '', 10)
    pdf.cell(70, 7, f"{p_data['Name']}")
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Invoice #:")
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 7, f"{p_data['Invoice']}", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Age / Gender:")
    pdf.set_font("Arial", '', 10)
    pdf.cell(70, 7, f"{p_data['Age']} / {p_data['Gender']}")
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 7, "Date:")
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 7, f"{p_data['Date']}", ln=True)
    
    pdf.line(10, 55, 200, 55)
    pdf.ln(10)

    # Table Header
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 10, " TEST DESCRIPTION", 1, 0, 'L', True)
    pdf.cell(40, 10, " RESULT", 1, 0, 'C', True)
    pdf.cell(40, 10, " UNIT", 1, 0, 'C', True)
    pdf.cell(40, 10, " NORMAL RANGE", 1, 1, 'C', True)
    
    # Data Rows
    pdf.set_font("Arial", '', 10)
    for res in results_list:
        pdf.cell(70, 9, f" {res['name']}", 1)
        pdf.set_font("Arial", 'B', 10) # Result bold
        pdf.cell(40, 9, f" {res['val']}", 1, 0, 'C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(40, 9, f" {res['unit']}", 1, 0, 'C')
        pdf.cell(40, 9, f" {res['range']}", 1, 1, 'C')
        
    # Footer
    pdf.set_y(-40)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 5, "This is a computer generated report and does not require signature.", ln=True, align='C')
    pdf.cell(0, 5, f"Report developed by {LAB_DETAILS['developer']}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')