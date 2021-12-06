from flask import render_template, redirect, url_for, flash, request, g
from werkzeug.urls import url_parse

#from app import db
from app.crud_queries import bp
#DE LA BD
from app.database import get_db

@bp.route('/crear-cia', methods=['GET','POST'])
def crear_cia():

    if request.method == 'POST':

        #LOGO - CDESCRIPCION - NOMBRE_CIA - COLEGIO_PROC FASE_ALCANZADA

        #Genero el ID llamando a una función de Oracle.
        conn, cursor = get_db()
        nuevo_cod_cia = cursor.callfunc('NUEVO_COD_CIA', int)

        logo = request.form['LOGO']
        cdescripcion = request.form['CDESCRIPCION']
        nombre_cia = request.form['NOMBRE_CIA']
        colegio_proc = int(request.form['COLEGIO_PROC'])
        fase_alcanzada = int(request.form['FASE_ALCANZADA'])

        cursor.callproc('insertar_cia',[nuevo_cod_cia, logo, cdescripcion, nombre_cia, colegio_proc, fase_alcanzada])
        flash('Se ha registrado a la empresa con ID número {}'.format(nuevo_cod_cia))
        conn.commit()
        return redirect('/crear-cia')

    return render_template('crud_queries/crear_nueva_cia.html')

@bp.route('/puntuar-cia',methods=['GET','POST'])
def puntuar_cia():
    """
    Esto es la pagina con puntajes. Para el Jurado.
    """
    conn, cursor = get_db()
    sql_query = "SELECT COD_CIA, NOMBRE_CIA, COL.NOMBRE_COL FROM COMPAÑIA C, \
        COLEGIO COL WHERE COL.COD_COLEGIO = C.COLEGIO_PROC"

    cursor.execute(sql_query)
    tabla_companias = cursor.fetchall()
    #close_db()
    return render_template('crud_queries/puntuar.html', tabla_companias=tabla_companias)

@bp.route('/puntuar', methods=['POST'])
def puntuar():

    conn, cursor = get_db()
    cod_cia = request.form["COD_CIA"]
    punt_acum = request.form["PUNT_ACUM"]
    cursor.callproc('ingresarNotas',[int(cod_cia), int(punt_acum)])
    conn.commit()

    return redirect('puntuar-cia')

@bp.route('/resultados')
def resultados():
    conn, cursor = get_db()

    sql_query = "SELECT COD_CIA, NOMBRE_CIA, COL.NOMBRE_COL, \
        FASE_ALCANZADA FROM COMPAÑIA C, COLEGIO COL WHERE COL.COD_COLEGIO = C.COLEGIO_PROC ORDER BY C.FASE_ALCANZADA DESC"

    cursor.execute(sql_query)
    tabla_resultados = cursor.fetchall()
    #print(tabla_resultados)
    return render_template('crud_queries/resultados.html', tabla_resultados=tabla_resultados)

@bp.route('/mantenimiento')
def mantenimiento():
    return render_template('crud_queries/mantenimiento.html')


@bp.route('/mantenimiento-cia')
def mantenimiento_cia():
    conn, cursor = get_db()

    sql_query = "SELECT C.COD_CIA, C.LOGO, C.CDESCRIPCION, C.NOMBRE_CIA, C.COLEGIO_PROC, \
        C.FASE_ALCANZADA, RS.LINK, RS.RSNOMBRE AS NOMBRE_RED_SOCIAL, P.PUNT_ACUM, P.COD_FASE FROM COMPAÑIA C LEFT JOIN RED_SOCIAL RS ON C.COD_CIA = RS.COD_CIA LEFT JOIN PARTICIPA_EN P ON P.COD_CIA = C.COD_CIA"
    
    cursor.execute(sql_query)
    tabla = cursor.fetchall()
    print("Se ha eliminado el {}".format(id))
    return render_template('crud_queries/mantenimiento-cia.html', tabla=tabla)

@bp.route('/eliminar/<int:id>')
def eliminar(id):
    """
    FALTA ELIMINAR REGISTROS SELECCIONADOS CON PROCEDURE.
    """
    conn, cursor = get_db()

    sql_delete = "DELETE FROM COMPAÑIA WHERE COD_CIA = {}".format(id)

    cursor.execute(sql_delete)
    conn.commit()
    return redirect('/')

@bp.route('/editar/<int:id>')
def editar(id):
    """
    Abrir formulario de edición
    """
    conn, cursor = get_db()

    cursor.execute("SELECT * FROM COMPAÑIA WHERE COD_CIA = {}".format(id))
    compania = cursor.fetchall()
    print('COMPANIA QUERIE EDITAR:', compania[0])

    cursor.execute("SELECT * FROM RED_SOCIAL WHERE COD_CIA = {}".format(id))
    red_social = cursor.fetchall()
    
    cursor.execute("SELECT * FROM PARTICIPA_EN WHERE COD_CIA = {}".format(id))
    participa_en = cursor.fetchall()

    return render_template('crud_queries/editar.html', compania = compania,\
        red_social = red_social, participa_en = participa_en)

@bp.route('/actualizar-cia', methods=['POST'])
def actualizar_cia():
    """
    Actualizar segun el edit form
    """

    cod_cia = request.form['COD_CIA']
    logo = request.form['LOGO']
    cdescripcion = request.form['CDESCRIPCION']
    cole_proc = request.form['COLEGIO_PROC']
    nombre_cia = request.form['NOMBRE_CIA'] 
    fase_alcanzada = request.form['FASE_ALCANZADA']

    sql_update = f"UPDATE COMPAÑIA SET  logo = '{logo}', cdescripcion = '{cdescripcion}',\
        colegio_proc = {cole_proc}, nombre_cia = '{nombre_cia}',\
             fase_alcanzada={fase_alcanzada} WHERE COD_CIA = {cod_cia}"

    conn, cursor = get_db()

    cursor.execute(sql_update)

    conn.commit()

    return redirect('/mantenimiento-cia')

@bp.route('/actualizar-red-social', methods=['POST'])
def actualizar_red_social():
    
    link_red = request.form['RED_SOC']
    nombre_red = request.form['NOMBRE_RED']
    cod_cia = request.form['COD_CIA']

    sql_update = f"UPDATE RED_SOCIAL SET LINK = '{link_red}'\
        , RSNOMBRE = '{nombre_red}' WHERE COD_CIA = {cod_cia}"

    conn, cursor = get_db()
    cursor.execute(sql_update)
    conn.commit()

    return redirect('/mantenimiento-cia')

@bp.route('/actualizar-participa', methods=['POST'])
def actualizar_participa():
    
    punt_acum = request.form['PUNT_ACUM']
    cod_fase = request.form['COD_FASE']
    cod_cia = request.form['COD_CIA']

    sql_update = f"UPDATE PUNT_ACUM SET LINK = '{punt_acum}'\
        , COD_FASE = '{cod_fase}' WHERE COD_CIA = {cod_cia}"

    conn, cursor = get_db()
    cursor.execute(sql_update)
    conn.commit()

    return redirect('/mantenimiento-cia')


@bp.route('/mantenimiento-jurados')
def mantenimiento_jurados():
    conn, cursor = get_db()

    sql_query = "SELECT COD_JURADO, JPRIMER_NOMBRE, JPRIMER_APELLIDO, CORREO_JURADO, \
        LINKEDIN FROM JURADO"

    cursor.execute(sql_query)
    tabla_jurado = cursor.fetchall()

    return render_template('crud_queries/mantenimiento-jurados.html', tabla_jurado = tabla_jurado)

@bp.route('/editar-jurado/<int:id>')
def editar_jurado(id):
    """
    Abrir formulario de edición de Jurados
    """

    conn, cursor = get_db()
    cursor.execute("SELECT * FROM JURADO WHERE COD_JURADO = {}".format(id))
    jurado_data = cursor.fetchall()
    print("JURADO DATA:", jurado_data)
        
    return render_template('crud_queries/editar-jurado.html', jurado_data=jurado_data)

@bp.route('/ver-actividades-jurado/<int:id>')
def ver_actividad(id):
    """
    Listar las actividades de cada jurado
    """
    conn, cursor = get_db()

    cursor.execute("SELECT * FROM ACTIVIDAD WHERE COD_JURADO = {}".format(id))
    actividades = cursor.fetchall()

    return render_template('crud_queries/ver-actividades-jurado.html', actividades=actividades,id=id)

@bp.route('/actualizar-jurado', methods=['POST'])
def actualizar_jurado():
    """
    Actualizar segun el edit form
    """
    COD_JURADO = int(request.form['COD_JURADO'])
    JPRIMER_NOMBRE = request.form['JPRIMER_NOMBRE']	
    JSEG_NOMBRE = request.form['JSEG_NOMBRE']	
    JPRIMER_APELLIDO = request.form['JPRIMER_APELLIDO']	
    JSEG_APELLIDO = request.form['JSEG_APELLIDO']	
    CORREO_JURADO = request.form['CORREO_JURADO']	
    LINKEDIN = request.form['LINKEDIN']

    conn, cursor = get_db()

    cursor.callproc("update_jurado",[COD_JURADO, JPRIMER_NOMBRE, JSEG_NOMBRE, JPRIMER_APELLIDO, JSEG_APELLIDO,\
        CORREO_JURADO, LINKEDIN])
    
    flash("Se editó correctamente al jurado nro {}: {} {} {}".format(COD_JURADO, JPRIMER_NOMBRE, JSEG_NOMBRE, JPRIMER_APELLIDO))

    conn.commit()
    return redirect('/mantenimiento-jurados')


@bp.route('/sgte-fase', methods=['GET','POST'])
def sgte_fase():

    conn, cursor = get_db()

    sql_query = "SELECT COD_CIA, NOMBRE_CIA, COL.NOMBRE_COL, \
        FASE_ALCANZADA FROM COMPAÑIA C, COLEGIO COL WHERE COL.COD_COLEGIO = C.COLEGIO_PROC ORDER BY C.FASE_ALCANZADA DESC"

    cursor.execute(sql_query)
    tabla_resultados = cursor.fetchall()

    if request.method == 'POST':
        conn, cursor = get_db()
        nro_part = int(request.form['NRO_PARTICIPANTES'])
        cursor.callproc('ganadoresRonda',[nro_part])
        conn.commit()
        return redirect('/sgte-fase')

    return render_template('crud_queries/sgte_fase.html', tabla_resultados=tabla_resultados)



