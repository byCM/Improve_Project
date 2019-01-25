from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Item, Menu, Ingredient


class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Test', 'Test@Test.com', 'Test123')

        self.ingredient_1 = Ingredient.objects.create(name='Chocolate')
        self.ingredient_2 = Ingredient.objects.create(name='Vanilla')
        self.ingredient_3 = Ingredient.objects.create(name='Strawberry')

        self.item_1 = Item.objects.create(
            name='Chocolate',
            description='Chocolate Drink',
            chef=self.user)
        self.item_1.ingredients = [self.ingredient_1, self.ingredient_2]

        self.item_2 = Item.objects.create(
            name='Vanilla',
            description='Vanilla Drink',
            chef=self.user)
        self.item_2.ingredients = [self.ingredient_3]

        self.menu_new = Menu.objects.create(
            season='Shakes',
            expiration_date=datetime.date(timezone.now() + timedelta(days=1)))
        self.menu_new.items = [self.item_1, self.item_2]

        self.menu_old = Menu.objects.create(
            season='Chocolate Shake',
            expiration_date=datetime.date(timezone.now() - timedelta(days=1)))
        self.menu_old.items = (self.item_1,)

        self.menu_no_date = Menu.objects.create(
            season='Vanilla Shake',
            expiration_date=None)
        self.menu_no_date.items = (self.item_2,)

    def test_menu_detail(self):
        """Tests menu_detail in views"""
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': self.menu_new.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertEqual(self.menu_new, resp.context['menu'])
        self.assertContains(resp, self.menu_new.season)

    def test_new_menu(self):
        """ create_new_menu view"""
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_new_menu_user(self):
        """ Tests create_new_menu with a user"""
        self.client.login(username='Test', password='Test123')
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')