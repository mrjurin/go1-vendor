import frappe
import json
from frappe.query_builder import Order



@frappe.whitelist()
def get_userid():
    return frappe.session.user


@frappe.whitelist()
def get_user():
    user_check = get_userid()
    if user_check:
        name = frappe.db.get_value("User", user_check, "full_name")
        return name
    return ""


@frappe.whitelist()
def get_test():
    user_check = get_userid()
    if user_check != "Administrator":
        query = """
            SELECT parent 
            FROM `tabPortal User` 
            WHERE user = %s 
            AND parenttype = 'Supplier'
        """
        supplier = frappe.db.sql(query, (user_check,), as_dict=True)
        if supplier:
            return supplier[0]["parent"]
    else:
        return ""


@frappe.whitelist()
def get_issues(**field_filters):
    my_data = get_test()
    filters = {}
    if my_data:
        filters["custom_supplier"] = my_data

    final_filter = json.loads(field_filters.get("field_filters", "{}"))

    if final_filter:
        for key, value in final_filter.items():
            if key != "cmd" and value:
                filters[key] = value
    issues = frappe.db.get_all("Issue", fields=["*"], filters=filters)
    return issues


# @frappe.whitelist()
# def get_test():
#     user_check=get_userid()
#     if user_check!="Administrator":
#         query = frappe.db.sql(f"""SELECT S.supplier_name
#                                 FROM `tabSupplier` S
#                                 INNER JOIN `tabAddress` A ON A.name = S.supplier_primary_address
#                                 WHERE A.email_id = '{user_check}'
#                                 AND A.disabled = 0""")
#         return query
#     return 'Admin'

# @frappe.whitelist()
# def get_issues(**field_filters):
#     my_data = get_test()
#     # Setting filters based on supplier data
#     # filters = {}
#     if my_data ='Admin':
#         filters = {}
#     elif my_data:
#         filters['custom_supplier'] = my_data
#     final_filter = json.loads(field_filters.get('field_filters'))

#     if final_filter != "":
#         for key, value in final_filter.items():
#             if key != 'cmd':
#                 if value:  # Only apply non-empty filters
#                     filters[key] = value

#             # frappe.log_error("issye",filters)

#     issues = frappe.db.get_all("Issue", fields=['*'], filters=filters)
#     return issues



@frappe.whitelist()
def get_quotation(**field_filters):
    my_data = get_test()
    frappe.log_error("sfds", my_data)

    filters = {"status": "Submitted"}

    if my_data:
        filters["supplier"] = my_data

    final_filter = json.loads(field_filters.get("field_filters"))
    if final_filter:
        for key, value in final_filter.items():
            if key != "cmd" and value:
                if key == "vendor":
                    filters["supplier"] = value
                else:
                    filters[key] = value

    quotations = frappe.db.get_all(
        "Request for Quotation", fields=["*"], filters=filters
    )

    # supplier_item = frappe.db.get_all("Request for Quotation Supplier", fields=['*'])
    # quotation_items = frappe.db.get_all("Request for Quotation Item", fields=['*'])

    quotation_docs = []

    for quotation in quotations:
        supplier_item = frappe.db.get_all(
            "Request for Quotation Supplier",
            fields=["*"],
            filters={"parent": quotation["name"]},
        )
        quotation_items = frappe.db.get_all(
            "Request for Quotation Item",
            fields=["*"],
            filters={"parent": quotation["name"]},
        )
        # items = [item for item ni quotation_items if item["parent"] == quotation["name"]]
        # suppliers = [supplier for supplier in supplier_item if supplier["parent"] == quotation["name"]]

        quotation["items"] = quotation_items
        quotation["suppliers"] = supplier_item
        quotation["supplier"] = my_data
        quotation_docs.append(quotation)

    return quotation_docs


@frappe.whitelist()
def get_purchaseorder(**field_filters):
    my_data = get_test()
    # Setting filters based on supplier data
    filters = {}
    if my_data:
        filters["supplier"] = my_data
    final_filter = json.loads(field_filters.get("field_filters"))

    if final_filter != "":
        for key, value in final_filter.items():
            if key != "cmd":
                if value:  # Only apply non-empty filters
                    filters[key] = value

    purchase_orders = frappe.db.get_all("Purchase Order", fields=["*"], filters=filters)

    purchase_order_docs = []

    for order in purchase_orders:
        purchase_order_items = frappe.db.get_all(
            "Purchase Order Item", fields=["*"], filters={"parent": order["name"]}
        )
        taxes_and_charges = frappe.db.get_all(
            "Purchase Taxes and Charges",
            fields=["*"],
            filters={"parent": order["name"]},
        )
        payment_schedule = frappe.db.get_all(
            "Payment Schedule",
            fields=["*"],
            filters={"parent": order["name"]},
        )

        order["items"] = purchase_order_items
        order["taxes"] = taxes_and_charges
        order["payments"] = payment_schedule

        purchase_order_docs.append(order)

    purchase_order_docs = additional_data(purchase_order_docs)

    return purchase_order_docs


@frappe.whitelist()
def get_blanketorder(**field_filters):
    my_data = get_test()
    filters = {}
    if my_data:
        filters["supplier"] = my_data

    final_filter = json.loads(field_filters.get("field_filters"))
    if final_filter:
        for key, value in final_filter.items():
            if key != "cmd" and value:
                if key == "vendor":
                    filters["supplier"] = value
                else:
                    filters[key] = value
    blankets = frappe.db.get_all("Blanket Order", fields=["*"], filters=filters)
    blankets_docs = []

    for blanket in blankets:
        supplier_items = frappe.db.get_all(
            "Blanket Order Item",
            fields=["*"],
            filters={"parent": blanket["name"]},
        )

        blanket["items"] = supplier_items
        blankets_docs.append(blanket)

    return blankets_docs


# supplier quotation
@frappe.whitelist()
def get_supplierquotation(**field_filters):
    my_data = get_test()

    filters = {}
    if my_data:
        filters["supplier"] = my_data
    final_filter = json.loads(field_filters.get("field_filters"))
    if final_filter != "":
        for key, value in final_filter.items():
            if key != "cmd":
                if value:
                    filters[key] = value

    quotations = frappe.db.get_all("Supplier Quotation", fields=["*"], filters=filters)
    quotation_docs = []

    for quotation in quotations:
        supplier_items = frappe.db.get_all(
            "Supplier Quotation Item",
            fields=["*"],
            filters={"parent": quotation["name"]},
        )
        taxes_and_charges = frappe.db.get_all(
            "Purchase Taxes and Charges",
            fields=["*"],
            filters={"parent": quotation["name"]},
        )

        quotation["items"] = supplier_items
        quotation["taxes"] = taxes_and_charges

        quotation_docs.append(quotation)

    quotation_docs = additional_data(quotation_docs)

    return quotation_docs


# Purchase invoice
@frappe.whitelist()
def get_purchaseinvoice(**field_filters):
    my_data = get_test()

    filters = {}
    if my_data:
        filters["supplier"] = my_data

    final_filter = json.loads(field_filters.get("field_filters"))
    if final_filter != "":
        for key, value in final_filter.items():
            if key != "cmd":
                if value:
                    filters[key] = value

    invoices = frappe.db.get_all("Supplier Invoice", fields=["*"], filters=filters)
    invoice_docs = []

    for invoice in invoices:
        invoice_items = frappe.db.get_all(
            "Purchase Invoice Item", fields=["*"], filters={"parent": invoice["name"]}
        )
        taxes_and_charges = frappe.db.get_all(
            "Purchase Taxes and Charges",
            fields=["*"],
            filters={"parent": invoice["name"]},
        )

        invoice["items"] = invoice_items
        invoice["taxes"] = taxes_and_charges

        invoice_docs.append(invoice)

    invoice_docs = additional_data(invoice_docs)

    return invoice_docs


@frappe.whitelist()
def get_address(**field_filters):
    my_data = get_test()

    # Setting filters based on supplier data
    filters = {}
    # if my_data:
    # filters['supplier'] = my_data

    # frappe.log_error("types",type(field_filters))

    final_filter = json.loads(field_filters.get("field_filters"))
    # frappe.log_error('final_filter ',final_filter)
    if final_filter != "":
        for key, value in final_filter.items():
            if key != "cmd":
                if value:  # Only apply non-empty filters
                    filters[key] = value

    address_list = []

    addresses = frappe.db.get_all("Address", fields=["*"], filters=filters)

    for address in addresses:
        if my_data:
            filters = {"parent": address["name"]}
        else:
            filters = {"link_doctype": "Supplier"}

        links = frappe.db.get_all("Dynamic Link", fields=["*"], filters=filters)
        address["links"] = links
        address_list.append(address)

    address_data = []
    for address in address_list:
        for link in address["links"]:
            if link["link_name"] in my_data:
                address_data.append(address)

    return address_data if my_data else address_list


@frappe.whitelist()
def additional_data(addtional_docs):
    for quotation in addtional_docs:
        quotation["grand_total"] = frappe.utils.fmt_money(
            quotation.get("grand_total"), currency=quotation.get("currency")
        )
        quotation["total"] = frappe.utils.fmt_money(
            quotation.get("total"), currency=quotation.get("currency")
        )
        quotation["rounded_total"] = frappe.utils.fmt_money(
            quotation.get("rounded_total"), currency=quotation.get("currency")
        )
        quotation["total_taxes_and_charges"] = frappe.utils.fmt_money(
            quotation.get("total_taxes_and_charges"), currency=quotation.get("currency")
        )

        # Formatting dates
        quotation["posting_date"] = frappe.utils.formatdate(
            quotation.get("posting_date"), "dd-MM-yyyy"
        )
        if quotation.get("due_date"):
            quotation["due_date"] = frappe.utils.formatdate(
                quotation.get("due_date"), "dd-MM-yyyy"
            )

        # Formatting item rates and amounts
        for item in quotation["items"]:
            item["rate"] = frappe.utils.fmt_money(
                item["rate"], currency=quotation.get("currency")
            )
            item["amount"] = frappe.utils.fmt_money(
                item["amount"], currency=quotation.get("currency")
            )

        for taxe in quotation["taxes"]:
            taxe["rate"] = frappe.utils.fmt_money(
                taxe["rate"], currency=quotation.get("currency")
            )
            taxe["tax_amount"] = frappe.utils.fmt_money(
                taxe["tax_amount"], currency=quotation.get("currency")
            )
            taxe["total"] = frappe.utils.fmt_money(
                taxe["total"], currency=quotation.get("currency")
            )
        # Fetch and add supplier address details
        if quotation.get("supplier_address"):
            address = frappe.get_doc("Address", quotation["supplier_address"])
            quotation.update(
                {
                    "sup_address_line1": address.address_line1,
                    "sup_address_line2": address.address_line2,
                    "sup_city": address.city,
                    "sup_country": address.country,
                    "sup_state": address.state,
                    "sup_phone": address.phone,
                    "sup_pincode": address.pincode,
                }
            )

        if quotation.get("shipping_address"):
            address = frappe.get_doc("Address", quotation["shipping_address"])
            quotation.update(
                {
                    "ship_address_line1": address.address_line1,
                    "ship_address_line2": address.address_line2,
                    "ship_city": address.city,
                    "ship_country": address.country,
                    "ship_state": address.state,
                    "ship_phone": address.phone,
                    "ship_pincode": address.pincode,
                }
            )
    return addtional_docs


@frappe.whitelist(allow_guest=True)
def get_register(registerdata):
    # frappe.log_error(message=f"Initial data type: {type(registerdata)}", title="Data Type Check")

    register_data = json.loads(registerdata)

    # Log the parsed data type

    # frappe.log_error("Parsed Data Type",type(register_data))

    register = frappe.new_doc("Supplier Registration")

    register.first_name = register_data.get("first_name")
    register.last_name = register_data.get("last_name")
    register.phone = register_data.get("phone")
    register.email = register_data.get("email")
    register.state = register_data.get("state")
    register.zip_code = register_data.get("zip_code")
    register.country = register_data.get("country")
    register.address_line1 = register_data.get("address_line1")
    register.address_line2 = register_data.get("address_line2")
    register.city = register_data.get("city")
    # register.website = register_data('website')

    # Log the final register document as a dictionary
    # frappe.log_error(message=f"Register document: {register.as_dict()}", title="Register Document")

    register.insert()
    frappe.db.commit()


@frappe.whitelist(allow_guest=True)
def check_supplier(email):    
    if "Supplier" not in frappe.get_roles(email):
        return {"status": "error", "message": "Email does not have the required Supplier role"}    
   
    query = """
        SELECT parent 
        FROM `tabPortal User` 
        WHERE user = %s 
        AND parenttype = 'Supplier'
    """
    supplier = frappe.db.sql(query, (email,), as_dict=True)

    if supplier:
        return {"status": "success", "message": "Email is associated with a Supplier."}
    
    return {"status": "error", "message": "Email not found in Supplier portal users."}





# --------------------------------- Notification data-----------------------------------

@frappe.whitelist()
def get_notifications():
    Notification = frappe.qb.DocType("Notification Log")
    query = (
        frappe.qb.from_(Notification)
        .select("*")
        .where(Notification.for_user == frappe.session.user)
        .orderby("creation", order=Order.desc)
    )
    notifications = query.run(as_dict=True)

    _notifications = []
    for notification in notifications:
        
        _notifications.append(
            {
                "creation": notification.creation,
                "name": notification.name,
                "subject": notification.subject,
                "from_user": {
                    "name": notification.from_user,
                    "full_name": frappe.get_value(
                        "User", notification.from_user, "full_name"
                    ),
                },
                "type": notification.type,
                "to_user": notification.for_user,
                "read": notification.read,            
                "notification_text": notification.email_content,                
               
            }
        )
    return _notifications
    


@frappe.whitelist()
def mark_as_read(user=None, doc=None):   
    user = user or frappe.session.user    
    filters = {"for_user": user, "read": False}
    or_filters = []
    if doc:
        or_filters = [           
            {"name": doc},
        ]
    for n in frappe.get_all("Notification Log", filters=filters, or_filters=or_filters):
        d = frappe.get_doc("Notification Log", n.name)
        d.read = True
        d.save()