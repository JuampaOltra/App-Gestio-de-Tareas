from flask import Flask, render_template, request, redirect, url_for, flash
import db
from models import Tarea
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hola'

@app.route("/")
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    return render_template("index.html", lista_de_tareas=todas_las_tareas)

@app.route("/crear-tarea", methods=["GET", "POST"])
def crear():
    """ En esta funcion utilizo la libreria datetime(date) con la cual averiguo en el dia en el que estamos para que la aplicacion
    no deje crear tareas que se finalicen antes de la fecha actual. En ese caso mosrtara un mensaje con flash. Tambien mostrara un mensaje en el caso de
    crear l aplicacion  din contenido"""
    dia = str(date.today())                         # aqui con date de datetime he metido en una variable el dia de hoy y asi comparar con reuest form. de fecha para no poder crear tareas fechas anteriores
    diaInt = int(dia.replace('-', ''))              # con replace le quito los guiones para poder comparar como integer
    diaEntrada = request.form['fechaOk']
    diaEntradaInt = int(diaEntrada.replace('-', ''))

    if request.method == 'POST':
        contenido = request.form["contenido-tarea"]

        if not contenido:
            flash('NO PUEDE CREAR UNA TAREA SIN CONTENIDO')
        elif diaEntradaInt < diaInt:
            flash('NO PUEDE CREAR UNA TAREA CON FECHA ANTERIOR A HOY')
        elif not contenido and not diaEntrada:             # en este caso no funciona me sale un ValueError que he tratdo de quitar con una excepcion y tp m sale --ValueError: invalid literal for int() with base 10: '' -- este seria el error
            flash('DEBE PONER CONTENIDO Y FECHA A SU TAREA') # le he tenido que poner el requirimiento obligatorio por html
        else:
            tarea = Tarea(contenido=request.form["contenido-tarea"], hecha=False, categoria=request.form["categoria-tarea"], fecha=request.form['fechaOk'])
            db.session.add(tarea)
            db.session.commit()
            db.session.close()
            return redirect(url_for("home"))
    return redirect(url_for("home")), dia

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=id).delete()
    db.session.commit()
    db.session.close()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=id).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    db.session.close()
    return redirect(url_for("home"))

@app.route("/tarea-fecha/<id>", methods =["GET", "POST"])
def fecha(id):
    """ esta vista no tiene ninguna funcion solo redirigir a home. """
    tarea = db.session.query(Tarea).get(id)
    return redirect(url_for("home"))


@app.route("/editar-tarea/<id>", methods =["GET", "POST"])
def editar(id):
    """"en esta vista doy acceso a la tarea a traves del metodo get con tarea.id y le doy la posibilidad de modificar
    los tres campos al usuario. En caso de que alguno no se modifique se queda como estaba"""

    tarea = db.session.query(Tarea).get(id)
    dia = str(date.today())
    diaInt = int(dia.replace('-', ''))
    diaEntrada = tarea.fecha
    diaEntradaInt = int(diaEntrada.replace('-', ''))

    if request.method == 'POST':
        contenidoNew = request.form['mod_contenido']
        categoriaNew = request.form['mod_categoria']
        fechaNew = request.form['mod_fecha']

        if not contenidoNew:
            flash('TIENE QUE PONER ALGÚN CONTENIDO')
        elif not fechaNew:
            flash('TIENE QUE PONER ALGUNA CONTENIDO')
        elif diaEntradaInt < diaInt:                    # este condicional sobraria porque no se pueden crear tareas previas a la fecha actual y al modificar tiene en el calendario como minimo el dia actual
            flash('NO PUEDE CREAR UNA TAREA CON FECHA ANTERIOR A HOY')  # aunque surge el problema de que si pasa la fecha o no le pongo el minimo de fecha al editar puedes ponerle una fecha anterior de la tarea no se puede modificar porque me da error al comparar con request.form[?mod:fecha]. Como te explico en el documento de texto
        else:
            tarea.contenido = contenidoNew
            tarea.categoria = categoriaNew
            tarea.fecha = fechaNew
            db.session.add(tarea)
            db.session.commit()
            db.session.close()
            return redirect(url_for("home"))

    return render_template("editar.html", mod_tarea=tarea, dia=dia)


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
