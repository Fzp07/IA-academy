from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import GeneticAlgorithmService

@login_required
def genetic_demo_index(request):
    if request.method == 'POST':
        try:
            # Obtener parámetros del formulario
            function_name = request.POST.get('function', 'f1')
            population_size = int(request.POST.get('population_size', 50))
            generations = int(request.POST.get('generations', 100))
            cx_prob = float(request.POST.get('crossover_prob', 0.7))
            mut_prob = float(request.POST.get('mutation_prob', 0.2))
            selection_type = request.POST.get('selection_type', 'tournament')
            
            # Ejecutar algoritmo genético
            result = GeneticAlgorithmService.maximize_function(
                function_name=function_name,
                population_size=population_size,
                generations=generations,
                cx_prob=cx_prob,
                mut_prob=mut_prob,
                selection_type=selection_type
            )
            
            context = {
                'result': result,
                'params': {
                    'function': function_name,
                    'population_size': population_size,
                    'generations': generations,
                    'crossover_prob': cx_prob,
                    'mutation_prob': mut_prob,
                    'selection_type': selection_type
                }
            }
            
            messages.success(request, '¡Algoritmo Genético ejecutado exitosamente!')
            return render(request, 'genetic_demo/result.html', context)
            
        except Exception as e:
            messages.error(request, f'Error al ejecutar el algoritmo: {str(e)}')
            return render(request, 'genetic_demo/index.html')
    
    # GET: mostrar formulario
    return render(request, 'genetic_demo/index.html')

@login_required
def genetic_demo_result(request):
    return render(request, 'genetic_demo/result.html')