-En la carpeta donde sera su proyecto es necesario crear un "entorno virtual"
----->pueden usar:
python -m venv venv
(o el nombre que ustedes quieren)
------>o:
python3 -m venv venv
(o el nombre que ustedes quieren)

-luego es necesario "activar el entorno virtual"
----->pueden usar:
source venv/Scripts/activate
(o el nombre que ustedes pusieron al crear el venv)
-para saber si si fue activado en su consola del bash veran : (venv) o el nombre que le pusieron al crearlo.

-es necesario instalar las dependencias (el venv debe estar activo) en este caso :
pip install fastapi uvicorn sqlalchemy psycopg2-binary

    -fastapi :  es la del framework
    -uvicorn :  es como el nodemon un watcher
    -sqlalchemy:    la orm
    -psycopg2-binary: tamien ayuda con el manejo de postgresql

-para poder activar el watcher se necesita tener un archivo "main" o de cualquier nombre y haber declarado una variable "app"(o otro nombre), y usar este comando:
uvicorn main:app --reload

notas: cada que se vuelva usar el programa es necesario activar el venv si no saldran errores de que no se reconocen las dependencias.
