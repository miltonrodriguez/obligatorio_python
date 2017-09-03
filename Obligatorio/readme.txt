-------------
|Integrantes|
-------------
Patricia Aldaz     CI 3.813.973-6    paldaz@mail.antel.com.uy
Milton Rodriguez   CI 4.292.854-9    mhrodriguez@antel.com.uy

---------------------------------------
A continuacion se enumeran las URL de las funcionalidaes y una pequeña explicacion de las decisione de desarrolo que se tomaron en cada una de ellas.

Ingreso al sistema:
http://127.0.0.1:8000/biblio/

Requerimientos
Deben contemplarse las siguientes funcionalidades:
1. Información general del sistema, con menú de links que lleve hacia las restantes
funcionalidades.
	-http://127.0.0.1:8000/biblio/
2. Préstamo: Dado un número de socio y un número de ISBN realiza un préstamo. Toma cualquier
inventario asociado al ISBN. Falla si no hay copias disponibles o si el socio es moroso.
	-http://127.0.0.1:8000/biblio/prestamo/
	-Al prestar, no se coloca la fecha de fin del prestamo, solo se coloca la fecha inicio.
3. Devolución: Dado un número de socio y un número de inventario específico, realiza la
devolución (si está fuera de fecha, el socio pasa a ser moroso, ese estado solo podrá ser
levantado vía admin).
	-http://127.0.0.1:8000/biblio/devolucion/
	-Al devolver, se calcula la fecha de devolucion como fecha_inicio + 7 dias. Si le dia de hoy es mayor que el dia de devolucion calculado, se coloca al socio como moroso.
4. Dado un número de socio obtener su información (datos personales y libros prestados hasta la
fecha).
	-Se hizo en 2 partes:
		1- http://127.0.0.1:8000/biblio/list_socios - tabla de socios con links
		2- http://127.0.0.1:8000/biblio/socio/{documento}- informacion del socio
5. Dado un número de inventario obtener la información del libro y mostrar su estado. Si está
prestado cdebe desplegarse la info del socio
	-Se hizo en 2 partes:
		1- http://127.0.0.1:8000/biblio/list_copias - tabla de copias con links y filtro
		2-http://127.0.0.1:8000/biblio/copia/{inventario} - informacion de la copia
6. Dado un ISBN obtener la información del libro y mostrar las copias que tiene y su estado (si
están disponibles o prestadas).
	-Se hizo en 2 partes:
		1- http://127.0.0.1:8000/biblio/list_libros -  tabla de libros con links y filtro
		2- http://127.0.0.1:8000/biblio/libro/{ISBN} - informacion del libro
7. Lista de socios clasificados como morosos
	-http://127.0.0.1:8000/biblio/morosos lista de morosos con link al socio moroso
8. Lista de préstamos realizados en una fecha dada indicando qué socio tiene la copia e incluyendo
fecha de devolución pautada.
	-Se hizo en 2 partes:
		1- http://127.0.0.1:8000/biblio/prestamo_fecha/ - campo fecha para seleccionar la fecha a buscar
		2- http://127.0.0.1:8000/biblio/prestamo_fecha/?fecha={yyyy-mm-dd} - listado de prestamos en una fecha
		La url no coincide exactamente con lo pautado en la letra.
9. Lista de socios “futuros morosos”: Se trata de aquellos socios que no han realizado la
devolución (en la fecha actual), pero que debían hacerlo.
	-http://127.0.0.1:8000/biblio/futuros_morosos
	Para esta funcionalidad se hace el mismo calculo que en la devolucion.
	Se calcula la fecha de devolucion como fecha_inicio + 7 dias. 
	Si el dia de hoy es mayor que el dia de devolucion calculado, se coloca al socio en la lista de futuros morosos.
	