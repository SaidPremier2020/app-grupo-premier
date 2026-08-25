import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. INICIALIZAR MEMORIA ---
if 'pantalla_actual' not in st.session_state:
    st.session_state.pantalla_actual = 'inicio'

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA Y API
# ---------------------------------------------------------
st.set_page_config(page_title="GRUPO PREMIER | Catálogo", page_icon="🏢", layout="centered")

GOOGLE_API_KEY = "AQ.Ab8RN6Jmm0DppGdLbEveLJBtR0Hp9ghzs0aLPaHlapqotjpAWw"
genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------------------------------------------
# 🔒 SISTEMA DE LOGIN Y SEGURIDAD
# ---------------------------------------------------------
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

USUARIOS_PERMITIDOS = {
    "said.avila@vpremier.com": "Premier2026*",
}

if not st.session_state.autenticado:
    st.title("🔒 Acceso Restringido")
    st.markdown("Por favor, ingresa tus credenciales de Grupo Premier para continuar.")
    
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        if correo in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[correo] == contrasena:
            st.session_state.autenticado = True
            st.session_state.usuario_actual = correo
            st.rerun()
        else:
            st.error("❌ Correo o contraseña incorrectos. Intenta de nuevo.")
            
    st.stop()

with st.sidebar:
    st.write(f"👤 Conectado como: **{st.session_state.usuario_actual}**")
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

# =========================================================
# PANTALLA 1: INICIO 
# =========================================================
if st.session_state.pantalla_actual == 'inicio':

    try:
        logo = Image.open("logo_premier.png")
        st.image(logo, width=250)
    except FileNotFoundError:
        st.warning("⚠️ Logotipo no encontrado. Guarda tu logo como 'logo_premier.png' en la misma carpeta.")

    st.title("Bienvenido a GRUPO PREMIER")
    st.markdown("Somos líderes en brindar soluciones de excelencia. Explora nuestro catálogo de servicios.")
    st.divider()

    st.header("Nuestros Servicios")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Servicios Integrales"): 
            st.session_state.pantalla_actual = 'Servicios Integrales'
            st.rerun()
            
    with col2:
        if st.button("Grupos y Convenciones"):
            st.session_state.pantalla_actual = 'grupos'
            st.rerun()
        
    with col3:
        if st.button("Call Center 24/7"):
            st.session_state.pantalla_actual = 'call_center'
            st.rerun()
        
    st.divider()

    
    st.header("💬 Asistente Virtual GRUPO PREMIER")
    st.write("¿Tienes alguna duda sobre nuestros servicios? Conversa con nuestro asistente.")

    # EL CEREBRO ACTUALIZADO DE LA IA
    INFORMACION_EMPRESA = """
    Eres el asistente virtual oficial de GRUPO PREMIER. Tu tono debe ser profesional, amable, servicial y enfocado a brindar la mayor información posible del Grupo. 
    NUNCA inventes precios ni servicios que no estén en este documento. Si te preguntan algo que no sabes, pide amablemente que dejen sus datos para que un asesor humano los contacte.
    
    **SOBRE NOSOTROS:**
    Somos GRUPO PREMIER, Agencia de servicios integrales especializada en el viajero y eventos, con 50 años de experiencia, trabajando para Gobierno y Sector Privado. Contamos con certificaciones como ISO 9001, Turismo Incluyente, Distintivo M, entre otras.
    
    **1. SERVICIOS INTEGRALES:**
    - Movilidad y Transporte: Vuelos, helicópteros, renta de autos, transporte privado de lujo, yates y cruceros.
    - Viajes y Turismo: Hoteles, paquetes, tours, boletos para espectáculos, actividades extremas y turismo especializado.
    - Soluciones Corporativas: Relaciones públicas con gobierno, comunicación, manejo de medios y servicios notariales.
    - Logística y Seguridad: Seguridad privada, visas, fletes, mudanzas, traductores y edecanes.
    
    **2. GRUPOS Y CONVENCIONES (EVENTOS):**
    - Logística y Espacios: Renta de recintos, vallas, mobiliario, fabricación de stands y oficios de montaje.
    - Estrategia y Diseño: Diseño gráfico, imagen corporativa, uniformes, trofeos y placas.
    - Gastronomía: Catering y banquetes de alta calidad.
    - Tecnología y Shows: Audio, video, iluminación (AVI), shows de drones, pirotecnia y contratación de artistas.
    - Actividades: Team building, campamentos, campañas políticas y jueceo deportivo.
    - Seguridad: Servicios médicos, ambulancias y logística de obras de arte.
    
    **CONTACTO (Call Center 24/7):**
    - Teléfono: +52 55 54480500
    - Correo: contacto@grupopremier.com
    - Horario de atención: Las 24 horas los 365 días del año
    """

    if "historial_chat" not in st.session_state:
        st.session_state.historial_chat = []

    for mensaje in st.session_state.historial_chat:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        st.session_state.historial_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando la base de datos de Grupo Premier..."):
                contexto_conversacion = INFORMACION_EMPRESA + "\n\nHistorial de la conversación hasta ahora:\n"
                for msg in st.session_state.historial_chat:
                    rol = "Cliente" if msg["role"] == "user" else "Asistente"
                    contexto_conversacion += f"{rol}: {msg['content']}\n"

                try:
                    modelo = genai.GenerativeModel('gemini-flash-latest')
                    respuesta = modelo.generate_content(contexto_conversacion)
                    st.markdown(respuesta.text)
                    st.session_state.historial_chat.append({"role": "assistant", "content": respuesta.text})
                except Exception as e:
                    st.error(f"Error técnico de conexión: {e}")


# =========================================================
# PANTALLA 2: SERVICIOS INTEGRALES
# =========================================================
elif st.session_state.pantalla_actual == 'Servicios Integrales':
    
    if st.button("⬅️ Regresar al Inicio"):
        st.session_state.pantalla_actual = 'inicio'
        st.rerun()
        
    st.markdown("---")
    st.title("📈 Servicios Integrales")
    
    st.write("En Grupo Premier, sabemos que cada viaje, evento o proyecto es único. Por ello, hemos diseñado un ecosistema integral de servicios pensados para superar tus expectativas. Ya sea que busques la adrenalina de una nueva aventura, la logística perfecta para tu corporativo o el confort de un traslado exclusivo, estamos aquí para hacerlo realidad. Explora nuestras categorías y descubre cómo transformamos tus ideas en experiencias inolvidables.")
    
    st.markdown("---")
    
    with st.expander("✈️ Movilidad y Transporte a Medida"):
        st.markdown("**Todo lo que necesitas para llegar a tu destino con el nivel de confort que elijas.**")
        st.markdown('''
        *   **Vuelos y Aire:** Boletos de avión, helicópteros, jets privados/taxis aéreos e instituciones aeroportuarias.
        *   **Terrestre:** Renta de autos (y customización), transporte privado/lujo (Sprinter, Van, Suburban, etc.), trenes de pasajeros, autobuses turísticos hop-on/hop-off y traslados aeropuerto-hotel.
        *   **Marítimo:** Yates privados, cruceros y ferry's.
        ''')
        if st.button("Cotizar Transporte", key="btn_transporte"):
            st.success("¡Excelente! Te contactaremos pronto para tu transporte.")
            
    with st.expander("🌍 Viajes, Turismo y Experiencias"):
        st.markdown("**Diseñamos desde la tranquilidad de tu descanso hasta la aventura de tu vida.**")
        st.markdown('''
        *   **Hospedaje y Viajes:** Hoteles, paquetes FIT nacionales e internacionales, tours, grupos de mochileros "Nómadas" y OTAS.
        *   **Aventura y Entretenimiento:** Boletos para espectáculos, actividades turísticas (tirolesa, buceo, auroras boreales, avistamientos, etc.), acuarios y reservas gastronómicas.
        *   **Turismo Especializado:** Servicios turísticos inclusivos, guías de turistas, venta de artesanías y seguros de viaje.
        ''')
        if st.button("Diseñar mi experiencia", key="btn_turismo"):
            st.success("¡Vamos a planear el viaje de tus sueños!")
            
    with st.expander("🏢 Soluciones Corporativas y Relaciones Públicas"):
        st.markdown("**El respaldo institucional y comercial que tu empresa o evento requiere.**")
        st.markdown('''
        *   **Alianzas y Gestoría:** Relaciones públicas con gobiernos (federales, estatales y municipales), relaciones comerciales con asociaciones turísticas y gestoría de certificaciones empresariales.
        *   **Comunicación:** Manejo de medios de comunicación.
        *   **Legal:** Servicios notariales.
        ''')
        if st.button("Hablar con un asesor corporativo", key="btn_corp"):
            st.success("Un asesor se pondrá en contacto contigo a la brevedad.")
            
    with st.expander("🛡️ Logística, Seguridad y Soporte"):
        st.markdown("**Servicios operativos para que tú solo te preocupes por disfrutar o hacer negocios.**")
        st.markdown('''
        *   **Protección y Trámites:** Seguridad privada, gestoría de visas y servicios de vacunación para viajeros.
        *   **Logística:** Fletes, mudanzas, trenes de carga y mensajería/paquetería privada.
        *   **Soporte a Eventos:** Edecanes, traductores de idiomas y servicios de florería/floristas.
        ''')
        if st.button("Solicitar Soporte Operativo", key="btn_logistica"):
            st.success("Estamos listos para apoyarte con tu logística.")


# =========================================================
# PANTALLA 3: GRUPOS Y CONVENCIONES
# =========================================================
elif st.session_state.pantalla_actual == 'grupos':
    
    if st.button("⬅️ Regresar al Inicio"):
        st.session_state.pantalla_actual = 'inicio'
        st.rerun()
        
    st.markdown("---")
    st.title("🤝 Grupos y Convenciones")
    
    st.info("Bienvenido a nuestra división de Grupos y Convenciones. Sabemos que detrás de cada gran evento hay una visión única y un sinfín de detalles. Por eso, nuestro propósito es convertir tus ideas en experiencias memorables y sin contratiempos. Desde la logística integral hasta la producción audiovisual más innovadora, ponemos a tu disposición un equipo de expertos y un catálogo 360º de soluciones. Tú imagina el evento perfecto; nosotros nos encargamos de hacerlo realidad.")
    
    st.divider()
    st.subheader("Explora nuestro catálogo de soluciones")
    st.write("Haz clic en cada categoría para descubrir todos los servicios que ofrecemos:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🏗️ Logística y Producción de Espacios"):
            st.markdown("""
            - Renta de recintos e inmuebles para eventos
            - Renta de vallas y carpas
            - Renta de mobiliario
            - Modelado y fabricación de stands
            - Creación y montaje de estructuras gráficas, escenografías y carros alegóricos
            - Servicios de contratación de oficios para montaje (plomero, carpintero, electricista, mecánico, albañil)
            """)
            
        with st.expander("🎨 Estrategia, Diseño y Reconocimientos"):
            st.markdown("""
            - Levantamiento de imagen corporativa
            - Servicio de diseño gráfico y consultoría de imagen
            - Servicio de impresión y creación de productos publicitarios
            - Venta de uniformes corporativos
            - Venta de trofeos, medallas, reconocimientos y placas conmemorativas
            """)
            
        with st.expander("🍽️ Gastronomía y Hospitalidad"):
            st.markdown("""
            - Servicio de catering especializado
            - Servicio de banquetera de alta calidad
            """)

    with col2:
        with st.expander("🎵 Tecnología, Audiovisual y Espectáculos"):
            st.markdown("""
            - Servicio integral de AVI (Audio, Video e Iluminación)
            - Espectáculos con drones programados
            - Servicios de pirotecnia y fuegos artificiales
            - Contratación de talento: grupos musicales, artistas, cómicos, DJ's y representaciones culturales
            """)
            
        with st.expander("🎯 Eventos y Actividades Especializadas"):
            st.markdown("""
            - Coordinación y logística integral
            - Eventos corporativos y académicos
            - Gestión y manejo de servicios integrales para campañas políticas
            - Programación de capacitación empresarial
            - Actividades recreativas: team building, campamentos, cursos de verano y olimpiadas
            - Servicio de arbitraje y jueceo para eventos deportivos
            """)

        with st.expander("🛡️ Seguridad y Cuidados Integrales"):
            st.markdown("""
            - Renta de servicios médicos, enfermeros y ambulancias
            - Servicios farmacéuticos para eventos
            - Logística y traslados seguros de obras de arte
            """)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Cotiza tu evento con nosotros 📅", use_container_width=True, type="primary"):
        st.success("¡Excelente decisión! Un asesor se pondrá en contacto contigo pronto.")


# =========================================================
# PANTALLA 4: CALL CENTER 24/7
# =========================================================
elif st.session_state.pantalla_actual == 'call_center':
    
    if st.button("⬅️ Regresar al Inicio"):
        st.session_state.pantalla_actual = 'inicio'
        st.rerun()
        
    st.markdown("---")
    st.title("📞 Call Center y Atención al Cliente")
    st.write("Estamos disponibles para ti las 24 horas, los 365 días del año.")
    
    st.subheader("Nuestros medios de contacto:")
    st.write("📞 **Teléfono Principal:** +52 55 5448 0500")
    st.write("✉️ **Correo Electrónico:** contacto@grupopremier.com")