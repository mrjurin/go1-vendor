import frappe
from frappe.utils import flt


@frappe.whitelist()
def make_supplier_invoice(source_name, target_doc=None, ignore_permissions=False):
    from frappe.model.mapper import get_mapped_doc

    target_doc = get_mapped_doc(
        "Purchase Order",
        source_name,
        {
            "Purchase Order Item": {
                "doctype": "Purchase Invoice Item",
            },
            "" "Purchase Order": {
                "doctype": "Supplier Invoice",
                "field_map": {"rounded_total": "rounded_total"},
            },
        },
        target_doc,
        ignore_permissions=ignore_permissions,
    )
    return target_doc


@frappe.whitelist()
def get_navbar_routes():
    # check = frappe.get_single("Go1 Navbar Settings")
    user_details = frappe.get_all(
        "Sidebar Settings",
        filters={"parent": "Go1 Navbar Settings", "enabled": 1},
        fields=["*"],
        order_by="idx",
    )
    return user_details


@frappe.whitelist()
def get_navbar_logo():
    check = frappe.get_single("Go1 Navbar Settings")
    navbar = f"{frappe.utils.get_url()}{check.application_logo}"
    return {"app_logo": navbar, "datas": check}


@frappe.whitelist()
def get_request():
    quotation = frappe.get_meta("Request for Quotation")
    return quotation


@frappe.whitelist()
def get_address():
    address = frappe.get_meta("Address")
    return address


@frappe.whitelist()
def get_purchase():
    meta = frappe.get_meta("Purchase Order")
    return meta


@frappe.whitelist()
def get_blanket():
    meta = frappe.get_meta("Blanket Order")
    return meta


@frappe.whitelist()
def get_supplier():
    supplier = frappe.get_meta("Supplier Quotation")
    return supplier


@frappe.whitelist()
def get_invoice():
    invoice = frappe.get_meta("Supplier Invoice")
    return invoice


@frappe.whitelist()
def get_issues():
    issue = frappe.get_meta("Issue")
    return issue



@frappe.whitelist()
def get_purchase_order_grand_total():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        query = frappe.db.sql(
            """
            SELECT COALESCE(AVG(grand_total), 0) AS total_grand_total
            FROM `tabPurchase Order`
            WHERE docstatus = 1
            AND MONTH(transaction_date) = MONTH(CURRENT_DATE())
            AND YEAR(transaction_date) = YEAR(CURRENT_DATE()) 
            AND supplier= %s
        """,
            (supplier),
            as_dict=True,
        )
        total = query[0].get("total_grand_total", 0) if query else 0
        return {"total_grand_total": total}
    else:
        query = frappe.db.sql(
            """
            SELECT COALESCE(AVG(grand_total), 0) AS total_grand_total
            FROM `tabPurchase Order`
            WHERE docstatus = 1
            AND MONTH(transaction_date) = MONTH(CURRENT_DATE())
            AND YEAR(transaction_date) = YEAR(CURRENT_DATE()) 
           
        """,
            as_dict=True,
        )
        total = query[0].get("total_grand_total", 0) if query else 0
        return {"total_grand_total": total}


# Number Card2
@frappe.whitelist()
def get_pending_quotation_count():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        query = frappe.db.sql(
            """
                SELECT COUNT(Q.name) AS total_count
                FROM `tabRequest for Quotation` Q
                INNER JOIN `tabRequest for Quotation Supplier` QS ON Q.name = QS.parent
                WHERE Q.custom_actioned = 0  
                AND QS.supplier = %s
                """,
            (supplier),
            as_dict=True,
        )
        count = query[0].get("total_count", 0) if query else 0
        return {"total_count": count}

    else:
        query = frappe.db.sql(
            """
                SELECT COUNT(*) AS total_count
                FROM `tabRequest for Quotation`
                WHERE custom_actioned = 0
                """,
            as_dict=True,
        )
        count = query[0].get("total_count", 0) if query else 0
        return {"total_count": count}


# Number Card3
@frappe.whitelist()
def get_pending_invoice():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        query = frappe.db.sql(
            """
                    SELECT COUNT(*) AS total_count
                    FROM `tabPurchase Invoice`
                    WHERE docstatus = 1  
                    AND status = 'Unpaid'
                    AND supplier = %s
                    """,
            (supplier),
            as_dict=True,
        )
        count = query[0].get("total_count", 0) if query else 0
        return {"total_count": count}

    else:
        query = frappe.db.sql(
            """
                    SELECT COUNT(*) AS total_count
                    FROM `tabPurchase Invoice`
                    WHERE docstatus = 1  
                    AND status = 'Unpaid'
                    """,
            as_dict=True,
        )
        count = query[0].get("total_count", 0) if query else 0
        return {"total_count": count}


# Number Card4
@frappe.whitelist()
def get_pending_inwards():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        query = frappe.db.sql(
            """
            SELECT COUNT(*) AS total_count
            FROM `tabPurchase Order`
            WHERE docstatus = 1  
            AND status IN ('To Receive And Bill', 'To Receive')
            AND supplier =%s
        """,
            (supplier),
            as_dict=True,
        )
        count = query[0].get("total_count", 0) if query else 0
        return {"total_count": count}
    else:
        query = frappe.db.sql(
            """
            SELECT COUNT(*) AS total_count
            FROM `tabPurchase Order`
            WHERE docstatus = 1  
            AND status IN ('To Receive And Bill', 'To Receive')
        """,
            as_dict=True,
        )
        count = query[0].get("total_count", 0) if query else 0
        return {"total_count": count}


# Doughnut Chart1
@frappe.whitelist()
def get_purchase_order_status_analysis():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        query = frappe.db.sql(
            """
            SELECT 
                status,
                COUNT(*) AS status_count
            FROM `tabPurchase Order`
            WHERE docstatus < 2 
            AND supplier=%s
            GROUP BY status
        """,
            (supplier),
            as_dict=True,
        )

        status_data = {"Billed Amount": 0, "Amount to Bill": 0}
        for row in query:
            if row["status"] == "Completed":
                status_data["Billed Amount"] += row["status_count"]
            elif row["status"] in ["To Receive and Bill", "To Bill"]:
                status_data["Amount to Bill"] += row["status_count"]

        return {"status_data": status_data}
    else:
        query = frappe.db.sql(
            """
            SELECT 
                status,
                COUNT(*) AS status_count
            FROM `tabPurchase Order`
            WHERE docstatus < 2 
            GROUP BY status
        """,
            as_dict=True,
        )
        status_data = {"Billed Amount": 0, "Amount to Bill": 0}
        for row in query:
            if row["status"] == "Completed":
                status_data["Billed Amount"] += row["status_count"]
            elif row["status"] in ["To Receive and Bill", "To Bill"]:
                status_data["Amount to Bill"] += row["status_count"]

        return {"status_data": status_data}


# Doughnut Chart2
@frappe.whitelist()
def get_quotation_status_counts():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        completed_query = frappe.db.sql(
            """
            SELECT COUNT(Q.name) AS total_count
            FROM `tabRequest for Quotation` Q
            INNER JOIN `tabRequest for Quotation Supplier` QS ON Q.name = QS.parent
            WHERE Q.custom_actioned = 1
            AND QS.supplier=%s
        """,
            (supplier),
            as_dict=True,
        )
        pending_query = frappe.db.sql(
            """
            SELECT COUNT(Q.name) AS total_count
            FROM `tabRequest for Quotation` Q 
            INNER JOIN `tabRequest for Quotation Supplier` QS ON Q.name = QS.parent
            WHERE custom_actioned = 0
            AND QS.supplier=%s

        """,
            (supplier),
            as_dict=True,
        )

        completed_count = (
            completed_query[0].get("total_count", 0) if completed_query else 0
        )
        pending_count = pending_query[0].get("total_count", 0) if pending_query else 0

        return {
            "status_data": {
                "Completed": completed_count,
                "Pending": pending_count,
            }
        }
    else:
        completed_query = frappe.db.sql(
            """
            SELECT COUNT(*) AS total_count
            FROM `tabRequest for Quotation` 
            WHERE custom_actioned = 1
        """,
            as_dict=True,
        )
        pending_query = frappe.db.sql(
            """
            SELECT COUNT(*) AS total_count
            FROM `tabRequest for Quotation` 
            WHERE custom_actioned = 0
        """,
            as_dict=True,
        )

        completed_count = (
            completed_query[0].get("total_count", 0) if completed_query else 0
        )
        pending_count = pending_query[0].get("total_count", 0) if pending_query else 0

        return {
            "status_data": {
                "Completed": completed_count,
                "Pending": pending_count,
            }
        }


# Bar Chart
@frappe.whitelist()
def get_top_sold_items():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        query = frappe.db.sql(
            """
            SELECT poi.item_code, poi.item_name, COUNT(*) as item_count
            FROM `tabPurchase Order Item` poi
            WHERE parent IN (
                SELECT name
                FROM `tabPurchase Order`
                WHERE docstatus = 1  
                AND supplier =%s
            )
            GROUP BY poi.item_code, poi.item_name
            ORDER BY item_count DESC
            LIMIT 5
        """,
            (supplier),
            as_dict=True,
        )
        return {"message": {"items": query}}
    else:
        query = frappe.db.sql(
            """
            SELECT poi.item_code, poi.item_name, COUNT(*) as item_count
            FROM `tabPurchase Order Item` poi
            WHERE parent IN (
                SELECT name
                FROM `tabPurchase Order`
                WHERE docstatus = 1  
            )
            GROUP BY poi.item_code, poi.item_name
            ORDER BY item_count DESC
            LIMIT 5
        """,
            as_dict=True,
        )
        return {"message": {"items": query}}


# Line Chart
@frappe.whitelist()
def get_monthly_grand_total():
    supplier = get_test().get("name") if get_test() else None
    if supplier:
        grand_total_data = frappe.db.sql(
            r"""
            SELECT
                DATE_FORMAT(transaction_date, '%%b') as month,
                SUM(grand_total) as monthly_total
            FROM `tabPurchase Order`
            WHERE docstatus = 1
            AND supplier = %s
            GROUP BY DATE_FORMAT(transaction_date, '%%Y-%%m')
            ORDER BY FIELD(DATE_FORMAT(transaction_date, '%%b'), 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar')
        """,
            (supplier),
            as_dict=True,
        )

        financial_year_order = [
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jan",
            "Feb",
            "Mar",
        ]
        monthly_totals = {month: 0 for month in financial_year_order}

        for record in grand_total_data:
            month = record.get("month")
            total = flt(record.get("monthly_total"))
            if month in monthly_totals:
                monthly_totals[month] += total

        return {
            "labels": list(monthly_totals.keys()),
            "data": list(monthly_totals.values()),
        }
    else:
        grand_total_data = frappe.db.sql(
            """
            SELECT
                DATE_FORMAT(transaction_date, '%b') as month,
                SUM(grand_total) as monthly_total
            FROM `tabPurchase Order`
            WHERE docstatus = 1
            GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
            ORDER BY FIELD(DATE_FORMAT(transaction_date, '%b'), 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar')
        """,
            as_dict=True,
        )

        financial_year_order = [
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jan",
            "Feb",
            "Mar",
        ]
        monthly_totals = {month: 0 for month in financial_year_order}

        for record in grand_total_data:
            month = record.get("month")
            total = flt(record.get("monthly_total"))
            if month in monthly_totals:
                monthly_totals[month] += total

        return {
            "labels": list(monthly_totals.keys()),
            "data": list(monthly_totals.values()),
        }


@frappe.whitelist()
def fetch_supplier_invoice():
    meta = frappe.get_meta("Supplier Invoice")
    fields_to_return = [
        "posting_date",
        "bill_no",
        "supplier_name",
        "bill_date",
    ]
    field_details = []

    for field in meta.fields:
        if field.fieldname in fields_to_return:
            field_details.append(
                {
                    "label": field.label,
                    "fieldname": field.fieldname,
                    "fieldtype": field.fieldtype,
                }
            )

    return field_details


@frappe.whitelist()
def fetch_supplier_invoice_items():
    child_table_meta = frappe.get_meta("Purchase Invoice Item")
    fields_to_return = ["rate", "uom", "qty", "item_code", "amount", "item_name"]

    field_details = []

    for field in child_table_meta.fields:
        if field.fieldname in fields_to_return:
            field_details.append(
                {
                    "label": field.label,
                    "fieldname": field.fieldname,
                    "fieldtype": field.fieldtype,
                }
            )

    return field_details


@frappe.whitelist()
def fetch_purchase_orders(supplier):
    return frappe.db.sql(
        """
        SELECT po.name, po.schedule_date, po.company
        FROM `tabPurchase Order` po
        WHERE po.status IN ('To Bill', 'To Receive And Bill')
        AND po.supplier = %s
        AND EXISTS (
            SELECT 1 FROM `tabPurchase Order Item` poi
            LEFT JOIN (
                SELECT purchase_order, item_code, SUM(qty) AS received_qty
                FROM `tabPurchase Invoice Item`
                GROUP BY purchase_order, item_code
            ) pii ON poi.parent = pii.purchase_order AND poi.item_code = pii.item_code
            WHERE poi.parent = po.name
            AND IFNULL(poi.qty, 0) != IFNULL(pii.received_qty, 0)
        )
    """,
        (supplier),
        as_dict=True,
    )

@frappe.whitelist()
def get_purchase_order_items(po_names):
    items = frappe.db.get_all(
        "Purchase Order Item",
        filters={"parent": ("in", po_names)},
        fields=[
            "parent as purchase_order_reference",
            "uom",
            "item_code",
            "item_name",
            "schedule_date",
            "qty",
            "rate",
            "amount",
        ],
    )

    purchase_invoice_items = frappe.db.get_all(
        "Purchase Invoice Item",
        filters={"purchase_order": ("in", po_names)},
        fields=["purchase_order", "item_code", "qty"],
    )

    invoiced_qty_map = {}
    for item in purchase_invoice_items:
        key = (item["purchase_order"], item["item_code"])
        invoiced_qty_map[key] = invoiced_qty_map.get(key, 0) + item["qty"]

    for item in items:
        key = (item["purchase_order_reference"], item["item_code"])
        invoiced_qty = invoiced_qty_map.get(key, 0)
        item["qty"] = max(0, item["qty"] - invoiced_qty)

    return items


@frappe.whitelist()
def get_userid():
    return frappe.session.user


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
            supplier_id = supplier[0]["parent"]
            supplier_name = frappe.db.get_value(
                "Supplier", supplier_id, "supplier_name"
            )
            return {"name": supplier_id, "supplier_name": supplier_name}
    else:
        return ""


@frappe.whitelist()
def get_rfq_details(rfq_id):
    rfq = frappe.get_doc("Request for Quotation", rfq_id)
    supplier = get_test()
    rfq_details = {
        "company": rfq.company,
        "transaction_date": rfq.transaction_date,
        "items": [],
        "name": rfq.name,
    }
    for item in rfq.items:
        rfq_details["items"].append(
            {
                "item_code": item.item_code,
                "uom": item.uom,
                "qty": item.qty,
                "warehouse": item.warehouse,
            }
        )
    return {"message": rfq_details, "supplier": supplier}
