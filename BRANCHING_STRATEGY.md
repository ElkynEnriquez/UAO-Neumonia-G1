# Estrategia de Ramas - UAO Neumonía G1

## Resumen Ejecutivo
Este proyecto utiliza un flujo de 3 ramas (GitFlow simplificado):
- **`dev`**: integración y desarrollo activo
- **`uat`**: pruebas de aceptación del usuario
- **`main`**: producción (siempre desplegable)

---

## Jerarquía y Flujo de Promotions

```
feature branches
      ↓
    dev  ← Integración diaria
      ↓ (cuando está listo)
    uat  ← Pruebas formales (UAT)
      ↓ (si UAT aprueba)
    main ← Producción (releases)
```

### Interpretación:
1. Los desarrolladores crean ramas de feature desde `dev` y hacen PR hacia `dev`.
2. Cuando hay un conjunto de features listo, se promueve `dev` → `uat` para pruebas de aceptación.
3. Si UAT aprueba, se fusiona `uat` → `main` y se desplega a producción.
4. `main` siempre representa lo que está en producción.

---

## Descripción de Cada Rama

### `dev` (Desarrollo)
- **Propósito**: Rama de integración continua para desarrollo.
- **Base**: Originada de `main`.
- **Quién escribe**: Desarrolladores (vía PRs desde feature branches).
- **Protección**: Requiere PR y al menos 1 revisión.
- **Actualización**: 
  - Diaria o según merges de features.
  - Ocasionalmente: sincroniza desde `main` si hay hotfixes.
- **Uso**:
  ```bash
  git checkout -b feature/login-page dev
  # ... haz cambios ...
  git push -u origin feature/login-page
  # Luego: crear PR en GitHub (feature/login-page → dev)
  ```

### `uat` (User Acceptance Testing)
- **Propósito**: Rama de pruebas formales antes de producción.
- **Base**: Promocionada desde `dev` cuando hay un candidate de release.
- **Quién escribe**: Gerente de release o DevOps (vía PR controlado).
- **Protección**: Requiere PR, mínimo 2 revisiones, CI verde.
- **Actualización**: 
  - Semanal o según el ciclo de sprints.
  - Se fusiona desde `dev` con merge commit (`--no-ff`).
- **Uso**:
  ```bash
  # Desde main o dev, crear PR: dev → uat
  git checkout uat
  git pull origin uat
  git merge --no-ff origin/dev
  git push origin uat
  ```

### `main` (Producción)
- **Propósito**: Rama de producción. Lo que está aquí está desplegado.
- **Base**: Siempre estable.
- **Quién escribe**: Solo gerente de release o DevOps (vía PR).
- **Protección**: 
  - Requiere PR, mínimo 2 revisiones.
  - CI checks deben pasar (si aplica).
  - No se permite push directo.
- **Actualización**: 
  - Después de que UAT aprueba (merge `uat` → `main`).
  - Crear tag de release: `git tag -a v1.0.0 -m "Release v1.0.0"`.
- **Despliegue**: Se dispara automáticamente o manual desde `main` a producción.
- **Sincronización inversa**: Si hay hotfixes en `main`, volver a merguear a `dev` para mantener en sync.

---

## Flujo Completo de Trabajo

### 1️⃣ Desarrollo (feature → `dev`)
```bash
# Crear feature desde dev
git checkout dev
git pull origin dev
git checkout -b feature/mi-funcionalidad

# Hacer commits
git add .
git commit -m "feat: agregar funcionalidad X"

# Subir y crear PR
git push -u origin feature/mi-funcionalidad
# En GitHub: PR feature/mi-funcionalidad → dev (esperar revisión)
```

### 2️⃣ Integración en `dev`
```bash
# Revisor aprueba y mergea PR en GitHub
# Luego, actualizar dev localmente:
git checkout dev
git pull origin dev
```

### 3️⃣ Promover `dev` → `uat` (Gerente de Release)
```bash
# Cuando hay un conjunto de features listos para UAT
git fetch origin

git checkout uat
git pull origin uat

# Mergear dev en uat (preservar historial con --no-ff)
git merge --no-ff origin/dev -m "Merge dev into uat: release candidate X"

git push origin uat

# (Opcional) crear tag candidato
git tag -a rc-1.0.0 -m "Release Candidate 1.0.0"
git push origin rc-1.0.0
```

### 4️⃣ Pruebas en `uat`
- El equipo QA/UAT prueba en el environment de UAT (desplegado desde rama `uat`).
- Si hay bugs: arreglar en feature branch desde `dev`, mergear a `dev`, luego sincronizar `uat`.
- Si todo está ok: aprobar para producción.

### 5️⃣ Promover `uat` → `main` (Gerente de Release)
```bash
# Una vez UAT aprueba
git fetch origin

git checkout main
git pull origin main

# Mergear uat en main
git merge --no-ff origin/uat -m "Merge uat into main: Release v1.0.0"

git push origin main

# Crear tag de release formal
git tag -a v1.0.0 -m "Release v1.0.0 - production"
git push origin v1.0.0
```

### 6️⃣ Despliegue a Producción
```bash
# Desplegar desde main (manual o automático vía CI/CD)
git checkout main
git pull origin main
# ... ejecutar scripts de deploy ...
```

### 7️⃣ Hotfixes (Emergencias en Producción)
```bash
# Si hay un bug urgente en main
git checkout -b hotfix/critico main

# Arreglar bug
git add .
git commit -m "hotfix: corregir X"

# PR hotfix → main
git push -u origin hotfix/critico
# (En GitHub: PR hotfix/critico → main, esperar revisión rápida)

# Una vez merged en main, sincronizar dev y uat
git checkout dev
git pull origin dev
git merge origin/main
git push origin dev

git checkout uat
git pull origin uat
git merge origin/main
git push origin uat
```

---

## Protecciones en GitHub (Recomendadas)

### Para `main`:
- ✅ Require pull request reviews before merging (2 reviews mínimo)
- ✅ Require status checks to pass before merging (si hay CI)
- ✅ Require branches to be up to date before merging
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ❌ Allow force pushes: deshabilitado
- ❌ Allow deletions: deshabilitado

### Para `uat`:
- ✅ Require pull request reviews before merging (1-2 reviews)
- ✅ Require status checks to pass
- ❌ Allow force pushes
- ❌ Allow deletions

### Para `dev`:
- ✅ Require pull request reviews before merging (1 review mínimo)
- ❌ Force pushes permitidos (opcional, si equipo es pequeño)

---

## Convenciones de Commit

```
feat: agregar nueva funcionalidad
fix: corregir bug
docs: cambios en documentación
style: cambios de formato/linting
refactor: refactorizar código
test: agregar/modificar tests
chore: tareas de mantenimiento (deps, build)

Ejemplo:
git commit -m "feat: agregar autenticación con JWT"
git commit -m "fix: corregir diagnóstico de neumonía en pacientes > 65 años"
```

---

## Guía Práctica: Flujo Paso a Paso

### Paso 1️⃣: Prepara tu rama base (`dev`)
```powershell
# Cambiar a dev
git checkout dev

# Descargar los últimos cambios del remoto
git pull origin dev
```

### Paso 2️⃣: Crea tu rama de feature
```powershell
# Crear rama DESDE dev con nombre descriptivo
# Formato: tipo/descripción-corta
git checkout -b feature/nombre-funcionalidad

# Ejemplos:
# git checkout -b feature/agregar-login
# git checkout -b chore/setup-project-config
# git checkout -b fix/corregir-diagnostico
```

**Verifica que estés en la rama correcta:**
```powershell
git branch
# Deberías ver:
# * feature/nombre-funcionalidad  ← el asterisco indica tu rama actual
#   dev
#   main
#   uat
```

### Paso 3️⃣: Haz cambios en tus archivos
- Abre VS Code
- Edita los archivos que necesites (`.gitignore`, `main.py`, `models.py`, etc.)
- Guarda los cambios (Ctrl+S)

### Paso 4️⃣: Verifica qué cambiaste
```powershell
git status
```

**Output esperado:**
```
On branch feature/nombre-funcionalidad
Changes not staged for commit:
  modified:   .gitignore
  modified:   pyproject.toml
  modified:   main.py

Untracked files:
  new_file.py
```

### Paso 5️⃣: Prepara los cambios (staging)
```powershell
# Opción A: agregar archivos específicos
git add .gitignore pyproject.toml main.py

# Opción B: agregar TODOS los cambios (cuidado, verifica primero)
git add .
```

**Verifica que quedó preparado:**
```powershell
git status
# Deberías ver "Changes to be committed:"
```

### Paso 6️⃣: Haz commit (registra cambios)
```powershell
# Formato: tipo(scope): descripción breve
git commit -m "feat(auth): agregar autenticación JWT"

# Ejemplos:
# git commit -m "chore: configurar .gitignore y pyproject.toml"
# git commit -m "fix(diagnostic): corregir algoritmo de detección"
# git commit -m "docs: actualizar README con instrucciones"
```

### Paso 7️⃣: ¿Más cambios? Repite pasos 3-6
```powershell
# Si necesitas hacer más cambios:
# 1. Edita más archivos
# 2. git add archivos-nuevos
# 3. git commit -m "otro cambio"
# 4. Repite según sea necesario
```

**Puedes tener múltiples commits en una rama:**
```
commit 1: "feat(auth): agregar login"
commit 2: "feat(auth): agregar validación"
commit 3: "test(auth): agregar tests"
```

### Paso 8️⃣: Sube tu rama al remoto (GitHub)
```powershell
# Primera vez en esta rama (crea rama remota y establece seguimiento)
git push -u origin feature/nombre-funcionalidad

# Próximas veces en esta rama (solo actualiza)
git push origin feature/nombre-funcionalidad
```

### Paso 9️⃣: Crea un Pull Request (PR) en GitHub
1. Ve a https://github.com/ElkynEnriquez/UAO-Neumonia-G1
2. GitHub debería mostrar un mensaje: **"Compare & pull request"**
3. Haz clic en ese botón
4. **Verifica:**
   - **Base**: `dev` (NO `main`)
   - **Compare**: `feature/nombre-funcionalidad`
5. Agrega descripción clara de qué cambios hiciste
6. Solicita revisores (Code Reviewers)
7. Haz clic en **"Create Pull Request"**

### Paso 🔟: Espera revisión y aprobación
- Reviewer revisa tu código
- Si pide cambios: haz más commits en tu rama local y haz `git push`
- Si aprueba: alguien mergea el PR en GitHub

### Paso 1️⃣1️⃣: Limpia después de mergear
```powershell
# Una vez que el PR esté mergeado en GitHub

# Eliminar rama local
git branch -d feature/nombre-funcionalidad

# Eliminar rama remota
git push origin --delete feature/nombre-funcionalidad

# Actualizar dev con los cambios nuevos
git checkout dev
git pull origin dev
```

---

## Comandos Rápidos de Referencia

```bash
# Ver todas las ramas locales y remotas
git branch -a

# Actualizar dev
git checkout dev
git pull --rebase origin dev

# Crear feature desde dev
git checkout -b feature/nombre-feature dev
git push -u origin feature/nombre-feature

# Eliminar rama local (después de mergear)
git branch -d nombre-feature

# Eliminar rama remota (después de mergear)
git push origin --delete nombre-feature

# Ver historial de commits con gráfico
git log --graph --oneline --all

# Crear tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

---

## Preguntas Frecuentes (FAQ)

**P: ¿Qué pasa si mergeo accidentalmente a `main`?**  
R: Si `main` está protegida, GitHub lo bloqueará. Si ya está merged, revertir con: `git revert <commit-hash>`.

**P: ¿Puedo hacer push directo a `uat` o `main`?**  
R: No. Siempre usar PR (pull request) para mantener trazabilidad y control.

**P: ¿Con qué frecuencia debo actualizar `dev` desde `main`?**  
R: Después de cada release o si hay hotfixes en `main`, sincroniza `dev` para evitar conflictos futuros.

**P: ¿Qué rama uso para desarrollo local?**  
R: Crea siempre una `feature/...` desde `dev`, no trabajes directamente en `dev`.

**P: ¿Cuándo creo un tag?**  
R: Cuando haces merge a `main` para una release. Tag = versión formal (v1.0.0, v1.0.1, etc.).

---

## Responsabilidades por Rol

| Rol | `dev` | `uat` | `main` |
|-----|-------|-------|--------|
| **Desarrollador** | Crea PR desde features | Solo lectura | Solo lectura |
| **Code Reviewer** | Revisa PR de features | Revisa PR de `dev`→`uat` | Revisa PR de `uat`→`main` |
| **QA/UAT** | Prueba en dev | Prueba activamente | Solo lectura |
| **Gerente de Release** | Supervisa integración | Promueve `dev`→`uat` | Promueve `uat`→`main`, crea tags |
| **DevOps** | Monitorea CI | Monitorea CI | Despliegue a producción |

---

## Próximos Pasos

1. Proteger ramas en GitHub (Settings → Branches → Add rule).
2. Comunicar esta estrategia al equipo.
3. Crear las primeras features desde `dev` y probar el flujo.
4. Documentar en el README principal cómo trabajar con ramas.

---

**Última actualización**: 30 de enero de 2026  
**Autor**: Equipo UAO Neumonía G1
