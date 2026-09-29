import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape"
res_dir = r"c:\Users\modip\Downloads\earn\app\src\main\res"

# 1. Update AndroidManifest.xml to add VIBRATE permission
write_file(os.path.join(res_dir, "AndroidManifest.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.VIBRATE" />
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

# 2. Update screen_gameplay.xml to include tutorial text
write_file(os.path.join(res_dir, "layout", "screen_gameplay.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F5F5F7">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:padding="16dp"
            android:gravity="center_vertical">
            <Button
                android:id="@+id/btnGameBack"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Back"
                android:backgroundTint="#9E9E9E"/>
            <TextView
                android:id="@+id/tvLevelTitle"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="Level 1"
                android:textSize="24sp"
                android:textStyle="bold"
                android:textColor="#1A237E"
                android:gravity="center" />
            <Button
                android:id="@+id/btnGameSettings"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Settings"
                android:backgroundTint="#9E9E9E"/>
        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:paddingHorizontal="16dp"
            android:paddingBottom="8dp"
            android:gravity="center_vertical">
            <TextView
                android:id="@+id/tvHearts"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="♥♥♥"
                android:textSize="32sp"
                android:textColor="#E53935" />
            <Space
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1" />
            <TextView
                android:id="@+id/tvArrows"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Arrows: 3"
                android:textSize="20sp"
                android:textStyle="bold"
                android:textColor="#1A237E" />
        </LinearLayout>

        <TextView
            android:id="@+id/tvTutorial"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Tap arrows to slide them out.\\nDon't let them crash!"
            android:textSize="16sp"
            android:textAlignment="center"
            android:textColor="#757575"
            android:paddingBottom="8dp"
            android:visibility="gone" />

        <FrameLayout
            android:id="@+id/gameContainer"
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_weight="1" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:padding="16dp"
            android:gravity="center">
            <Button
                android:id="@+id/btnHint"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Hint (3)"
                android:backgroundTint="#2196F3"
                android:layout_marginEnd="16dp"/>
            <Button
                android:id="@+id/btnUndo"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Undo"
                android:backgroundTint="#2196F3"/>
        </LinearLayout>
    </LinearLayout>

    <LinearLayout
        android:id="@+id/overlayView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:gravity="center"
        android:background="#DDFFFFFF"
        android:visibility="gone"
        android:clickable="true"
        android:focusable="true">
        
        <TextView
            android:id="@+id/tvOverlayTitle"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="LEVEL CLEARED!"
            android:textSize="40sp"
            android:textStyle="bold"
            android:textColor="#1A237E"
            android:layout_marginBottom="32dp" />

        <Button
            android:id="@+id/btnOverlayPrimary"
            android:layout_width="200dp"
            android:layout_height="60dp"
            android:text="NEXT LEVEL"
            android:textSize="20sp"
            android:backgroundTint="#2196F3"
            android:layout_marginBottom="16dp" />
            
        <Button
            android:id="@+id/btnOverlaySecondary"
            android:layout_width="200dp"
            android:layout_height="60dp"
            android:text="MENU"
            android:textSize="20sp"
            android:backgroundTint="#9E9E9E" />
    </LinearLayout>
</FrameLayout>
""")

# 3. Update GameRenderer.kt with polished empty-slot grid background
write_file(os.path.join(base_dir, "game", "GameRenderer.kt"), """
package com.example.arrowscape.game

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.PathMeasure
import android.graphics.RectF

class GameRenderer {
    // Polished empty-slot look for the grid
    private val slotPaint = Paint().apply {
        color = Color.parseColor("#E8E8EC")
        style = Paint.Style.FILL
        isAntiAlias = true
    }
    
    private val arrowPaint = Paint().apply {
        color = Color.parseColor("#1A237E")
        style = Paint.Style.STROKE
        strokeJoin = Paint.Join.ROUND
        strokeCap = Paint.Cap.ROUND
        isAntiAlias = true
    }
    
    private val headPaint = Paint().apply {
        color = Color.parseColor("#1A237E")
        style = Paint.Style.FILL
        isAntiAlias = true
    }

    private val textPaint = Paint().apply {
        color = Color.parseColor("#1A237E")
        isAntiAlias = true
        textSize = 80f
        textAlign = Paint.Align.CENTER
        isFakeBoldText = true
    }

    private val drawPath = Path()
    private val headPath = Path()
    private val pathMeasure = PathMeasure()
    private val pos = FloatArray(2)
    private val tan = FloatArray(2)
    private val cellRect = RectF()

    fun onSizeChanged(gameState: GameState) {
        arrowPaint.strokeWidth = gameState.cellSize * 0.55f // Slightly thicker arrows
    }

    fun draw(canvas: Canvas, gameState: GameState, view: GameView) {
        val engine = gameState.engine
        val cs = gameState.cellSize
        val offX = gameState.offsetX
        val offY = gameState.offsetY

        // Draw rounded empty slots for grid
        for (x in 0 until engine.gridWidth) {
            for (y in 0 until engine.gridHeight) {
                val cx = offX + x * cs
                val cy = offY + y * cs
                cellRect.set(cx + 4f, cy + 4f, cx + cs - 4f, cy + cs - 4f)
                canvas.drawRoundRect(cellRect, 16f, 16f, slotPaint)
            }
        }

        for (arrow in engine.activeArrows) {
            if (arrow == view.blockedArrow) {
                val shakeOffset = kotlin.math.sin(view.blockedProgress * Math.PI * 4).toFloat() * cs * 0.15f
                canvas.save()
                canvas.translate(shakeOffset * arrow.exitDirection.dx, shakeOffset * arrow.exitDirection.dy)
                
                // Flash red slightly
                val oldColor = arrowPaint.color
                arrowPaint.color = Color.parseColor("#E53935")
                headPaint.color = Color.parseColor("#E53935")
                drawArrow(canvas, arrow, cs, offX, offY)
                arrowPaint.color = oldColor
                headPaint.color = oldColor
                
                canvas.restore()
            } else {
                drawArrow(canvas, arrow, cs, offX, offY)
            }
        }

        view.escapingArrow?.let { arrow ->
            drawEscapingArrow(canvas, arrow, view.escapingProgress, cs, offX, offY, engine.gridWidth, engine.gridHeight)
        }
    }

    private fun drawArrow(canvas: Canvas, arrow: Arrow, cs: Float, offX: Float, offY: Float) {
        drawPath.reset()
        if (arrow.path.isEmpty()) return

        for ((i, pt) in arrow.path.withIndex()) {
            val cx = offX + pt.x * cs + cs / 2f
            val cy = offY + pt.y * cs + cs / 2f
            if (i == 0) drawPath.moveTo(cx, cy)
            else drawPath.lineTo(cx, cy)
        }
        canvas.drawPath(drawPath, arrowPaint)

        val headPt = arrow.path.last()
        val hx = offX + headPt.x * cs + cs / 2f
        val hy = offY + headPt.y * cs + cs / 2f
        drawArrowHead(canvas, hx, hy, arrow.exitDirection.angle, cs)
    }

    private fun drawArrowHead(canvas: Canvas, x: Float, y: Float, angle: Float, cs: Float) {
        canvas.save()
        canvas.translate(x, y)
        canvas.rotate(angle)
        
        val size = cs * 0.45f // Slightly larger arrowhead
        headPath.reset()
        headPath.moveTo(size, 0f)
        headPath.lineTo(-size * 0.6f, size * 0.7f)
        headPath.lineTo(-size * 0.6f, -size * 0.7f)
        headPath.close()
        
        canvas.drawPath(headPath, headPaint)
        canvas.restore()
    }

    private fun drawEscapingArrow(canvas: Canvas, arrow: Arrow, progress: Float, cs: Float, offX: Float, offY: Float, gridWidth: Int, gridHeight: Int) {
        val extPath = mutableListOf<Point>()
        extPath.addAll(arrow.path)
        var curr = arrow.path.last()
        val maxDist = maxOf(gridWidth, gridHeight) + 3
        for (i in 0 until maxDist) {
            curr = Point(curr.x + arrow.exitDirection.dx, curr.y + arrow.exitDirection.dy)
            extPath.add(curr)
        }

        drawPath.reset()
        for ((i, pt) in extPath.withIndex()) {
            val cx = offX + pt.x * cs + cs / 2f
            val cy = offY + pt.y * cs + cs / 2f
            if (i == 0) drawPath.moveTo(cx, cy)
            else drawPath.lineTo(cx, cy)
        }

        pathMeasure.setPath(drawPath, false)
        val originalLength = (arrow.path.size - 1) * cs
        val totalDistance = maxDist * cs
        val offset = progress * totalDistance
        val startD = offset
        val endD = offset + originalLength

        val renderPath = Path()
        pathMeasure.getSegment(startD, endD, renderPath, true)
        canvas.drawPath(renderPath, arrowPaint)

        if (pathMeasure.getPosTan(endD, pos, tan)) {
            val angle = (Math.atan2(tan[1].toDouble(), tan[0].toDouble()) * 180 / Math.PI).toFloat()
            drawArrowHead(canvas, pos[0], pos[1], angle, cs)
        }
    }
}
""")

# 4. Update GameView.kt to play ToneGenerator sounds and Haptics based on Settings
write_file(os.path.join(base_dir, "game", "GameView.kt"), """
package com.example.arrowscape.game

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.view.MotionEvent
import android.view.View
import android.view.animation.AccelerateInterpolator

class GameView(context: Context) : View(context) {

    val gameState = GameState()
    private val renderer = GameRenderer()
    
    private var isAnimating = false
    
    var escapingArrow: Arrow? = null
    var escapingProgress: Float = 0f
    
    var blockedArrow: Arrow? = null
    var blockedProgress: Float = 0f

    var onStateChanged: (() -> Unit)? = null
    var onLevelWon: (() -> Unit)? = null
    var onGameOver: (() -> Unit)? = null

    // Lightweight audio using built-in tones
    private val toneGen = ToneGenerator(AudioManager.STREAM_MUSIC, 100)
    private val vibrator = context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
    
    private val prefs = context.getSharedPreferences("ArrowScapePrefs", Context.MODE_PRIVATE)

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        gameState.updateDimensions(w, h)
        renderer.onSizeChanged(gameState)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (event.action == MotionEvent.ACTION_DOWN) {
            if (isAnimating || gameState.engine.status != GameStatus.PLAYING) return true
            
            val pt = gameState.getGridCoords(event.x, event.y)
            if (pt.x in 0 until gameState.engine.gridWidth && pt.y in 0 until gameState.engine.gridHeight) {
                val result = gameState.engine.handleTap(pt.x, pt.y)
                handleMoveResult(result)
                onStateChanged?.invoke()
            }
            return true
        }
        return super.onTouchEvent(event)
    }

    private fun playSound(tone: Int, duration: Int) {
        if (prefs.getBoolean("sound", true)) {
            toneGen.startTone(tone, duration)
        }
    }

    private fun playVibration(duration: Long) {
        if (prefs.getBoolean("vibration", true)) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vibrator.vibrate(VibrationEffect.createOneShot(duration, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                vibrator.vibrate(duration)
            }
        }
    }

    private fun handleMoveResult(result: MoveResult) {
        when (result) {
            is Escaped -> {
                isAnimating = true
                playSound(ToneGenerator.TONE_PROP_BEEP, 100)
                playVibration(20)
                
                escapingArrow = result.arrow
                val anim = ValueAnimator.ofFloat(0f, 1f)
                anim.duration = 350
                anim.interpolator = AccelerateInterpolator()
                anim.addUpdateListener { 
                    escapingProgress = it.animatedValue as Float
                    invalidate()
                }
                anim.addListener(object : AnimatorListenerAdapter() {
                    override fun onAnimationEnd(animation: Animator) {
                        isAnimating = false
                        escapingArrow = null
                        invalidate()
                        checkGameEnd()
                    }
                })
                anim.start()
            }
            is Blocked -> {
                isAnimating = true
                playSound(ToneGenerator.TONE_PROP_NACK, 150)
                playVibration(80)
                
                blockedArrow = result.arrow
                val anim = ValueAnimator.ofFloat(0f, 1f)
                anim.duration = 300
                anim.addUpdateListener { 
                    blockedProgress = it.animatedValue as Float
                    invalidate()
                }
                anim.addListener(object : AnimatorListenerAdapter() {
                    override fun onAnimationEnd(animation: Animator) {
                        isAnimating = false
                        blockedArrow = null
                        invalidate()
                        checkGameEnd()
                    }
                })
                anim.start()
            }
            Ignored -> {}
        }
    }

    private fun checkGameEnd() {
        if (gameState.engine.status == GameStatus.WON) {
            playSound(ToneGenerator.TONE_SUP_CONFIRM, 300)
            onLevelWon?.invoke()
        } else if (gameState.engine.status == GameStatus.GAME_OVER) {
            playSound(ToneGenerator.TONE_SUP_ERROR, 500)
            onGameOver?.invoke()
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        renderer.draw(canvas, gameState, this)
    }
}
""")

# 5. Update MainActivity.kt to bind Settings and Tutorial
write_file(os.path.join(base_dir, "MainActivity.kt"), """
package com.example.arrowscape

import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.Button
import android.widget.FrameLayout
import android.widget.GridLayout
import android.widget.LinearLayout
import android.widget.Switch
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.example.arrowscape.game.GameStatus
import com.example.arrowscape.game.GameView
import com.example.arrowscape.game.LevelManager

class MainActivity : AppCompatActivity() {

    private lateinit var rootLayout: FrameLayout
    
    private val prefs by lazy { getSharedPreferences("ArrowScapePrefs", Context.MODE_PRIVATE) }
    private var unlockedLevel: Int
        get() = prefs.getInt("unlocked_level", 0)
        set(value) { prefs.edit().putInt("unlocked_level", value).apply() }
        
    private var currentLevelIndex = 0
    private var hintCount = 3

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        WindowCompat.setDecorFitsSystemWindows(window, false)
        val insetsController = WindowCompat.getInsetsController(window, window.decorView)
        insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        insetsController.hide(WindowInsetsCompat.Type.systemBars())

        rootLayout = FrameLayout(this)
        setContentView(rootLayout)
        
        showHome()
    }

    private fun setScreen(layoutResId: Int): View {
        rootLayout.removeAllViews()
        val view = LayoutInflater.from(this).inflate(layoutResId, rootLayout, false)
        rootLayout.addView(view)
        return view
    }

    private fun showHome() {
        val view = setScreen(R.layout.screen_home)
        view.findViewById<Button>(R.id.btnPlay).setOnClickListener { showLevelSelect() }
        view.findViewById<Button>(R.id.btnSettings).setOnClickListener { showSettings() }
    }

    private fun showSettings() {
        val view = setScreen(R.layout.screen_settings)
        
        val swSound = view.findViewById<Switch>(R.id.swSound)
        val swVibration = view.findViewById<Switch>(R.id.swVibration)
        
        swSound.isChecked = prefs.getBoolean("sound", true)
        swVibration.isChecked = prefs.getBoolean("vibration", true)
        
        swSound.setOnCheckedChangeListener { _, isChecked -> prefs.edit().putBoolean("sound", isChecked).apply() }
        swVibration.setOnCheckedChangeListener { _, isChecked -> prefs.edit().putBoolean("vibration", isChecked).apply() }
        
        view.findViewById<Button>(R.id.btnSettingsBack).setOnClickListener { showHome() }
    }

    private fun showLevelSelect() {
        val view = setScreen(R.layout.screen_level_select)
        view.findViewById<Button>(R.id.btnBack).setOnClickListener { showHome() }
        
        val grid = view.findViewById<GridLayout>(R.id.levelGrid)
        for (i in LevelManager.levels.indices) {
            val btn = Button(this).apply {
                text = "${i + 1}"
                textSize = 20f
                layoutParams = GridLayout.LayoutParams().apply {
                    width = 200
                    height = 200
                    setMargins(16, 16, 16, 16)
                }
                if (i <= unlockedLevel) {
                    setBackgroundColor(Color.parseColor("#2196F3"))
                    setTextColor(Color.WHITE)
                    setOnClickListener {
                        currentLevelIndex = i
                        showGameplay()
                    }
                } else {
                    setBackgroundColor(Color.parseColor("#E0E0E0"))
                    setTextColor(Color.GRAY)
                }
            }
            grid.addView(btn)
        }
    }

    private fun showGameplay() {
        val view = setScreen(R.layout.screen_gameplay)
        
        val gameContainer = view.findViewById<FrameLayout>(R.id.gameContainer)
        val gameView = GameView(this)
        gameContainer.addView(gameView)
        
        gameView.gameState.loadLevel(currentLevelIndex)
        hintCount = 3
        
        val tvLevelTitle = view.findViewById<TextView>(R.id.tvLevelTitle)
        val tvHearts = view.findViewById<TextView>(R.id.tvHearts)
        val tvArrows = view.findViewById<TextView>(R.id.tvArrows)
        val tvTutorial = view.findViewById<TextView>(R.id.tvTutorial)
        val btnHint = view.findViewById<Button>(R.id.btnHint)
        val overlayView = view.findViewById<LinearLayout>(R.id.overlayView)
        val tvOverlayTitle = view.findViewById<TextView>(R.id.tvOverlayTitle)
        val btnOverlayPrimary = view.findViewById<Button>(R.id.btnOverlayPrimary)
        val btnOverlaySecondary = view.findViewById<Button>(R.id.btnOverlaySecondary)
        
        tvLevelTitle.text = "Level ${currentLevelIndex + 1}"
        
        // Show tutorial only on Level 1
        tvTutorial.visibility = if (currentLevelIndex == 0) View.VISIBLE else View.GONE
        
        fun updateHUD() {
            val lives = gameView.gameState.engine.lives
            tvHearts.text = "♥".repeat(lives) + "♡".repeat(3 - lives)
            tvArrows.text = "Arrows: ${gameView.gameState.engine.activeArrows.size}"
            btnHint.text = "Hint ($hintCount)"
        }
        
        view.findViewById<Button>(R.id.btnGameBack).setOnClickListener { showLevelSelect() }
        view.findViewById<Button>(R.id.btnGameSettings).setOnClickListener { showSettings() }
        
        btnHint.setOnClickListener {
            if (hintCount > 0 && gameView.gameState.engine.status == GameStatus.PLAYING) {
                hintCount--
                updateHUD()
            }
        }
        
        gameView.onStateChanged = { updateHUD() }
        
        gameView.onLevelWon = {
            if (currentLevelIndex == unlockedLevel && unlockedLevel < LevelManager.levels.size - 1) {
                unlockedLevel++
            }
            overlayView.visibility = View.VISIBLE
            if (currentLevelIndex == LevelManager.levels.size - 1) {
                showAllCompleted()
            } else {
                tvOverlayTitle.text = "LEVEL CLEARED!"
                tvOverlayTitle.setTextColor(Color.parseColor("#1A237E"))
                btnOverlayPrimary.text = "NEXT LEVEL"
                btnOverlayPrimary.setOnClickListener {
                    currentLevelIndex++
                    showGameplay()
                }
                btnOverlaySecondary.setOnClickListener { showLevelSelect() }
            }
        }
        
        gameView.onGameOver = {
            overlayView.visibility = View.VISIBLE
            tvOverlayTitle.text = "OUT OF LIVES"
            tvOverlayTitle.setTextColor(Color.parseColor("#E53935"))
            btnOverlayPrimary.text = "RETRY"
            btnOverlayPrimary.setOnClickListener {
                gameView.gameState.engine.resetLevel()
                overlayView.visibility = View.GONE
                updateHUD()
                gameView.invalidate()
            }
            btnOverlaySecondary.setOnClickListener { showLevelSelect() }
        }
        
        updateHUD()
    }

    private fun showAllCompleted() {
        val view = setScreen(R.layout.screen_all_completed)
        view.findViewById<Button>(R.id.btnAllCompletedMenu).setOnClickListener { showHome() }
    }
}
""")

print("Polish applied")
