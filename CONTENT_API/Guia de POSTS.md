
---

## **Endpoints para Series**

### **Crear Serie**
**POST** `/series`

Crea una nueva serie junto con su primera temporada y primer episodio.

- **Body JSON:**
  ```json
  {
      "titulo": "string",
      "sinopsis": "string",
      "lanzamiento": "YYYY",
      "duracion": 120,
      "generos": [1, 2],
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "titulo": "string",
      "sinopsis": "string",
      "lanzamiento": "YYYY"
  }
  ```

---

### **Actualizar Serie**
**PUT** `/series/<int:id>`

Actualiza la información de una serie y sus géneros o elenco.

- **Body JSON:**
  ```json
  {
      "titulo": "string",
      "sinopsis": "string",
      "lanzamiento": "YYYY",
      "generos": [1, 2],
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "titulo": "string",
      "sinopsis": "string",
      "lanzamiento": "YYYY"
  }
  ```

---

### **Agregar Géneros a Serie**
**POST** `/series/<int:serie_id>/generos`

Asocia géneros al primer episodio de una serie existente.

- **Body JSON:**
  ```json
  {
      "generos": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Géneros agregados exitosamente"}
  ```

---

### **Agregar Cast a Serie**
**POST** `/series/<int:serie_id>/cast`

Asocia personajes al primer episodio de una serie existente.

- **Body JSON:**
  ```json
  {
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Cast agregado exitosamente"}
  ```

---

### **Actualizar Géneros de Serie**
**PUT** `/series/<int:serie_id>/generos`

Actualiza los géneros del primer episodio de una serie.

- **Body JSON:**
  ```json
  {
      "generos": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Géneros actualizados exitosamente"}
  ```

---

### **Actualizar Cast de Serie**
**PUT** `/series/<int:serie_id>/cast`

Actualiza el elenco del primer episodio de una serie.

- **Body JSON:**
  ```json
  {
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Cast actualizado exitosamente"}
  ```

---

## **Endpoints para Películas**

### **Crear Película**
**POST** `/peliculas`

Crea una nueva película y asocia géneros o personajes opcionales.

- **Body JSON:**
  ```json
  {
      "titulo": "string",
      "duracion": 120,
      "sinopsis": "string",
      "lanzamiento": "YYYY",
      "generos": [1, 2],
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "titulo": "string",
      "duracion": 120,
      "sinopsis": "string",
      "lanzamiento": "YYYY"
  }
  ```

---

### **Actualizar Película**
**PUT** `/peliculas/<int:id>`

Actualiza la información, géneros o elenco de una película.

- **Body JSON:**
  ```json
  {
      "titulo": "string",
      "duracion": 120,
      "sinopsis": "string",
      "lanzamiento": "YYYY",
      "generos": [1, 2],
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "titulo": "string",
      "duracion": 120,
      "sinopsis": "string",
      "lanzamiento": "YYYY"
  }
  ```

---

### **Agregar Géneros a Película**
**POST** `/peliculas/<int:pelicula_id>/generos`

Asocia géneros a una película existente.

- **Body JSON:**
  ```json
  {
      "generos": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Géneros agregados exitosamente"}
  ```

---

### **Agregar Cast a Película**
**POST** `/peliculas/<int:pelicula_id>/cast`

Asocia personajes a una película existente.

- **Body JSON:**
  ```json
  {
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Cast agregado exitosamente"}
  ```

---

### **Actualizar Géneros de Película**
**PUT** `/peliculas/<int:pelicula_id>/generos`

Actualiza los géneros de una película.

- **Body JSON:**
  ```json
  {
      "generos": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Géneros actualizados exitosamente"}
  ```

---

### **Actualizar Cast de Película**
**PUT** `/peliculas/<int:pelicula_id>/cast`

Actualiza el elenco de una película.

- **Body JSON:**
  ```json
  {
      "cast": [1, 2]
  }
  ```
- **Response:**
  ```json
  {"message": "Cast actualizado exitosamente"}
  ```

---

## **Endpoints para Personajes**

### **Crear Persona**
**POST** `/personas`

Crea una persona (actor).

- **Body JSON:**
  ```json
  {
      "nombre": "string",
      "apellidos": "string",
      "edad": 30,
      "foto": "url"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "nombre": "string",
      "apellidos": "string",
      "edad": 30,
      "foto": "url"
  }
  ```

---

### **Actualizar Persona**
**PUT** `/personas/<int:id>`

Actualiza una persona.

- **Body JSON:**
  ```json
  {
      "nombre": "string",
      "apellidos": "string",
      "edad": 30,
      "foto": "url"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "nombre": "string",
      "apellidos": "string",
      "edad": 30,
      "foto": "url"
  }
  ```

---

### **Crear Personaje**
**POST** `/personajes`

Crea un personaje.

- **Body JSON:**
  ```json
  {
      "nombre": "string",
      "actor_id": 1
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "nombre": "string",
      "actor_id": 1
  }
  ```

---

### **Actualizar Personaje**
**PUT** `/personajes/<int:id>`

Actualiza un personaje.

- **Body JSON:**
  ```json
  {
      "nombre": "string",
      "actor_id": 1
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "nombre": "string",
      "actor_id": 1
  }
  ```

---

## **Endpoints para Géneros**

### **Crear Género**
**POST** `/generos`

Crea un nuevo género, verificando duplicados.

- **Body JSON:**
  ```json
  {
      "nombre": "string"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "nombre": "string"
  }
  ```

---

### **Actualizar Género**
**PUT** `/generos/<int:id>`

Actualiza un género, verificando duplicados.

- **Body JSON:**
  ```json
  {
      "nombre": "string"
  }
  ```
- **Response:**
  ```json
  {
      "id": 1,
      "nombre": "string"
  }
  ```

