from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('ШАУРМА', _('Shawarma')),
        ('НА МАНГАЛЕ', _('Grilled')),
        ('ЛАХМАДЖО', _('Lahmajo')),
        ('ФАЛАФЕЛ', _('Falafel')),
        ('СУПЫ', _('Soups')),
        ('НАПИТКИ', _('Drinks')),
        ('ЗАКУСКИ', _('Snacks')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    name_hy = models.CharField(max_length=200, blank=True, verbose_name=_("Name (Armenian)"))
    name_ru = models.CharField(max_length=200, blank=True, verbose_name=_("Name (Russian)"))
    name_en = models.CharField(max_length=200, blank=True, verbose_name=_("Name (English)"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    description_hy = models.TextField(blank=True, verbose_name=_("Description (Armenian)"))
    description_ru = models.TextField(blank=True, verbose_name=_("Description (Russian)"))
    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name=_("Category"))
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, verbose_name=_("Image"))
    is_available = models.BooleanField(default=True, verbose_name=_("Available"))
    
    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
    
    def get_translated_name(self):
        from django.utils import translation
        lang = translation.get_language()
        
        if lang == 'hy' and self.name_hy:
            return self.name_hy
        elif lang == 'ru' and self.name_ru:
            return self.name_ru
        elif lang == 'en' and self.name_en:
            return self.name_en
        else:
            return self.name
    
    def get_translated_description(self):
        from django.utils import translation
        lang = translation.get_language()
        
        if lang == 'hy' and self.description_hy:
            return self.description_hy
        elif lang == 'ru' and self.description_ru:
            return self.description_ru
        elif lang == 'en' and self.description_en:
            return self.description_en
        else:
            return self.description
    
    def get_translated_category(self):
        from django.utils.translation import gettext as _
        for code, label in self.CATEGORY_CHOICES:
            if code == self.category:
                return str(label)
        return self.category


class Order(models.Model):
    customer_name = models.CharField(max_length=200, verbose_name=_("Customer Name"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    order_details = models.TextField(verbose_name=_("Order Details"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Price"), default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    is_processed = models.BooleanField(default=False, verbose_name=_("Processed"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("User"))
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']
    
    def __str__(self):
        from django.utils.translation import gettext as _
        return _("Order from %(name)s - %(date)s") % {
            'name': self.customer_name,
            'date': self.created_at.strftime('%d.%m.%Y %H:%M')
        }