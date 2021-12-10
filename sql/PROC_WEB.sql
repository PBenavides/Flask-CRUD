--Procedimiento para ingresarNotas toma como parametros un codigo de compañia y una nota
CREATE OR REPLACE PROCEDURE ingresarNotas(p_codigo compañia.cod_cia%type, p_nota number) is
    BEGIN
        UPDATE PARTICIPA_EN
        SET punt_acum = punt_acum + p_nota
        WHERE participa_en.cod_cia = p_codigo; 
    END;


--Procedimiento para insertar valores en compañia
CREATE OR REPLACE PROCEDURE insertar_cia(cod compañia.cod_cia%type,
logo compañia.logo%type, descrip compañia.cdescripcion%type, 
nombre compañia.nombre_cia%type, col_proc compañia.colegio_proc%type,
fase compañia.fase_alcanzada%type) is
   BEGIN
       INSERT INTO COMPAÑIA
       VALUES
       (cod, logo, descrip, nombre, col_proc, fase);
    END;

--procedimiento actualziar tabla jurados
create or replace procedure update_jurado(
    cod jurado.cod_jurado%type,
    pri_n jurado.jprimer_nombre%type,
    seg_n jurado.jseg_nombre%type,
    pri_a jurado.jprimer_apellido%type,
    seg_a jurado.jseg_apellido%type,
    correo jurado.correo_jurado%type,
    lnkdn jurado.linkedin%type)
 is
    begin
    update jurado set
    jprimer_nombre = pri_n,
    jseg_nombre = seg_n,
    jprimer_apellido = pri_a,
    jseg_apellido = seg_a,
    correo_jurado = correo,
    linkedin = lnkdn
    where cod_jurado=cod;
    end;

--procedimiento actualizar compañia
create or replace procedure update_cia(
    logo_ compañia.logo%type,
    cdescripcion_ compañia.cdescripcion%type,
    nombre_cia_ compañia.nombre_cia%type,
    colegio_proc_ compañia.colegio_proc%type,
    fase_alcanzada_  compañia.fase_alcanzada%type,
    cod_cia_ compañia.cod_cia%type)
 is
    begin
    update compañia set
    logo = logo_,
    cdescripcion = cdescripcion_,
    nombre_cia = nombre_cia_,
    colegio_proc = colegio_proc_,
    fase_alcanzada = fase_alcanzada_
    where cod_cia= cod_cia_;
    end;

--procedimiento actualizar red social
create or replace procedure update_red_social(
    link_  red_social.link%type,
    rsnombre_  red_social.rsnombre%type,
    cod_cia_  red_social.cod_cia%type)
    is
    begin
    update red_social set
    link = link_,
    rsnombre = rsnombre_
    where cod_cia = cod_cia_;
    end;

--procedimiento actualizar tabla participa_en

create or replace procedure update_participa_en(
    punt_acum_  participa_en.punt_acum%type,
    cod_fase_  participa_en.cod_fase%type,
    cod_cia_  participa_en.cod_cia%type)
    is
    begin
    update participa_en set
    punt_acum = punt_acum_,
    cod_fase = cod_fase_
    where cod_cia = cod_cia_;
    end;


--Procedimiento para generar ganadores por ronda, recibe como parametro la cantidad de ganadores a los que se le actualizra su fase alcanzada
CREATE OR REPLACE PROCEDURE ganadoresRonda(p_cantidad_participantes number) is
    BEGIN
        UPDATE COMPAÑIA
        SET Fase_alcanzada = Fase_alcanzada + 1
        WHERE cod_cia IN (
            SELECT PARTICIPA_EN.cod_cia
            FROM PARTICIPA_EN 
            order by punt_acum DESC 
            FETCH FIRST p_cantidad_participantes ROWS ONLY );
    END;


--FUNCION PARA GENERAR UN NUEVO ID PARA LA COMPAÑIA
CREATE OR REPLACE FUNCTION NUEVO_COD_CIA RETURN NUMBER AS
    NUEVO_COD COMPAÑIA.COD_CIA%TYPE;
    BEGIN
        SELECT MAX(COD_CIA) + 1 INTO NUEVO_COD
        FROM COMPAÑIA;
        RETURN NUEVO_COD;
    END;

--procedimiento para eliminar jurado.
CREATE OR REPLACE PROCEDURE ELIMINAR_JURADO(COD NUMBER) AS
BEGIN
    DELETE ACTIVIDAD WHERE COD_JURADO=COD;
    DELETE JURADO WHERE COD_JURADO=COD;
END;

CREATE OR REPLACE PROCEDURE ELIMINAR_CIA(COD NUMBER) AS
BEGIN
    DELETE RED_SOCIAL WHERE COD_CIA=COD;
    DELETE ESTUDIANTE WHERE COD_CIA=COD;
    DELETE GUIA_A WHERE COD_CIA=COD;
    DELETE PARTICIPA_EN WHERE COD_CIA=COD;
    DELETE COMPAÑIA WHERE COD_CIA=COD;
END;

---------------- Dado que cx_Oracle no permite llamar a través de dbms_output, los SELECTS han sido inyectados
---------------- directamente a través del código SQL. A continuación se verán los selects usados en toda la app.
--PROMEDIO DE PUNTAJES POR REGION.
SELECT ROUND(AVG(PUNT_ACUM),2) AS PROMEDIO_PUNTAJES, REGION 
    FROM (SELECT C.COD_CIA, C.NOMBRE_CIA, P.PUNT_ACUM, J.REGION, J.TIPO_COL, J.NOMBRE_COL
    FROM COMPAÑIA C
    LEFT JOIN PARTICIPA_EN P ON P.COD_CIA = C.COD_CIA
    LEFT JOIN (SELECT COL.REGION, COL.TIPO_COL, COL.NOMBRE_COL, E.COD_CIA
    FROM ESTUDIANTE E LEFT JOIN COLEGIO COL ON COL.COD_COLEGIO = E.COD_COLEGIO) J ON J.COD_CIA = C.COD_CIA)
    GROUP BY REGION

-- Para la informacion del jurado
SELECT COD_CIA, NOMBRE_CIA, COL.NOMBRE_COL FROM COMPAÑIA C, COLEGIO COL 
       WHERE COL.COD_COLEGIO = C.COLEGIO_PROC AND Fase_alcanzada IN (SELECT MAX(Fase_alcanzada) FROM COMPAÑIA)

-- Mostrar resultados.
SELECT COD_CIA, NOMBRE_CIA, COL.NOMBRE_COL, FASE_ALCANZADA FROM COMPAÑIA C, COLEGIO COL
            WHERE COL.COD_COLEGIO = C.COLEGIO_PROC ORDER BY C.FASE_ALCANZADA DESC

-- Mostrar mantenimiento. Join de 3 tablas
SELECT C.COD_CIA, C.LOGO, C.CDESCRIPCION, C.NOMBRE_CIA, C.COLEGIO_PROC,
        C.FASE_ALCANZADA, RS.LINK, RS.RSNOMBRE AS NOMBRE_RED_SOCIAL, P.PUNT_ACUM, P.COD_FASE FROM COMPAÑIA C
LEFT JOIN RED_SOCIAL RS ON C.COD_CIA = RS.COD_CIA 
LEFT JOIN PARTICIPA_EN P ON P.COD_CIA = C.COD_CIA

--SELECT DE MANTENIMIENTO DE JURADOS.
SELECT COD_JURADO, JPRIMER_NOMBRE, JPRIMER_APELLIDO, CORREO_JURADO, LINKEDIN FROM JURADO

--SELECT PARA ACTIVIDADES DE JURADO
--SELECT * FROM ACTIVIDAD WHERE COD_JURADO = {}

--SELECT PARA LA VISTA DEL ADMIN. SIGUIENTE FASE.
SELECT COD_CIA, NOMBRE_CIA, COL.NOMBRE_COL,
        FASE_ALCANZADA FROM COMPAÑIA C, COLEGIO COL WHERE COL.COD_COLEGIO = C.COLEGIO_PROC ORDER BY C.FASE_ALCANZADA DESC