import os
import sys

try:
    import anthropic
except ImportError:
    print("Error: no se encontró la librería 'anthropic'. Instala las dependencias con 'pip install -r requirements.txt'.")
    sys.exit(1)


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: debes definir la variable de entorno ANTHROPIC_API_KEY.")
        print("En Windows PowerShell:")
        print("  $env:ANTHROPIC_API_KEY = 'tu_api_key'\n  python test.py")
        return 1

    client = anthropic.Anthropic(api_key=api_key)

    print("Probando la API de Anthropic...")

    # Primero intentamos listar modelos si la librería lo soporta.
    if hasattr(client, "models") and hasattr(client.models, "list"):
        try:
            models = client.models.list()
            print("La API funciona. Modelos disponibles:")

            model_names = []
            if isinstance(models, dict):
                candidates = models.get("data") or models.get("models") or models.get("items") or []
            else:
                candidates = models

            if isinstance(candidates, list):
                for item in candidates:
                    if isinstance(item, dict) and "id" in item:
                        model_names.append(item["id"])
                    elif isinstance(item, dict) and "model" in item:
                        model_names.append(item["model"])
                    else:
                        model_names.append(str(item))

            if model_names:
                for name in model_names:
                    print(f"- {name}")
            else:
                print(models)

            print("\nSi la lista de modelos se devolvió sin errores, la conexión es correcta.")
            return 0
        except Exception as e:
            print(f"No se pudo listar modelos: {e}")
            print("Intentando una llamada de mensaje directa...\n")

    try:
        response = client.messages.create(
            model="claude-4",
            max_tokens=10,
            system="Eres un asistente de prueba.",
            messages=[{"role": "user", "content": "Hola"}]
        )
        print("La llamada a la API funcionó con el modelo 'claude-4'.")
        print("Respuesta básica:")
        print(response)
        return 0
    except Exception as e:
        print("Error al hacer la llamada de prueba a la API:")
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
