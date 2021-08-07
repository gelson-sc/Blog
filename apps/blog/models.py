from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile-images/%y/%m/%d/', default='profile-images/default.png',
                                    blank=False, null=False)
    birth_date = models.DateField(verbose_name='Data de nascimento', null=True, blank=True)
    whatsapp = models.CharField(verbose_name=u"Whatsapp", max_length=25, null=True, blank=True)
    date_updated = models.DateTimeField(verbose_name='Última Atualização', auto_now=True)
    date_add = models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True)
    status = models.BooleanField(verbose_name='Status', default=True)

    def __str__(self):
        return 'Account {} {} '.format(self.user.username, self.whatsapp)

    def get_first_name(self):
        return self.user.firstname.split(" ")[0]

    class Meta:
        db_table = 'blog_account'
        verbose_name_plural = 'Contas'
        verbose_name = 'Conta'


class Category(models.Model):
    title = models.CharField(verbose_name='Título', max_length=50, unique=True)
    description = models.TextField(verbose_name='Descricão', null=True, blank=True)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Ativo', default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('blog:list_of_post_by_category', args=[self.slug])
        return "/categories/%s/" % self.slug

    class Meta:
        db_table = 'blog_category'
        verbose_name_plural = 'Categorias'
        verbose_name = 'Categoria'


class Post(models.Model):
    STATUS = (
        (0, "Inativo"),
        (1, "Rascunho"),
        (2, "Publicado")
    )
    RATING_CHOICES = ((1, "★☆☆☆☆"), (2, "★★☆☆☆"), (3, "★★★☆☆"), (4, "★★★★☆"), (5, "★★★★★"),)

    title = models.CharField(verbose_name='Título', max_length=200, unique=True)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(verbose_name='Slug', max_length=200, unique=True)
    author = models.ForeignKey(Account, verbose_name=u"Conta", on_delete=models.CASCADE, related_name='account_posts')
    views = models.IntegerField(verbose_name='Visualizacões', default=0)
    rating = models.PositiveIntegerField(verbose_name='Estrelas', null=True, blank=True, choices=RATING_CHOICES,
                                         default=1)
    like = models.PositiveIntegerField(verbose_name='Gostei', null=True, blank=True, default=0)
    unlike = models.PositiveIntegerField(verbose_name='Não gostei', null=True, blank=True, default=0)
    content = models.TextField(verbose_name='Conteúdo')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    enable_comments = models.BooleanField(verbose_name='Habilitar comentários', default=False)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs={"slug": str(self.slug)})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']
        db_table = 'blog_post'
        verbose_name_plural = 'Post'
        verbose_name = 'Posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
        verbose_name_plural = 'Comentários'
        verbose_name = 'Comentário'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
