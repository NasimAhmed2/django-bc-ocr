# import libraries
import os
from pprint import pprint
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential




def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join(
        "Page #{}: {}".format(region.page_number, format_polygon(region.polygon))
        for region in bounding_regions
    )


def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])


def analyze_invoice(path):
    
    # file_path = r'D:\DJANGO\Blue Consulting Ocr\BC_OCR\pdf_pages\42_page_1.pdf'
    file_path = "D:\DJANGO\Blue Consulting Ocr\BC_OCR"+ str(path)
    file_path_ = rf"{file_path}"
    result_dict = {}
    # file_path = 'D:/sample_pdf10.pdf'
    with open(file_path_, "rb") as file:
        pdf_content = file.read()

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", pdf_content
    )
    invoices = poller.result()

    for idx, invoice in enumerate(invoices.documents):
        print("--------Recognizing invoice #{}--------".format(idx + 1))
        
        
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            result_dict['VendorName'] = vendor_name.value
            
            
        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            value = vendor_address.value
            address = str(value.house_number)+', '+str(value.road)+', '+str(value.city)+', '+str(value.state)+', '+str(value.postal_code)+', '+str(value.country_region)
            result_dict['VendorAddress'] = address 
#             result_dict['VendorAddress'] = vendor_address.value
            
        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
            result_dict['VendorAddressRecipient'] = vendor_address_recipient.value
            
        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
            result_dict['CustomerName'] = customer_name.value
            
        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
            result_dict['CustomerId'] = customer_id.value
            
        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
            value = vendor_address.value
            address = str(value.house_number)+', '+str(value.road)+', '+str(value.city)+', '+str(value.state)+', '+str(value.postal_code)+', '+str(value.country_region)
            result_dict['CustomerAddress'] = address
#             result_dict['CustomerAddress'] = str(customer_address.value)
            
        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
            result_dict['CustomerAddressRecipient'] = customer_address_recipient.value
            
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            result_dict['InvoiceId'] = invoice_id.value
            
        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            result_dict['InvoiceDate'] = str(invoice_date.value)
            
        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            result_dict['InvoiceTotal'] = str(invoice_total.value)
            
        Customer_Gst_No = invoice.fields.get('CustomerTaxId')
        if Customer_Gst_No:
            result_dict["Cutomer Gst No."] = Customer_Gst_No.value

        Vendor_Gst_No = invoice.fields.get('VendorTaxId')
        if Vendor_Gst_No:
            result_dict["Vendor Gst No."] = Vendor_Gst_No.value

        due_date = invoice.fields.get("DueDate")   
        if due_date:
            result_dict['DueDate'] = str(due_date.value)
            
        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order:
            result_dict['PurchaseOrder'] = purchase_order.value
            
        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
            value = vendor_address.value
            address = str(value.house_number)+', '+str(value.road)+', '+str(value.city)+', '+str(value.state)+', '+str(value.postal_code)+', '+str(value.country_region)
            result_dict['BillingAddress'] = address
#             result_dict['BillingAddress'] = billing_address.value
            
        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient:
            result_dict['BillingAddressRecipient'] = billing_address_recipient.value
            
        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
            value = vendor_address.value
            address = str(value.house_number)+', '+str(value.road)+', '+str(value.city)+', '+str(value.state)+', '+str(value.postal_code)+', '+str(value.country_region)
            result_dict['ShippingAddress'] = address
#             result_dict['ShippingAddress'] = shipping_address.value
            
        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
            result_dict['ShippingAddressRecipient'] = shipping_address_recipient.value
            
        print("Invoice items:")
        result_dict["Invoice items:"] = {}
        try:
            for idx, item in enumerate(invoice.fields.get("Items").value):
                dictt = {}
                print("...Item #{}".format(idx + 1))
                item_description = item.value.get("Description")
                if item_description:
                    dictt['item_description'] = item_description.value 

                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    dictt['item_quantity'] = item_quantity.value 

                unit = item.value.get("Unit")
                if unit:
                    dictt['unit'] = str(unit.value) 

                unit_price = item.value.get("UnitPrice")
                if unit_price:
                    dictt['unit_price'] = str(unit_price.value)  

                product_code = item.value.get("ProductCode")
                if product_code:
                    dictt['product_code'] = product_code.value 

                item_date = item.value.get("Date")
                if item_date:
                    dictt['item_date'] = str(item_date.value)

                tax = item.value.get("Tax")
                if tax:
                    dictt['tax'] = str(tax.value)
                    
                tax_rate = item.value.get("TaxRate")
                if tax:
                    dictt['tax_rate'] = str(tax_rate.value)


                amount = item.value.get("Amount")
                if amount:
                    dictt['amount'] = str(amount.value)


                result_dict["Invoice items:"]['item#'+str(idx+1)] = dictt
        except:
            pass
        
        print("Tax items:")
        result_dict["tax items"] = {}
        tax_key = ''
        try:
            for idx, item in enumerate(invoice.fields.get("TaxDetails").value):
                if 'CGST' in item.content.upper():
                    tax_key = 'CGST'
                elif 'SGST' in item.content.upper():
                    tax_key = 'SGST'
                elif 'IGST' in item.content.upper():
                    tax_key = 'IGST'
                dictt = {}
                print(tax_key)
                amount = item.value.get("Amount")
                if amount:
                    dictt['amount'] = str(amount.value)

                rate = item.value.get("Rate")
                if rate:
                    dictt['rate'] = str(rate.value)
                result_dict["tax items"][tax_key] = dictt
                
        except:
            pass
        
        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            result_dict['SubTotal'] = str(subtotal.value)
            
        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            result_dict['TotalTax'] = str(total_tax.value)
            
        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            result_dict['PreviousUnpaidBalance'] = previous_unpaid_balance.value
            
        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            result_dict['AmountDue'] = amount_due.value
            
        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            result_dict['ServiceStartDate'] = str(service_start_date.value) 
           
        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            result_dict['ServiceEndDate'] = str(service_end_date.value) 
            
        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            result_dict['ServiceAddress'] = service_address.value 
            
        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            result_dict['service_address_recipient'] = service_address_recipient.value

        Payment_Term = invoice.fields.get("PaymentTerm")
        if Payment_Term:
            result_dict['Payment_Term'] = Payment_Term.value
            

        print("----------------------------------------")
        # pprint(result_dict)
        return result_dict

def hello(urls):
    dict_hello = {'CustomerAddress': '60, Harish Chatterjee Street, Kolkata, None, 700025, None',
                'CustomerAddressRecipient': 'Everest Industries Limited',
                'CustomerName': 'Everest Industries Limited',
                'Cutomer Gst No.': '19AAACE7550N1Z7',
                'Invoice items:': {'item#1': {'amount': '1200.0',
                                            'item_date': 'None',
                                            'unit_price': '1200.0'},
                                    'item#2': {'amount': '1200.0',
                                            'item_description': '#82456090 Date: '
                                                                '29-11-2023\n'
                                                                'Vehicle Group: Dzire | '
                                                                'WB23C 9877\n'
                                                                'Duty Type: 8H 80KMs '
                                                                '(Kolkata)\n'
                                                                'Passengers: Bibek Behur',
                                            'item_quantity': 1.0,
                                            'unit_price': '1200.0'},
                                    'item#3': {'amount': '0.0',
                                            'item_description': 'Charges',
                                            'item_quantity': 1.0,
                                            'unit_price': '0.0'}},
                'InvoiceDate': '2023-12-28',
                'InvoiceId': 'RC2324-007090',
                'InvoiceTotal': '₹1200.0',
                'SubTotal': '₹1200.0',
                'Vendor Gst No.': '19ABBFR668911ZB',
                'VendorAddress': '60, Harish Chatterjee Street, Kolkata, None, 700025, None',
                'VendorAddressRecipient': 'Rameshwar Car Rentals',
                'VendorName': 'Rameshwar Car Rentals',
                'tax items': {'CGST': {'amount': '₹30.0', 'rate': '2.5%:'}, 'SGST': {}}}
    # for i in range(len(urls)):
    #     field = 'field'+str(i)
    #     dict_hello[field] = f"My Name Is Nasim {i}"
    return dict_hello


# if __name__ == "__main__":
#     analyze_invoice()