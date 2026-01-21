# Testing con pytest

## 🚀 Inicio Rápido

### Usando el script helper
```bash
# Todos los tests con coverage
./run_tests.sh

# Solo unitarios
./run_tests.sh unit

# Solo integración
./run_tests.sh integration

# Tests rápidos (para en el primer error)
./run_tests.sh fast

# Con coverage detallado
./run_tests.sh coverage
```

## 📋 Comandos Directos

### Ejecutar todos los tests
```bash
cd backend
pytest
```

### Ejecutar tests por tipo
```bash
# Solo tests unitarios
pytest tests/unit/ -v

# Solo tests de integración
pytest tests/integration/ -m integration -v

# Tests E2E (cuando estén implementados)
pytest tests/e2e/ -m e2e -v
```

## 📊 Coverage

### Con reporte HTML
```bash
pytest --cov=app --cov-report=html

# Ver reporte en navegador
open htmlcov/index.html
```

### Con reporte en terminal
```bash
pytest --cov=app --cov-report=term-missing
```

## 🎯 Tests específicos

### Un archivo
```bash
pytest tests/unit/test_content_agent.py -v
```

### Una clase
```bash
pytest tests/unit/test_content_agent.py::TestContentAgent -v
```

### Un test específico
```bash
pytest tests/unit/test_content_agent.py::TestContentAgent::test_generate_basic_content -v
```

## 📈 Estado Actual

**✅ 21/21 tests passing**
- 16 tests unitarios
- 5 tests de integración
- 52% coverage del código

## 🛠️ Desarrollo

### Ejecutar en modo watch
```bash
pip install pytest-watch
./run_tests.sh watch
# o
ptw -- -v
```

### Tests rápidos durante desarrollo
```bash
# Para en el primer error
pytest -x -v

# Solo tests que fallaron la última vez
pytest --lf

# Tests modificados recientemente
pytest --testmon
```

## 🐛 Debugging

### Con output completo
```bash
pytest -vv -s
```

### Con pdb en fallos
```bash
pytest --pdb
```

### Solo warnings
```bash
pytest -v --tb=no -q
```
