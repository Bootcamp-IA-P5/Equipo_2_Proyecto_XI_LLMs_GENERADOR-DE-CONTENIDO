#!/bin/bash
# Script para ejecutar tests con diferentes opciones

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Test Runner para Content Generator${NC}\n"

case "$1" in
    unit)
        echo -e "${GREEN}Ejecutando tests unitarios...${NC}"
        python -m pytest tests/unit/ -v --no-cov
        ;;
    integration)
        echo -e "${GREEN}Ejecutando tests de integración...${NC}"
        python -m pytest tests/integration/ -v --no-cov
        ;;
    coverage)
        echo -e "${GREEN}Ejecutando tests con coverage...${NC}"
        python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
        echo -e "\n${BLUE}📊 Reporte HTML generado en: htmlcov/index.html${NC}"
        ;;
    fast)
        echo -e "${GREEN}Tests rápidos (sin coverage)...${NC}"
        python -m pytest tests/ -v --no-cov -x
        ;;
    watch)
        echo -e "${GREEN}Modo watch (requiere pytest-watch)...${NC}"
        ptw -- -v --no-cov
        ;;
    *)
        echo "Uso: ./run_tests.sh [unit|integration|coverage|fast|watch]"
        echo ""
        echo "Opciones:"
        echo "  unit        - Solo tests unitarios"
        echo "  integration - Solo tests de integración"
        echo "  coverage    - Todos los tests con coverage report"
        echo "  fast        - Tests rápidos (para en primer error)"
        echo "  watch       - Modo watch (ejecuta automáticamente)"
        echo ""
        echo "Sin argumentos, ejecuta todos los tests:"
        python -m pytest tests/ -v --cov=app --cov-report=term-missing
        ;;
esac
