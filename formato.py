from fastapi.responses import HTMLResponse

def tabla_formato(tabla, titulo: str) -> HTMLResponse:
    """
    Convierte un DataFrame de pandas en una tabla HTML con formato bootstrap
    
    Args:
        tabla: DataFrame de pandas
        titulo: Título que se mostrará en la página
        
    Returns:
        HTMLResponse: Respuesta HTML con la tabla formateada
    """
    tabla_html = tabla.to_html(
        index=False,
        classes='table table-bordered table-striped-columns table-hover text-center',
    )
    html_total = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          rel="stylesheet"
        >
        <style>
            .table thead th {{
                text-align: center;
                vertical-align: middle;
                background-color: #3c0069;
                color: white; 
            }} 
            body {{
                background-color: #f8f9fa;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
                padding: 25px;
            }}
            h2 {{
                color: #3c0069;
                font-weight: bold;
            }}
        </style>    
    </head>
    <body>
        <div class="container my-5">
            <h2 class="text-center mb-4">{titulo}</h2>
            <div class="table-responsive">
                {tabla_html}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_total)