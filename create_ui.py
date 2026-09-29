import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

res_dir = r"c:\Users\modip\Downloads\earn\app\src\main\res\layout"
src_dir = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape"

# screen_home.xml
write_file(os.path.join(res_dir, "screen_home.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#F5F5F7">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="ARROW SCAPE"
        android:textSize="48sp"
        android:textStyle="bold"
        android:textColor="#1A237E"
        android:layout_marginBottom="64dp" />

    <Button
        android:id="@+id/btnPlay"
        android:layout_width="200dp"
        android:layout_height="60dp"
        android:text="PLAY"
        android:textSize="24sp"
        android:backgroundTint="#2196F3"
        android:textColor="#FFFFFF"
        android:layout_marginBottom="24dp" />

    <Button
        android:id="@+id/btnSettings"
        android:layout_width="200dp"
        android:layout_height="60dp"
        android:text="SETTINGS"
        android:textSize="24sp"
        android:backgroundTint="#9E9E9E"
        android:textColor="#FFFFFF" />
</LinearLayout>
""")

# screen_level_select.xml
write_file(os.path.join(res_dir, "screen_level_select.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#F5F5F7">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="16dp"
        android:gravity="center_vertical">
        <Button
            android:id="@+id/btnBack"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Back"
            android:backgroundTint="#9E9E9E"/>
        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="SELECT LEVEL"
            android:textSize="24sp"
            android:textStyle="bold"
            android:textColor="#1A237E"
            android:gravity="center" />
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:padding="16dp">
        <GridLayout
            android:id="@+id/levelGrid"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:columnCount="3"
            android:alignmentMode="alignBounds"
            android:useDefaultMargins="true" />
    </ScrollView>
</LinearLayout>
""")

# screen_gameplay.xml
write_file(os.path.join(res_dir, "screen_gameplay.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F5F5F7">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">

        <!-- Top Bar -->
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

        <!-- Stats Bar -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:paddingHorizontal="16dp"
            android:paddingBottom="16dp"
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

        <!-- Game Board Container -->
        <FrameLayout
            android:id="@+id/gameContainer"
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_weight="1" />

        <!-- Bottom Bar -->
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

    <!-- Overlay -->
    <LinearLayout
        android:id="@+id/overlayView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:gravity="center"
        android:background="#CCFFFFFF"
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

# screen_settings.xml
write_file(os.path.join(res_dir, "screen_settings.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#F5F5F7">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="SETTINGS"
        android:textSize="32sp"
        android:textStyle="bold"
        android:textColor="#1A237E"
        android:layout_marginBottom="64dp" />

    <Switch
        android:id="@+id/swSound"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Sound Effects   "
        android:textSize="20sp"
        android:textColor="#1A237E"
        android:checked="true"
        android:layout_marginBottom="24dp" />

    <Switch
        android:id="@+id/swVibration"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Vibration         "
        android:textSize="20sp"
        android:textColor="#1A237E"
        android:checked="true"
        android:layout_marginBottom="64dp" />

    <Button
        android:id="@+id/btnSettingsBack"
        android:layout_width="200dp"
        android:layout_height="60dp"
        android:text="BACK"
        android:textSize="24sp"
        android:backgroundTint="#9E9E9E"
        android:textColor="#FFFFFF" />
</LinearLayout>
""")

# screen_all_completed.xml
write_file(os.path.join(res_dir, "screen_all_completed.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#F5F5F7">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="🏆"
        android:textSize="80sp"
        android:layout_marginBottom="24dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="CONGRATULATIONS!"
        android:textSize="32sp"
        android:textStyle="bold"
        android:textColor="#1A237E"
        android:layout_marginBottom="16dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="You've mastered Arrow Scape."
        android:textSize="20sp"
        android:textColor="#424242"
        android:layout_marginBottom="64dp" />

    <Button
        android:id="@+id/btnAllCompletedMenu"
        android:layout_width="200dp"
        android:layout_height="60dp"
        android:text="MAIN MENU"
        android:textSize="24sp"
        android:backgroundTint="#2196F3"
        android:textColor="#FFFFFF" />
</LinearLayout>
""")

# Update GameRenderer.kt (remove text and hearts)
write_file(os.path.join(src_dir, "game", "GameRenderer.kt"), """
package com.example.arrowscape.game

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.PathMeasure

class GameRenderer {
    private val gridPaint = Paint().apply {
        color = Color.parseColor("#E0E0E0")
        style = Paint.Style.STROKE
        strokeWidth = 4f
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

    private val drawPath = Path()
    private val headPath = Path()
    private val pathMeasure = PathMeasure()
    private val pos = FloatArray(2)
    private val tan = FloatArray(2)

    fun onSizeChanged(gameState: GameState) {
        arrowPaint.strokeWidth = gameState.cellSize * 0.5f
    }

    fun draw(canvas: Canvas, gameState: GameState, view: GameView) {
        val engine = gameState.engine
        val cs = gameState.cellSize
        val offX = gameState.offsetX
        val offY = gameState.offsetY

        for (x in 0..engine.gridWidth) {
            val cx = offX + x * cs
            canvas.drawLine(cx, offY, cx, offY + engine.gridHeight * cs, gridPaint)
        }
        for (y in 0..engine.gridHeight) {
            val cy = offY + y * cs
            canvas.drawLine(offX, cy, offX + engine.gridWidth * cs, cy, gridPaint)
        }

        for (arrow in engine.activeArrows) {
            if (arrow == view.blockedArrow) {
                val shakeOffset = kotlin.math.sin(view.blockedProgress * Math.PI * 4).toFloat() * cs * 0.15f
                canvas.save()
                canvas.translate(shakeOffset * arrow.exitDirection.dx, shakeOffset * arrow.exitDirection.dy)
                drawArrow(canvas, arrow, cs, offX, offY)
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
        
        val size = cs * 0.4f
        headPath.reset()
        headPath.moveTo(size, 0f)
        headPath.lineTo(-size, size * 0.7f)
        headPath.lineTo(-size, -size * 0.7f)
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

# Update GameView.kt to add callbacks
write_file(os.path.join(src_dir, "game", "GameView.kt"), """
package com.example.arrowscape.game

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
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

    private fun handleMoveResult(result: MoveResult) {
        when (result) {
            is Escaped -> {
                isAnimating = true
                escapingArrow = result.arrow
                val anim = ValueAnimator.ofFloat(0f, 1f)
                anim.duration = 400
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
            onLevelWon?.invoke()
        } else if (gameState.engine.status == GameStatus.GAME_OVER) {
            onGameOver?.invoke()
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        renderer.draw(canvas, gameState, this)
    }
}
""")

# MainActivity.kt
write_file(os.path.join(src_dir, "MainActivity.kt"), """
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
        val btnHint = view.findViewById<Button>(R.id.btnHint)
        val overlayView = view.findViewById<LinearLayout>(R.id.overlayView)
        val tvOverlayTitle = view.findViewById<TextView>(R.id.tvOverlayTitle)
        val btnOverlayPrimary = view.findViewById<Button>(R.id.btnOverlayPrimary)
        val btnOverlaySecondary = view.findViewById<Button>(R.id.btnOverlaySecondary)
        
        tvLevelTitle.text = "Level ${currentLevelIndex + 1}"
        
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
                // Hint logic would go here (highlight an arrow)
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

# Update GameState.kt to support loadLevel
write_file(os.path.join(src_dir, "game", "GameState.kt"), """
package com.example.arrowscape.game

class GameState {
    var screenWidth: Int = 0
        private set
    var screenHeight: Int = 0
        private set
        
    var cellSize: Float = 0f
        private set
    var offsetX: Float = 0f
        private set
    var offsetY: Float = 0f
        private set

    lateinit var engine: GameEngine
    
    fun loadLevel(index: Int) {
        val template = LevelManager.levels[index]
        engine = GameEngine(
            gridWidth = template.width,
            gridHeight = template.height,
            initialArrows = template.arrows
        )
        updateDimensions(screenWidth, screenHeight)
    }

    fun updateDimensions(width: Int, height: Int) {
        if (width == 0 || height == 0 || !::engine.isInitialized) return
        this.screenWidth = width
        this.screenHeight = height
        
        val boardHeight = height * 0.9f
        val startY = height * 0.05f
        
        val sizeByWidth = width / engine.gridWidth.toFloat()
        val sizeByHeight = boardHeight / engine.gridHeight.toFloat()
        cellSize = minOf(sizeByWidth, sizeByHeight) * 0.9f
        
        offsetX = (width - (engine.gridWidth * cellSize)) / 2f
        offsetY = startY + (boardHeight - (engine.gridHeight * cellSize)) / 2f
    }

    fun getGridCoords(x: Float, y: Float): Point {
        if (!::engine.isInitialized) return Point(-1, -1)
        val gridX = ((x - offsetX) / cellSize).toInt()
        val gridY = ((y - offsetY) / cellSize).toInt()
        return Point(gridX, gridY)
    }
}
""")

print("UI architecture applied")
