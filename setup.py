import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn"

write_file(os.path.join(base_dir, "settings.gradle.kts"), """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "Arrow Scape"
include(":app")
""")

write_file(os.path.join(base_dir, "build.gradle.kts"), """
plugins {
    id("com.android.application") version "8.2.1" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
""")

write_file(os.path.join(base_dir, "gradle.properties"), """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
""")

write_file(os.path.join(base_dir, "gradle", "wrapper", "gradle-wrapper.properties"), """
distributionBase=PROJECT
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.2-bin.zip
zipStoreBase=PROJECT
zipStorePath=wrapper/dists
""")

write_file(os.path.join(base_dir, "app", "build.gradle.kts"), """
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.arrowscape"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.arrowscape"
        minSdk = 23
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        viewBinding = false
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
}
""")

write_file(os.path.join(base_dir, "app", "src", "main", "AndroidManifest.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.ArrowScape">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:configChanges="orientation|keyboardHidden|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

write_file(os.path.join(base_dir, "app", "src", "main", "res", "values", "strings.xml"), """
<resources>
    <string name="app_name">Arrow Scape</string>
</resources>
""")

write_file(os.path.join(base_dir, "app", "src", "main", "res", "values", "colors.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="background_color">#FF121212</color>
    <color name="primary_color">#FF4CAF50</color>
</resources>
""")

write_file(os.path.join(base_dir, "app", "src", "main", "res", "values", "themes.xml"), """
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.ArrowScape" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="android:windowBackground">@color/background_color</item>
        <item name="android:statusBarColor">@color/background_color</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:windowFullscreen">true</item>
    </style>
</resources>
""")

write_file(os.path.join(base_dir, "app", "src", "main", "res", "mipmap-anydpi-v26", "ic_launcher.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/primary_color" />
    <foreground android:drawable="@color/background_color" />
</adaptive-icon>
""")

write_file(os.path.join(base_dir, "app", "src", "main", "res", "mipmap-hdpi", "ic_launcher.png"), "") # Placeholder, will let Android Studio complain or replace later, or just don't create and use a color
# Instead of mipmap-hdpi/ic_launcher.png, I will just provide the vector XML for adaptive icons and a fallback drawable.
write_file(os.path.join(base_dir, "app", "src", "main", "res", "drawable", "ic_launcher.xml"), """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="@color/primary_color" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="@color/background_color" android:pathData="M54,20l-30,30h20v40h20v-40h20z"/>
</vector>
""")

# MainActivity
write_file(os.path.join(base_dir, "app", "src", "main", "java", "com", "example", "arrowscape", "MainActivity.kt"), """
package com.example.arrowscape

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.example.arrowscape.game.GameView

class MainActivity : AppCompatActivity() {

    private lateinit var gameView: GameView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Configure immersive mode
        WindowCompat.setDecorFitsSystemWindows(window, false)
        val insetsController = WindowCompat.getInsetsController(window, window.decorView)
        insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        insetsController.hide(WindowInsetsCompat.Type.systemBars())

        gameView = GameView(this)
        setContentView(gameView)
    }

    override fun onResume() {
        super.onResume()
        gameView.resume()
    }

    override fun onPause() {
        super.onPause()
        gameView.pause()
    }
}
""")

# GameView
write_file(os.path.join(base_dir, "app", "src", "main", "java", "com", "example", "arrowscape", "game", "GameView.kt"), """
package com.example.arrowscape.game

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.view.MotionEvent
import android.view.SurfaceHolder
import android.view.SurfaceView

class GameView(context: Context) : SurfaceView(context), SurfaceHolder.Callback {

    private var gameLoop: GameLoop? = null
    private val gameState = GameState()
    private val renderer = GameRenderer()
    private val inputHandler = InputHandler(gameState)

    init {
        holder.addCallback(this)
        isFocusable = true
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        resume()
    }

    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
        gameState.updateScreenDimensions(width, height)
    }

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        pause()
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        return inputHandler.handleTouchEvent(event)
    }

    fun update() {
        gameState.update()
    }

    override fun draw(canvas: Canvas) {
        super.draw(canvas)
        canvas.drawColor(Color.BLACK) // Clear screen
        renderer.draw(canvas, gameState)
    }

    fun resume() {
        if (gameLoop == null && holder.surface.isValid) {
            gameLoop = GameLoop(this, holder)
            gameLoop?.startLoop()
        }
    }

    fun pause() {
        gameLoop?.stopLoop()
        gameLoop = null
    }
}
""")

# GameLoop
write_file(os.path.join(base_dir, "app", "src", "main", "java", "com", "example", "arrowscape", "game", "GameLoop.kt"), """
package com.example.arrowscape.game

import android.graphics.Canvas
import android.view.SurfaceHolder

class GameLoop(
    private val gameView: GameView,
    private val surfaceHolder: SurfaceHolder
) : Thread() {

    private var isRunning = false

    fun startLoop() {
        isRunning = true
        start()
    }

    fun stopLoop() {
        isRunning = false
        try {
            join()
        } catch (e: InterruptedException) {
            e.printStackTrace()
        }
    }

    override fun run() {
        var startTime: Long
        var timeMillis: Long
        var waitTime: Long
        val targetTime = 1000L / 60L // Target 60 FPS

        while (isRunning) {
            startTime = System.nanoTime()
            var canvas: Canvas? = null

            try {
                canvas = surfaceHolder.lockCanvas()
                synchronized(surfaceHolder) {
                    if (canvas != null) {
                        gameView.update()
                        gameView.draw(canvas)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                if (canvas != null) {
                    try {
                        surfaceHolder.unlockCanvasAndPost(canvas)
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }
            }

            timeMillis = (System.nanoTime() - startTime) / 1000000
            waitTime = targetTime - timeMillis

            if (waitTime > 0) {
                try {
                    sleep(waitTime)
                } catch (e: InterruptedException) {
                    e.printStackTrace()
                }
            }
        }
    }
}
""")

# GameState
write_file(os.path.join(base_dir, "app", "src", "main", "java", "com", "example", "arrowscape", "game", "GameState.kt"), """
package com.example.arrowscape.game

class GameState {
    var screenWidth: Int = 0
        private set
    var screenHeight: Int = 0
        private set

    fun updateScreenDimensions(width: Int, height: Int) {
        this.screenWidth = width
        this.screenHeight = height
    }

    fun update() {
        // Update game logic here (e.g., physics, animations)
    }
    
    fun processTap(x: Float, y: Float) {
        // Handle a tap event
    }
}
""")

# InputHandler
write_file(os.path.join(base_dir, "app", "src", "main", "java", "com", "example", "arrowscape", "game", "InputHandler.kt"), """
package com.example.arrowscape.game

import android.view.MotionEvent

class InputHandler(private val gameState: GameState) {
    fun handleTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                gameState.processTap(event.x, event.y)
                return true
            }
        }
        return false
    }
}
""")

# GameRenderer
write_file(os.path.join(base_dir, "app", "src", "main", "java", "com", "example", "arrowscape", "game", "GameRenderer.kt"), """
package com.example.arrowscape.game

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint

class GameRenderer {
    
    private val paint = Paint().apply {
        color = Color.GREEN
        isAntiAlias = true
        textSize = 50f
    }

    fun draw(canvas: Canvas, gameState: GameState) {
        // Render the game board and objects based on gameState
        if (gameState.screenWidth > 0 && gameState.screenHeight > 0) {
            val text = "Arrow Scape"
            val textWidth = paint.measureText(text)
            canvas.drawText(
                text, 
                (gameState.screenWidth - textWidth) / 2f, 
                gameState.screenHeight / 2f, 
                paint
            )
        }
    }
}
""")

print("Setup complete")
