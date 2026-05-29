import sys
import os
from random import choice

# Check for required libraries
try:
    import pandas as pd
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    from twilio.rest import Client
except ImportError as e:
    print(f"❌ Missing library: {e.name}. Install it using 'pip install {e.name.lower()}'")
    sys.exit(1)

# --- Twilio Configuration (replace with your real credentials) ---
# --- Twilio Configuration (replace with your real credentials) ---
TWILIO_SID = 'AC10ea33ce3e62fc3453927a3a0b91ec98'  # Replace with your Account SID
TWILIO_TOKEN = 'a7e0d08881f81b10c6e2afaaa87dec69'  # Replace with your Auth Token
TWILIO_FROM = '+12025550123'  # e.g., +12025550123
USER_PHONE = '+918688344301'  # Replace with the target phone number

# --- Load Dataset (optional) ---
DATASET_PATH = "financial_loan_updated.xlsx"  # Adjust path as needed
data = pd.DataFrame()

if os.path.exists(DATASET_PATH):
    try:
        if DATASET_PATH.endswith('.xlsx'):
            data = pd.read_excel(DATASET_PATH)
        else:
            data = pd.read_csv(DATASET_PATH)
        print("✅ Dataset loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")

# --- Send Alert SMS ---
def send_sms_alert(msg):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=msg,
            from_=TWILIO_FROM,
            to=USER_PHONE
        )
        print("📩 Alert sent:", message.sid)
        return True
    except Exception as e:
        messagebox.showerror("SMS Error", f"Failed to send SMS: {str(e)}")
        print(f"❌ SMS failed: {e}")
        return False

# --- Fraud Detection Simulation ---
def is_document_fake():
    return choice([True, False])  # Replace with ML model later

# --- Document Upload Window ---
def ask_for_documents(parent, selected_loan):
    doc_window = tk.Toplevel(parent)
    doc_window.title(f"{selected_loan} - Upload Documents")
    doc_window.geometry("400x300")
    doc_window.transient(parent)
    doc_window.grab_set()

    uploaded_docs = {}

    def upload_file(doc_name):
        path = filedialog.askopenfilename(
            title=f"Upload {doc_name}",
            filetypes=[("PDF files", "*.pdf"), ("Image files", "*.png *.jpg *.jpeg")]
        )
        if path:
            uploaded_docs[doc_name] = path
            messagebox.showinfo("Upload Successful", f"{doc_name} uploaded successfully!")

    def submit_documents():
        if "Aadhar" not in uploaded_docs or "PAN" not in uploaded_docs:
            messagebox.showerror("Error", "Please upload both Aadhar and PAN documents.")
            return
        
        doc_window.destroy()
        if is_document_fake():
            messagebox.showerror("Fraud Detected", "Fake Document Detected! Loan Rejected.")
            send_sms_alert(f"🚨 Fraud Alert: Fake documents submitted for {selected_loan} loan.")
        else:
            messagebox.showinfo("Success", "Documents verified successfully. Loan Approved!")
            send_sms_alert(f"✅ Loan Approved: {selected_loan} loan documents verified.")

    def cancel():
        if messagebox.askyesno("Confirm", "Cancel document upload?"):
            doc_window.destroy()

    # UI elements
    ttk.Label(doc_window, text="Upload Required Documents", font=('Arial', 12)).pack(pady=10)
    ttk.Button(doc_window, text="Upload Aadhar Card", command=lambda: upload_file("Aadhar")).pack(pady=5)
    ttk.Button(doc_window, text="Upload PAN Card", command=lambda: upload_file("PAN")).pack(pady=5)
    ttk.Button(doc_window, text="Submit", command=submit_documents).pack(pady=10)
    ttk.Button(doc_window, text="Cancel", command=cancel).pack(pady=5)

# --- Loan Type Selection Window ---
def main_window():
    root = tk.Tk()
    root.title("Loan Application System")
    root.geometry("400x300")

    selected_loan = tk.StringVar()

    def proceed():
        loan = selected_loan.get()
        if loan:
            ask_for_documents(root, loan)
        else:
            messagebox.showwarning("Warning", "Please select a loan type.")

    def exit_app():
        if messagebox.askyesno("Confirm", "Exit application?"):
            root.destroy()

    # UI
    ttk.Label(root, text="Select Loan Type", font=('Arial', 14)).pack(pady=10)
    loan_dropdown = ttk.Combobox(root, textvariable=selected_loan, values=["Home Loan", "Car Loan", "Education Loan" ,"House Loan","Credit card Loan","House improvements Loan","Medical Loan","Wedding loan","Personal Loan","Medical Loan"])
    loan_dropdown.pack(pady=5)
    ttk.Button(root, text="Next", command=proceed).pack(pady=10)
    ttk.Button(root, text="Exit", command=exit_app).pack(pady=5)

    root.mainloop()

# --- Start Application ---
if __name__ == "__main__":
    main_window()


 