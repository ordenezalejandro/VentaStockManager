from django.shortcuts import render
from .models import Proveedor
from .forms import CompraAdminForm
from dal import autocomplete
from django.db import models

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


class ProveedorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Proveedor.objects.none()

        qs = Proveedor.objects.all()

        if self.q:
            qs = qs.filter(
                models.Q(nombre__icontains=self.q)|
                models.Q(apellido__icontains=self.q))

        return qs