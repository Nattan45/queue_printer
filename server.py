from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import win32print
import win32ui
import win32con

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get Default Printer Name
printer_name = win32print.GetDefaultPrinter()
print(f"🖨️ Default Printer: {printer_name}")



@app.route('/print', methods=['POST'])
def print_ticket():
    try:
        data = request.json
        ticket_number = data.get("ticketNumber", "0000")
        company_name = data.get("companyName", "Unknown Organization")
        service_name = data.get("serviceName", "Unknown ")
        created_at = data.get("createdAt", "Unknown Time")

        print(ticket_number, company_name, service_name, created_at)

        # Open printer
        hprinter = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(hprinter, 2)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)

        # ✅ Set Paper Size for 80mm Thermal Printer
        pdc.SetMapMode(win32con.MM_TWIPS)  # Scale to printer DPI
        pdc.StartDoc("Ticket Print")
        pdc.StartPage()

        # ✅ Create Bold, Regular Font
        font_regular = win32ui.CreateFont({
            "name": "Arial",
            "height": 250,  # Font size (twips, 1/1440 inch)
            "weight": 600,  # Bold text
        })
        pdc.SelectObject(font_regular)

        # ✅ Adjust Printing Coordinates (Ensure everything fits)
        x = 100  # X position (left margin)
        y = 100  # Y position (start from top)

        line_height = -350  # Adjust spacing (negative moves down)

        pdc.TextOut(x, y, "==============================")
        y += line_height
        pdc.TextOut(x, y, "                        MESOB Ticket           ")
        y += line_height
        pdc.TextOut(x, y, f"Ticket: {ticket_number}")
        y += line_height

        # Change font size for the specific line to make it bigger
        font_large = win32ui.CreateFont({
            "name": "Arial",
            "height": 400,  # Larger font size (twips)
            "weight": 600,  # Bold text
        })
        pdc.SelectObject(font_large)

        # Print the specific line with large font
        pdc.TextOut(x, y, f"Number: {ticket_number.split('-')[-1]}")
        y += line_height

        # Revert to the regular font for the rest of the ticket
        pdc.SelectObject(font_regular)

        # Print Organization Name
        pdc.TextOut(x, y, f"Orgainzation: {company_name}")
        y += line_height

        pdc.TextOut(x, y, f"Service Name: {service_name}")
        y += line_height

        

        pdc.TextOut(x, y, f"Printed at: {created_at}")
        y += line_height
        pdc.TextOut(x, y, "==============================")

        # ✅ End Print Job
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

        return jsonify({"message": "✅ Printed Successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3033, debug=True)
