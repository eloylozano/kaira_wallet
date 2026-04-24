Para que **Kaira** pase de ser un prototipo visual a una herramienta real, este es el orden lógico que yo seguiría. He diseñado este checklist priorizando el **"Core Loop"** (el ciclo básico de uso): si no puedes meter datos, no tienes nada que ver ni que exportar.

### 🏁 Checklist de Desarrollo: Hoja de Ruta

#### 1. El Formulario de Transacción (Prioridad Máxima 🔴)
Sin datos, la app está vacía. Es lo primero que debes pulir.
* [x] Crear el componente de entrada de datos (monto, categoría, descripción).
* [x] Implementar un teclado numérico personalizado (tipo cajero) para que se sienta iOS.
* [x] Guardar los datos en un Store o LocalStorage.

#### 2. El Historial de Movimientos (Prioridad Alta 🟠)
Necesitas ver lo que acabas de anotar para sentir que la app "funciona".
* [x] Crear una lista scrollable de transacciones.
* [x] Agrupar gastos por fecha (Hoy, Ayer, esta semana).
* [x] Implementar el "Swipe to delete" (deslizar para borrar), muy típico de iPhone.
* [x] Diseño de las filas con iconos por categoría.

#### 3. El Dashboard / Inicio (Prioridad Media 🟡)
Aquí es donde la app se pone "bonita" y útil de un vistazo.
* [x] Crear la tarjeta de "Balance Total".
* [x] Gráfico simple (quizás de donuts o barras) de gastos por categoría.
* [x] Resumen de gastos del mes actual vs mes anterior.

#### 4. Exportación y Limpieza (Prioridad Baja 🟢)
Lo que mencionabas antes. Se hace al final porque depende de tener muchos datos para probar.
* [ ] Generar el archivo CSV a partir de lo guardado en LocalStorage.
* [ ] Función de "Borrar todo" (con el modal de confirmación que ya tienes).

---
