<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentación - Sistema de Gestión de Turnos</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body class="bg-light py-5">

<div class="container bg-white p-5 rounded shadow-sm" style="max-width: 900px;">
    
  <header class="border-bottom pb-3 mb-4">
      <h1 class="fw-bold text-dark">
          <i class="fa-solid fa-book-bookmark text-primary me-2"></i>Documentación del Sistema
      </h1>
      <p class="text-muted mb-0">Sistema de Optimización y Organización de Turnos — Bienestar Universitario</p>
  </header>

  <section class="mb-4">
      <h3 class="h4 fw-bold text-secondary"><i class="fa-solid fa-bullseye me-2"></i>Propósito</h3>
      <p>
          Este proyecto propone un sistema eficiente para la organización de turnos y préstamos en Bienestar Universitario de la Universidad Católica de Colombia. Su objetivo principal es vincular de forma estricta y relacional a los <strong>estudiantes</strong> con los <strong>implementos disponibles</strong> (deportivos o culturales), asegurando un control de stock en tiempo real y evitando conflictos de asignación.
      </p>
  </section>

  <section class="mb-4">
      <h3 class="h4 fw-bold text-secondary"><i class="fa-solid fa-layer-group me-2"></i>Stack Tecnológico</h3>
      <ul>
          <li><strong>Backend:</strong> FastAPI (Python) con programación asíncrona y SQLModel.</li>
          <li><strong>Base de Datos:</strong> PostgreSQL en la nube (Neon / Supabase).</li>
          <li><strong>Frontend:</strong> Plantillas HTML dinámicas con el motor Jinja2 y Bootstrap 5.</li>
      </ul>
  </section>

  <section class="mb-4">
        <h3 class="h4 fw-bold text-secondary"><i class="fa-solid fa-route me-2"></i>Mapa de Endpoints</h3>
        <p class="text-muted small">Listado completo de rutas semánticas construidas en el backend agrupadas por módulo:</p>
      <div class="table-responsive">
          <table class="table table-bordered table-striped align-middle">
              <thead class="table-dark">
                  <tr>
                      <th style="width: 15%;">Método</th>
                      <th style="width: 35%;">Ruta</th>
                      <th style="width: 50%;">Acción de Negocio</th>
                  </tr>
              </thead>
              <tbody>
                  <tr class="table-secondary fw-bold"><td colspan="3"><i class="fa-solid fa-house me-2"></i>Módulo Principal</td></tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>  
                      <td><code>/</code></td>  
                      <td>Dashboard principal con el carrusel de accesos rápidos e interactivos.</td>
                  </tr>
                  <tr class="table-secondary fw-bold"><td colspan="3"><i class="fa-solid fa-receipt me-2"></i>Módulo de Gestión de Turnos (Préstamos)</td></tr>  
                  <tr>      
                      <td><span class="badge bg-success w-100">GET</span></td>  
                      <td><code>/turnos</code></td>  
                      <td>Panel de visualización de todos los turnos registrados (Activos / Finalizados).</td>
                  </tr>
                  <tr>      
                      <td><span class="badge bg-success w-100">GET</span></td>  
                      <td><code>/turno/{id}</code></td>  
                      <td>Vista extendida de un turno con enlaces interactivos a los perfiles de recursos.</td>
                  </tr>  
                  <tr>      
                      <td><span class="badge bg-success w-100">GET</span></td>  
                      <td><code>/turno/nuevo</code></td>  
                      <td>Renderiza el formulario HTML para la asignación de un nuevo préstamo.</td>
                  </tr>  
                  <tr>
                      <td><span class="badge bg-primary w-100">POST</span></td>
                      <td><code>/turno/nuevo</code></td>
                      <td>Procesa y valida las reglas de negocio para abrir un nuevo turno en la BD Cloud.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/turno/editar/{id}</code></td>
                      <td>Carga el formulario de modificación con los datos persistidos del turno.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-warning text-dark w-100">PATCH</span></td>
                      <td><code>/turno/{id}</code></td>
                      <td>Actualiza de forma parcial la información o parámetros del turno seleccionado.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-danger w-100">DELETE</span></td>
                      <td><code>/turno/{id}</code></td>
                      <td>Baja lógica: Finaliza el préstamo y libera inmediatamente el implemento deportivo.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-warning text-dark w-100">PATCH</span></td>
                      <td><code>/turno/rehabilitar/{id}</code></td>
                      <td>Revierte la finalización de un préstamo para regresarlo a estado activo bajo control de stock.</td>
                  </tr>
                  <tr class="table-secondary fw-bold"><td colspan="3"><i class="fa-solid fa-user-graduate me-2"></i>Módulo de Estudiantes</td></tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/estudiantes</code></td>
                      <td>Listado general del censo de estudiantes registrados en Bienestar Universitario.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/estudiante/{id}</code></td>
                      <td>Capturador por ID: Muestra el perfil del alumno y su historial transaccional de uso.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/estudiante/nuevo</code></td>
                      <td>Renderiza el formulario de alta para nuevos usuarios académicos.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-primary w-100">POST</span></td>
                      <td><code>/estudiante/nuevo</code></td>
                      <td>Inserta un nuevo registro de estudiante validando su código único institucional.</td>
                  </tr>
                  <tr class="table-secondary fw-bold"><td colspan="3"><i class="fa-solid fa-futbol me-2"></i>Módulo de Inventario de Implementos</td></tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/implementos</code></td>
                      <td>Grilla general del inventario físico disponible en los almacenes deportivos y culturales.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/implemento/{id}</code></td>
                      <td>Capturador por ID: Muestra las especificaciones técnicas del recurso y su estado actual.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-success w-100">GET</span></td>
                      <td><code>/implemento/nuevo</code></td>
                      <td>Renderiza el formulario de inserción para nuevas adquisiciones de material.</td>
                  </tr>
                  <tr>
                      <td><span class="badge bg-primary w-100">POST</span></td>
                      <td><code>/implemento/nuevo</code></td>
                      <td>Registra el nuevo implemento en el inventario cloud asignando su categoría base.</td>
                  </tr>
              </tbody>
          </table>
      </div>
  </section>

  <section class="mb-4">
      <h3 class="h4 fw-bold text-secondary"><i class="fa-solid fa-scale-balanced me-2"></i>Reglas de Negocio</h3>
      <ol>
          <li><strong>Disponibilidad de implemento:</strong> Un recurso deportivo que se encuentra en un turno activo no puede ser asignado a otro estudiante hasta que el préstamo vigente sea finalizado.</li>
          <li><strong>Integridad de datos:</strong> No se permite la creación de turnos si los identificadores del estudiante o del implemento no existen previamente en la base de datos cloud.</li>
          <li><strong>Persistencia transaccional:</strong> El cierre de turnos mediante <code>DELETE</code> realiza una baja lógica para no perder el histórico de estadísticas del módulo.</li>
      </ol>
  </section>

  <section class="mb-0">
      <h3 class="h4 fw-bold text-secondary"><i class="fa-solid fa-terminal me-2"></i>Despliegue Local</h3>
      <p class="mb-2">Comandos secuenciales para arrancar el entorno de desarrollo:</p>
      <pre class="bg-dark text-white p-3 rounded text-start"><code># 1. Clonar el repositorio
git clone https://github.com/Simon-Acosta-1580

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/scripts/activate

# 3. Instalar dependencias
pip install fastapi uvicorn sqlmodel psycopg2-binary jinja2

# 4. Iniciar el servidor
uvicorn main:app --reload</code></pre>
        <p class="small text-muted mt-2">El sistema quedará disponible en: <code>http://127.0.0.1:8000</code></p>
    </section>

</div>

</body>
</html>
