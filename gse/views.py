from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializer import ContactSerializer
from django.db.models import Q
from .helper import format_data, validate_email, validate_phone
from django.shortcuts import redirect

def home_view(requst):
	return redirect('resolve-contact')


@api_view(['GET'])
def get_contact(requst):

	
	contacts = Contact.objects.all()
	serializer = ContactSerializer(contacts,many=True)
	response_data = format_data(serializer)
	return Response(response_data)



@api_view(['POST'])
def resolve_contact(request):

	if not isinstance(request.data, dict):
		return Response({'error': 'Invalid input format. Expected a JSON object.'}, status=400)

	email = request.data.get('email')
	phone = request.data.get('phone')
	

	if not email and not phone:
		return Response({'Error:  Email and Phone is required'}, status=400)

	if email and not validate_email(email):
		return Response({'error': 'Invalid email format'}, status=400)

	if phone and not validate_phone(phone):
		return Response({'error': 'Invalid phone number format'}, status=400)

	existing_record = Contact.objects.filter(email=email, phone=phone).first()
	
	if existing_record :
		primary_contact = existing_record.primary_contact
		related_contacts = Contact.objects.filter(primary_contact=primary_contact)
		serializer = ContactSerializer(related_contacts,many=True)
		response_data = format_data(serializer)
		return Response(response_data)


	else:

		contacts = Contact.objects.filter(Q(email=email) | Q(phone=phone))

		email_exists = contacts.filter(email=email).exists()
		phone_exists = contacts.filter(phone=phone).exists()
		

		if email_exists and phone_exists:

			unique = contacts.values('primary_contact').distinct()
			unique_primary_contacts = list({item['primary_contact'] for item in unique})

			if len(unique_primary_contacts) == 1:
				related_contacts = Contact.objects.filter(primary_contact__in=unique_primary_contacts)
				serializer = ContactSerializer(related_contacts,many=True)
				#response_data = format_data(serializer)
				return Response(response_data)




			contacts = Contact.objects.filter(id__in=unique_primary_contacts)
			primary_contact = contacts.earliest('created_at').primary_contact
			all_contacts = Contact.objects.filter(primary_contact__in=unique_primary_contacts)
			all_contacts.update(primary_contact=primary_contact)
			related_contacts = primary_contact.linked_contacts.all()
			serializer = ContactSerializer(related_contacts,many=True)
			response_data = format_data(serializer)
			return Response(response_data)

		else:

			contacts = Contact.objects.filter(email = email) | Contact.objects.filter(phone=phone)

			if contacts.exists():
				primary_contact = contacts.earliest('created_at').primary_contact
				secondary_contact = Contact(email=email,phone=phone,primary_contact=primary_contact)
				secondary_contact.save()

			else:
				primary_contact = Contact(email=email,phone=phone)
				primary_contact.save()
				primary_contact.primary_contact = primary_contact
				primary_contact.save()


			related_contacts = Contact.objects.filter(primary_contact=primary_contact)
			serializer = ContactSerializer(related_contacts,many=True)
			response_data = format_data(serializer)
			return Response(response_data)
