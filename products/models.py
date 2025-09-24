from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey('self',verbose_name=_('parent'), on_delete=models.CASCADE, null=True, blank=True,)
    title = models.CharField(verbose_name=_('title'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), upload_to='categories', blank=True)
    is_enabled = models.BooleanField(verbose_name=_('is enabled'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Product(models.Model):
   title = models.CharField(verbose_name=_('title'), max_length=50)
   description = models.TextField(verbose_name=_('description'), blank=True)
   avatar = models.ImageField(verbose_name=_('avatar'), upload_to='products/', blank=True)
   price = models.PositiveIntegerField(verbose_name=_('price'), default=0)
   is_enabled = models.BooleanField(verbose_name=_('is enabled'), default=True)
   categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True,related_name='products')
   created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
   updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

   class Meta:
       db_table = 'products'
       verbose_name = _('product')
       verbose_name_plural = _('products')

   def __str__(self):
      return self.title

class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPES = (
        (FILE_AUDIO, _('Audio file')),
        (FILE_VIDEO, _('Video file')),
        (FILE_PDF, _('PDF file')),
    )
    product = models.ForeignKey(Product, verbose_name=_('product'),related_name='files', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('title'), max_length=50)
    file_type = models.PositiveIntegerField(choices=FILE_TYPES, verbose_name=_('file type'))
    file = models.FileField(verbose_name=_('file'), upload_to='files/%y/%m/%d')
    is_enabled = models.BooleanField(verbose_name=_('is enabled'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
      return self.title