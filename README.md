# Parcial 2 - Django Backend

**Curso:** Desarrollo de Aplicaciones Web I -- 4E  
**Docente:** Jose Javier Torres Vanstrahlen  
**Estudiante:** Luis M.  

Backend en Django nativo con modelos relacionales (`Proyecto` y `Tarea`) registrados en el administrador de Django y persistidos en SQLite.

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.14**
- **Django 6.1**
- **SQLite 3**

---

## 📁 Estructura de Modelos

### 1. `Proyecto`
- `nombre`: `CharField(max_length=100)`
- `descripcion`: `TextField()`
- `fecha_inicio`: `DateField()`
- Método `__str__` retornando `nombre`.

### 2. `Tarea`
- `titulo`: `CharField(max_length=100)`
- `completada`: `BooleanField(default=False)`
- `proyecto`: `ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')`
- Método `__str__` retornando `titulo`.

---

## 🚀 Instrucciones de Ejecución

1. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # En Windows
   ```

2. Instalar Django:
   ```bash
   pip install django
   ```

3. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

4. Iniciar servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

5. Acceder al panel de administración:
   - **URL:** `http://127.0.0.1:8000/admin/`
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`
