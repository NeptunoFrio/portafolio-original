package com.pocketforge.launcher;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.File;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {

    private static final String MODRINTH_API_URL = "https://modrinth.com";
    
    static {
        try {
            System.loadLibrary("pocketforge_core");
        } catch (UnsatisfiedLinkError e) {
            android.util.Log.e("PocketForge", "Error al cargar libreria grafica: " + e.getMessage());
        }
    }

    public native boolean inicializarTraductorGrafico();
    public native void aplicarFlagsOptimizacion(int nivelOptimizacion);

    private EditText cajaBusqueda;
    private Button botonBuscar;
    private LinearLayout contenedorListaMods;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.dash_layout);

        cajaBusqueda = findViewById(R.id.cajaBusqueda);
        botonBuscar = findViewById(R.id.botonBuscar);
        contenedorListaMods = findViewById(R.id.contenedorListaMods);

        // Inicializamos el motor gráfico nativo
        if (inicializarTraductorGrafico()) {
            aplicarFlagsOptimizacion(3); 
        }

        botonBuscar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void気に(View v) {
                String textoBuscado = cajaBusqueda.getText().toString().trim();
                if (textoBuscado.isEmpty()) {
                    Toast.makeText(MainActivity.this, "Escribe el nombre de un mod", Toast.LENGTH_SHORT).show();
                } else {
                    ejecutarBusquedaEnSegundoPlano(textoBuscado);
                }
            }
        });

        // Lanzamos las descargas del núcleo en paralelo al iniciar
        descargarVersionMinecraftBase("1.21.1");
        configurarJava21Movel();
    }

    // NUEVA FUNCIÓN: Descarga e instala el JRE de Java 21 para procesadores de celular (ARM64)
    private void configurarJava21Movel() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    android.util.Log.i("PocketForge", "Verificando entorno de Java 21 nativo...");
                    
                    // URL de un binario OpenJDK de Java 21 optimizado para Linux/Android ARM64
                    String urlJava21 = "https://github.com";
                    
                    String rutaJava = System.getProperty("user.home") + File.separator + "PocketForge" + File.separator + "runtime" + File.separator + "java21";
                    File carpetaJava = new File(rutaJava);
                    
                    if (!carpetaJava.exists()) {
                        carpetaJava.mkdirs();
                        
                        File archivoTarGz = new File(carpetaJava, "java21.tar.gz");
                        android.util.Log.i("PocketForge", "Descargando Java 21 ARM64 en: " + archivoTarGz.getAbsolutePath());

                        URL url = new URL(urlJava21);
                        HttpURLConnection conexion = (HttpURLConnection) url.openConnection();
                        conexion.setRequestProperty("User-Agent", "PocketForge/Launcher/1.0");

                        try (BufferedInputStream en = new BufferedInputStream(conexion.getInputStream());
                             FileOutputStream salida = new FileOutputStream(archivoTarGz)) {
                            
                            byte[] buffer = new byte[4096];
                            int bytesLeidos;
                            while ((bytesLeidos = en.read(buffer, 0, 4096)) != -1) {
                                salida.write(buffer, 0, bytesLeidos);
                            }
                            android.util.Log.i("PocketForge", "¡Archivo Java 21 descargado! Listo para descompresión interna.");
                            
                            // NOTA TÉCNICA: En la fase de ejecución final, el launcher descomprime este .tar.gz
                            // y ejecuta el binario "java" usando permisos de ejecución chmod +x en Android.
                        }
                    } else {
                        android.util.Log.i("PocketForge", "Java 21 ya se encuentra instalado en el dispositivo.");
                    }

                } catch (Exception e) {
                    android.util.Log.e("PocketForge", "Error al configurar Java 21: " + e.getMessage());
                }
            }
        }).start();
    }

    private void descargarVersionMinecraftBase(final String version) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    String urlClienteMojang = "https://mojang.com";
                    String rutaVersiones = System.getProperty("user.home") + File.separator + "PocketForge" + File.separator + "versions" + File.separator + version;
                    File carpetaVersion = new File(rutaVersiones);
                    if (!carpetaVersion.exists()) carpetaVersion.mkdirs();

                    File jarMinecraft = new File(carpetaVersion, version + ".jar");
                    if (!jarMinecraft.exists()) {
                        URL url = new URL(urlClienteMojang);
                        HttpURLConnection conexion = (HttpURLConnection) url.openConnection();
                        conexion.setRequestProperty("User-Agent", "PocketForge/Launcher/1.0");

                        try (BufferedInputStream en = new BufferedInputStream(conexion.getInputStream());
                             FileOutputStream salida = new FileOutputStream(jarMinecraft)) {
                            byte[] buffer = new byte[4096];
                            int bytesLeidos;
                            while ((bytesLeidos = en.read(buffer, 0, 4096)) != -1) {
                                salida.write(buffer, 0, bytesLeidos);
                            }
                            android.util.Log.i("PocketForge", "¡Juego base Minecraft " + version + " descargado!");
                        }
                    }
                } catch (Exception e) {
                    android.util.Log.e("PocketForge", "Error en juego base: " + e.getMessage());
                }
            }
        }).start();
    }

    private void ejecutarBusquedaEnSegundoPlano(final String nombreMod) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    String urlConQuery = MODRINTH_API_URL + nombreMod.replace(" ", "%20");
                    URL url = new URL(urlConQuery);
                    HttpURLConnection conexion = (HttpURLConnection) url.openConnection();
                    conexion.setRequestMethod("GET");
                    conexion.setRequestProperty("User-Agent", "PocketForge/Launcher/1.0");

                    if (conexion.getResponseCode() == HttpURLConnection.HTTP_OK) {
                        actualizarInterfazConResultados(nombreMod);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    private void actualizarInterfazConResultados(final String modEncontrado) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                contenedorListaMods.removeAllViews();
                Button botonMod = new Button(MainActivity.this);
                botonMod.setText("Instalar " + modEncontrado + " (Modrinth)");
                botonMod.setBackgroundColor(0xFF4CAF50); 
                botonMod.setTextColor(0xFFFFFFFF);     
                contenedorListaMods.addView(botonMod);
            }
        });
    }
}
