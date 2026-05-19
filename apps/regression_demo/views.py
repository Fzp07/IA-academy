from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from .services import RegressionService
import pandas as pd

@login_required
def regression_demo_index(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            csv_file = request.FILES['csv_file']
            x_column = request.POST.get('x_column')
            y_column = request.POST.get('y_column')
            test_size = float(request.POST.get('test_size', 0.2))
            
            # Verificar que el archivo es CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Por favor, sube un archivo CSV válido.')
                return render(request, 'regression_demo/index.html')
            
            # Procesar el archivo
            result = RegressionService.process_csv(csv_file, x_column, y_column, test_size)
            
            # Guardar en sesión para mostrar resultados
            request.session['regression_result'] = {
                'metrics': result['metrics'],
                'plot_json': result['plot_json'],
                'dataset_info': result['dataset_info'],
                'x_column': x_column,
                'y_column': y_column
            }
            
            messages.success(request, '¡Análisis completado exitosamente!')
            
            context = {
                'result': result,
                'x_column': x_column,
                'y_column': y_column,
                'columns': result['dataset_info']['columnas']
            }
            
            return render(request, 'regression_demo/result.html', context)
            
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
            return render(request, 'regression_demo/index.html')
    
    # Para GET, mostrar el formulario
    return render(request, 'regression_demo/index.html')

@login_required
def regression_demo_result(request):
    result = request.session.get('regression_result')
    if not result:
        messages.warning(request, 'No hay resultados para mostrar. Por favor, realiza un análisis primero.')
        return redirect('regression_demo:index')
    
    return render(request, 'regression_demo/result.html', {'result': result})