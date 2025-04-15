from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product , Category, Hub
import csv

def products_list(request):
    if request.GET.get('export') == 'csv':
       
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        # Definir encabezados
        fieldnames = ['name', 'categorys', 'hubs', 'price']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()

        # Obtener productos con sus categorías y hubs
        products = Product.objects.all().prefetch_related('category', 'hub')
        
        # Esxpedir productos en el CSV
        for product in products:
            writer.writerow({
                'name': product.name,
                'categorys': '|'.join(cat.name for cat in product.category.all()),
                'hubs': '|'.join(hub.name for hub in product.hub.all()),
                'price': product.price
            })
        
        return response 

    #  si no es un export, mostrar la lista de productos
    products = Product.objects.all().prefetch_related('category', 'hub')
    return render(request, 'products_list.html', {'products': products})

def products_upload(request):
    errors = []

    success_count = 0
    total_rows = 0
    required_fields = ['name', 'categorys', 'hubs', 'price']

    
    if request.method == 'POST':
        ## Obtener el archivo CSV
        csv_file = request.FILES.get('csv_file')
            
        # Validar que el archivo termine en .csv
        if not csv_file.name.endswith('.csv'):
            errors.append('El archivo debe ser un archivo CSV')
         
            
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines() 
            reader = csv.DictReader(decoded_file)
            
            # Obtener el número de filas
            for row_number, row in enumerate(reader, start=1):
             total_rows += 1

            # Validar que todos los campos esten presentes [name, category, hubs, price]
             if all(row.get(field, '').strip() for field in required_fields):
                success_count += 1   
                try:
   
                   # Crear el producto
                    product ,created = Product.objects.get_or_create(
                        name=row['name'].strip(),
                        price=float(row['price'].strip()) if row['price'].strip() else 0,
                    )
                    
    
             # Validar las categorías
                    categories_names = [cat.strip() for cat in row['categorys'].split('|')]
                    for cat_name in categories_names:
                        if cat_name: 
                            category, _ = Category.objects.get_or_create(name=cat_name)
                            product.category.add(category)
                    
            # Validar los hubs
                    hubs_names = [hub.strip() for hub in row['hubs'].split('|')]
                    for hub_name in hubs_names:
                        if hub_name:
                            hub, _ = Hub.objects.get_or_create(name=hub_name)
                            product.hub.add(hub)
                    product.save()
                    
                except Exception as row_error:
                    print(f'Error procesando fila {row_number}: {str(row_error)}')
                    continue

         
            if success_count != total_rows:
                if success_count == 0:
                    # agregar mensaje de error varias filas
                    errors.extend(
                        [
                            "No se ha encontrado ninguna fila con los campos requeridos",
                        f"Campos requeridos: ({', '.join(required_fields)})",
                        ]
                    
                    )

                else:
                    errors.append(f'Se han procesado {success_count} de {total_rows} filas')

            
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')

    return render(request, 'upload.html', {
    "errors": errors,
    "success_count": success_count,
    "total_rows": total_rows,
    "success": success_count > 0 and success_count == total_rows,
    
    })