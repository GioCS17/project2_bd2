

# Division del proyecto 

Dentro de la implementacion hemos decidido dividir procesamiento en el servidor en 4 archivos python cuales son los siguientes:

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
En este archivo cargamos los parámetros para poder trabajar con el app de Twitter.

## Preprocess
Este archivo cuenta con 5 variables globales:
- inverted_index: para mantener el indice invertido que se genera al cargar los archivos tweeters.
- stop_file: define la ruta del archivo desde donde carga los stopwords.
- aditional_characters: variable string auxiliar que nos permite trabajar con comodidad en el filtro de characteres especiales.
- stemmer: instancia que se genera de la libreria Stemmer para poder lematizar las palabras del atributo text en tweeters.
- stopwords: arreglo que almacena todas las palabras que son stopwords y se encuentran almacenadas en el archivo definido en la ruta stop_file.

Tambien se define 5 funciones:
### load_step_words
Este metodo permite hacer la carga de stopwords desde el archivo con ruta definida en stop_file. Los stopwords son almacenados en memoria local mediante un array.

### clean_word
Este metodo permite limpiar cada palabra que se le envie, devolviendo una palabra sin caracteres especiales ni espacios en los extremos. Su uso esprimariamente para el proceso de tokenizar las palabras.

### tokenize
Este metodo permite generar un array de palabras del atributo text para cada tweeters. Devuelve un array de palabras limpias y para ello hace uso del metodo clean_word. Su proceso se da mediante un for recorriendo cada palabra del atributo text y a medida que se recorre se envia la palabra a clean_word para limpieza, luego se verifica la longitud y si no pertenece a un stopword. Si su longitud es mayor a 0 y no esta dentro del arreglo stopwords se inserta al arreglo que luego retornara al finalizar el for. 

### stemming


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
