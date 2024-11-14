from . import db

# Definir la tabla de asociación para géneros y contenidos
generos_contenidos = db.Table('GenerosContenidos',
    db.Column('idContenido', db.Integer, db.ForeignKey('Contenidos.id'), primary_key=True),
    db.Column('idGenero', db.Integer, db.ForeignKey('Generos.id'), primary_key=True)
)

# Definir la tabla de asociación para personajes y contenidos
personajes_contenidos = db.Table('PersonajesContenidos',
    db.Column('personaje_id', db.Integer, db.ForeignKey('Personajes.id'), primary_key=True),
    db.Column('contenido_id', db.Integer, db.ForeignKey('Contenidos.id'), primary_key=True),
    db.Column('rol', db.String, nullable=False)
)

class Contenido(db.Model):
    __tablename__ = 'Contenidos'
    id = db.Column(db.Integer, primary_key=True)
    duracion = db.Column(db.Integer)
    sinopsis = db.Column(db.String)
    lanzamiento = db.Column('anio', db.Integer)
    tipo = db.Column(db.String, nullable=False)  # 'pelicula' o 'episodio'
    titulo = db.Column(db.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'contenido'
    }
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'duracion': self.duracion,
            'sinopsis': self.sinopsis,
            'lanzamiento': self.lanzamiento,
            'tipo': self.tipo,
        }

class Episodio(Contenido):
    __tablename__ = 'Episodios'
    id = db.Column(db.Integer, db.ForeignKey('Contenidos.id'), primary_key=True)
    idTemporada = db.Column(db.Integer, db.ForeignKey('Temporadas.id'), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'episodio',
    }
    generos = db.relationship('Genero', secondary=generos_contenidos, backref='episodios', lazy=True)
    cast = db.relationship('Personaje', secondary=personajes_contenidos, backref='episodios', lazy=True)
    def to_dict_full(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'duracion': self.duracion,
            'sinopsis': self.sinopsis,
            'lanzamiento': self.lanzamiento,
            'tipo': self.tipo,
            'idTemporada': self.idTemporada,
        }


class Pelicula(Contenido):
    __mapper_args__ = {
        'polymorphic_identity': 'pelicula',
    }
    generos = db.relationship('Genero', secondary=generos_contenidos, backref='peliculas', lazy=True)
    cast = db.relationship('Personaje', secondary=personajes_contenidos, backref='peliculas', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'duracion': self.duracion,
            'sinopsis': self.sinopsis,
            'lanzamiento': self.lanzamiento,
            'tipo': self.tipo,
            'generos': [genero.nombre for genero in self.generos],
            'cast': [personaje.to_dict() for personaje in self.cast]
        }

class Serie(db.Model):
    __tablename__ = 'Series'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    sinopsis = db.Column(db.String)
    lanzamiento = db.Column('anio', db.Integer)
    temporadas = db.relationship('Temporada', backref='serie', lazy=True)
    @property
    def generos(self):
        primer_episodio = db.session.query(Episodio).join(Temporada).filter(Temporada.serie_id == self.id).order_by(Episodio.id).first()
        if primer_episodio:
            return primer_episodio.generos
        return []
    @property
    def cast(self):
        primer_episodio = db.session.query(Episodio).join(Temporada).filter(Temporada.serie_id == self.id).order_by(Episodio.id).first()
        if primer_episodio:
            return primer_episodio.cast
        return []
    @property
    def num_temporadas(self):
        return len(self.temporadas)
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'sinopsis': self.sinopsis,
            'lanzamiento': self.lanzamiento,
            'generos': [genero.nombre for genero in self.generos],
            'cast': [personaje.to_dict() for personaje in self.cast],
            'temporadas': [temporada.to_dict() for temporada in self.temporadas],
            'num_temporadas': self.num_temporadas
        }

class Temporada(db.Model):
    __tablename__ = 'Temporadas'
    id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('Series.id'), nullable=False)
    nombre = db.Column(db.String)
    lanzamiento = db.Column('anio', db.Integer)
    episodios = db.relationship('Episodio', backref='temporada', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'lanzamiento': self.lanzamiento,
            'episodios': [episodio.to_dict() for episodio in self.episodios]
        }
    def to_dict_full(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'lanzamiento': self.lanzamiento,
            'episodios': [episodio.to_dict() for episodio in self.episodios],
            'idSerie': self.serie_id
        }

class Genero(db.Model):
    __tablename__ = 'Generos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)

class Persona(db.Model):
    __tablename__ = 'Personas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellidos = db.Column(db.String)
    edad = db.Column(db.Integer)
    foto = db.Column(db.String)

    # Relación inversa con los personajes
    personajes = db.relationship('Personaje', back_populates='persona', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'foto': self.foto,
            'personajes': [personaje.to_dict_half() for personaje in self.personajes]
        }
    def to_dict_half(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'foto': self.foto,
        }

class Personaje(db.Model):
    __tablename__ = 'Personajes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('Personas.id'), nullable=False)
    # Relación con la persona asociada
    persona = db.relationship('Persona', back_populates='personajes', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'actor': self.persona.to_dict_half()
        }
    def to_dict_half(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
        }