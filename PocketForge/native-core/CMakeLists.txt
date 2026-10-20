# Define la versión mínima de CMake requerida por Android Studio
cmake_minimum_required(VERSION 3.22.1)

# Nombre de nuestro proyecto nativo
project("pocketforge_core")

# Añade la librería nativa y le dice qué archivos debe compilar
add_library(
        pocketforge_core # Nombre de la librería (.so) que usará Java
        SHARED           # Indica que es una librería compartida
        gl_wrapper.cpp   # El archivo de traducción gráfica que escribimos antes
)

# Busca las librerías del sistema de Android para poder pintar gráficos y mostrar logs
find_library(
        log-lib
        log
)

# Enlaza nuestro traductor gráfico con las librerías del sistema operativo
target_link_libraries(
        pocketforge_core
        ${log-lib}
        android
        EGL
        GLESv3 # Habilita soporte para OpenGL ES 3.0 de alta velocidad
)
