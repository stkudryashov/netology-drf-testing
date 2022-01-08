import pytest

from django.urls import reverse
from students.models import *


@pytest.mark.django_db
def test_courses_detail(api_client, course_factory):
    course_factory()
    course = Course.objects.first()

    url = reverse('courses-detail', kwargs={'pk': course.pk})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data.get('name') == course.name


@pytest.mark.django_db
def test_courses_list(api_client, course_factory):
    course_factory(_quantity=10)

    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 10


@pytest.mark.django_db
def test_filter_by_id(api_client, course_factory):
    course_factory(_quantity=10)

    url = reverse('courses-list')
    response = api_client.get(url, data={'id': Course.objects.last().id})

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_filter_by_name(api_client, course_factory):
    course_factory(_quantity=10)

    url = reverse('courses-list')
    response = api_client.get(url, data={'name': Course.objects.last().name})

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_course(api_client):
    url = reverse('courses-list')
    response = api_client.post(url, data={'name': 'Python Web Development'})

    assert response.status_code == 201
    assert response.data.get('name') == 'Python Web Development'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course_factory()
    course = Course.objects.last()

    url = reverse('courses-detail', kwargs={'pk': course.pk})
    response = api_client.patch(url, data={'name': 'PHP Web Development'})

    assert response.status_code == 200
    assert response.data.get('name') == 'PHP Web Development'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course_factory()
    course = Course.objects.last()

    url = reverse('courses-detail', kwargs={'pk': course.pk})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert len(api_client.get(reverse('courses-list')).data) == 0
