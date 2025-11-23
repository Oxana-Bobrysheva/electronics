from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Contact, NetworkNode


class NetworkModelTests(TestCase):
    def setUp(self):
        """Создаем тестовые данные для каждого теста"""

    def test_network_node_creation(self):
        """Тест создания NetworkNode"""
        contact = Contact.objects.create(
            email="factory@example.com",
            country="Russia",
            city="Moscow",
            street="Factory Street",
            house_number="1"
        )

        factory = NetworkNode.objects.create(
            name="Test Factory",
            contact=contact
        )

        self.assertEqual(factory.name, "Test Factory")
        self.assertEqual(factory.level, 0)

    def test_retail_network_level(self):
        """Тест вычисления уровня для розничной сети"""
        factory_contact = Contact.objects.create(
            email="factory2@example.com",
            country="Russia",
            city="Moscow",
            street="Factory Street",
            house_number="2"
        )

        retail_contact = Contact.objects.create(
            email="retail@example.com",
            country="Russia",
            city="Moscow",
            street="Retail Street",
            house_number="3"
        )

        factory = NetworkNode.objects.create(
            name="Test Factory",
            contact=factory_contact
        )

        retail = NetworkNode.objects.create(
            name="Test Retail",
            contact=retail_contact,
            supplier=factory
        )

        self.assertEqual(retail.level, 1)

    def test_entrepreneur_level(self):
        """Тест вычисления уровня для предпринимателя"""
        factory_contact = Contact.objects.create(
            email="factory3@example.com",
            country="Russia",
            city="Moscow",
            street="Factory Street",
            house_number="4"
        )

        retail_contact = Contact.objects.create(
            email="retail2@example.com",
            country="Russia",
            city="Moscow",
            street="Retail Street",
            house_number="5"
        )

        entrepreneur_contact = Contact.objects.create(
            email="entrepreneur@example.com",
            country="Russia",
            city="Moscow",
            street="Entrepreneur Street",
            house_number="6"
        )

        factory = NetworkNode.objects.create(
            name="Test Factory",
            contact=factory_contact
        )

        retail = NetworkNode.objects.create(
            name="Test Retail",
            contact=retail_contact,
            supplier=factory
        )

        entrepreneur = NetworkNode.objects.create(
            name="Test Entrepreneur",
            contact=entrepreneur_contact,
            supplier=retail
        )

        self.assertEqual(entrepreneur.level, 2)


class NetworkAPITests(TestCase):
    def setUp(self):
        """Создаем тестовые данные и пользователя"""
        self.client = APIClient()

        # Создаем активного пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_active=True
        )

        # Создаем тестовые данные
        self.contact = Contact.objects.create(
            email="api_test@example.com",
            country="Russia",
            city="Moscow",
            street="API Street",
            house_number="7"
        )

        self.factory = NetworkNode.objects.create(
            name="API Factory",
            contact=self.contact
        )

    def test_api_access_without_auth(self):
        """Тест доступа к API без аутентификации"""
        response = self.client.get('/api/network-nodes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_access_with_auth(self):
        """Тест доступа к API с аутентификацией"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/network-nodes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_filter_by_country(self):
        """Тест фильтрации по стране"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/network-nodes/?contact__country=Russia')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'API Factory')

    def test_debt_field_read_only(self):
        """Тест что поле debt нельзя изменить через API"""
        self.client.force_authenticate(user=self.user)

        # Пытаемся изменить debt через PUT
        data = {'name': 'Updated Factory', 'debt': '1000.00'}
        response = self.client.put(f'/api/network-nodes/{self.factory.id}/', data)

        print(response)
        self.factory.refresh_from_db()
        self.assertEqual(self.factory.debt, 0)
