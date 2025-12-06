"""
Utilidades para impresión automática
Janet Rosa Bici - Sistema de Ventas
"""

import os
import platform
import subprocess
import tempfile

def detectar_impresora_predeterminada():
    """
    Detectar la impresora predeterminada del sistema
    """
    try:
        sistema = platform.system()
        
        if sistema == "Windows":
            # En Windows, usar wmic para obtener la impresora predeterminada
            try:
                resultado = subprocess.check_output(
                    'wmic printer where default=true get name',
                    shell=True,
                    text=True
                )
                lineas = resultado.strip().split('\n')
                if len(lineas) > 1:
                    impresora = lineas[1].strip()
                    if impresora:
                        return impresora
            except:
                pass
            
            # Método alternativo con PowerShell
            try:
                resultado = subprocess.check_output(
                    'powershell -command "Get-WmiObject -Query \\"SELECT * FROM Win32_Printer WHERE Default=$true\\" | Select-Object -ExpandProperty Name"',
                    shell=True,
                    text=True
                )
                impresora = resultado.strip()
                if impresora:
                    return impresora
            except:
                pass
        
        elif sistema == "Linux":
            # En Linux, usar lpstat
            try:
                resultado = subprocess.check_output(['lpstat', '-d'], text=True)
                if 'system default destination:' in resultado:
                    impresora = resultado.split('system default destination:')[1].strip()
                    return impresora
            except:
                pass
        
        elif sistema == "Darwin":  # macOS
            # En macOS, usar lpstat
            try:
                resultado = subprocess.check_output(['lpstat', '-d'], text=True)
                if 'system default destination:' in resultado:
                    impresora = resultado.split('system default destination:')[1].strip()
                    return impresora
            except:
                pass
        
        return None
        
    except Exception as e:
        print(f"Error al detectar impresora: {e}")
        return None

def listar_impresoras():
    """
    Listar todas las impresoras disponibles
    """
    try:
        sistema = platform.system()
        impresoras = []
        
        if sistema == "Windows":
            try:
                resultado = subprocess.check_output(
                    'wmic printer get name',
                    shell=True,
                    text=True
                )
                lineas = resultado.strip().split('\n')[1:]  # Saltar header
                impresoras = [linea.strip() for linea in lineas if linea.strip()]
            except:
                pass
        
        elif sistema in ["Linux", "Darwin"]:
            try:
                resultado = subprocess.check_output(['lpstat', '-p'], text=True)
                for linea in resultado.split('\n'):
                    if linea.startswith('printer'):
                        partes = linea.split()
                        if len(partes) > 1:
                            impresoras.append(partes[1])
            except:
                pass
        
        return impresoras
        
    except Exception as e:
        print(f"Error al listar impresoras: {e}")
        return []

def imprimir_archivo(archivo_path, impresora=None):
    """
    Imprimir un archivo directamente
    
    Args:
        archivo_path: Ruta del archivo a imprimir (HTML, PDF, TXT)
        impresora: Nombre de la impresora (None = predeterminada)
    """
    try:
        sistema = platform.system()
        
        if not impresora:
            impresora = detectar_impresora_predeterminada()
        
        if sistema == "Windows":
            # En Windows, usar el comando print
            if impresora:
                # Imprimir en impresora específica
                comando = f'print /D:"{impresora}" "{archivo_path}"'
            else:
                # Imprimir en impresora predeterminada
                comando = f'print "{archivo_path}"'
            
            subprocess.run(comando, shell=True, check=True)
            return True
            
        elif sistema in ["Linux", "Darwin"]:
            # En Linux/macOS, usar lp
            if impresora:
                comando = ['lp', '-d', impresora, archivo_path]
            else:
                comando = ['lp', archivo_path]
            
            subprocess.run(comando, check=True)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error al imprimir: {e}")
        return False

def imprimir_html_directo(html_content, impresora=None):
    """
    Imprimir contenido HTML directamente
    
    Args:
        html_content: Contenido HTML como string
        impresora: Nombre de la impresora (None = predeterminada)
    """
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        # Imprimir el archivo
        resultado = imprimir_archivo(temp_path, impresora)
        
        # Limpiar archivo temporal después de un momento
        try:
            import time
            time.sleep(2)
            os.unlink(temp_path)
        except:
            pass
        
        return resultado
        
    except Exception as e:
        print(f"Error al imprimir HTML: {e}")
        return False

def abrir_dialogo_impresion(archivo_path):
    """
    Abrir el diálogo de impresión del sistema
    """
    try:
        sistema = platform.system()
        
        if sistema == "Windows":
            # Abrir con el programa predeterminado y mostrar diálogo de impresión
            os.startfile(archivo_path, 'print')
            return True
            
        elif sistema == "Darwin":  # macOS
            # Abrir con el comando open
            subprocess.run(['open', '-a', 'Preview', archivo_path])
            return True
            
        elif sistema == "Linux":
            # Intentar con xdg-open
            subprocess.run(['xdg-open', archivo_path])
            return True
        
        return False
        
    except Exception as e:
        print(f"Error al abrir diálogo de impresión: {e}")
        return False

def verificar_impresora_disponible():
    """
    Verificar si hay al menos una impresora disponible
    """
    impresoras = listar_impresoras()
    return len(impresoras) > 0

def obtener_info_impresora():
    """
    Obtener información sobre la configuración de impresión
    """
    info = {
        'sistema': platform.system(),
        'impresora_predeterminada': detectar_impresora_predeterminada(),
        'impresoras_disponibles': listar_impresoras(),
        'tiene_impresoras': False
    }
    
    info['tiene_impresoras'] = len(info['impresoras_disponibles']) > 0
    
    return info

# Función de prueba
if __name__ == "__main__":
    print("=" * 60)
    print("INFORMACIÓN DE IMPRESIÓN")
    print("=" * 60)
    
    info = obtener_info_impresora()
    
    print(f"\nSistema Operativo: {info['sistema']}")
    print(f"\nImpresora Predeterminada: {info['impresora_predeterminada'] or 'No detectada'}")
    print(f"\nImpresoras Disponibles ({len(info['impresoras_disponibles'])}):")
    
    if info['impresoras_disponibles']:
        for i, impresora in enumerate(info['impresoras_disponibles'], 1):
            print(f"  {i}. {impresora}")
    else:
        print("  No se detectaron impresoras")
    
    print("\n" + "=" * 60)
