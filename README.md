# Pre-requisitos:
- **Pip**
	 - sudo apt install python3-pip
	 - pip3 --version
- **Entorno virtual**
	 - pip3 install virtualenv
	 - which virtualenv
	 - virtualenv -p #name_file_virtual
	 - source #name_file_virtual/bin/activate
- **Flask**
	- pip install Flask
- **Cython**
	- pip install Cython
- **Stemmer**
	- pip install PyStemmer

- **Tweepy**
	- pip install tweepy

# Division del proyecto 

## Frontend

Para la implementación en frontend hacemos uso de las librerias **bulma css** para manejar el aspectos de las vistas de forma muy flexible y ligera, y **Vuejs** para el manejo de eventos y acciones desde las vista. Vuejs permite la comunicacion de las vistas con tu archivo o código javascript de forma muy fácil. Para la comunicación con el backend nos apoyamos de la libreria **axios**. Solo contamos con un archivo *index.html* para la carga de archivos json por el usuario y para la consulta previa de los tweets bajo un ingreso de alguna query en lenguaje natural. Al final del documento probar apreciar algunas imagenes que muestra como se encuentra index.html.  

## Backend

Dentro de la implementación en backend hemos decidido dividir el procesamiento en el servidor en 4 archivos python cuales son los siguientes:

## InvertedIndexDisk

En este archivo guardamos las funciones para generar un Inverted Index en disco.

- **Document**: la clase document almacena un identificador y el texto en minúscula contenido en dicho documento, para cada tweet se usará su id y su respectivo texto.
- **InvertedIndex**: En esta clase tenemos las funciones para procesar los tweets y generar un archivo con los datos del índice invertido, las funciones son:
	- **Process**: Recibe una lista de objetos Document y recorre cada palabra del texto de cada documento. Guarda las palabras diferentes en un archivo *words.txt*, donde a cada palabra se le asigna un identificador, mientras que en un archivo *initial.txt* guarda un conjunto <IdWord, IdDoc, Freq>, que corresponde al identificador de la palabra, el identificador del documento o tweet y su frequencia.
	- **SortRuns**: Recibe como parámetro un entero *k*, esta función separa el archivo creado durante *Process* en diferentes archivos ordenados con *k* datos cada uno. 
	- **Merging**: Mergea los archivos *sortruns* generados anteriormente para crear un archivo final con el índice invertido ordenado.
- **CreateTwitter**: Recibe como parámetro la data mandada desde el navegador con los archivos json para crear el índice invertido, recorre cada archivo para crear un índice invertido con los tweets usando las funciones de la clase InvertedIndex.
- **GenerateIndex**: Con esta función cargamos el índice invertido a memoria principal y lo almacenamos en un diccionario, además también recibimos el número de tweets.

## Params
En este archivo cargamos los parámetros para poder trabajar con el app de Twitter. Es necesario contar con una cuenta de tweeter y copiar el token que te suministra el aplicativo para poder usar el api.

## Preprocess
Este archivo nos permitira hacer la limpieza y preparacion del contenido en el atributo text en cada tweeter. Para ello, se hace uso de 5 variables globales y 5 funciones.

Las 5 variables globales son las siguientes:
- **inverted_index**: para mantener el indice invertido que se genera al cargar los archivos tweeters.
- **stop_file**: define la ruta del archivo desde donde carga los stopwords.
- **aditional_characters**: variable string auxiliar que nos permite trabajar con comodidad en el filtro de characteres especiales.
- **stemmer**: instancia que se genera de la libreria Stemmer para poder lematizar las palabras del atributo text en tweeters.
- **stopwords**: arreglo que almacena todas las palabras que son stopwords y se encuentran almacenadas en el archivo definido en la ruta *stop_file*.

Las 5 funciones funciones que cuenta son las siguientes:
### load_step_words
Este función permite hacer la carga de stopwords desde el archivo con ruta definida en *stop_file*. Los stopwords son almacenados en memoria local mediante un array.

### clean_word
Este función permite limpiar cada palabra que se le envie, devolviendo una palabra sin caracteres especiales ni espacios en los extremos. Su uso es principalmente para el proceso de tokenizar las palabras.

### tokenize
Este función permite generar un array de palabras del atributo text para cada tweeters. Devuelve un array de palabras limpias y para ello hace uso del metodo clean_word. Su proceso se da mediante un for recorriendo cada palabra del atributo text y a medida que se recorre se envia la palabra a clean_word para limpieza, luego se verifica la longitud y si no pertenece a un stopword. Si su longitud es mayor a 0 y no esta dentro del arreglo stopwords se inserta al arreglo que luego retornara al finalizar el for. 

### stemming
Este función permite generar las raíces de los tokens generados por la función *tokenize*. Se sabe que las raíces entre algunas palabras son las mismas y es con las raíces que al final trabajaremos para generar el índice. Para generar la raíces se apoya de la librería Stemmer mediante la funcion **stemWords**. Además es necesario previamente al crear la instancia de Stemmer, definir que idioma se usara, en nuestro caso *spanish*.


## Server
En server.py creamos nuestro servidor web para hacer las operaciones con nuestro Inverted Index, usamos la librería Flask para poder correr el servidor.

- **Search_tweets** *(Ruta: /tweets/< text>)*:
Usamos esta ruta para hacer las consultas de búsqueda. Cargamos el índice invertido y el archivo de palabras desde disco, buscamos el identificador de cada tweet y lo almacenamos en un array junto a su score. Finalmente para cada identificador hacemos una consulta con app de Twitter para obtener datos del usuario y del Tweet.

- **Index** *(Ruta: /)*:
En esta ruta cargamos nuestro front end para la visualización.

- **GetRamsin** *(Ruta: /upload)*:
Usamos esta ruta para cargar los archivos mandados desde el navegador y generar el índice invertido en disco.

## Pruebas

Nuestra vista se separa en dos partes, una para cargar los archivos y generar el índice invertido y otra para hacer las consultas.

![Imagen1](/img/imagen1.PNG)

Al realizar una búsqueda aparecerán los datos del tweet y del usuario, los tweets estarán ordenados de acuerdo a su score tf.idf.

![Imagen2](/img/imagen2.jpg)
