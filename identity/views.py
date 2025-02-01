from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializer import ContactSerializer
from django.db.models import Q

@api_view(['GET'])
def get_contact(requst):
	serializer = ContactSerializer({'id':1,'email':'suhail@suhail.com','phone':'6468767273'})
	return Response(serializer.data)


@api_view(['POST'])
def resolve_contact(requst):
	email = requst.data.get('email')
	phone = requst.data.get('phone')
	

	if not email and not phone:
		return Response({'Error: Either Email or Phone is required'}, status=400)

	existing_record = Contact.objects.filter(email=email, phone=phone).first()
	
	if existing_record :
		primary_contact = existing_record.primary_contact
		related_contacts = Contact.objects.filter(primary_contact=primary_contact)
		serializer = ContactSerializer(related_contacts,many=True)
		return Response(serializer.data)


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
				return Response(serializer.data)




			contacts = Contact.objects.filter(id__in=unique_primary_contacts)
			primary_contact = contacts.earliest('created_at').primary_contact
			all_contacts = Contact.objects.filter(primary_contact__in=unique_primary_contacts)
			all_contacts.update(primary_contact=primary_contact)
			related_contacts = primary_contact.linked_contacts.all()
			serializer = ContactSerializer(related_contacts,many=True)
			return Response(serializer.data)
		    

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
			return Response(serializer.data)


