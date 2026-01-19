# Guía de Contribución

¡Gracias por tu interés en contribuir al Generador de Contenido! Esta guía te ayudará a empezar.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Ejecutar Tests](#ejecutar-tests)
- [Reportar Bugs](#reportar-bugs)

## 🤝 Código de Conducta

Este proyecto sigue el [Contributor Covenant](https://www.contributor-covenant.org/). Al participar, se espera que mantengas un ambiente respetuoso y colaborativo.

## 💡 Cómo Contribuir

### Tipos de Contribuciones

- 🐛 **Bug Fixes**: Corregir errores identificados
- ✨ **Features**: Nuevas funcionalidades
- 📚 **Documentación**: Mejorar o ampliar docs
- 🧪 **Tests**: Añadir o mejorar cobertura de tests
- ⚡ **Performance**: Optimizaciones de rendimiento
- 🎨 **UI/UX**: Mejoras en la interfaz

### Workflow Básico

1. **Fork** el repositorio
2. **Clone** tu fork localmente
3. **Crea una rama** para tu feature/fix
4. **Realiza cambios** siguiendo los estándares
5. **Ejecuta tests** para validar
6. **Commit** con mensajes descriptivos
7. **Push** a tu fork
8. **Abre un PR** contra `main`

## 🛠 Configuración del Entorno

### Requisitos Previos

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Git

### Backend Setup

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus API keys

# Ejecutar tests
pytest
```

### Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build
```

### Docker Setup

```bash
# Construir y levantar servicios
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 📝 Estándares de Código

### Python (Backend)

#### Style Guide

- Seguir [PEP 8](https://pep8.org/)
- Máximo 120 caracteres por línea
- Usar type hints cuando sea posible
- Docstrings en formato Google

```python
def generate_content(
    topic: str,
    platform: str,
    audience: str = "general"
) -> dict:
    """
    Genera contenido adaptado a la plataforma.
    
    Args:
        topic: Tema del contenido
        platform: Plataforma objetivo (twitter, instagram, etc)
        audience: Audiencia objetivo
        
    Returns:
        dict: Contenido generado con metadata
        
    Raises:
        ValueError: Si el topic está vacío
    """
    pass
```

#### Linting

```bash
# Ejecutar flake8
flake8 app tests --max-line-length=120

# Auto-format con black
black app tests
```

### JavaScript/React (Frontend)

#### Style Guide

- Seguir [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Usar functional components con hooks
- Nombres descriptivos para componentes y funciones
- JSDoc para funciones complejas

```javascript
/**
 * Genera contenido mediante API
 * @param {Object} data - Datos del formulario
 * @param {string} data.topic - Tema del contenido
 * @param {string} data.platform - Plataforma objetivo
 * @returns {Promise<Object>} Contenido generado
 */
export const generateContent = async (data) => {
  // implementation
};
```

#### Linting

```bash
# Ejecutar ESLint
npm run lint

# Auto-fix
npm run lint -- --fix
```

## 🔄 Proceso de Pull Request

### Antes de Crear el PR

1. ✅ **Tests pasan**: `pytest` (backend) y `npm test` (frontend)
2. ✅ **Linting OK**: Sin errores de flake8 o ESLint
3. ✅ **Cobertura mantenida**: No reducir coverage actual
4. ✅ **Documentación actualizada**: Si añades features
5. ✅ **Commits limpios**: Rebase si es necesario

### Formato del PR

**Título**: `[Tipo] Descripción breve`

Tipos:
- `[Feature]` - Nueva funcionalidad
- `[Fix]` - Corrección de bug
- `[Docs]` - Cambios en documentación
- `[Test]` - Añadir o mejorar tests
- `[Refactor]` - Refactorización sin cambios funcionales
- `[Perf]` - Mejoras de performance

**Descripción**:
```markdown
## Descripción
Breve explicación de los cambios

## Tipo de Cambio
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests unitarios añadidos/actualizados
- [ ] Tests de integración ejecutados
- [ ] Testing manual realizado

## Checklist
- [ ] Mi código sigue el style guide
- [ ] He revisado mi propio código
- [ ] He comentado áreas complejas
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] Tests nuevos/existentes pasan localmente
- [ ] Coverage no ha disminuido

## Screenshots (si aplica)
```

### Revisión del PR

- Se requiere al menos **1 aprobación** de un maintainer
- CI/CD debe pasar (GitHub Actions)
- No merge conflicts con `main`
- Se utiliza **Squash and Merge** para mantener historial limpio

## 🧪 Ejecutar Tests

### Backend Tests

```bash
cd backend

# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Solo unit tests
pytest tests/unit/

# Solo integration tests
pytest tests/integration/

# Test específico
pytest tests/unit/test_content_agent.py -v

# Con debug output
pytest -vv --log-cli-level=INFO

# Modo watch (re-run al guardar)
pytest-watch
```

### Frontend Tests

```bash
cd frontend

# Ejecutar tests
npm test

# Con cobertura
npm test -- --coverage

# Modo watch
npm test -- --watch
```

### E2E Tests

```bash
# Levantar servicios
docker-compose up -d

# Ejecutar E2E tests
cd backend
pytest tests/e2e/

# Cleanup
docker-compose down
```

## 🐛 Reportar Bugs

### Antes de Reportar

1. Busca en [Issues existentes](https://github.com/tu-repo/issues)
2. Verifica que sea reproducible
3. Identifica la versión afectada

### Template de Bug Report

```markdown
## Descripción del Bug
Descripción clara del problema

## Pasos para Reproducir
1. Ir a '...'
2. Click en '...'
3. Scroll hasta '...'
4. Ver error

## Comportamiento Esperado
Qué debería ocurrir

## Comportamiento Actual
Qué ocurre realmente

## Screenshots
Si aplica, añadir screenshots

## Entorno
- OS: [e.g. macOS 13.0]
- Python: [e.g. 3.9.12]
- Node: [e.g. 18.16.0]
- Browser: [e.g. Chrome 120]

## Logs/Traceback
```python
# Pegar el traceback completo aquí
```

## Contexto Adicional
Cualquier otra información relevante
```

## 📚 Recursos Adicionales

- [README.md](./README.md) - Documentación general
- [Backend README](./backend/tests/README.md) - Guía de testing
- [API Documentation](http://localhost:8000/docs) - Swagger UI
- [Architecture Guide](./docs/ARCHITECTURE.md) - Diseño del sistema

## 🙋‍♀️ ¿Preguntas?

- **Issues**: Para bugs y feature requests
- **Discussions**: Para preguntas generales
- **Email**: equipo2@factoriaf5.org

---

**¡Gracias por contribuir!** 🎉

Cada contribución, por pequeña que sea, ayuda a mejorar este proyecto.
