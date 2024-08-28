# .\.venv\Scripts\activate
# afbff5

import ply.lex as lex
from flask import Flask, render_template, request

# Instancia de App en Flask
app = Flask(__name__)

reserved = {
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'int': 'INT',
}

identificador ={
    'main': 'MAIN',
    'n': 'N',
}

tokens = ['PABIERTO', 'PCERRADO','LLABIERTO', 'SIMBOLO','LLACERRADO','ENTERO', 'OPERADOR'] + list(reserved.values()) + list(identificador.values())

t_PUBLIC = r'public'
t_STATIC = r'static'
t_VOID = r'void'
t_INT = r'int'

t_MAIN = r'main'
t_N = r'n'


t_ignore = ' \t\r'
t_PABIERTO = r'\('
t_PCERRADO = r'\)'
t_LLABIERTO = r'\{'
t_LLACERRADO = r'\}'
t_SIMBOLO =  r'.'
t_OPERADOR = r'\='
t_ENTERO = r'\d+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t=0

def t_error(t):
    print('Caracter no valido', t.value[0])
    t.lexer.skip(1)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code','')

        lexer = lex.lex()
        lexer.input(code)  # Asegúrate de usar 'code' y no 'content'

        result_lexema = []
        contador= {}
        for tok in lexer:
            if tok.type in reserved.values():
                descripcion = "Reservada"
            elif tok.type == "PABIERTO":
                descripcion = "Parentecis abierto"
            elif tok.type == "PCERRADO":
                descripcion = "Parentecis Cerrado"
            elif tok.type == "LLABIERTO":
                descripcion = "Llave abierta"
            elif tok.type == "LLACERRADO":
                descripcion = "Llave Cerrada"
            elif tok.type == "=":
                descripcion = "Operador"
            elif tok.type in identificador.values():
                descripcion = "Identificador"
            elif tok.type == "ENTERO":
                descripcion = "Entero"
            elif tok.type == "Simbolo":
                descripcion = "SIMBOLO"
            else:
                descripcion = "Simbolo"
            
            result_lexema.append((descripcion, tok.value, tok.lineno))

        for tipo, palabra, numero in result_lexema:
            if tipo in contador:
                contador[tipo] += 1
            else:
                contador[tipo] = 1

        return render_template('index.html', tokens=result_lexema, contador=contador)
    return render_template('index.html', tokens=None)


if __name__ == "__main__":
    app.run(debug=True)


