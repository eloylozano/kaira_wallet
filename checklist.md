Para que **Kaira** pase de ser un prototipo visual a una herramienta real, este es el orden lógico que yo seguiría. He diseñado este checklist priorizando el **"Core Loop"** (el ciclo básico de uso): si no puedes meter datos, no tienes nada que ver ni que exportar.

### 🏁 Checklist de Desarrollo: Hoja de Ruta

#### 1. El Formulario de Transacción (Prioridad Máxima 🔴)
Sin datos, la app está vacía. Es lo primero que debes pulir.
* [ ] Crear el componente de entrada de datos (monto, categoría, descripción).
* [ ] Implementar un teclado numérico personalizado (tipo cajero) para que se sienta iOS.
* [ ] Guardar los datos en un Store o LocalStorage.
* [ ] Añadir la vibración que ya configuramos al confirmar el gasto.

#### 2. El Historial de Movimientos (Prioridad Alta 🟠)
Necesitas ver lo que acabas de anotar para sentir que la app "funciona".
* [ ] Crear una lista scrollable de transacciones.
* [ ] Agrupar gastos por fecha (Hoy, Ayer, esta semana).
* [ ] Implementar el "Swipe to delete" (deslizar para borrar), muy típico de iPhone.
* [ ] Diseño de las filas con iconos por categoría.

#### 3. El Dashboard / Inicio (Prioridad Media 🟡)
Aquí es donde la app se pone "bonita" y útil de un vistazo.
* [ ] Crear la tarjeta de "Balance Total".
* [ ] Gráfico simple (quizás de donuts o barras) de gastos por categoría.
* [ ] Resumen de gastos del mes actual vs mes anterior.

#### 4. Exportación y Limpieza (Prioridad Baja 🟢)
Lo que mencionabas antes. Se hace al final porque depende de tener muchos datos para probar.
* [ ] Generar el archivo CSV a partir de lo guardado en LocalStorage.
* [ ] Función de "Borrar todo" (con el modal de confirmación que ya tienes).
* [ ] Pantalla de bienvenida (Onboarding) para cuando alguien abre la app por primera vez.

---

### ¿Por dónde empezar hoy?

Si ya tienes el **PinLock** y los **Ajustes** medio listos, yo iría directo a por el **Formulario para crear transacción**. 

Es la parte más divertida de diseñar porque puedes jugar con:
1.  **Selector de categorías** con iconos sutiles.
2.  **Input gigante** para el dinero (que se sienta importante).
3.  **Transiciones**: Que el formulario salga desde abajo (tipo *Sheet* de iOS).

**¿Quieres que empecemos a montar el formulario de entrada de gastos con ese estilo Glassmorphism?** O si prefieres, podemos atacar el Historial para ver cómo se listan los datos. ¡Tú diriges!