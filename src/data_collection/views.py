from django.shortcuts import render, redirect, get_object_or_404
from .models import ScrapedData, Product
from django.contrib.auth.decorators import login_required

@login_required
def product_selection(request):
    products = Product.objects.all()
    return render(request, 'product_selection.html', {'products': products})

@login_required
def scraped_data_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    scraped_data = ScrapedData.objects.filter(product=product, archived=False).order_by('-listing_date', 'created_at')
    return render(request, 'scraped_data_list.html', {'product': product, 'scraped_data': scraped_data})

@login_required
def archive_selected(request):
    if request.method == 'POST':
        # Recupera os IDs enviados pelo formulário
        ids = request.POST.getlist('selected_items')
        product_id = request.POST.get('product_id')
        # Marca os registros como arquivados
        ScrapedData.objects.filter(id__in=ids).update(archived=True)
        return redirect('scraped_data_list', product_id=product_id)
