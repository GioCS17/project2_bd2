
# Division del proyecto 

Dentro de la implementacion hemos decidido dividir procesamiento en el servidor en 4 archivos python cuales son los siguientes:

## InvertedIndexDisk


## Params


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
