import json
import re

def format_data(serializer):
    result = {"contactIds": [], "emails": [], "phones": [] }
    emails_set = set()
    phones_set = set()
    
    for contact in serializer.data:
        result["contactIds"].append(contact["id"])
        
        email = contact["email"].strip()
        if email not in emails_set:
            emails_set.add(email)
            result["emails"].append(email)
        
        phone = contact["phone"]
        if phone not in phones_set:
            phones_set.add(phone)
            result["phones"].append(phone)
    
    response_data =result
    return response_data


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_phone(phone):
    phone = phone.replace('+', '')
    if not phone.isdigit():
        return False
    return True