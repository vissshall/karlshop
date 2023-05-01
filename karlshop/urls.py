from django.contrib import admin
from django.conf import settings
from django.urls import path

from django.conf.urls.static import static
from mainapp import views as mainapp


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",mainapp.homePage),
    path("shop/<str:mc>/<str:sc>/<str:br>/",mainapp.shopPage),
    path("price-filter/",mainapp.priceFilterPage),
    path("single-product/<int:num>/",mainapp.singleProductPage),
    path("cart/",mainapp.cartPage),
    path("checkout/",mainapp.checkoutPage), 
    path("search/",mainapp.searchPage),
    path('login/',mainapp.loginPage),
    path('logout/',mainapp.logoutPage),
    path('signup/',mainapp.signupPage),
    path("profile/",mainapp.profilePage),
    path("update-profile/",mainapp.updateProfilePage),
    path("add-to-cart/",mainapp.addToCartPage),
    path("delete-cart/<str:num>/",mainapp.deleteFromCartPage),
    path("update-cart/<str:num>/<str:op>/",mainapp.updateCartPage),
    path('placeholder/',mainapp.placeOrderPage),
    path('confirmation/',mainapp.confirmationPage),
    path('add-to-wishlist/<int:num>/',mainapp.addToWishlistPage),
    path('remove-from-wishlist/<int:num>/',mainapp.removeFromWishlistPage),
    path('contact/',mainapp.contactUsPage),
    path('forget-password1/',mainapp.forgetPasswordPage1),
    path('forget-password2/',mainapp.forgetPasswordPage2),
    path('forget-password3/',mainapp.forgetPasswordPage3),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',mainapp.paymentSuccess),
 ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
