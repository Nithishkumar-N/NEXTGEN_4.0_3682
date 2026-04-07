from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import UserProfile

class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='supplier',
            company_name='Test Company',
            phone='9876543210'
        )
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.role, 'supplier')
        self.assertTrue(profile.is_supplier())
        self.assertFalse(profile.is_buyer())
    
    def test_buyer_profile(self):
        """Test buyer profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='buyer',
            company_name='Buyer Company'
        )
        self.assertTrue(profile.is_buyer())
        self.assertFalse(profile.is_supplier())
    
    def test_supplier_approval(self):
        """Test supplier approval status"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='supplier',
            is_approved=False
        )
        self.assertFalse(profile.is_approved)
        
        profile.is_approved = True
        profile.save()
        self.assertTrue(profile.is_approved)


class AuthenticationTest(TestCase):
    """Test authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            role='buyer'
        )
    
    def test_login_page_loads(self):
        """Test login page loads"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_successful_login(self):
        """Test successful login"""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
    
    def test_invalid_login(self):
        """Test invalid credentials"""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_register_page_loads(self):
        """Test register page loads"""
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_logout_redirects_to_login(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertRedirects(response, '/accounts/login/')


class ProfileViewTest(TestCase):
    """Test profile view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.user,
            role='supplier',
            company_name='Test Company'
        )
    
    def test_profile_requires_login(self):
        """Test that profile view requires login"""
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')
    
    def test_authenticated_user_can_view_profile(self):
        """Test authenticated user can view profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
