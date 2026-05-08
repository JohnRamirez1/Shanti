import streamlit as st
import anthropic
import json

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agente Ayurveda",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 { font-family: 'Cormorant Garamond', serif; }

.main { background: #FAFAF7; }
.block-container { padding-top: 2rem; max-width: 720px; }

.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid #E8E5DC;
    margin-bottom: 2rem;
}
.hero-logo {
    width: 64px; height: 64px;
    background: #E1F5EE;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem;
    font-size: 32px;
    border: 1px solid #9FE1CB;
}
.hero h1 { font-size: 2.2rem; color: #1a3a2a; margin-bottom: 0.3rem; font-weight: 600; }
.hero p { color: #6B7B6E; font-size: 0.95rem; }

.phase-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 14px; border-radius: 20px;
    font-size: 12px; font-weight: 500; margin-bottom: 1rem;
    letter-spacing: 0.04em;
}
.badge-prakriti { background: #E1F5EE; color: #085041; border: 1px solid #9FE1CB; }
.badge-vikriti  { background: #EEEDFE; color: #26215C; border: 1px solid #AFA9EC; }
.badge-dieta    { background: #FAEEDA; color: #412402; border: 1px solid #EF9F27; }

.question-card {
    background: white;
    border: 1px solid #E8E5DC;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.q-number { font-size: 11px; color: #9AA89D; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.q-text { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: #1a3a2a; margin-bottom: 1rem; line-height: 1.5; }
.progress-label { font-size: 12px; color: #6B7B6E; margin-bottom: 0.4rem; }

.result-box {
    background: white;
    border: 1px solid #E8E5DC;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
}
.dosha-vata  { border-left: 4px solid #534AB7; }
.dosha-pitta { border-left: 4px solid #D85A30; }
.dosha-kapha { border-left: 4px solid #1D9E75; }

.score-row { display: flex; justify-content: center; gap: 2rem; margin: 1rem 0; }
.score-item { text-align: center; }
.score-num { font-size: 2rem; font-weight: 600; font-family: 'Cormorant Garamond', serif; }
.score-lbl { font-size: 11px; color: #9AA89D; letter-spacing: 0.06em; }
.v-color { color: #534AB7; }
.p-color { color: #D85A30; }
.k-color { color: #1D9E75; }

.diet-section {
    background: white;
    border: 1px solid #E8E5DC;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.diet-section h3 { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: #1a3a2a; margin-bottom: 0.75rem; }

.recipe-card {
    background: #FAFAF7;
    border: 1px solid #E8E5DC;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.recipe-name { font-weight: 500; color: #1a3a2a; margin-bottom: 0.25rem; }
.recipe-desc { font-size: 13px; color: #6B7B6E; line-height: 1.5; }

.macro-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 1rem 0; }
.macro-card {
    background: #F5F3EE;
    border-radius: 10px;
    padding: 0.75rem;
    text-align: center;
}
.macro-val { font-size: 1.4rem; font-weight: 600; font-family: 'Cormorant Garamond', serif; color: #1a3a2a; }
.macro-lbl { font-size: 11px; color: #6B7B6E; }

.info-box {
    background: #E1F5EE;
    border: 1px solid #9FE1CB;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    font-size: 13px;
    color: #085041;
    margin: 0.75rem 0;
}
.warn-box {
    background: #FAEEDA;
    border: 1px solid #EF9F27;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    font-size: 13px;
    color: #412402;
    margin: 0.75rem 0;
}

.stButton > button {
    background: #1D9E75 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.5rem !important;
    width: 100%;
}
.stButton > button:hover { background: #0F6E56 !important; }

.btn-secondary > button {
    background: white !important;
    color: #1a3a2a !important;
    border: 1px solid #E8E5DC !important;
}
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border-color: #E8E5DC !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stRadio > div { gap: 0.5rem; }
.stRadio > div > label {
    background: white;
    border: 1px solid #E8E5DC;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: all 0.15s;
}
</style>
""", unsafe_allow_html=True)

# ─── KNOWLEDGE BASE ─────────────────────────────────────────────────────────────

PRAKRITI_QUESTIONS = [
    ("Generalmente soy rápido en mis actividades.", "P"),
    ("Ronco mientras duermo.", "V"),
    ("Mi piel está grasosa / húmeda.", "K"),
    ("Tengo venas prominentes en mi piel.", "V"),
    ("Mis cabellos son de color cobrizo.", "P"),
    ("Hablo continuamente sin interrupciones.", "V"),
    ("No puedo tolerar el clima cálido ni alimentos muy calientes.", "P"),
    ("La gente me considera de naturaleza gentil y amable.", "K"),
    ("Soy aventurero.", "P"),
    ("Cambio de amigos con frecuencia.", "V"),
    ("Me gusta perdonar.", "K"),
    ("Generalmente soy lento y constante en mis actividades.", "K"),
    ("Mi piel está seca.", "V"),
    ("No puedo tolerar el estrés mental.", "V"),
    ("Mis cabellos son de color negro.", "K"),
    ("Tengo tendencia a la enemistad fuerte / enemistad oculta.", "K"),
    ("Tengo una buena y duradera memoria.", "K"),
    ("Soy generoso con las personas leales.", "P"),
    ("Me tomo el tiempo para comprender las cosas.", "K"),
    ("Mis cabellos están rizados.", "P"),
    ("Soy propenso a tener úlceras en la boca con frecuencia.", "P"),
    ("Soy relativamente malo recordando eventos antiguos.", "V"),
    ("Tengo voz fuerte.", "P"),
    ("Generalmente soy rápido al iniciar actividades.", "V"),
    ("Tengo amistades estables.", "K"),
    ("Me gusta quejarme sin motivos aparentes.", "V"),
    ("Generalmente mi cuerpo está caliente.", "P"),
    ("Generalmente bebo líquidos con frecuencia.", "P"),
    ("A veces tengo tendencia a despertarme asustado/a.", "V"),
    ("A menudo caigo presa / cedo a mis tentaciones.", "V"),
    ("Generalmente estoy tranquilo y sereno.", "K"),
    ("La gente me admira como una persona valiente.", "P"),
    ("Generalmente no me enfermo fácilmente.", "K"),
    ("Tengo fuerza moderada.", "P"),
    ("Me enojo muy fácilmente pero también me calmo fácilmente.", "P"),
    ("Me gusta profundizar en los temas.", "P"),
    ("Mis decisiones son impredecibles.", "V"),
    ("Generalmente tengo hambre y como en grandes cantidades.", "P"),
    ("Tengo mucha fuerza.", "K"),
    ("Soy bueno en debates y argumentando.", "P"),
    ("Me valoran por mi temperamento científico.", "P"),
    ("Soy rápido para comprender las cosas.", "V"),
    ("Hablo habitualmente tras una intensa deliberación.", "K"),
    ("Mis ojos se enrojecen rápidamente al exponerme a la ira / licor / luz solar.", "P"),
    ("Tengo poca fuerza.", "V"),
    ("Mi voz es ronca (áspera) por naturaleza.", "V"),
    ("Generalmente duermo mucho tiempo.", "K"),
    ("Me gusta la música / los instrumentos musicales.", "K"),
    ("Soy implacable con las personas que compiten conmigo.", "P"),
    ("Generalmente camino despacio.", "K"),
    ("Generalmente bebo poco líquido y puedo soportar la sed durante un período prolongado.", "K"),
    ("Generalmente sudo mucho.", "P"),
    ("Tengo mucho vello corporal.", "K"),
    ("Soy justo y tengo un gran sentido del deber.", "K"),
    ("Me gustan los perfumes y me gusta decorar.", "P"),
    ("Mi voz es agradable y tranquilizadora.", "K"),
    ("Respeto a mis maestros y amigos.", "K"),
    ("Estoy contento con lo que tengo.", "K"),
    ("Generalmente mi sueño es superficial y corto.", "V"),
    ("Soy propenso a enfermedades frecuentes.", "V"),
    ("Se me conoce como una persona inteligente / hábil.", "P"),
    ("Soy muy bueno en lo académico.", "K"),
    ("Me gustan las actividades atrevidas como la caza.", "V"),
    ("Puedo soportar situaciones difíciles.", "K"),
    ("Tengo una tendencia a apegarme y desapegarme rápidamente en las relaciones.", "V"),
    ("Me siento cómodo con masajes con aceite y baño de vapor.", "V"),
    ("Me gustan los lujos y los placeres.", "V"),
    ("Generalmente camino rápido y puedo soportar largas caminatas.", "V"),
    ("Mi cuerpo está relativamente fresco o frío.", "K"),
    ("Mi comprensión de las situaciones es constante y estable.", "K"),
    ("Generalmente sudo poco.", "K"),
    ("Generalmente, mis deposiciones son fáciles de evacuar y blandas.", "P"),
    ("Me resulta difícil controlar mis celos / envidia.", "P"),
    ("Soy propenso a enojarme.", "V"),
    ("Se me parte muy fácil el pelo.", "V"),
    ("Generalmente olvido las cosas rápidamente.", "V"),
    ("Generalmente no puedo tolerar el frío y puedo sentirme triste frente a este clima.", "V"),
    ("Soy valiente y capaz de afrontar cualquier circunstancia.", "P"),
    ("Mis palmas y plantas están agrietadas.", "V"),
    ("Generalmente sudo con mal olor.", "P"),
    ("Por lo general, no me afecta ni me molesta omitir una comida.", "K"),
]

VIKRITI_QUESTIONS = [
    {
        "categoria": "Digestión: ¿Cómo se siente después de comer?",
        "opciones": {
            "V": "A veces con sueño, a veces activo",
            "P": "Muy activo",
            "K": "Con sueño, lento"
        }
    },
    {
        "categoria": "Peristaltsis: ¿Cómo son sus movimientos intestinales?",
        "opciones": {
            "V": "Se mueve mucho el intestino y suena",
            "P": "Antiperistaltsis: náusea, reflujo o agrieras",
            "K": "Muy lentos, no se siente el movimiento"
        }
    },
    {
        "categoria": "Hambre: ¿Cómo es su apetito?",
        "opciones": {
            "V": "Irregular, a veces mucha hambre, otras muy poca",
            "P": "Mucho apetito",
            "K": "Bajo apetito"
        }
    },
    {
        "categoria": "Comidas: ¿Cuántas veces come durante el día?",
        "opciones": {
            "V": "Como muchas veces, pico mucho",
            "P": "3 o más veces durante el día",
            "K": "1 o 2 al día"
        }
    },
    {
        "categoria": "Cantidad de comida",
        "opciones": {
            "V": "Irregular, a veces mucha, a veces muy poca",
            "P": "Mucha comida",
            "K": "Poca comida, se llena muy rápido"
        }
    },
    {
        "categoria": "Antojos: ¿Qué tipo de alimentos se le antoja comer?",
        "opciones": {
            "V": "Comida caliente, con especias, salado, seco",
            "P": "Comida dulce, amarga, astringente",
            "K": "Comida dulce, picante, estimulante (chocolate, té, café)"
        }
    },
    {
        "categoria": "¿Por qué pica comida entre comidas?",
        "opciones": {
            "V": "Por miedo o ansiedad",
            "P": "Cuando está concentrado resolviendo un problema",
            "K": "Cuando está triste o deprimido"
        }
    },
    {
        "categoria": "Sed",
        "opciones": {
            "V": "A veces mucha, a veces muy poca",
            "P": "Mucha sed, boca y garganta seca",
            "K": "Poca sed, la boca está húmeda"
        }
    },
    {
        "categoria": "Síntomas digestivos más comunes",
        "opciones": {
            "V": "Gases, distensión abdominal, dolor en zonas laterales",
            "P": "Ardor estomacal, náuseas, vómito, reflujo, agrieras",
            "K": "Sensación de llenura y pesadez"
        }
    },
    {
        "categoria": "Orina",
        "opciones": {
            "V": "Escasa, difícil evacuación, sin color",
            "P": "Abundante, amarilla o rojiza, se siente caliente al salir",
            "K": "Moderada, blanca como leche"
        }
    },
    {
        "categoria": "Sudor y olor corporal",
        "opciones": {
            "V": "Escaso sudor, sin olor",
            "P": "Abundante sudor, olor fuerte",
            "K": "Moderado sudor, frío, con olor agradable"
        }
    },
    {
        "categoria": "Evacuación y heces fecales",
        "opciones": {
            "V": "Estreñimiento: heces duras, como bolitas o de difícil evacuación",
            "P": "Heces abundantes y sueltas, tendencia a la diarrea",
            "K": "Heces moderadas, sólidas, 1-2 al día, en ocasiones con moco"
        }
    },
    {
        "categoria": "Gases",
        "opciones": {
            "V": "Hacen ruido al salir, mal olor, a veces no puede sacarlos",
            "P": "Salen calientes, olor ácido",
            "K": "Muy poco gas, no suenan, no huelen u olor dulce"
        }
    },
    {
        "categoria": "Boca",
        "opciones": {
            "V": "Seca",
            "P": "Sabor ácido o amargo",
            "K": "Húmeda y con mucha saliva"
        }
    },
    {
        "categoria": "Lengua",
        "opciones": {
            "V": "Seca, coloración hacia morado",
            "P": "Roja, puede tener coloración amarilla en la parte central",
            "K": "Toda la lengua blanca"
        }
    },
    {
        "categoria": "Aliento",
        "opciones": {
            "V": "Huele a lo que come",
            "P": "Ácido o metálico",
            "K": "Dulce como el de las manzanas"
        }
    },
    {
        "categoria": "Rostro",
        "opciones": {
            "V": "Poca grasa, arrugas notorias, se ve preocupado",
            "P": "Tendencia al acné, se ve enojado o con mirada crítica",
            "K": "Hinchado, pálido, se nota la papada"
        }
    },
    {
        "categoria": "Ojos",
        "opciones": {
            "V": "Ojeras evidentes oscuras",
            "P": "Rojos, sensibles a la luz, pican con facilidad",
            "K": "Hinchados con edema en los párpados"
        }
    },
    {
        "categoria": "Nivel de energía",
        "opciones": {
            "V": "Se cansa fácilmente",
            "P": "Se cansa si tiene hambre",
            "K": "Se cansa después de comer"
        }
    },
    {
        "categoria": "Naturaleza mental",
        "opciones": {
            "V": "Rápido, adaptable, indeciso",
            "P": "Inteligente, penetrante, crítico",
            "K": "Lento, firme, calmado"
        }
    },
    {
        "categoria": "Memoria",
        "opciones": {
            "V": "Se da cuenta rápido pero olvida fácilmente (mala memoria corto plazo)",
            "P": "Buena memoria a corto y largo plazo",
            "K": "Lento para captar, pero no olvida (buena memoria largo plazo)"
        }
    },
    {
        "categoria": "Emociones predominantes en los últimos meses",
        "opciones": {
            "V": "Miedo, ansiedad, nerviosismo, temblores, desarraigo",
            "P": "Ira, enojo, irritabilidad, tendencia a la discusión",
            "K": "Calma, apego sentimental, depresión, indiferencia, tristeza"
        }
    },
    {
        "categoria": "Sueño",
        "opciones": {
            "V": "Ligero, superficial, insomnio por preocupación (4-6 horas)",
            "P": "Moderado, puede despertarse en la madrugada (6-8 horas)",
            "K": "Pesado y profundo, le cuesta levantarse (8-10 horas)"
        }
    },
    {
        "categoria": "Actividad onírica (sueños)",
        "opciones": {
            "V": "Volar, movimiento, agitado, pesadillas",
            "P": "Sueña a color, conflictos, apasionados",
            "K": "Románticos, sentimentales, sueña con agua, sueña poco"
        }
    },
    {
        "categoria": "Enfermedades manifestadas en los últimos meses",
        "opciones": {
            "V": "Dolor, artritis, articulaciones que suenan, hemorroides, confusión mental",
            "P": "Fiebre, infecciones, inflamación, acné, eczema, úlceras, sangrados",
            "K": "Enfermedades respiratorias, gripa, tos, diabetes, colesterol alto, depresión"
        }
    },
    {
        "categoria": "Piel",
        "opciones": {
            "V": "Seca",
            "P": "Semi-grasa, con tendencia al acné, manchas rojas",
            "K": "Húmeda y grasa"
        }
    },
    {
        "categoria": "Peso",
        "opciones": {
            "V": "Tendencia a perder peso",
            "P": "Sube y baja fácilmente o se mantiene estable",
            "K": "Tendencia a ganar peso"
        }
    },
]

RECETAS = {
    "Vata": {
        "principios": "Alimentos calientes, húmedos, nutritivos y ligeramente oleosos. Sabores dulce, ácido y salado. Evitar alimentos fríos, crudos, secos y amargos.",
        "desayuno": [
            {"nombre": "Fruta especiada", "descripcion": "Fruta dulce (pera, manzana, mango, durazno) cocinada con ghee, canela, clavo, cardamomo y panela. Reconfortante y fácil de digerir."},
            {"nombre": "Rava Uthapam", "descripcion": "Tortilla de harina de maíz con yogurt, cubierta de cebolla, tomate, zanahoria y cilantro. Servir con chutney de tomate."}
        ],
        "almuerzo": [
            {"nombre": "Arroz de limón", "descripcion": "Arroz basmati con cúrcuma, mostaza negra, jengibre, marañones y zumo de limón. Nutritivo y digestivo."},
            {"nombre": "Raita de cohombro y zanahoria", "descripcion": "Yogurt con pepino, zanahoria, cebolla, tomate y Vata churna. Refrescante y probiótico."}
        ],
        "cena": [
            {"nombre": "Chapathi con Dal curry", "descripcion": "Pan integral de trigo acompañado de lentejas rojas con ghee, comino, cebolla, ajo, jengibre y cúrcuma."}
        ],
        "bebidas": [
            {"nombre": "Leche dorada", "descripcion": "Leche con ghee, cúrcuma, pimienta negra, nuez moscada, cardamomo y canela. Reconfortante nocturna."},
            {"nombre": "Té Vata", "descripcion": "Infusión de jengibre, comino y semillas de cilantro con miel o panela."}
        ],
        "postre": [
            {"nombre": "Kheer", "descripcion": "Arroz con leche especiado con cardamomo, panela y decorado con marañones y uvas pasas."}
        ],
        "churna": "Vata Churna: jengibre en polvo, ajo en polvo, comino, cilantro, pimienta negra, anís y sal. Usar para condimentar todas las comidas.",
        "evitar": ["Alimentos fríos o crudos", "Legumbres secas en exceso", "Cafeína", "Alimentos muy amargos o astringentes", "Ayunos prolongados"],
        "favorables": ["Arroz basmati", "Lentejas rojas", "Ghee", "Frutas dulces cocidas", "Jengibre", "Canela", "Cardamomo", "Aceite de sésamo"]
    },
    "Pitta": {
        "principios": "Alimentos frescos, dulces, amargos y astringentes. Evitar picantes, ácidos, salados en exceso y alimentos muy calientes. Priorizar alimentos refrescantes.",
        "desayuno": [
            {"nombre": "Dosa de frijol mungo", "descripcion": "Crepe de frijol mungo y arroz blanco fermentado con jengibre y cilantro. Servir con chutney de coco refrescante."},
            {"nombre": "Chutney de coco", "descripcion": "Coco rallado licuado con sal, agua, jengibre y cebolla, finalizado con semillas de mostaza en ghee."}
        ],
        "almuerzo": [
            {"nombre": "Jeera rice", "descripcion": "Arroz basmati con semillas de comino tostadas en ghee, decorado con hojas de cilantro. Digestivo y ligero."},
            {"nombre": "Palak paneer", "descripcion": "Espinaca con queso campesino, especias suaves (comino, cilantro, cúrcuma) y jengibre. Rico en hierro y proteína."}
        ],
        "cena": [
            {"nombre": "Crema de verdura dulce", "descripcion": "Crema de ahuyama o zanahoria con ghee, cebolla, jengibre, ajo y leche de coco. Suave y refrescante."}
        ],
        "bebidas": [
            {"nombre": "Mango lassi", "descripcion": "Yogurt con mango de azúcar y cardamomo. Refrescante y equilibrante del calor Pitta."},
            {"nombre": "Té Pitta", "descripcion": "Infusión de hinojo, comino y semillas de cilantro con miel. Refrescante digestivo."}
        ],
        "postre": [
            {"nombre": "Gajar ka halwa", "descripcion": "Zanahoria rallada cocinada en leche con ghee, panela y cardamomo, decorada con almendras y marañones."}
        ],
        "churna": "Pitta Churna: cúrcuma, comino, cilantro, hinojo, cardamomo, pimienta negra y canela. Usar moderadamente para condimentar.",
        "evitar": ["Alimentos picantes", "Frituras", "Alcohol", "Tomate, ají, pimentón en exceso", "Sal en exceso", "Alimentos muy ácidos", "Ayuno prolongado"],
        "favorables": ["Arroz basmati", "Frijol mungo", "Coco", "Mango", "Espinaca", "Ahuyama", "Zanahoria", "Ghee", "Cilantro", "Hinojo", "Menta"]
    },
    "Kapha": {
        "principios": "Alimentos ligeros, secos, calientes y estimulantes. Sabores picante, amargo y astringente. Evitar dulces pesados, lácteos en exceso, frituras y alimentos fríos.",
        "desayuno": [
            {"nombre": "Oats upma", "descripcion": "Avena tostada cocinada con aceite de girasol, mostaza negra, cebolla, jengibre, chili, zanahoria, arvejas y cúrcuma. Ligero y estimulante."}
        ],
        "almuerzo": [
            {"nombre": "Masala Khichdi", "descripcion": "Arroz basmati con lenteja rosada, verduras mixtas (zanahoria, arvejas, habichuelas) y especias completas (cardamomo, canela, clavo, comino). Nutritivo y digestivo."}
        ],
        "cena": [
            {"nombre": "Sambar", "descripcion": "Sopa de lentejas con tamarindo, verduras (zanahoria, habichuelas, berenjena, tomate) y especias. Ligero y depurativo para la noche."}
        ],
        "bebidas": [
            {"nombre": "Té Kapha", "descripcion": "Infusión de jengibre, clavos y canela con miel o panela. Estimulante y descongestionante."},
            {"nombre": "Té chai", "descripcion": "Té negro con leche, jengibre, cardamomo, canela y clavos. Solo en la mañana."}
        ],
        "postre": [
            {"nombre": "Kesari", "descripcion": "Harina de maíz precocida cocinada en agua con panela, ghee, marañones y uvas pasas. Postre ocasional y ligero."}
        ],
        "churna": "Kapha Churna: jengibre en polvo, comino, pimienta negra, canela y fenogreco. Usar generosamente para estimular la digestión.",
        "evitar": ["Lácteos en exceso (queso, helado, yogurt frío)", "Azúcar refinada", "Frituras", "Alimentos fríos o refrigerados", "Comer entre comidas", "Exceso de sal", "Trigo en exceso"],
        "favorables": ["Avena", "Cebada", "Lentejas", "Frijol mungo", "Verduras amargas (berenjena, rábano)", "Jengibre", "Pimienta negra", "Cúrcuma", "Miel (sin calentar)"]
    }
}

# ─── MACRONUTRIENT CALCULATOR ───────────────────────────────────────────────────

def calcular_macros(peso_kg, talla_cm, edad, sexo, actividad, dosha_desequilibrio):
    """Harris-Benedict + factor actividad + ajuste Ayurveda"""
    if sexo == "Femenino":
        tmb = 655.1 + (9.563 * peso_kg) + (1.850 * talla_cm) - (4.676 * edad)
    else:
        tmb = 66.47 + (13.75 * peso_kg) + (5.003 * talla_cm) - (6.755 * edad)

    factores = {
        "Sedentario": 1.2,
        "Actividad ligera": 1.375,
        "Actividad moderada": 1.55,
        "Actividad intensa": 1.725
    }
    calorias = tmb * factores.get(actividad, 1.375)

    ajustes = {
        "Vata":  {"prot": 0.20, "carb": 0.55, "gras": 0.25},
        "Pitta": {"prot": 0.22, "carb": 0.50, "gras": 0.28},
        "Kapha": {"prot": 0.25, "carb": 0.45, "gras": 0.30},
    }
    ratio = ajustes.get(dosha_desequilibrio, ajustes["Vata"])

    return {
        "calorias": round(calorias),
        "proteinas_g": round((calorias * ratio["prot"]) / 4),
        "carbohidratos_g": round((calorias * ratio["carb"]) / 4),
        "grasas_g": round((calorias * ratio["gras"]) / 9),
    }

# ─── CLAUDE AI HELPER ──────────────────────────────────────────────────────────

def llamar_claude(prompt, system_prompt):
    client = anthropic.Anthropic(api_key=st.session_state.api_key)
    modelos = [
        "claude-sonnet-4-5-20250514",
        "claude-opus-4-1-20250805",
    ]
    errores = []

    for modelo in modelos:
        try:
            msg = client.messages.create(
                model=modelo,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except Exception as e:
            error_text = str(e)
            errores.append(f"{modelo}: {error_text}")
            if "invalid_api_key" in error_text.lower() or "unauthorized" in error_text.lower():
                return f"Error: clave de API inválida o no autorizada. {error_text}"
            if "not_found_error" in error_text or "model:" in error_text:
                continue
            return f"Error: {error_text}"

    return ("Error: no se encontró un modelo Claude disponible con esta API key. "
            "Modelos intentados: " + ", ".join(modelos) + ". "
            "Detalles: " + " | ".join(errores))

def generar_diagnostico_prakriti(scores, nombre):
    short_to_full = {"V": "Vata", "P": "Pitta", "K": "Kapha"}
    dosha_max = short_to_full[max(scores, key=scores.get)]
    system = """Eres un experto en Ayurveda de la tradición del Ashtanga Hridayam. 
    Hablas en español. Eres empático, sabio y preciso. 
    Explica el dosha Prakriti del paciente de forma clara, inspiradora y personalizada.
    Máximo 150 palabras. No uses markdown pesado, solo texto natural."""
    prompt = f"""El paciente {nombre} completó el Test Prakriti con estos resultados:
    Vata: {scores['V']} respuestas
    Pitta: {scores['P']} respuestas  
    Kapha: {scores['K']} respuestas
    Dosha dominante: {dosha_max}
    
    Explica brevemente qué significa su constitución {dosha_max} y sus características principales."""
    return llamar_claude(prompt, system)

def generar_diagnostico_vikriti(scores_v, nombre, prakriti):
    short_to_full = {"V": "Vata", "P": "Pitta", "K": "Kapha"}
    dosha_deseq = short_to_full[max(scores_v, key=scores_v.get)]
    system = """Eres un experto en Ayurveda de la tradición del Ashtanga Hridayam.
    Hablas en español. Eres empático y claro.
    Explica el desequilibrio actual del paciente de forma comprensiva y motivadora.
    Máximo 150 palabras. Texto natural."""
    prompt = f"""Paciente: {nombre}
    Prakriti (constitución): {prakriti}
    Test Vikriti (últimos 3 meses):
    Vata: {scores_v['V']} síntomas
    Pitta: {scores_v['P']} síntomas
    Kapha: {scores_v['K']} síntomas
    Dosha desequilibrado: {dosha_deseq}
    
    Explica qué significa este desequilibrio {dosha_deseq} y por qué es importante tratarlo ahora."""
    return llamar_claude(prompt, system)

def generar_plan_dieta(nombre, prakriti, vikriti, macros, actividad, recetas_info):
    system = """Eres un experto en nutrición Ayurvédica basado en el Ashtanga Hridayam y la tradición clásica.
    Hablas en español. Creas planes alimenticios personalizados, prácticos y motivadores.
    Integras sabiduría Ayurvédica con nutrición moderna.
    Máximo 300 palabras. Texto claro y organizado."""
    prompt = f"""Crea un plan dietético personalizado para {nombre}:
    - Prakriti (constitución): {prakriti}
    - Vikriti (desequilibrio actual): {vikriti}
    - Actividad física: {actividad}
    - Calorías diarias recomendadas: {macros['calorias']} kcal
    - Proteínas: {macros['proteinas_g']}g | Carbohidratos: {macros['carbohidratos_g']}g | Grasas: {macros['grasas_g']}g
    
    Recetas disponibles del libro de cocina Ayurvédica para {vikriti}:
    {recetas_info}
    
    Crea:
    1. Un párrafo de orientación general personalizada
    2. Horarios de comida recomendados según el dosha
    3. 3 consejos Ayurvédicos específicos para equilibrar {vikriti}
    4. Reminder: repetir el Test Vikriti en 3 meses"""
    return llamar_claude(prompt, system)


def descripcion_prakriti_local(dosha):
    textos = {
        "Vata": "Tu constitución Vata es ligera, creativa y sensible. En Ayurveda, Vata se asocia con movimiento, creatividad y cambio. Mantener regularidad en las comidas, descanso y calor es clave para equilibrarlo.",
        "Pitta": "Tu constitución Pitta es intensa, decidida y metabólica. Pitta se asocia con fuego digestivo y claridad mental. Para mantener el equilibrio, favorece alimentos frescos, dulces y evita el exceso de picante y calor.",
        "Kapha": "Tu constitución Kapha es estable, fuerte y con buena resistencia. Kapha se relaciona con tierra y agua, dando estabilidad y calma. Para equilibrarlo, prioriza movimiento, ligereza y sabores cálidos y secos."
    }
    return textos.get(dosha, "Tu constitución ayurvédica se ha calculado correctamente.")


def descripcion_vikriti_local(dosha):
    textos = {
        "Vata": "Actualmente tu desequilibrio se acerca a Vata, lo que puede manifestarse como sequedad, inquietud y fatiga mental. Es importante nutrir con calor, rutinas estables y alimentos húmedos y nutritivos.",
        "Pitta": "Actualmente tu desequilibrio se acerca a Pitta, lo que puede manifestarse como irritabilidad, acidez o inflamación. Apunta a enfriar, calmar y balancear con alimentos dulces, amargos y refrescantes.",
        "Kapha": "Actualmente tu desequilibrio se acerca a Kapha, lo que puede manifestarse como pesadez, letargo o congestión. Busca movimiento, comidas ligeras y especias que estimulen la digestión para recuperar el balance."
    }
    return textos.get(dosha, "Tu desequilibrio actual se ha calculado correctamente.")

# ─── SESSION STATE ─────────────────────────────────────────────────────────────

defaults = {
    "step": "inicio",
    "paciente": {},
    "prakriti_idx": 0,
    "prakriti_scores": {"V": 0, "P": 0, "K": 0},
    "prakriti_resultado": "",
    "prakriti_dosha": "",
    "vikriti_idx": 0,
    "vikriti_scores": {"V": 0, "P": 0, "K": 0},
    "vikriti_resultado": "",
    "vikriti_dosha": "",
    "dieta_generada": "",
    "api_key": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HEADER ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <div class="hero-logo">🌿</div>
  <h1>Agente Ayurveda</h1>
  <p>Diagnóstico de dosha · Plan alimenticio personalizado</p>
</div>
""", unsafe_allow_html=True)

# ─── STEP: INICIO / REGISTRO ───────────────────────────────────────────────────

if st.session_state.step == "inicio":
    st.markdown("### Registro del paciente")

    with st.form("registro"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo")
            edad = st.number_input("Edad", min_value=10, max_value=100, value=30, step=1)
            sexo = st.selectbox("Sexo biológico", ["Femenino", "Masculino"])
        with col2:
            peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=65.0, step=0.5)
            talla = st.number_input("Estatura (cm)", min_value=100.0, max_value=220.0, value=165.0, step=0.5)
            actividad = st.selectbox("Nivel de actividad física", [
                "Sedentario", "Actividad ligera", "Actividad moderada", "Actividad intensa"
            ])
        enviado = st.form_submit_button("Comenzar diagnóstico Ayurveda 🌿")

    if enviado:
        if not nombre:
            st.error("Por favor completa tu nombre para continuar.")
        else:
            st.session_state.paciente = {
                "nombre": nombre, "edad": int(edad), "sexo": sexo,
                "peso": peso, "talla": talla, "actividad": actividad
            }
            st.session_state.step = "prakriti"
            st.rerun()

    st.markdown("""
    <div class="info-box">
        <strong>¿Cómo funciona?</strong><br>
        1. Registro de datos personales<br>
        2. Test Prakriti — tu constitución de nacimiento (se realiza una sola vez)<br>
        3. Test Vikriti — tu desequilibrio actual (se recomienda cada 3 meses)<br>
        4. Luego ingresarás tu API Key para obtener las recomendaciones del agente Ayurveda
    </div>
    """, unsafe_allow_html=True)

# ─── STEP: TEST PRAKRITI ───────────────────────────────────────────────────────

elif st.session_state.step == "prakriti":
    nombre = st.session_state.paciente["nombre"]
    total = len(PRAKRITI_QUESTIONS)
    idx = st.session_state.prakriti_idx

    st.markdown('<span class="phase-badge badge-prakriti">🌱 Test Prakriti — Constitución de nacimiento</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-label">Afirmación {idx+1} de {total}</div>', unsafe_allow_html=True)
    st.progress((idx) / total)

    pregunta, dosha = PRAKRITI_QUESTIONS[idx]

    st.markdown(f"""
    <div class="question-card">
        <div class="q-number">AFIRMACIÓN {idx+1} DE {total}</div>
        <div class="q-text">"{pregunta}"</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓ Sí, me identifica"):
            st.session_state.prakriti_scores[dosha] += 1
            if idx + 1 >= total:
                st.session_state.step = "resultado_prakriti"
            else:
                st.session_state.prakriti_idx += 1
            st.rerun()
    with col2:
        if st.button("✗ No me identifica"):
            if idx + 1 >= total:
                st.session_state.step = "resultado_prakriti"
            else:
                st.session_state.prakriti_idx += 1
            st.rerun()

    scores = st.session_state.prakriti_scores
    st.markdown(f"""
    <div style="display:flex;gap:1rem;justify-content:center;margin-top:1rem">
        <span class="v-color" style="font-size:13px">Vata: <strong>{scores['V']}</strong></span>
        <span class="p-color" style="font-size:13px">Pitta: <strong>{scores['P']}</strong></span>
        <span class="k-color" style="font-size:13px">Kapha: <strong>{scores['K']}</strong></span>
    </div>
    """, unsafe_allow_html=True)

# ─── STEP: RESULTADO PRAKRITI ──────────────────────────────────────────────────

elif st.session_state.step == "resultado_prakriti":
    scores = st.session_state.prakriti_scores
    short_to_full = {"V": "Vata", "P": "Pitta", "K": "Kapha"}
    dosha_max = short_to_full[max(scores, key=scores.get)]
    nombre = st.session_state.paciente["nombre"]
    st.session_state.prakriti_dosha = dosha_max

    colores = {"Vata": "#534AB7", "Pitta": "#D85A30", "Kapha": "#1D9E75"}
    emojis  = {"Vata": "🌬️", "Pitta": "🔥", "Kapha": "🌊"}
    clase   = {"Vata": "dosha-vata", "Pitta": "dosha-pitta", "Kapha": "dosha-kapha"}

    st.markdown(f'<span class="phase-badge badge-prakriti">🌱 Resultado Prakriti</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-box {clase[dosha_max]}">
        <div style="font-size:2.5rem">{emojis[dosha_max]}</div>
        <h2 style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:#1a3a2a;margin:0.5rem 0">
            Tu constitución es <span style="color:{colores[dosha_max]}">{dosha_max}</span>
        </h2>
        <div class="score-row">
            <div class="score-item"><div class="score-num v-color">{scores['V']}</div><div class="score-lbl">VATA</div></div>
            <div class="score-item"><div class="score-num p-color">{scores['P']}</div><div class="score-lbl">PITTA</div></div>
            <div class="score-item"><div class="score-num k-color">{scores['K']}</div><div class="score-lbl">KAPHA</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.prakriti_resultado:
        st.session_state.prakriti_resultado = descripcion_prakriti_local(dosha_max)

    st.markdown(f"""
    <div class="diet-section">
        <h3>Interpretación de tu Prakriti</h3>
        <p style="color:var(--color-text-secondary);line-height:1.7">{st.session_state.prakriti_resultado}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Tu Prakriti es tu constitución de nacimiento y no cambia. 
        Ahora realizaremos el Test Vikriti para identificar tu desequilibrio actual.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Continuar con Test Vikriti →"):
        st.session_state.step = "vikriti"
        st.rerun()

# ─── STEP: TEST VIKRITI ────────────────────────────────────────────────────────

elif st.session_state.step == "vikriti":
    total = len(VIKRITI_QUESTIONS)
    idx = st.session_state.vikriti_idx

    st.markdown('<span class="phase-badge badge-vikriti">💜 Test Vikriti — Desequilibrio actual (últimos 3 meses)</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-label">Pregunta {idx+1} de {total}</div>', unsafe_allow_html=True)
    st.progress(idx / total)

    q = VIKRITI_QUESTIONS[idx]

    st.markdown(f"""
    <div class="question-card">
        <div class="q-number">PREGUNTA {idx+1} DE {total}</div>
        <div class="q-text">{q['categoria']}</div>
    </div>
    """, unsafe_allow_html=True)

    opciones_display = {v: f"{k} — {v}" for k, v in q["opciones"].items()}
    opciones_keys = list(q["opciones"].values())
    seleccion = st.radio("Selecciona la opción que más te describe:", opciones_keys, key=f"vikriti_{idx}", label_visibility="collapsed")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Siguiente →", key=f"btn_v_{idx}"):
            dosha_sel = [k for k, v in q["opciones"].items() if v == seleccion][0]
            st.session_state.vikriti_scores[dosha_sel] += 1
            if idx + 1 >= total:
                st.session_state.step = "resultado_vikriti"
            else:
                st.session_state.vikriti_idx += 1
            st.rerun()

    scores = st.session_state.vikriti_scores
    st.markdown(f"""
    <div style="display:flex;gap:1rem;justify-content:center;margin-top:1rem">
        <span class="v-color" style="font-size:13px">Vata: <strong>{scores['V']}</strong></span>
        <span class="p-color" style="font-size:13px">Pitta: <strong>{scores['P']}</strong></span>
        <span class="k-color" style="font-size:13px">Kapha: <strong>{scores['K']}</strong></span>
    </div>
    """, unsafe_allow_html=True)

# ─── STEP: RESULTADO VIKRITI ───────────────────────────────────────────────────

elif st.session_state.step == "resultado_vikriti":
    scores_v = st.session_state.vikriti_scores
    short_to_full = {"V": "Vata", "P": "Pitta", "K": "Kapha"}
    dosha_deseq = short_to_full[max(scores_v, key=scores_v.get)]
    nombre = st.session_state.paciente["nombre"]
    prakriti = st.session_state.prakriti_dosha
    st.session_state.vikriti_dosha = dosha_deseq

    colores = {"Vata": "#534AB7", "Pitta": "#D85A30", "Kapha": "#1D9E75"}
    emojis  = {"Vata": "🌬️", "Pitta": "🔥", "Kapha": "🌊"}
    clase   = {"Vata": "dosha-vata", "Pitta": "dosha-pitta", "Kapha": "dosha-kapha"}

    st.markdown('<span class="phase-badge badge-vikriti">💜 Resultado Vikriti</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-box {clase[dosha_deseq]}">
        <div style="font-size:2.5rem">{emojis[dosha_deseq]}</div>
        <h2 style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:#1a3a2a;margin:0.5rem 0">
            Desequilibrio actual: <span style="color:{colores[dosha_deseq]}">{dosha_deseq}</span>
        </h2>
        <div class="score-row">
            <div class="score-item"><div class="score-num v-color">{scores_v['V']}</div><div class="score-lbl">VATA</div></div>
            <div class="score-item"><div class="score-num p-color">{scores_v['P']}</div><div class="score-lbl">PITTA</div></div>
            <div class="score-item"><div class="score-num k-color">{scores_v['K']}</div><div class="score-lbl">KAPHA</div></div>
        </div>
        <p style="font-size:13px;color:#6B7B6E;margin-top:0.5rem">Prakriti: {prakriti} · Vikriti: {dosha_deseq}</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.vikriti_resultado:
        st.session_state.vikriti_resultado = descripcion_vikriti_local(dosha_deseq)

    st.markdown(f"""
    <div class="diet-section">
        <h3>Interpretación de tu Vikriti</h3>
        <p style="color:var(--color-text-secondary);line-height:1.7">{st.session_state.vikriti_resultado}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
        El Test Vikriti debe repetirse cada 3 meses ya que tu desequilibrio puede cambiar con las estaciones, 
        el estrés, la alimentación y otros factores de vida.
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.markdown("""
        <div class="info-box">
            Para generar tus recomendaciones personalizadas necesitas ingresar tu API Key de Anthropic Claude.
        </div>
        """, unsafe_allow_html=True)
        api_key_input = st.text_input("API Key de Anthropic (Claude)", type="password",
                                      help="Obtén tu key en console.anthropic.com")
        if st.button("Guardar API Key y generar plan"):
            if api_key_input:
                st.session_state.api_key = api_key_input
                st.session_state.step = "dieta"
                st.rerun()
            else:
                st.error("Por favor ingresa tu API Key para continuar.")
    else:
        if st.button("Generar mi plan alimenticio personalizado 🌿"):
            st.session_state.step = "dieta"
            st.rerun()

# ─── STEP: DIETA ───────────────────────────────────────────────────────────────

elif st.session_state.step == "dieta":
    p = st.session_state.paciente
    prakriti = st.session_state.prakriti_dosha
    vikriti = st.session_state.vikriti_dosha
    recetas = RECETAS[vikriti]

    macros = calcular_macros(
        p["peso"], p["talla"], p["edad"],
        p["sexo"], p["actividad"], vikriti
    )

    st.markdown('<span class="phase-badge badge-dieta">🍃 Tu plan alimenticio Ayurvédico personalizado</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-box">
        <h2 style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#1a3a2a">
            Plan para {p['nombre']}
        </h2>
        <p style="color:#6B7B6E;font-size:13px">
            Prakriti: <strong>{prakriti}</strong> · 
            Vikriti: <strong>{vikriti}</strong> · 
            Actividad: <strong>{p['actividad']}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Macros
    st.markdown("""
    <div class="diet-section">
        <h3>Requerimientos nutricionales diarios</h3>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="macro-grid">
        <div class="macro-card">
            <div class="macro-val">{macros['calorias']}</div>
            <div class="macro-lbl">Calorías (kcal)</div>
        </div>
        <div class="macro-card">
            <div class="macro-val">{macros['proteinas_g']}g</div>
            <div class="macro-lbl">Proteínas</div>
        </div>
        <div class="macro-card">
            <div class="macro-val">{macros['carbohidratos_g']}g</div>
            <div class="macro-lbl">Carbohidratos</div>
        </div>
    </div>
    <div class="macro-grid" style="grid-template-columns:1fr 2fr">
        <div class="macro-card">
            <div class="macro-val">{macros['grasas_g']}g</div>
            <div class="macro-lbl">Grasas saludables</div>
        </div>
        <div class="macro-card" style="text-align:left;padding-left:1rem">
            <div style="font-size:12px;color:#6B7B6E">Distribución Ayurvédica para <strong>{vikriti}</strong></div>
            <div style="font-size:13px;color:#1a3a2a;margin-top:4px">
                Proteínas · Grasas saludables · Carbohidratos complejos
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Principios
    st.markdown(f"""
    <div class="diet-section">
        <h3>Principios dietéticos para equilibrar {vikriti}</h3>
        <p style="color:var(--color-text-secondary);line-height:1.7">{recetas['principios']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Recetas
    for seccion, titulo, icono in [
        ("desayuno", "Desayuno", "🌅"),
        ("almuerzo", "Almuerzo", "☀️"),
        ("cena", "Cena", "🌙"),
        ("bebidas", "Bebidas medicinales", "🍵"),
        ("postre", "Postre ocasional", "🍯"),
    ]:
        st.markdown(f"""
        <div class="diet-section">
            <h3>{icono} {titulo}</h3>
        """, unsafe_allow_html=True)
        for r in recetas[seccion]:
            st.markdown(f"""
            <div class="recipe-card">
                <div class="recipe-name">{r['nombre']}</div>
                <div class="recipe-desc">{r['descripcion']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Churna
    st.markdown(f"""
    <div class="diet-section">
        <h3>✨ Tu mezcla de especias (Churna)</h3>
        <p style="color:var(--color-text-secondary);line-height:1.7">{recetas['churna']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Favorables y a evitar
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='diet-section'><h3>✓ Alimentos favorables</h3>", unsafe_allow_html=True)
        for a in recetas["favorables"]:
            st.markdown(f"<div style='font-size:13px;color:#085041;padding:3px 0'>• {a}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='diet-section'><h3>✗ Alimentos a evitar</h3>", unsafe_allow_html=True)
        for a in recetas["evitar"]:
            st.markdown(f"<div style='font-size:13px;color:#791F1F;padding:3px 0'>• {a}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Plan personalizado con IA
    if not st.session_state.dieta_generada:
        with st.spinner("El agente Ayurveda está creando tu plan personalizado..."):
            recetas_info = f"Desayuno: {[r['nombre'] for r in recetas['desayuno']]}. Almuerzo: {[r['nombre'] for r in recetas['almuerzo']]}. Cena: {[r['nombre'] for r in recetas['cena']]}."
            plan = generar_plan_dieta(
                p["nombre"], prakriti, vikriti, macros, p["actividad"], recetas_info
            )
            st.session_state.dieta_generada = plan

    if st.session_state.dieta_generada:
        st.markdown(f"""
        <div class="diet-section">
            <h3>📋 Plan personalizado — Recomendaciones del agente Ayurveda</h3>
            <p style="color:var(--color-text-secondary);line-height:1.8">{st.session_state.dieta_generada}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
        <strong>Recordatorio importante:</strong> El Test Vikriti debe repetirse cada 3 meses 
        para actualizar tu plan alimenticio. Tu desequilibrio puede cambiar con las estaciones del año, 
        el estrés, los cambios de vida y otros factores.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong>Descargo de responsabilidad:</strong> Este plan es una guía Ayurvédica personalizada 
        y no reemplaza la consulta con un médico o especialista en Ayurveda certificado.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Repetir Test Vikriti (cada 3 meses)"):
        st.session_state.vikriti_idx = 0
        st.session_state.vikriti_scores = {"V": 0, "P": 0, "K": 0}
        st.session_state.vikriti_resultado = ""
        st.session_state.vikriti_dosha = ""
        st.session_state.dieta_generada = ""
        st.session_state.step = "vikriti"
        st.rerun()

    if st.button("🏠 Nuevo paciente"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

