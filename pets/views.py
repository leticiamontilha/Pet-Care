from rest_framework.views import APIView, Request, Response, status
from django.db.models import Q
from pets.models import Pet
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

# Create your views here.

class PetViews(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")
        
        try:
            group = Group.objects.get(
                scientific_name__iexact=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
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
        traits_data = request.query_params.get("trait", None)

        if traits_data:
            pets = Pet.objects.filter(traits__name=traits_data)

            result_page = self.paginate_queryset(pets, request, view=self)
            
            serializer = PetSerializer(result_page, many=True)

            return self.get_paginated_response(serializer.data)
        
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result_page, many=True)
    
        return self.get_paginated_response(serializer.data)


class PetDetaisView(APIView):
    def get(self, request:Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request:Request, pet_id= int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def patch(self, request:Request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            try:
                new_group = Group.objects.get(
                    scientific_name=group_data["scientific_name"]
                )
                pet.group = new_group

            except Group.DoesNotExist:
                add_group = Group.objects.create(**group_data)
                pet.group = add_group
        
        if traits_data:
            for traits in traits_data:
                 traits_obj = Trait.objects.filter(
                    name__iexact=traits["name"]
                ).first()
                 
            if not traits_obj:
                traits_obj = Trait.objects.create(**traits)

            pet.traits.add(traits_obj)
        
        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        
        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status=status.HTTP_200_OK)
