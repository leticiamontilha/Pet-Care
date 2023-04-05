from rest_framework.views import APIView, Request, Response, status
from django.db.models import Q
from pets.models import Pet
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class PetViews(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")
        
        group = Group.objects.get(
            scientific_name__iexact=group_data["scientific_name"]
        )
        
        if not group:
            group = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=group)

        for trait_el in traits_data:
            trait = Trait.objects.filter(
                name__iexact=trait_el["name"]
            ).first()

            if not trait: 
                trait = Trait.objects.create(**trait_el)
            pet.traits.add(trait)

        serializer = PetSerializer(pet)
        pet.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
   

    def get(self, request:Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result_page, many=True)
    
        return self.get_paginated_response(serializer.data)


class PetDetaisView(APIView):
    ...
   