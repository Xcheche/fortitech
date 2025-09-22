from django.shortcuts import render

# Create your views here.


def shop(request):
    # TODO: Implement shop view to display products, categories, and handle filtering and sorting
    return render(request, "shop/shop.html")


# Shop detail view
# TODO: Implement shop detail view
def shop_detail(request):
    return render(request, "shop/shop-detail.html")


# Category view
# TODO: Implement category view to filter products by category


# Search view
# TODO: Implement search functionality to filter products by search query and ajax for dynamic results
