"""
Script de prueba para el sistema de códigos de barras
Prueba las funciones de búsqueda y validación
"""
from controllers.products import (
    buscar_por_codigo_barras, 
    codigo_barras_disponible, 
    generar_codigo_barras,
    obtener_productos
)

def test_buscar_por_codigo_barras():
    """Probar búsqueda por código de barras"""
    print("\n=== Test: Buscar por Código de Barras ===")
    
    # Buscar un código de ejemplo
    codigo = "7500100000101"
    producto = buscar_por_codigo_barras(codigo)
    
    if producto:
        print(f"✅ Producto encontrado:")
        print(f"   - ID: {producto.get('id_producto')}")
        print(f"   - Código: {producto.get('codigo')}")
        print(f"   - Código de Barras: {producto.get('codigo_barras')}")
        print(f"   - Nombre: {producto.get('nombre')}")
        print(f"   - Precio: ${producto.get('precio'):.2f}")
        print(f"   - Stock: {producto.get('stock')} unidades")
    else:
        print(f"❌ No se encontró producto con código: {codigo}")

def test_codigo_disponible():
    """Probar validación de código disponible"""
    print("\n=== Test: Validar Código Disponible ===")
    
    # Probar código existente
    codigo_existente = "7500100000101"
    disponible = codigo_barras_disponible(codigo_existente)
    print(f"Código {codigo_existente}: {'❌ Ya existe' if not disponible else '✅ Disponible'}")
    
    # Probar código nuevo
    codigo_nuevo = "7509999999999"
    disponible = codigo_barras_disponible(codigo_nuevo)
    print(f"Código {codigo_nuevo}: {'❌ Ya existe' if not disponible else '✅ Disponible'}")

def test_generar_codigo():
    """Probar generación de códigos"""
    print("\n=== Test: Generar Códigos de Barras ===")
    
    for i in range(5):
        codigo = generar_codigo_barras(1, i+1)
        print(f"Código generado {i+1}: {codigo}")

def test_listar_productos_con_codigos():
    """Listar productos con sus códigos de barras"""
    print("\n=== Test: Listar Productos con Códigos ===")
    
    productos = obtener_productos()
    
    if productos:
        print(f"\nTotal de productos: {len(productos)}\n")
        print(f"{'ID':<5} {'Código':<12} {'Código Barras':<15} {'Nombre':<30} {'Stock':<8}")
        print("-" * 80)
        
        for p in productos[:10]:  # Mostrar solo los primeros 10
            id_prod = p.get('id_producto', 'N/A')
            codigo = p.get('codigo', 'N/A')
            codigo_barras = p.get('codigo_barras', 'Sin código')
            nombre = p.get('nombre', 'N/A')[:28]
            stock = p.get('stock', 0)
            
            print(f"{id_prod:<5} {codigo:<12} {codigo_barras:<15} {nombre:<30} {stock:<8}")
    else:
        print("❌ No hay productos en la base de datos")

def test_simulacion_venta():
    """Simular una venta con código de barras"""
    print("\n=== Test: Simulación de Venta ===")
    
    # Simular escaneo de código de barras
    codigo_escaneado = "7500100000101"
    print(f"📱 Escaneando código: {codigo_escaneado}")
    
    producto = buscar_por_codigo_barras(codigo_escaneado)
    
    if producto:
        print(f"\n✅ Producto agregado al carrito:")
        print(f"   {producto.get('nombre')}")
        print(f"   Precio: ${producto.get('precio'):.2f}")
        print(f"   Stock disponible: {producto.get('stock')} unidades")
        
        # Simular venta de 2 unidades
        cantidad = 2
        stock_actual = producto.get('stock', 0)
        
        if cantidad <= stock_actual:
            nuevo_stock = stock_actual - cantidad
            print(f"\n💰 Venta procesada:")
            print(f"   Cantidad vendida: {cantidad}")
            print(f"   Total: ${producto.get('precio') * cantidad:.2f}")
            print(f"   Stock anterior: {stock_actual}")
            print(f"   Stock nuevo: {nuevo_stock}")
        else:
            print(f"\n❌ Stock insuficiente")
            print(f"   Solicitado: {cantidad}")
            print(f"   Disponible: {stock_actual}")
    else:
        print(f"❌ Producto no encontrado")

if __name__ == "__main__":
    print("=" * 80)
    print("SISTEMA DE CÓDIGOS DE BARRAS - JANET ROSA BICI")
    print("=" * 80)
    
    try:
        test_buscar_por_codigo_barras()
        test_codigo_disponible()
        test_generar_codigo()
        test_listar_productos_con_codigos()
        test_simulacion_venta()
        
        print("\n" + "=" * 80)
        print("✅ Todos los tests completados")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error durante los tests: {str(e)}")
        import traceback
        traceback.print_exc()
