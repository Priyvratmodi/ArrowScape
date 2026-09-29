import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape\game"
main_activity = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape\MainActivity.kt"

# Remove GameLoop.kt
loop_path = os.path.join(base_dir, "GameLoop.kt")
if os.path.exists(loop_path):
    os.remove(loop_path)
    
# Remove InputHandler.kt (merged into GameView)
input_path = os.path.join(base_dir, "InputHandler.kt")
if os.path.exists(input_path):
    os.remove(input_path)

# Update MainActivity.kt
write_file(main_activity, """
package com.example.arrowscape

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.example.arrowscape.game.GameView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        WindowCompat.setDecorFitsSystemWindows(window, false)
        val insetsController = WindowCompat.getInsetsController(window, window.decorView)
        insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        insetsController.hide(WindowInsetsCompat.Type.systemBars())

        setContentView(GameView(this))
    }
}
""")

# Models.kt
write_file(os.path.join(base_dir, "Models.kt"), """
package com.example.arrowscape.game

data class Point(val x: Int, val y: Int)

enum class Direction(val dx: Int, val dy: Int, val angle: Float) {
    UP(0, -1, 270f), 
    DOWN(0, 1, 90f), 
    LEFT(-1, 0, 180f), 
    RIGHT(1, 0, 0f)
}

class Arrow(
    val id: Int,
    val path: List<Point>,
    val exitDirection: Direction
)
""")

# Engine.kt
write_file(os.path.join(base_dir, "Engine.kt"), """
package com.example.arrowscape.game

sealed class MoveResult
data class Escaped(val arrow: Arrow) : MoveResult()
data class Blocked(val arrow: Arrow, val blockingArrowId: Int?) : MoveResult()
object Ignored : MoveResult()

enum class GameStatus { PLAYING, WON, GAME_OVER }

class GameEngine(
    val gridWidth: Int,
    val gridHeight: Int,
    private val initialArrows: List<Arrow>
) {
    var lives: Int = 3
        private set
    var status: GameStatus = GameStatus.PLAYING
        private set
    val activeArrows = mutableListOf<Arrow>()

    init {
        resetLevel()
    }

    fun resetLevel() {
        lives = 3
        status = GameStatus.PLAYING
        activeArrows.clear()
        initialArrows.forEach { activeArrows.add(it) }
    }

    fun getArrowAt(p: Point): Arrow? {
        return activeArrows.find { arrow -> arrow.path.contains(p) }
    }

    fun handleTap(x: Int, y: Int): MoveResult {
        if (status != GameStatus.PLAYING) {
            resetLevel()
            return Ignored
        }
        
        val target = getArrowAt(Point(x, y)) ?: return Ignored
        
        if (isExitClear(target)) {
            activeArrows.remove(target)
            if (activeArrows.isEmpty()) {
                status = GameStatus.WON
            }
            return Escaped(target)
        } else {
            lives -= 1
            if (lives <= 0) {
                status = GameStatus.GAME_OVER
            }
            return Blocked(target, null)
        }
    }
    
    private fun isExitClear(arrow: Arrow): Boolean {
        val head = arrow.path.last()
        var curr = Point(head.x + arrow.exitDirection.dx, head.y + arrow.exitDirection.dy)
        
        while (curr.x in 0 until gridWidth && curr.y in 0 until gridHeight) {
            val blockingArrow = getArrowAt(curr)
            if (blockingArrow != null && blockingArrow.id != arrow.id) {
                return false
            }
            curr = Point(curr.x + arrow.exitDirection.dx, curr.y + arrow.exitDirection.dy)
        }
        return true
    }
}
""")

# GameState.kt
write_file(os.path.join(base_dir, "GameState.kt"), """
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

    val engine = GameEngine(
        gridWidth = 6,
        gridHeight = 6,
        initialArrows = listOf(
            Arrow(1, listOf(Point(2, 4), Point(2, 3), Point(2, 2)), Direction.UP),
            Arrow(2, listOf(Point(1, 1), Point(2, 1), Point(3, 1)), Direction.RIGHT),
            Arrow(3, listOf(Point(4, 3), Point(3, 3)), Direction.LEFT),
            Arrow(4, listOf(Point(0, 5), Point(1, 5), Point(2, 5), Point(3, 5)), Direction.RIGHT)
        )
    )

    fun updateDimensions(width: Int, height: Int) {
        this.screenWidth = width
        this.screenHeight = height
        
        val boardHeight = height * 0.8f
        val startY = height * 0.2f
        
        val sizeByWidth = width / engine.gridWidth.toFloat()
        val sizeByHeight = boardHeight / engine.gridHeight.toFloat()
        cellSize = minOf(sizeByWidth, sizeByHeight) * 0.9f
        
        offsetX = (width - (engine.gridWidth * cellSize)) / 2f
        offsetY = startY + (boardHeight - (engine.gridHeight * cellSize)) / 2f
    }

    fun getGridCoords(x: Float, y: Float): Point {
        val gridX = ((x - offsetX) / cellSize).toInt()
        val gridY = ((y - offsetY) / cellSize).toInt()
        return Point(gridX, gridY)
    }
}
""")

# GameView.kt
write_file(os.path.join(base_dir, "GameView.kt"), """
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

    private val gameState = GameState()
    private val renderer = GameRenderer()
    
    private var isAnimating = false
    
    var escapingArrow: Arrow? = null
    var escapingProgress: Float = 0f
    
    var blockedArrow: Arrow? = null
    var blockedProgress: Float = 0f

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        gameState.updateDimensions(w, h)
        renderer.onSizeChanged(gameState)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (event.action == MotionEvent.ACTION_DOWN) {
            if (isAnimating) return true
            
            val pt = gameState.getGridCoords(event.x, event.y)
            if (pt.x in 0 until gameState.engine.gridWidth && pt.y in 0 until gameState.engine.gridHeight) {
                val result = gameState.engine.handleTap(pt.x, pt.y)
                handleMoveResult(result)
            } else if (gameState.engine.status != GameStatus.PLAYING) {
                gameState.engine.handleTap(-1, -1)
                invalidate()
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
                    }
                })
                anim.start()
            }
            Ignored -> {}
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        renderer.draw(canvas, gameState, this)
    }
}
""")

# GameRenderer.kt
write_file(os.path.join(base_dir, "GameRenderer.kt"), """
package com.example.arrowscape.game

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.PathMeasure

class GameRenderer {

    private val bgPaint = Paint().apply { color = Color.parseColor("#F5F5F7") }
    private val gridPaint = Paint().apply {
        color = Color.parseColor("#E0E0E0")
        style = Paint.Style.STROKE
        strokeWidth = 4f
    }
    
    private val arrowPaint = Paint().apply {
        color = Color.parseColor("#1A237E") // Dark navy
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

    private val heartPaint = Paint().apply {
        color = Color.parseColor("#E53935") // Red
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

    // Reusable objects
    private val drawPath = Path()
    private val headPath = Path()
    private val heartPath = Path()
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

        canvas.drawRect(0f, 0f, gameState.screenWidth.toFloat(), gameState.screenHeight.toFloat(), bgPaint)

        // Draw grid lines
        for (x in 0..engine.gridWidth) {
            val cx = offX + x * cs
            canvas.drawLine(cx, offY, cx, offY + engine.gridHeight * cs, gridPaint)
        }
        for (y in 0..engine.gridHeight) {
            val cy = offY + y * cs
            canvas.drawLine(offX, cy, offX + engine.gridWidth * cs, cy, gridPaint)
        }

        // Draw Hearts
        drawHearts(canvas, engine.lives, gameState.screenWidth.toFloat(), offY)

        // Draw active arrows
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

        // Draw escaping arrow animation
        view.escapingArrow?.let { arrow ->
            drawEscapingArrow(canvas, arrow, view.escapingProgress, cs, offX, offY, engine.gridWidth, engine.gridHeight)
        }

        // Draw overlays
        if (engine.status == GameStatus.WON) {
            canvas.drawColor(Color.parseColor("#99FFFFFF"))
            canvas.drawText("CLEARED!", gameState.screenWidth / 2f, gameState.screenHeight / 2f, textPaint)
        } else if (engine.status == GameStatus.GAME_OVER) {
            canvas.drawColor(Color.parseColor("#99FFFFFF"))
            val oldColor = textPaint.color
            textPaint.color = Color.parseColor("#E53935")
            canvas.drawText("GAME OVER", gameState.screenWidth / 2f, gameState.screenHeight / 2f, textPaint)
            textPaint.color = oldColor
        }
    }

    private fun drawHearts(canvas: Canvas, lives: Int, width: Float, boardTop: Float) {
        val heartRadius = 25f
        val spacing = 100f
        val startX = width / 2f - spacing
        val cy = boardTop / 2f

        for (i in 0 until 3) {
            val cx = startX + i * spacing
            heartPath.reset()
            heartPath.moveTo(cx, cy + heartRadius)
            heartPath.cubicTo(cx - heartRadius * 1.5f, cy - heartRadius * 0.5f, cx - heartRadius * 0.5f, cy - heartRadius * 1.5f, cx, cy - heartRadius * 0.5f)
            heartPath.cubicTo(cx + heartRadius * 0.5f, cy - heartRadius * 1.5f, cx + heartRadius * 1.5f, cy - heartRadius * 0.5f, cx, cy + heartRadius)
            
            if (i < lives) {
                heartPaint.color = Color.parseColor("#E53935")
            } else {
                heartPaint.color = Color.parseColor("#E0E0E0")
            }
            canvas.drawPath(heartPath, heartPaint)
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

print("View architecture applied")
