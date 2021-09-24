import itertools

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from Edu_book.models import Product
from Edu_comment.forms import CommentForm
from Edu_comment.models import ProductComment
from Edu_course.models import Course
from Edu_order.forms import UserNewOrderForm


class ProductsList(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.get_main_products()


# class ProductsListByCategory(ListView):
#     template_name = 'products/products_list.html'
#     paginate_by = 6
#
#     def get_queryset(self):
#         print(self.kwargs)
#         category_name = self.kwargs['category_name']
#         category = ProductCategory.objects.filter(name__iexact=category_name).first()
#         if category is None:
#             raise Http404('صفحه ی مورد نظر یافت نشد')
#         return Product.objects.get_products_by_category(category_name)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, *args, **kwargs):
    selected_product_id = kwargs['productId']
    new_order_form = UserNewOrderForm(request.POST or None, initial={'product_id': selected_product_id})

    product = Product.objects.get_by_id(selected_product_id)

    if product is None or not product.active or not product.is_main:
        raise Http404('محصول مورد نظر یافت نشد')


    if request.method == 'POST':

        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            full_name = request.POST['full_name']
            email = request.POST['email']
            text = request.POST['text']
            print(full_name,email,text)
            product_object = Product.objects.get_by_id(selected_product_id)
            ProductComment.objects.create(full_name=full_name,email=email,text=text,object=product_object,confirmed=False).save()

            return HttpResponseRedirect(f'/products/{selected_product_id}/{product_object.title.replace(" ", "-")}')

    comment_list = ProductComment.objects.filter(object__id=selected_product_id,confirmed=True).all()

    form = CommentForm()

    # related_products = Product.objects.get_queryset().filter(categories__product=product).distinct()

    # grouped_related_products = my_grouper(3, related_products)

    context = {
        'product': product,
        'new_order_form' : new_order_form,
        'comments': comment_list,
        'form': form

    }

    return render(request, 'products/product_detail.html', context)


class SearchProductsView(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        if query is not None:


            return  Product.objects.search(query)

        return Product.objects.get_active_products()


def product_detail_from_home(request, *args, **kwargs):
    selected_product_id = kwargs['productId']

    product = Product.objects.get_by_id(selected_product_id)

    if product is None or not product.active:
        raise Http404('محصول مورد نظر یافت نشد')

    context = {
        'product': product,

    }

    return render(request, 'home_page.html', context)
