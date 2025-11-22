from database.db import crear_conexion

def resumen_apartados():
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM apartados")
    total = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS activos FROM apartados WHERE estado='Pendiente'")
    activos = cur.fetchone()["activos"]
    cur.execute("SELECT COUNT(*) AS completados FROM apartados WHERE estado='Pagado'")
    comp = cur.fetchone()["completados"]
    cur.execute("SELECT COUNT(*) AS cancelados FROM apartados WHERE estado='Cancelado'")
    canc = cur.fetchone()["cancelados"]
    cur.execute("SELECT COALESCE(SUM(saldo),0) AS pendiente_total FROM apartados WHERE estado='Pendiente'")
    pen = cur.fetchone()["pendiente_total"]
    conn.close(); return {"total": total, "activos": activos, "completados": comp, "cancelados": canc, "pendiente_total": pen}

def listar_apartados(estado=None, search=None, start_date=None, end_date=None, limit=100):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    where = []; params = []
    if estado and estado != 'Todos':
        where.append("a.estado=%s"); params.append(estado)
    if search:
        where.append("(c.nombre LIKE %s OR c.telefono LIKE %s)"); params.extend([f"%{search}%", f"%{search}%"])
    if start_date and end_date:
        where.append("DATE(a.fecha) BETWEEN %s AND %s"); params.extend([start_date, end_date])
    wsql = (" WHERE "+" AND ".join(where)) if where else ""
    sql = f"SELECT a.id_apartado, a.fecha, a.total, a.anticipo, a.saldo, a.fecha_limite, a.estado, c.nombre AS cliente FROM apartados a LEFT JOIN clientes c ON a.id_cliente=c.id_cliente{wsql} ORDER BY a.id_apartado DESC LIMIT %s"
    params.append(limit)
    cur.execute(sql, params)
    rows = cur.fetchall(); conn.close(); return rows

def exportar_apartados_csv(path, estado=None, search=None, start_date=None, end_date=None):
    rows = listar_apartados(estado=estado, search=search, start_date=start_date, end_date=end_date, limit=1000000)
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID","Cliente","Total","Anticipo","Saldo","Fecha","Fecha límite","Estado"])
        for a in rows:
            w.writerow([a["id_apartado"], a.get("cliente") or "-", f"{float(a['total']):.2f}", f"{float(a.get('anticipo') or 0):.2f}", f"{float(a.get('saldo') or 0):.2f}", str(a["fecha"]), str(a.get("fecha_limite") or ""), a["estado"]])
    return path

def crear_apartado(id_cliente=None, total=0.0, anticipo=0.0, fecha_limite=None):
    saldo = float(total) - float(anticipo)
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("INSERT INTO apartados (id_cliente, total, anticipo, saldo, fecha_limite, estado) VALUES (%s, %s, %s, %s, %s, %s)", (id_cliente, total, anticipo, saldo, fecha_limite, 'Pendiente'))
    conn.commit(); conn.close(); return True

def cambiar_estado(id_apartado, estado):
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("UPDATE apartados SET estado=%s WHERE id_apartado=%s", (estado, id_apartado))
    conn.commit(); conn.close(); return True

def registrar_anticipo(id_apartado, monto):
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("UPDATE apartados SET anticipo = anticipo + %s, saldo = GREATEST(saldo - %s, 0) WHERE id_apartado=%s", (monto, monto, id_apartado))
    conn.commit(); conn.close(); return True