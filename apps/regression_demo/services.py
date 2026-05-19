import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json

class RegressionService:
    @staticmethod
    def process_csv(file, x_column, y_column, test_size=0.2):
        """Procesa el archivo CSV y realiza regresión lineal"""
        
        # Leer CSV
        df = pd.read_csv(file)
        
        # Validar columnas
        if x_column not in df.columns or y_column not in df.columns:
            raise ValueError("Las columnas seleccionadas no existen en el archivo")
        
        # Preparar datos
        X = df[[x_column]].values
        y = df[y_column].values
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Entrenar modelo
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Predicciones
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Métricas
        metrics = {
            'coeficientes': {
                'intercepto': model.intercept_,
                'pendiente': model.coef_[0]
            },
            'r2_train': r2_score(y_train, y_pred_train),
            'r2_test': r2_score(y_test, y_pred_test),
            'rmse_train': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'rmse_test': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'mae_train': mean_absolute_error(y_train, y_pred_train),
            'mae_test': mean_absolute_error(y_test, y_pred_test)
        }
        
        # Crear gráfico interactivo
        fig = go.Figure()
        
        # Puntos de datos
        fig.add_trace(go.Scatter(
            x=X.flatten(), y=y,
            mode='markers',
            name='Datos Reales',
            marker=dict(color='blue', size=8, opacity=0.6)
        ))
        
        # Línea de regresión
        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_range = model.predict(x_range)
        
        fig.add_trace(go.Scatter(
            x=x_range.flatten(), y=y_range,
            mode='lines',
            name='Regresión Lineal',
            line=dict(color='red', width=2)
        ))
        
        # Configuración del gráfico
        fig.update_layout(
            title=f'Regresión Lineal: {y_column} vs {x_column}',
            xaxis_title=x_column,
            yaxis_title=y_column,
            hovermode='closest',
            template='plotly_white'
        )
        
        # Convertir a JSON
        plot_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        
        # Información del dataset
        dataset_info = {
            'filas': len(df),
            'columnas': list(df.columns),
            'tipos_datos': df.dtypes.astype(str).to_dict(),
            'estadisticas': df.describe().to_dict()
        }
        
        return {
            'metrics': metrics,
            'plot_json': plot_json,
            'dataset_info': dataset_info,
            'model': model,
            'df': df,
            'x_column': x_column,
            'y_column': y_column
        }