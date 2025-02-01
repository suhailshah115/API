import json

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
    
    response_data = json.dumps(result, separators=(',',':'))
    return response_data
