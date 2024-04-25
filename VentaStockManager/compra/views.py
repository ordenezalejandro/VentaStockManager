from django.shortcuts import render

from .forms import CompraAdminForm

def formulario_compra(request):
    if request.method == 'POST':
        form_compra = CompraAdminForm(request.POST,request.file)
        
        if form_compra.is_valid():           # Procesa los datos del formulario
            # Guarda los datos en la base de datos, etc.
            # Por ejemplo:
            compra = form_compra.save()

            return redirect('página_de_confirmación')  # Redirige a la página de confirmación
    else:
        form_compra = CompraAdminForm()
        
        return render(request, 'formulario_compra.html', {'form_compra': form_compra})
