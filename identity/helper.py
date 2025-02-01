import json
def format_data(serializer):
	result = {"contactIds": [],"emails": [],"phones": [] }
	for contact in serializer.data:
		result["contactIds"].append(contact["id"])
		result["emails"].append(contact["email"].strip())
		result["phones"].append(contact["phone"])
	response_data = json.dumps(result , separators=(',', ':'))
	return response_data

