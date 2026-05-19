from deap import base, creator, tools
import numpy as np
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
import random

# Crear tipos DEAP una sola vez a nivel de módulo
if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

class GeneticAlgorithmService:
    @staticmethod
    def maximize_function(function_name, population_size=50, generations=100, 
                         cx_prob=0.7, mut_prob=0.2, selection_type='tournament'):
        """
        Ejecuta algoritmo genético para maximizar una función
        """
        
        # Definir funciones objetivo
        functions = {
            'f1': {
                'func': lambda x: x[0]**2,
                'bounds': [-10, 10],
                'name': 'f(x) = x²',
                'dim': 1
            },
            'f2': {
                'func': lambda x: -((x[0]-2)**2) + 5,
                'bounds': [-5, 10],
                'name': 'f(x) = -(x-2)² + 5',
                'dim': 1
            },
            'knapsack': {
                'func': None,  # Implementación especial para mochila
                'bounds': [0, 1],
                'name': 'Problema de la Mochila',
                'dim': 10
            }
        }
        
        if function_name not in functions:
            raise ValueError("Función no válida")
        
        func_info = functions[function_name]
        
        if function_name == 'knapsack':
            return GeneticAlgorithmService._knapsack_ga(population_size, generations, 
                                                       cx_prob, mut_prob, selection_type)
        
        toolbox = base.Toolbox()

        # Atributos
        low, high = func_info['bounds']
        toolbox.register("attr_float", random.uniform, low, high)
        toolbox.register("individual", tools.initRepeat, creator.Individual,
                        toolbox.attr_float, n=func_info['dim'])
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        # Operadores genéticos
        toolbox.register("evaluate", lambda ind: (func_info['func'](ind),))
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)

        if selection_type == 'tournament':
            toolbox.register("select", tools.selTournament, tournsize=3)
        else:
            toolbox.register("select", tools.selRoulette)

        # Ejecutar algoritmo
        pop = toolbox.population(n=population_size)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)
        
        logbook = tools.Logbook()
        
        # Evaluación inicial
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        # Registrar estadísticas
        record = stats.compile(pop)
        logbook.record(gen=0, **record)
        
        # Evolución
        best_fitness_history = [record['max']]
        avg_fitness_history = [record['avg']]
        
        for gen in range(1, generations + 1):
            # Seleccionar nueva población
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))
            
            # Aplicar cruce
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cx_prob:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            
            # Aplicar mutación
            for mutant in offspring:
                if random.random() < mut_prob:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            # Evaluar individuos nuevos
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            # Reemplazar población
            pop[:] = offspring
            
            # Registrar estadísticas
            record = stats.compile(pop)
            logbook.record(gen=gen, **record)
            best_fitness_history.append(record['max'])
            avg_fitness_history.append(record['avg'])
        
        # Obtener mejor individuo
        best_ind = tools.selBest(pop, 1)[0]
        best_fitness = best_ind.fitness.values[0]
        
        # Crear gráfico de evolución
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(generations + 1)),
            y=best_fitness_history,
            mode='lines+markers',
            name='Mejor Fitness',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(range(generations + 1)),
            y=avg_fitness_history,
            mode='lines',
            name='Fitness Promedio',
            line=dict(color='blue', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Evolución del Fitness',
            xaxis_title='Generación',
            yaxis_title='Fitness',
            hovermode='closest',
            template='plotly_white'
        )
        
        plot_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        
        return {
            'best_solution': best_ind,
            'best_fitness': best_fitness,
            'best_fitness_history': best_fitness_history,
            'avg_fitness_history': avg_fitness_history,
            'plot_json': plot_json,
            'logbook': logbook,
            'function_name': func_info['name']
        }
    
    @staticmethod
    def _knapsack_ga(population_size, generations, cx_prob, mut_prob, selection_type):
        """Implementación especial para problema de la mochila"""
        
        # Definir items (peso, valor)
        items = [
            (2, 10), (3, 15), (5, 25), (7, 30), (1, 5),
            (4, 20), (6, 28), (3, 12), (2, 8), (5, 22)
        ]
        max_weight = 20
        
        toolbox = base.Toolbox()
        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual,
                        toolbox.attr_bool, n=len(items))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def evaluate(individual):
            total_weight = sum(items[i][0] for i in range(len(individual)) if individual[i])
            total_value = sum(items[i][1] for i in range(len(individual)) if individual[i])

            # Penalización por exceder peso
            if total_weight > max_weight:
                return (total_value * (max_weight / total_weight) * 0.5,)
            return (total_value,)

        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

        if selection_type == 'tournament':
            toolbox.register("select", tools.selTournament, tournsize=3)
        else:
            toolbox.register("select", tools.selRoulette)

        # Ejecutar algoritmo
        pop = toolbox.population(n=population_size)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)
        
        logbook = tools.Logbook()
        
        # Evaluación inicial
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        record = stats.compile(pop)
        logbook.record(gen=0, **record)
        
        best_fitness_history = [record['max']]
        avg_fitness_history = [record['avg']]
        
        for gen in range(1, generations + 1):
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))
            
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cx_prob:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            
            for mutant in offspring:
                if random.random() < mut_prob:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            pop[:] = offspring
            record = stats.compile(pop)
            logbook.record(gen=gen, **record)
            best_fitness_history.append(record['max'])
            avg_fitness_history.append(record['avg'])
        
        best_ind = tools.selBest(pop, 1)[0]
        best_fitness = best_ind.fitness.values[0]
        
        # Mostrar items seleccionados
        selected_items = [(i, items[i]) for i in range(len(best_ind)) if best_ind[i]]
        total_weight = sum(item[0] for _, item in selected_items)
        total_value = sum(item[1] for _, item in selected_items)
        
        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(generations + 1)),
            y=best_fitness_history,
            mode='lines+markers',
            name='Mejor Valor',
            line=dict(color='green', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=list(range(generations + 1)),
            y=avg_fitness_history,
            mode='lines',
            name='Valor Promedio',
            line=dict(color='blue', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Evolución del Problema de la Mochila',
            xaxis_title='Generación',
            yaxis_title='Valor',
            template='plotly_white'
        )
        
        plot_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        
        return {
            'best_solution': best_ind,
            'best_fitness': best_fitness,
            'selected_items': selected_items,
            'total_weight': total_weight,
            'total_value': total_value,
            'plot_json': plot_json,
            'function_name': 'Problema de la Mochila'
        }