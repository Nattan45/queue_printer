# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# from escpos.printer import Usb
# import usb.core
# import usb.util

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Set your printer's USB Vendor ID and Product ID
# VENDOR_ID = 0x0FE6  # Your printer's Vendor ID
# PRODUCT_ID = 0x811E  # Your printer's Product ID

# try:
#     # Try to initialize the printer
#     printer = Usb(VENDOR_ID, PRODUCT_ID, timeout=0)  # timeout=0 prevents hanging issues
#     print("✅ Printer connected successfully!")
# except Exception as e:
#     print(f"❌ Printer connection failed: {e}")
#     printer = None  # Set printer to None if initialization fails

# @app.route("/print", methods=["POST"])
# def print_ticket():
#     if not printer:
#         print("❌ Printer not connected")
#         return jsonify({"error": "Printer not connected"}), 500

#     print("✅ Print request received!")
    
#     data = request.json
#     ticket_number = data.get("ticketNumber", "0000")
#     company_name = data.get("companyName", "Unknown Company")
#     created_at = data.get("createdAt", "Unknown Date")

#     try:
#         printer.text("\n====================\n")
#         printer.set(align="center", bold=True)
#         printer.text("Your Ticket\n")
#         printer.set(align="left", bold=False)
#         printer.text(f"Company: {company_name}\n")
#         printer.text(f"Ticket No: {ticket_number}\n")
#         printer.text(f"Printed At: {created_at}\n")
#         printer.text("====================\n\n")
#         printer.cut()
        
#         print("✅ Ticket printed successfully!")
#         return jsonify({"message": "Ticket printed successfully"})

#     except Exception as e:
#         print(f"❌ Print Error: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)








from flask import Flask, request, jsonify
from flask_cors import CORS
from escpos.printer import Usb
import usb.core
import usb.util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your printer's USB Vendor ID and Product ID
VENDOR_ID = 0x0FE6  # Your printer's Vendor ID
PRODUCT_ID = 0x811E  # Your printer's Product ID

def initialize_printer():
    # Use usb.core to find the printer
    printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if printer is None:
        raise Exception("Printer not found")
    
    # Detach the kernel driver if necessary
    if printer.is_kernel_driver_active(0):
        printer.detach_kernel_driver(0)

    # Set the active configuration
    printer.set_configuration()
    
    return Usb(VENDOR_ID, PRODUCT_ID, timeout=0)  # Initialize escpos printer

try:
    printer = initialize_printer()
    print("✅ Printer connected successfully!")
    
    # Auto-print a test receipt when the server starts
    printer.text("\n====================\n")
    printer.set(align="center", bold=True)
    printer.text("Server Started!\n")
    printer.set(align="left", bold=False)
    printer.text("Flask print server is running.\n")
    printer.text("Listening on port 5001...\n")
    printer.text("====================\n\n")
    printer.cut()
    print("✅ Test receipt printed on startup!")

except Exception as e:
    print(f"❌ Printer connection failed: {e}")
    printer = None  # Set printer to None if initialization fails

@app.route("/print", methods=["POST"])
def print_ticket():
    if not printer:
        print("❌ Printer not connected")
        return jsonify({"error": "Printer not connected"}), 500

    print("✅ Print request received!")
    
    data = request.json
    ticket_number = data.get("ticketNumber", "0000")
    company_name = data.get("companyName", "Unknown Company")
    created_at = data.get("createdAt", "Unknown Date")

    try:
        printer.text("\n====================\n")
        printer.set(align="center", bold=True)
        printer.text("Your Ticket\n")
        printer.set(align="left", bold=False)
        printer.text(f"Company: {company_name}\n")
        printer.text(f"Ticket No: {ticket_number}\n")
        printer.text(f"Printed At: {created_at}\n")
        printer.text("====================\n\n")
        printer.cut()
        
        print("✅ Ticket printed successfully!")
        return jsonify({"message": "Ticket printed successfully"})

    except Exception as e:
        print(f"❌ Print Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
