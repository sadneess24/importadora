from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from m_categoria.models import Categoria
from cart.models import *
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
# Create your views here.
def tienda(request, category_slug=None):
    categorias = None
    productos = None

    if category_slug != None:
        categorias = get_object_or_404(Categoria, slug = category_slug)
        productos =Producto.objects.filter(categoria = categorias, is_available=True)
        paginador = Paginator(productos, 12)
        pagina = request.GET.get('pagina')
        pagina_productos = paginador.get_page(pagina)
        contar_producto = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True).order_by('id')
        paginador = Paginator(productos, 12)
        pagina = request.GET.get('pagina')
        pagina_productos = paginador.get_page(pagina)
        contar_producto = productos.count()

    contexto = {
        'productos': pagina_productos,
        'contar_producto': contar_producto,
    }
    return render(request, 'store/store.html', contexto)

def detalle_producto(request, category_slug, product_slug):
    try:
        single_product = Producto.objects.get(categoria__slug=category_slug, slug=product_slug)
        in_cart = CarroItem.objects.filter(carro__cart_id=_cart_id(request), producto=single_product).exists()
        variaciones = Variacion.objects.filter(producto=single_product, is_active=True)
        capacidad_variaciones = variaciones.filter(categoria_variacion='capacidad')
        tipo_variaciones = variaciones.filter(categoria_variacion='tipo')
        largo_variaciones = variaciones.filter(categoria_variacion='largo')
        color_variaciones = variaciones.filter(categoria_variacion='color')
        #return HttpResponse(in_cart)
        #exit()
    except Exception as e:
        raise e
    
    resenias = CalificacionResenia.objects.filter(producto_id=single_product.id, estado=True)

    contexto = {
        'single_product': single_product,
        'in_cart':in_cart,
        'capacidad_variaciones': capacidad_variaciones,
        'tipo_variaciones': tipo_variaciones,
        'largo_variaciones': largo_variaciones,
        'color_variaciones': color_variaciones,
        'resenias':resenias,
    }
    return render(request, 'store/product-detail.html', contexto)

def buscar(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            productos = Producto.objects.order_by('-created_date').filter(Q(descripcion__icontains=keyword) | Q(nombre_producto__icontains=keyword))
            contar_producto = productos.count()
    contexto = {
        'productos':productos,
        'contar_producto': contar_producto,
    }
    return render(request, 'store/store.html', contexto)

@login_required
def subir_resena(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ReseniaFormulario(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.producto = producto
            resena.user = request.user
            resena.ip = request.META.get('REMOTE_ADDR')
            resena.save()
            return redirect('detalle_producto', category_slug=producto.categoria.slug, product_slug=producto.slug)
    else:
        form = ReseniaFormulario()
    return render(request, 'store/product-detail.htmll', {'form': form, 'producto': producto})


@login_required
def modificar_resena(request, resena_id):
    resena = get_object_or_404(CalificacionResenia, id=resena_id, user=request.user)
    if request.method == 'POST':
        form = ReseniaFormulario(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            return redirect('detalle_producto', producto_id=resena.producto.id)
    else:
        form = ReseniaFormulario(instance=resena)
    return render(request, 'store/product-detail.html', {'form': form, 'producto': resena.producto})

@login_required
def eliminar_resena(request, resena_id):
    resena = get_object_or_404(CalificacionResenia, id=resena_id, user=request.user)
    if request.method == 'POST':
        resena.delete()
        return redirect('detalle_producto', producto_id=resena.producto.id)
    return render(request, 'store/product-detail.html', {'resena': resena})