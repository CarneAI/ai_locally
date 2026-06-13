#!/usr/bin/env python3
"""
🤖 MOTOR DE INTELIGENCIA ARTIFICIAL - SISTEMA COMPLETO DE RAZONAMIENTO
Versión 1.0 - Todo en un archivo

Sistema integrado de razonamiento lógico, memoria, decisiones, aprendizaje y NLP
Ejecutable directamente en terminal
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
import re
import sys

# ============================================================================
# 1. DEFINICIÓN DE TIPOS Y ESTRUCTURAS
# ============================================================================

class ThoughtType(Enum):
    """Tipos de pensamientos que puede generar la IA"""
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    DECISION = "decision"
    MEMORY_RECALL = "memory_recall"
    LEARNING = "learning"

@dataclass
class Thought:
    """Representación de un pensamiento individual"""
    thought_id: str
    content: str
    thought_type: ThoughtType
    confidence: float  # 0.0 - 1.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    related_thoughts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.thought_id,
            "content": self.content,
            "type": self.thought_type.value,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "related": self.related_thoughts
        }

@dataclass
class Memory:
    """Estructura de memoria a corto y largo plazo"""
    short_term: List[Thought] = field(default_factory=list)
    long_term: Dict[str, Any] = field(default_factory=dict)
    max_short_term = 10
    
    def add_short_term(self, thought: Thought):
        """Añade pensamiento a memoria corta plazo"""
        self.short_term.append(thought)
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)
    
    def save_long_term(self, key: str, value: Any):
        """Guarda información en memoria largo plazo"""
        self.long_term[key] = value
    
    def recall(self, query: str) -> List[Any]:
        """Recupera información de la memoria"""
        results = []
        for key, value in self.long_term.items():
            if query.lower() in key.lower():
                results.append(value)
        return results

@dataclass
class TextAnalysis:
    """Estructura para análisis de texto NLP"""
    original_text: str
    tokens: List[str]
    keywords: List[str]
    sentiment: float  # -1.0 a 1.0
    entities: List[Dict]
    intent: str

# ============================================================================
# 2. MOTOR DE RAZONAMIENTO LÓGICO
# ============================================================================

class ReasoningEngine:
    """Motor que implementa lógica de razonamiento deductivo e inductivo"""
    
    def __init__(self):
        self.thought_counter = 0
        self.reasoning_chain: List[Thought] = []
    
    def generate_thought_id(self) -> str:
        """Genera ID único para cada pensamiento"""
        self.thought_counter += 1
        return f"T{self.thought_counter:04d}"
    
    def deductive_reasoning(self, premises: List[str]) -> Thought:
        """
        Razonamiento deductivo: De lo general a lo particular
        Ejemplo: Si A implica B, y A es verdadero, entonces B es verdadero
        """
        reasoning_text = f"Razonamiento deductivo basado en: {'; '.join(premises)}"
        
        thought = Thought(
            thought_id=self.generate_thought_id(),
            content=reasoning_text,
            thought_type=ThoughtType.REASONING,
            confidence=0.85
        )
        self.reasoning_chain.append(thought)
        return thought
    
    def inductive_reasoning(self, observations: List[str]) -> Thought:
        """
        Razonamiento inductivo: De lo particular a lo general
        Encuentra patrones en observaciones
        """
        pattern_text = f"Patrón detectado en: {'; '.join(observations)}"
        
        # Calcula confianza basada en número de observaciones
        confidence = min(0.95, 0.5 + (len(observations) * 0.1))
        
        thought = Thought(
            thought_id=self.generate_thought_id(),
            content=pattern_text,
            thought_type=ThoughtType.REASONING,
            confidence=confidence
        )
        self.reasoning_chain.append(thought)
        return thought
    
    def abductive_reasoning(self, observation: str, possible_causes: List[str]) -> Thought:
        """
        Razonamiento abductivo: Encuentra la mejor explicación
        """
        best_cause = possible_causes[0] if possible_causes else "desconocido"
        conclusion = f"Observación: {observation} → Causa probable: {best_cause}"
        
        thought = Thought(
            thought_id=self.generate_thought_id(),
            content=conclusion,
            thought_type=ThoughtType.ANALYSIS,
            confidence=0.7
        )
        self.reasoning_chain.append(thought)
        return thought

# ============================================================================
# 3. MOTOR DE DECISIONES
# ============================================================================

class DecisionEngine:
    """Toma decisiones basadas en análisis de opciones"""
    
    def __init__(self):
        self.decision_history: List[Dict] = []
    
    def evaluate_options(self, options: Dict[str, List[Tuple[str, float]]]) -> str:
        """
        Evalúa múltiples opciones con pros/contras ponderados
        
        Args:
            options: {"opción": [("pro/contra", peso), ...]}
        
        Returns:
            Mejor opción
        """
        scores = {}
        
        for option, factors in options.items():
            score = sum(weight for _, weight in factors)
            scores[option] = score
        
        best_option = max(scores, key=scores.get)
        
        self.decision_history.append({
            "timestamp": datetime.now().isoformat(),
            "decision": best_option,
            "scores": scores
        })
        
        return best_option
    
    def risk_assessment(self, action: str, risk_factors: Dict[str, float]) -> float:
        """Calcula el nivel de riesgo de una acción"""
        total_risk = sum(risk_factors.values()) / len(risk_factors) if risk_factors else 0
        return min(1.0, total_risk)

# ============================================================================
# 4. MOTOR DE APRENDIZAJE
# ============================================================================

class LearningEngine:
    """Implementa aprendizaje a partir de experiencias"""
    
    def __init__(self):
        self.learned_patterns: Dict[str, Any] = {}
        self.experience_count = 0
    
    def learn_from_experience(self, context: str, outcome: str, success: bool):
        """Aprende de experiencias previas"""
        self.experience_count += 1
        
        key = f"exp_{self.experience_count}"
        self.learned_patterns[key] = {
            "context": context,
            "outcome": outcome,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
    
    def predict_outcome(self, context: str) -> Dict[str, Any]:
        """Predice resultado basado en experiencias previas"""
        similar_patterns = [
            p for k, p in self.learned_patterns.items()
            if context.lower() in p["context"].lower()
        ]
        
        if similar_patterns:
            success_rate = sum(1 for p in similar_patterns if p["success"]) / len(similar_patterns)
            return {
                "prediction": "probablemente exitoso" if success_rate > 0.5 else "probablemente fallará",
                "confidence": success_rate,
                "based_on": len(similar_patterns)
            }
        
        return {"prediction": "sin datos previos", "confidence": 0.0}

# ============================================================================
# 5. MOTOR DE PROCESAMIENTO DE LENGUAJE NATURAL (NLP)
# ============================================================================

class NLPEngine:
    """Motor de procesamiento de lenguaje natural"""
    
    def __init__(self):
        self.keyword_patterns = {
            "question": r".*\?$",
            "command": r"^(haz|hazme|crea|genera|muestra|dime|calcula|encuentra)",
            "greeting": r"^(hola|hi|buenos|buenas|saludos)",
            "goodbye": r"^(adiós|bye|hasta|salir)"
        }
    
    def tokenize(self, text: str) -> List[str]:
        """Divide el texto en tokens (palabras)"""
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens
    
    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extrae palabras clave del texto"""
        tokens = self.tokenize(text)
        
        # Palabras vacías comunes (stopwords)
        stopwords = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'es', 'por', 'con', 
                     'los', 'las', 'un', 'una', 'más', 'como', 'o', 'pero', 'si',
                     'para', 'al', 'del', 'su', 'no', 'esto', 'eso'}
        
        keywords = [t for t in tokens if t not in stopwords]
        return keywords[:max_keywords]
    
    def analyze_sentiment(self, text: str) -> float:
        """Analiza el sentimiento del texto (positivo/negativo)"""
        positive_words = {'bien', 'bueno', 'excelente', 'genial', 'perfecto', 'amor',
                         'maravilloso', 'fantástico', 'increíble', 'adorable'}
        negative_words = {'malo', 'horrible', 'terrible', 'odio', 'peor', 'problema',
                         'error', 'tristeza', 'triste', 'depresión'}
        
        tokens = set(self.tokenize(text))
        positive_count = len(tokens & positive_words)
        negative_count = len(tokens & negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        return (positive_count - negative_count) / total
    
    def detect_intent(self, text: str) -> str:
        """Detecta la intención del usuario"""
        for intent, pattern in self.keyword_patterns.items():
            if re.match(pattern, text, re.IGNORECASE):
                return intent
        return "general"
    
    def extract_entities(self, text: str) -> List[Dict]:
        """Extrae entidades nombradas (números, emails, URLs)"""
        entities = []
        
        # Buscar números
        numbers = re.findall(r"\d+", text)
        for num in numbers:
            entities.append({"type": "NUMBER", "value": num})
        
        # Buscar direcciones de email
        emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
        for email in emails:
            entities.append({"type": "EMAIL", "value": email})
        
        # Buscar URLs
        urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text)
        for url in urls:
            entities.append({"type": "URL", "value": url})
        
        return entities
    
    def analyze_text(self, text: str) -> TextAnalysis:
        """Análisis completo del texto"""
        return TextAnalysis(
            original_text=text,
            tokens=self.tokenize(text),
            keywords=self.extract_keywords(text),
            sentiment=self.analyze_sentiment(text),
            entities=self.extract_entities(text),
            intent=self.detect_intent(text)
        )
    
    def generate_response(self, analysis: TextAnalysis) -> str:
        """Genera respuesta basada en análisis"""
        intent = analysis.intent
        
        responses = {
            "greeting": "¡Hola! Bienvenido al motor de IA. ¿Cómo puedo ayudarte?",
            "goodbye": "¡Hasta pronto! Fue un placer conversar contigo.",
            "question": f"Pregunta detectada con palabras clave: {', '.join(analysis.keywords)}",
            "command": f"Comando detectado. Procesando: {' '.join(analysis.keywords)}",
            "general": f"Entendido. Analizando: {' '.join(analysis.keywords[:3])}"
        }
        
        return responses.get(intent, responses["general"])

# ============================================================================
# 6. IA PRINCIPAL - ORQUESTADOR
# ============================================================================

class ArtificialIntelligence:
    """Inteligencia Artificial - Orquestador principal"""
    
    def __init__(self, name: str = "AI_Assistant"):
        self.name = name
        self.reasoning = ReasoningEngine()
        self.decision = DecisionEngine()
        self.learning = LearningEngine()
        self.memory = Memory()
        self.nlp = NLPEngine()
        self.active = True
    
    def think(self, input_text: str) -> List[Thought]:
        """Proceso de pensamiento principal"""
        thoughts = []
        
        # 1. Análisis inicial
        analysis = Thought(
            thought_id=self.reasoning.generate_thought_id(),
            content=f"Analizando entrada: '{input_text}'",
            thought_type=ThoughtType.ANALYSIS,
            confidence=0.9
        )
        thoughts.append(analysis)
        self.memory.add_short_term(analysis)
        
        # 2. Razonamiento
        if "?" in input_text:
            reasoning = self.reasoning.inductive_reasoning([input_text])
            thoughts.append(reasoning)
            self.memory.add_short_term(reasoning)
        
        # 3. Recordar información relacionada
        memory_recall = self.memory.recall(input_text)
        if memory_recall:
            recall_thought = Thought(
                thought_id=self.reasoning.generate_thought_id(),
                content=f"Recuperada información relevante de memoria",
                thought_type=ThoughtType.MEMORY_RECALL,
                confidence=0.8
            )
            thoughts.append(recall_thought)
        
        return thoughts
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Procesa entrada del usuario y genera respuesta"""
        
        # Generar cadena de pensamientos
        thoughts = self.think(user_input)
        
        # Decidir acción
        options = {
            "responder_directamente": [("claridad", 0.8), ("velocidad", 0.9)],
            "buscar_más_información": [("precisión", 0.9), ("lentitud", -0.3)],
        }
        action = self.decision.evaluate_options(options)
        
        # Aprender de la interacción
        self.learning.learn_from_experience(
            context=user_input,
            outcome=action,
            success=True
        )
        
        # Preparar respuesta
        response = {
            "ai_name": self.name,
            "user_input": user_input,
            "thinking_process": [t.to_dict() for t in thoughts],
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    def display_thinking(self, response: Dict):
        """Muestra el proceso de pensamiento en terminal"""
        print(f"\n{'='*70}")
        print(f"🤖 {response['ai_name']} - Proceso de Pensamiento")
        print(f"{'='*70}")
        print(f"📥 Entrada: {response['user_input']}")
        print(f"\n🧠 Cadena de Pensamientos:")
        
        for i, thought in enumerate(response['thinking_process'], 1):
            print(f"\n   [{i}] {thought['type'].upper()}")
            print(f"       ID: {thought['id']}")
            print(f"       Contenido: {thought['content']}")
            print(f"       Confianza: {thought['confidence']:.2%}")
        
        print(f"\n✅ Acción Decidida: {response['action']}")
        print(f"{'='*70}\n")

# ============================================================================
# 7. INTERFAZ DE TERMINAL PRINCIPAL
# ============================================================================

def main():
    """Loop principal - Interfaz en Terminal"""
    ai = ArtificialIntelligence(name="AI_Reasoning_v1.0")
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║     🤖 MOTOR DE INTELIGENCIA ARTIFICIAL - SISTEMA COMPLETO     ║
    ║                                                                  ║
    ║  Sistema integrado de razonamiento lógico + procesamiento NLP    ║
    ║  Ejecutándose en terminal - Versión 1.0                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    📋 Comandos disponibles:
    ├─ Escribe normalmente para iniciar razonamiento
    ├─ 'analizar [texto]' - Análisis NLP detallado
    ├─ 'memoria' - Ver memoria de la IA
    ├─ 'aprendizaje' - Ver patrones aprendidos
    ├─ 'sentimiento [texto]' - Análisis de sentimiento
    ├─ 'salir' - Terminar programa
    └─ 'ayuda' - Mostrar esta información
    """)
    
    print("-" * 70 + "\n")
    
    while ai.active:
        try:
            user_input = input("🧠 Tú: ").strip()
            
            if not user_input:
                continue
            
            # Comandos especiales
            if user_input.lower() == "salir":
                print("\n👋 ¡Hasta luego! Sesión terminada.\n")
                ai.active = False
                break
            
            elif user_input.lower() == "ayuda":
                print("""
    📋 Comandos disponibles:
    ├─ Escribe normalmente para iniciar razonamiento
    ├─ 'analizar [texto]' - Análisis NLP detallado
    ├─ 'memoria' - Ver memoria de la IA
    ├─ 'aprendizaje' - Ver patrones aprendidos
    ├─ 'sentimiento [texto]' - Análisis de sentimiento
    ├─ 'salir' - Terminar programa
    └─ 'ayuda' - Mostrar esta información
                """)
                continue
            
            elif user_input.lower() == "memoria":
                print(f"\n📊 Memoria a Corto Plazo ({len(ai.memory.short_term)} items):")
                if ai.memory.short_term:
                    for i, thought in enumerate(ai.memory.short_term, 1):
                        print(f"   [{i}] {thought.content}")
                else:
                    print("   (vacía)")
                print()
                continue
            
            elif user_input.lower() == "aprendizaje":
                print(f"\n📚 Patrones Aprendidos ({ai.learning.experience_count} experiencias):")
                if ai.learning.learned_patterns:
                    for key, pattern in ai.learning.learned_patterns.items():
                        status = '✅' if pattern['success'] else '❌'
                        context_preview = pattern['context'][:40] + "..." if len(pattern['context']) > 40 else pattern['context']
                        print(f"   {key}: {status} {context_preview}")
                else:
                    print("   (sin datos)")
                print()
                continue
            
            elif user_input.lower().startswith("analizar "):
                text_to_analyze = user_input[9:]
                analysis = ai.nlp.analyze_text(text_to_analyze)
                
                print(f"\n📝 ANÁLISIS NLP:")
                print(f"   Intención: {analysis.intent.upper()}")
                print(f"   Palabras clave: {', '.join(analysis.keywords) or 'ninguna'}")
                print(f"   Sentimiento: {analysis.sentiment:+.2f}")
                print(f"   Entidades: {len(analysis.entities)} encontradas")
                if analysis.entities:
                    for entity in analysis.entities:
                        print(f"      - {entity['type']}: {entity['value']}")
                print()
                continue
            
            elif user_input.lower().startswith("sentimiento "):
                text_to_analyze = user_input[12:]
                sentiment = ai.nlp.analyze_sentiment(text_to_analyze)
                
                print(f"\n💬 ANÁLISIS DE SENTIMIENTO:")
                print(f"   Puntuación: {sentiment:+.2f}")
                if sentiment > 0.3:
                    print(f"   Tono: 😊 POSITIVO")
                elif sentiment < -0.3:
                    print(f"   Tono: 😞 NEGATIVO")
                else:
                    print(f"   Tono: 😐 NEUTRAL")
                print()
                continue
            
            # Procesamiento normal - Razonamiento + NLP
            print("\n🔄 Procesando...\n")
            
            # Análisis NLP
            nlp_analysis = ai.nlp.analyze_text(user_input)
            print(f"📊 Análisis NLP: {ai.nlp.generate_response(nlp_analysis)}\n")
            
            # Razonamiento de la IA
            response = ai.process_input(user_input)
            ai.display_thinking(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario.\n")
            ai.active = False
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
