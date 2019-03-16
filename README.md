PROYECTO PERSONAL DE ORDENES DE TRABAJO Y VENTANAS DE MANTENIMIENTO
===================================================================

El objetivo de esta aplicación es practicar mis conocimientos de Python y Django mediante la solución que resuelve la necesidad de administrar un portal de seguimiento de órdenes de trabajo y ventanas de mantenimiento de una empresa de TIC/Telecomunicaiones.

Para poder hacer uso de ella, es requerido lo siguiente.

## Instrucciones de instalación ##

1) Crear un entorno virtual (se debe tener previamente intalado env y pip)

> python3 -m venv ENTORNO

2) Activar el entorno

> source ENTORNO/bin/activate

3) Descargar este repositorio y acceder a este

4) Instalar Django contenido en el repositorio

> pip install -r requirements.txt

5) Crear un archivo db.sqlite3

> touch db.sqlite3

6) Migrar la base de datos

> python manage.py makemigrations

> python manage.py migrate

7) Crear un superusuario. OJO: El superusuario y los usuarios operarios deben tener la sintaxis de email en Office 365 para que funcione

> python manage.py createsuperuser

8) Arrancar el servidor

> python manage.py runserver

## Preparación de la aplicación ##

1) Acceder a http://127.0.0.1:8000/only_it_admin

2) Cargar la información necesaria para el uso de la aplicación en los siguientes catálogos

  - `Usuarios` Se debe cargar usuario, nombre, apellido e email de los usuarios. OJO: El usuario debe ser cargado con formato de email existente en la nube de Office 365. A su vez, en el campo de "Permisos de usuario" se debe seleccionar los siguientes dos privilegios si son necesarios.
      - Permiso `ordenes | orden | Can add orden`: El usuario con este privilegio puede crear órdenes y ventanas.
      - Permiso `ordenes | orden | Can change orden`: El usuario con este privilegio puede cambiar el estatus de una orden y ventanas.
      - Permiso `staff`: Solo ellos pueden entrar a módulo de administración de catálogos.
 - `Agente correo` Se debe cargar un mail y password de Office 365 del cual se enviarán todos las notificaciones
 - `Gerencias` Áreas funcionales de la empresa donde se ejecutan las actividades
 - `Supervisores` Responsables de las actividades. Estas pertenecen a una gerencia
 - `Localidades` Sitios de acción de las actividades
 - `Proveedores` Empresas dedicadas a ejecutar las actividades
 - `Ejecutores` Empleados de los proveedores que ejecutarán la actividad
 - `Servicios` Aquellos que ofrece la empresa de telecomunicaciones que pudieran ser afectados en las actividades

## Uso de la aplicacion ##

1) Acceder a http://127.0.0.1:8000

2) Ingresa un usuario y password creado en el catálogo de `Usuarios`

3) Realizar cualquiera de las siguientes 3 actividades

 3.1) `Alta de actividades` Si el usuario tiene privilegios de `Can add orden`, puede dar click al botón de  `Crear nueva orden`. Este te llevará a una ventana donde llenarás lo siguiente
  - `Información básica`
    - `Tipo de órden` - Puede ser órden de trabajo o ventana de mantenimiento
    - `Gerencia` - Gerencia activa responsable de la actividad
    - `Supervisión` - Supervisores activos dentro de la gerencia seleccionada responsable de la actividad
    - `Teléfono de contacto` - Ya sea que se deje el teléfono en el catálogo del supervisor seleccionado o se capture otro.
    - `Asunto de la actividad` - Redacción breve de la actividad
    - `Detalle de la actividad` - Redacción a profundidad de la actividad
  - `Programación`
    - `Localidades` - Se selecciona las localidades donde se trabajarán
    - `Periodo de la actividad` - Se especifica fecha y hora de inicio y fin de la actividad
    - `Periodo de afectación` (Solo en ventana de mantenimiento) - Se especifica fecha y hora de inicio y fin de una posible afectación de servicios en la actividad
  - `Proveedor`
    - `Proveedor` - Se selecciona a un proveedor activo que realice la actividad
    - `Responsables del lado de proveedor` - Se seleccionan a los ejecutores de la actividad contratados por el proveedor
  - `Listado de actividades`
    - `MOP` - Archivo adjunto de los detalles de la actividad
  - `Afectación` (Solo en ventana de mantenimiento)
    - `Servicios afectados` - Se seleccionan los servicios activos afectados por la actividad
    - `Clientes afectados` -  Se redactan los clientes afectados por la actividad
  - `Comentarios adicionales`
    - `Comentarios adicionales` - Se escriben comentarios varios a tomar en cuenta

Al final, se genera un ID de la órden con formato OT/[PROVEEDOR]/[LOCALIDAD]/[FECHA ACTIVIDAD]/[CONSECUTIVO] para órdenes de trabajo ó VM/[PROVEEDOR]/[LOCALIDAD]/[FECHA ACTIVIDAD]/[CONSECUTIVO] para ventanas de mantenimiento

 3.2) `Listado de órdenes` Se podrá apreciar el listado de órdenes y ventanas desplejando el ID, localidad, asunto, responsable y estatus. Los estatus pueden ser "En revisión", "Aceptada", "Rechaada", "En ejecución", "Finalizada".

 3.3) `Consulta y actualización de estatus de actividad` Al dar click en el botón de una actividad del estatus de la misma, lo llevará a otra pantalla con el detalle de la órden creada. Si el usuario tiene privilegios de `Can change orden`, se puede desplazar hasta abajo para cambiar el estatus de la órden, así como poner comentarios del cambio de estatus.

Los estatus varían dependiendo del estatus actual.

 - `En revisión` -> Puede elegir entre `Aceptado` o `Rechazado`
 - `Aceptado` -> Puede cambiar a `En ejecución`
 - `En ejecución` -> Puede cambiar a `Finalizado`

## Requerimientos no funcionales implementados ##

 - Cierre de sesión a los 10 minutos
 - Envío de correo electrónico de plataforma Office 365 a usuarios al crear y tener cambio de estatus de sus órdenes
