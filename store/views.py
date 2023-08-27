""
from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from store.filters import CubeFilter
from store.utils import check_validity

from .models import Cube
from .serializers import AdminCubeSerializer, CubeSerializer


def home(response):
    return HttpResponse("This is home page. Valid URL's are /create, /list, /my_list, /update, /delete")


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def create_box(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        str: _description_
    """

    if request.method == "POST":
        box = Cube(created_by=request.user)
        data = JSONParser().parse(request)
        serializer = AdminCubeSerializer(box, data=data, partial=True)
        if serializer.is_valid() and check_validity(request.user):
            serializer.save()
            return Response(
                data={
                    "success": True,
                    "Message": "Created Successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "Success": "False",
                "message": check_validity(request.user)[1],
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def list_box(request) -> list:
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        list: _description_
    """

    if request.method == "GET":
        box_queryset = Cube.objects.all()
        boxes = CubeFilter(request.GET, queryset=box_queryset).qs
        serializer = CubeSerializer(boxes, many=True)
        return Response(
            data={
                "success": True,
                "Message": "Fetched Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def my_list_box(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "GET":
        box_queryset = Cube.objects.filter(created_by=request.user)
        boxes = CubeFilter(request.GET, queryset=box_queryset).qs
        serializer = AdminCubeSerializer(boxes, many=True)
        return Response(
            data={
                "success": True,
                "Message": "Fetched Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def update_box(request):
    """_summary_

    Args:
        request (_type_): _description_
        pk (_type_): _description_

    Returns:
        _type_: _description_
    """

    if request.method == "PUT":
        data = JSONParser().parse(request)
        try:
            box = Cube.objects.get(pk=data.get("pk"))
        except Cube.DoesNotExist:
            data = dict()
            data["reason"] = "Box does not Exist"
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminCubeSerializer(box, data=data, partial=True)
        if serializer.is_valid() and check_validity(request.user)[0]:
            serializer.save()
            return Response(
                data={
                    "success": True,
                    "Message": "Updated Successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "Success": "False",
                "message": check_validity(request.user)[1],
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def delete_box(request):
    if request.method == "DELETE":
        data = JSONParser().parse(request)
        try:
            box = Cube.objects.get(pk=data.get("pk"))
            if request.user == box.created_by:
                box.delete()

                return Response(
                    data={
                        "success": True,
                        "Message": "Deleted Successfully",
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                data = dict()
                data["reason"] = "You must be creator of the Box."
                serializer = AdminCubeSerializer(box, data=data)
                return Response(data, status=status.HTTP_403_FORBIDDEN)

        except Cube.DoesNotExist:
            data = dict()
            data["reason"] = "Box does not Exist"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
