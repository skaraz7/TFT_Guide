# TFT Guide - Set 15 Project Plan

## 🎯 Objetivo
Crear una aplicación web completa para TFT Set 15 que proporcione composiciones meta, análisis profundo y comparativas de builds.

## 📋 Fases del Proyecto

### ✅ Fase 1: Recopilación de Datos Base (COMPLETADA)
- **Estado**: ✅ Completado
- **Descripción**: Obtención de datos oficiales de TFT Set 15
- **Fuente**: MetaTFT API (`https://data.metatft.com/lookups/TFTSet15_latest_en_us.json`)
- **Datos obtenidos**:
  - 79 campeones con costos, habilidades y sinergias
  - 237 objetos (básicos y combinados)
  - 151 sinergias con breakpoints y efectos
  - 359 aumentos hextech
- **Archivo**: `data_fetcher.py`

### 🔄 Fase 2: Base de Datos (EN PROGRESO)
- **Estado**: 🔄 Siguiente paso
- **Tecnología**: Firebase Firestore
- **Estructura de datos**:
  ```
  /champions/{championId}
  /items/{itemId}
  /traits/{traitId}
  /augments/{augmentId}
  /compositions/{compId}
  ```
- **Tareas**:
  - [ ] Configurar proyecto Firebase
  - [ ] Diseñar esquema de base de datos
  - [ ] Migrar datos parseados a Firestore
  - [ ] Crear índices para consultas optimizadas

### 🕷️ Fase 3: Web Scraping y Análisis Meta
- **Estado**: 📋 Planificado
- **Objetivo**: Obtener composiciones meta actuales y análisis de la comunidad
- **Fuentes objetivo**:
  - **MetaTFT.com**: Composiciones tier list
  - **TFTactics.gg**: Builds populares
  - **Reddit r/TeamfightTactics**: Análisis de comunidad
  - **Twitch/YouTube**: Builds de streamers
- **Tecnologías**:
  - Selenium para sitios con JavaScript
  - BeautifulSoup para parsing HTML
  - Requests para APIs públicas
- **Datos a extraer**:
  - Composiciones por tier (S, A, B, C, D)
  - Posicionamiento de campeones
  - Items recomendados por campeón
  - Estadísticas de winrate
  - Análisis de meta shifts

### 🔍 Fase 4: Análisis Profundo y Comparativas
- **Estado**: 📋 Planificado
- **Funcionalidades**:
  - **Comparador de composiciones**: Fortalezas/debilidades
  - **Análisis de sinergias**: Optimización de traits
  - **Recomendador de items**: Por campeón y situación
  - **Meta tracker**: Cambios en popularidad
  - **Simulador de matchups**: Predicción de resultados
- **Algoritmos**:
  - Sistema de scoring para composiciones
  - Análisis de contadores (rock-paper-scissors)
  - Machine learning para predicciones

### ⚛️ Fase 5: Frontend React
- **Estado**: 📋 Planificado
- **Tecnología**: React + TypeScript
- **Características**:
  - **Dashboard principal**: Overview del meta actual
  - **Explorador de composiciones**: Filtros por tier, costo, sinergias
  - **Builder interactivo**: Crear y testear builds
  - **Comparador**: Side-by-side de composiciones
  - **Guías detalladas**: Positioning, items, transiciones
  - **Responsive design**: Mobile-friendly
- **Componentes principales**:
  - ChampionGrid
  - CompositionCard
  - ItemBuilder
  - TraitCalculator
  - MetaAnalytics

### 🚀 Fase 6: Despliegue y Optimización
- **Estado**: 📋 Planificado
- **Hosting**: Vercel/Netlify para frontend
- **Backend**: Firebase Functions
- **Características**:
  - PWA (Progressive Web App)
  - Caché inteligente
  - Updates automáticos de datos
  - Analytics de uso

## 🛠️ Stack Tecnológico

### Backend
- **Base de datos**: Firebase Firestore
- **API**: Firebase Functions
- **Scraping**: Python (Selenium, BeautifulSoup)
- **Análisis**: Python (Pandas, NumPy)

### Frontend
- **Framework**: React + TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand/Redux Toolkit
- **Routing**: React Router
- **UI Components**: Headless UI

### DevOps
- **Version Control**: Git
- **CI/CD**: GitHub Actions
- **Hosting**: Vercel
- **Monitoring**: Firebase Analytics

## 📊 Métricas de Éxito
- **Datos**: >95% de composiciones meta cubiertas
- **Performance**: <2s tiempo de carga inicial
- **Actualización**: Datos actualizados cada 6 horas
- **Usabilidad**: Interfaz intuitiva y responsive
- **Precisión**: >90% accuracy en predicciones de meta

## 🗓️ Timeline Estimado
- **Fase 2**: 1 semana
- **Fase 3**: 2-3 semanas
- **Fase 4**: 2 semanas
- **Fase 5**: 3-4 semanas
- **Fase 6**: 1 semana

**Total estimado**: 9-11 semanas

## 📁 Estructura del Proyecto
```
TFT_Guide/
├── data/
│   ├── data_fetcher.py
│   └── scrapers/
├── backend/
│   ├── firebase/
│   └── analysis/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
└── PROJECT_PLAN.md
```