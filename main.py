"""
=============================================================================
PrintBai - Main PyScript Logic & Event-Driven Handlers
School Project: Business + Event-Driven Programming
Target: Runs directly in the browser via PyScript / Pyodide

Key Demonstrations:
1. Event-Driven Architecture (Click, Input, Change, Submit events)
2. State Synchronization between Service Cards, Calculator, and Order Form
3. Live reactive price calculation as user types/selects
4. Robust form validation in pure Python with inline error updates
=============================================================================
"""

import re
from pyscript import document, window, when

# ---------------------------------------------------------------------------
# Business Pricing Constants (PrintBai Student Rates)
# ---------------------------------------------------------------------------
RATE_BW = 2.00        # ₱2.00 per page for Black & White
RATE_COLOR = 5.00     # ₱5.00 per page for Colored
DOUBLE_SIDED_DISCOUNT = 0.00  # 1 sheet = 2 pages, pricing per printed page


# ---------------------------------------------------------------------------
# Helper DOM Utilities
# ---------------------------------------------------------------------------
def get_el(selector):
    """Retrieve an element safely from the document."""
    return document.querySelector(selector)


def set_text(selector, text):
    """Update textContent of an element safely."""
    el = get_el(selector)
    if el:
        el.textContent = str(text)


def set_html(selector, html_content):
    """Update innerHTML of an element safely."""
    el = get_el(selector)
    if el:
        el.innerHTML = str(html_content)


# ---------------------------------------------------------------------------
# Calculator Core Logic
# ---------------------------------------------------------------------------
def compute_calculator_state():
    """
    Extracts current inputs from the calculator DOM elements and computes
    rates, item breakdown, and total.
    Returns:
        dict containing (valid, pages, copies, p_type, paper_size, double_sided, rate, total, error_msg)
    """
    try:
        pages_input = get_el("#calc-pages")
        copies_input = get_el("#calc-copies")
        paper_size_select = get_el("#calc-paper-size")
        double_sided_check = get_el("#calc-double-sided")

        # Determine selected print type (radio group)
        bw_radio = get_el("#calc-type-bw")
        color_radio = get_el("#calc-type-color")
        is_color = color_radio.checked if color_radio else False

        p_type = "Colored" if is_color else "Black & White"
        rate = RATE_COLOR if is_color else RATE_BW

        # Safe parsing
        pages_raw = pages_input.value.strip() if pages_input else "1"
        copies_raw = copies_input.value.strip() if copies_input else "1"

        try:
            pages = int(pages_raw)
        except ValueError:
            pages = 0

        try:
            copies = int(copies_raw)
        except ValueError:
            copies = 0

        paper_size = paper_size_select.value if paper_size_select else "A4"
        is_double_sided = double_sided_check.checked if double_sided_check else False

        if pages <= 0 or copies <= 0:
            return {
                "valid": False,
                "pages": max(0, pages),
                "copies": max(0, copies),
                "p_type": p_type,
                "paper_size": paper_size,
                "double_sided": is_double_sided,
                "rate": rate,
                "total": 0.0,
                "error_msg": "Pages and copies must both be at least 1."
            }

        # Formula: Total = pages * copies * rate
        total = float(pages * copies * rate)

        return {
            "valid": True,
            "pages": pages,
            "copies": copies,
            "p_type": p_type,
            "paper_size": paper_size,
            "double_sided": is_double_sided,
            "rate": rate,
            "total": total,
            "error_msg": ""
        }

    except Exception as exc:
        print(f"[PyScript Calculator Error]: {exc}")
        return {
            "valid": False,
            "pages": 0,
            "copies": 0,
            "p_type": "Black & White",
            "paper_size": "A4",
            "double_sided": False,
            "rate": RATE_BW,
            "total": 0.0,
            "error_msg": str(exc)
        }


# ---------------------------------------------------------------------------
# EVENT HANDLER: Live Reactive Price Preview (Input & Change Events)
# ---------------------------------------------------------------------------
@when("input", "#calc-pages")
@when("input", "#calc-copies")
@when("change", "#calc-type-bw")
@when("change", "#calc-type-color")
@when("change", "#calc-paper-size")
@when("change", "#calc-double-sided")
def on_calc_input(event=None):
    """
    Event-driven handler triggered whenever the user types or toggles
    any parameter in the calculator. Demonstrates real-time Python reactivity.
    """
    calc = compute_calculator_state()
    
    # Update live preview banner
    preview_el = get_el("#live-preview-price")
    if preview_el:
        if calc["valid"]:
            preview_el.textContent = f"₱{calc['total']:,.2f}"
            preview_el.style.color = "var(--color-primary-dark)"
        else:
            preview_el.textContent = "₱0.00"
            preview_el.style.color = "var(--color-text-muted)"

    # Keep radio card visual highlight in sync
    bw_card = get_el("#card-type-bw")
    color_card = get_el("#card-type-color")
    if calc["p_type"] == "Colored":
        if color_card: color_card.classList.add("active")
        if bw_card: bw_card.classList.remove("active")
    else:
        if bw_card: bw_card.classList.add("active")
        if color_card: color_card.classList.remove("active")


# ---------------------------------------------------------------------------
# EVENT HANDLER: Full Calculation Breakdown (Click Event on "Calculate Total")
# ---------------------------------------------------------------------------
@when("click", "#btn-calculate")
def on_calculate_click(event=None):
    """
    Event-driven handler for the primary 'Calculate Total' button.
    Renders an itemized breakdown receipt directly into the DOM.
    """
    if event:
        event.preventDefault()

    calc = compute_calculator_state()

    breakdown_container = get_el("#calc-breakdown-details")
    if not breakdown_container:
        return

    if not calc["valid"]:
        set_html("#calc-breakdown-details", f"""
            <div style="color: var(--color-danger); padding: 1rem; background: #fef2f2; border-radius: 8px; font-size: 0.9rem;">
                ⚠️ <strong>Calculation Notice:</strong> {calc['error_msg']}
            </div>
        """)
        return

    # Build formatted itemized breakdown
    double_sided_badge = "Yes (Duplex)" if calc["double_sided"] else "No (Single-sided)"
    breakdown_html = f"""
        <div class="breakdown-list">
            <div class="breakdown-item">
                <span class="label">Printing Type:</span>
                <span class="val">{calc['p_type']}</span>
            </div>
            <div class="breakdown-item">
                <span class="label">Number of Pages:</span>
                <span class="val">{calc['pages']} page(s)</span>
            </div>
            <div class="breakdown-item">
                <span class="label">Number of Copies:</span>
                <span class="val">{calc['copies']} copy/copies</span>
            </div>
            <div class="breakdown-item">
                <span class="label">Paper Size:</span>
                <span class="val">{calc['paper_size']}</span>
            </div>
            <div class="breakdown-item">
                <span class="label">Double-Sided:</span>
                <span class="val">{double_sided_badge}</span>
            </div>
            <div class="breakdown-item">
                <span class="label">Applicable Rate:</span>
                <span class="val">₱{calc['rate']:.2f} / page</span>
            </div>
            <div class="breakdown-total-row">
                <span class="total-label">Estimated Total:</span>
                <span class="total-value">₱{calc['total']:,.2f}</span>
            </div>
        </div>
    """
    set_html("#calc-breakdown-details", breakdown_html)

    # Also automatically sync this calculation with the Order Form below
    sync_to_order_form(calc)


def sync_to_order_form(calc):
    """Helper to auto-populate the order form with calculated quantities."""
    try:
        order_type_select = get_el("#order-type")
        order_pages_input = get_el("#order-pages")
        order_copies_input = get_el("#order-copies")
        order_paper_select = get_el("#order-paper-size")

        if order_type_select:
            order_type_select.value = "bw" if calc["p_type"] == "Black & White" else "color"
        if order_pages_input and calc["pages"] > 0:
            order_pages_input.value = str(calc["pages"])
        if order_copies_input and calc["copies"] > 0:
            order_copies_input.value = str(calc["copies"])
        if order_paper_select:
            order_paper_select.value = calc["paper_size"]
    except Exception as exc:
        print(f"[Sync Order Form Warning]: {exc}")


# ---------------------------------------------------------------------------
# EVENT HANDLER: "Choose Service" from Services Cards
# ---------------------------------------------------------------------------
def select_service(service_name):
    """
    Updates the calculator and order form to match the chosen service,
    and smoothly scrolls the user down to the calculator.
    """
    bw_radio = get_el("#calc-type-bw")
    color_radio = get_el("#calc-type-color")
    order_type_select = get_el("#order-type")

    if service_name in ["bw", "research"]:
        if bw_radio: bw_radio.checked = True
        if color_radio: color_radio.checked = False
        if order_type_select: order_type_select.value = "bw"
    elif service_name in ["color", "project"]:
        if color_radio: color_radio.checked = True
        if bw_radio: bw_radio.checked = False
        if order_type_select: order_type_select.value = "color"

    # Trigger reactive update
    on_calc_input(None)

    # Smooth scroll to calculator
    calc_section = get_el("#calculator")
    if calc_section:
        calc_section.scrollIntoView({"behavior": "smooth"})


# Explicit event bindings for the 4 service buttons
@when("click", "#btn-choose-bw")
def on_choose_bw(event=None):
    if event: event.preventDefault()
    select_service("bw")

@when("click", "#btn-choose-color")
def on_choose_color(event=None):
    if event: event.preventDefault()
    select_service("color")

@when("click", "#btn-choose-research")
def on_choose_research(event=None):
    if event: event.preventDefault()
    select_service("research")

@when("click", "#btn-choose-project")
def on_choose_project(event=None):
    if event: event.preventDefault()
    select_service("project")


# ---------------------------------------------------------------------------
# EVENT HANDLER: Order Form Submission & Python Validation
# ---------------------------------------------------------------------------
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^[0-9+() -]{7,15}$")


def set_field_error(field_id, error_id, message=""):
    """Shows or hides validation error styling beside input fields."""
    input_el = get_el(field_id)
    error_el = get_el(error_id)
    if not input_el or not error_el:
        return

    if message:
        input_el.classList.add("is-invalid")
        error_el.textContent = message
        error_el.classList.add("show")
    else:
        input_el.classList.remove("is-invalid")
        error_el.textContent = ""
        error_el.classList.remove("show")


@when("submit", "#order-form")
def on_order_submit(event):
    """
    Event-driven form submission handler.
    1. Prevents default browser submission.
    2. Validates all inputs using pure Python logic.
    3. Displays specific error messages beside invalid fields.
    4. Upon success, dynamically renders a formatted order confirmation receipt.
    """
    event.preventDefault()

    # Read values from Order Form
    name_el = get_el("#order-name")
    phone_el = get_el("#order-phone")
    email_el = get_el("#order-email")
    type_el = get_el("#order-type")
    pages_el = get_el("#order-pages")
    copies_el = get_el("#order-copies")
    paper_el = get_el("#order-paper-size")
    fulfillment_el = get_el("#order-fulfillment")
    instructions_el = get_el("#order-instructions")

    name = name_el.value.strip() if name_el else ""
    phone = phone_el.value.strip() if phone_el else ""
    email = email_el.value.strip() if email_el else ""
    service_type = type_el.value if type_el else "bw"
    pages_raw = pages_el.value.strip() if pages_el else ""
    copies_raw = copies_el.value.strip() if copies_el else ""
    paper_size = paper_el.value if paper_el else "A4"
    fulfillment = fulfillment_el.value if fulfillment_el else "pickup"
    instructions = instructions_el.value.strip() if instructions_el else "None provided"

    # Reset all error states
    set_field_error("#order-name", "#error-order-name", "")
    set_field_error("#order-phone", "#error-order-phone", "")
    set_field_error("#order-email", "#error-order-email", "")
    set_field_error("#order-pages", "#error-order-pages", "")
    set_field_error("#order-copies", "#error-order-copies", "")

    has_error = False

    # 1. Name Validation
    if not name:
        set_field_error("#order-name", "#error-order-name", "Please enter your full name.")
        has_error = True
    elif len(name) < 2:
        set_field_error("#order-name", "#error-order-name", "Name must be at least 2 characters.")
        has_error = True

    # 2. Phone Validation
    if not phone:
        set_field_error("#order-phone", "#error-order-phone", "Please provide a contact number.")
        has_error = True
    elif not PHONE_REGEX.match(phone):
        set_field_error("#order-phone", "#error-order-phone", "Please enter a valid phone number (e.g. 09171234567).")
        has_error = True

    # 3. Email Validation
    if not email:
        set_field_error("#order-email", "#error-order-email", "Please enter your email address.")
        has_error = True
    elif not EMAIL_REGEX.match(email):
        set_field_error("#order-email", "#error-order-email", "Please enter a valid email address.")
        has_error = True

    # 4. Pages Validation
    try:
        pages = int(pages_raw)
        if pages <= 0:
            set_field_error("#order-pages", "#error-order-pages", "Please enter a valid number of pages (1 or more).")
            has_error = True
    except ValueError:
        set_field_error("#order-pages", "#error-order-pages", "Please enter a valid number of pages.")
        has_error = True
        pages = 0

    # 5. Copies Validation
    try:
        copies = int(copies_raw)
        if copies <= 0:
            set_field_error("#order-copies", "#error-order-copies", "Please enter at least 1 copy.")
            has_error = True
    except ValueError:
        set_field_error("#order-copies", "#error-order-copies", "Please enter at least 1 copy.")
        has_error = True
        copies = 0

    # 6. File Upload Validation
    set_field_error("#order-file", "#error-order-file", "")
    file_el = get_el("#order-file")
    has_file = False
    filename = "No file attached"
    file_size_str = ""

    if file_el and file_el.files and file_el.files.length > 0:
        has_file = True
        f = file_el.files.item(0)
        filename = f.name
        size_kb = round(f.size / 1024, 1)
        file_size_str = f"({size_kb} KB)"
    else:
        set_field_error("#order-file", "#error-order-file", "Please upload a document file to print (PDF, DOCX, etc.).")
        has_error = True

    confirmation_box = get_el("#order-confirmation")

    if has_error:
        if confirmation_box:
            confirmation_box.classList.remove("show")
        return

    # Calculate Order Total
    rate = RATE_COLOR if service_type == "color" else RATE_BW
    service_label = "Colored Printing (₱5.00/page)" if service_type == "color" else "Black & White Printing (₱2.00/page)"
    estimated_total = pages * copies * rate
    fulfillment_label = "Campus Kiosk Pickup" if fulfillment == "pickup" else "Student Dorm / Group Delivery"

    # Display Order Summary dynamically
    summary_html = f"""
        <div class="order-receipt-details">
            <div class="breakdown-list">
                <div class="breakdown-item">
                    <span class="label">Customer Name:</span>
                    <span class="val"><strong>{name}</strong></span>
                </div>
                <div class="breakdown-item">
                    <span class="label">Contact Info:</span>
                    <span class="val">{phone} &bull; {email}</span>
                </div>
                <div class="breakdown-item">
                    <span class="label">Service Selected:</span>
                    <span class="val">{service_label}</span>
                </div>
                <div class="breakdown-item">
                    <span class="label">Paper Size & Options:</span>
                    <span class="val">{paper_size} &bull; {fulfillment_label}</span>
                </div>
                <div class="breakdown-item">
                    <span class="label">Pages & Copies:</span>
                    <span class="val">{pages} pages &times; {copies} copy/copies</span>
                </div>
                <div class="breakdown-item">
                    <span class="label">Uploaded Document:</span>
                    <span class="val" style="color:var(--color-primary-light); font-weight:700;">📄 {filename} {file_size_str}</span>
                </div>
                <div class="breakdown-item">
                    <span class="label">Special Instructions:</span>
                    <span class="val"><em>{instructions}</em></span>
                </div>
                <div class="breakdown-total-row">
                    <span class="total-label">Estimated Total to Pay:</span>
                    <span class="total-value">₱{estimated_total:,.2f}</span>
                </div>
            </div>

            <!-- Email Notification Dispatch Banner -->
            <div class="email-dispatch-status">
                <span style="font-size:1.25rem;">📨</span>
                <div>
                    <strong>Dispatch Notification Sent:</strong>
                    <div>Document details and printing specs queued for delivery to: <code style="background:#fff; padding:2px 6px; border-radius:4px; font-weight:bold;">rdelarmente0@gmail.com</code></div>
                </div>
            </div>
        </div>
    """

    set_html("#order-receipt-content", summary_html)

    if confirmation_box:
        confirmation_box.classList.add("show")
        confirmation_box.scrollIntoView({"behavior": "smooth"})


@when("change", "#order-file")
def on_file_selected(event=None):
    """Update file name indicator as soon as user picks a file."""
    file_el = get_el("#order-file")
    info_el = get_el("#file-chosen-name")
    if file_el and file_el.files and file_el.files.length > 0:
        f = file_el.files.item(0)
        size_kb = round(f.size / 1024, 1)
        if info_el:
            info_el.textContent = f"Selected: {f.name} ({size_kb} KB)"
            info_el.style.color = "var(--color-primary)"
            info_el.style.fontWeight = "bold"
        set_field_error("#order-file", "#error-order-file", "")
    else:
        if info_el:
            info_el.textContent = "No file chosen yet (Max 15MB)"
            info_el.style.color = "var(--color-text-muted)"


# ---------------------------------------------------------------------------
# Initial PyScript Startup Notification
# ---------------------------------------------------------------------------
def on_init():
    """Run once when PyScript loads to initialize indicators and default state."""
    print("[PrintBai PyScript] Engine loaded and Event Listeners registered successfully.")
    
    # Update PyScript header badge
    dot = get_el("#py-status-dot")
    badge_text = get_el("#py-status-text")
    if dot: dot.classList.add("ready")
    if badge_text: badge_text.textContent = "Python 3 Runtime Active & Event Handlers Bound"

    # Initial live price calculation
    on_calc_input(None)
    on_calculate_click(None)


# Execute startup
on_init()
