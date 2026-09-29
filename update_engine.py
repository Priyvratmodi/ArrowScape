import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape\game"

# Engine.kt
write_file(os.path.join(base_dir, "Engine.kt"), """
package com.example.arrowscape.game

data class Point(val x: Int, val y: Int)

enum class Direction(val dx: Int, val dy: Int) {
    UP(0, -1), DOWN(0, 1), LEFT(-1, 0), RIGHT(1, 0)
}

class Arrow(
    val id: Int,
    initialPath: List<Point>,
    val exitDirection: Direction
) {
    var path: List<Point> = initialPath.toList()
        private set
        
    var isEscaping: Boolean = false

    fun stepEscape(boardWidth: Int, boardHeight: Int): Boolean {
        if (path.isEmpty()) return false
        val head = path.last()
        val newHead = Point(head.x + exitDirection.dx, head.y + exitDirection.dy)
        
        val newPath = mutableListOf<Point>()
        for (i in 0 until path.size - 1) {
            newPath.add(path[i + 1])
        }
        newPath.add(newHead)
        
        path = newPath.filter { it.x in 0 until boardWidth && it.y in 0 until boardHeight }
        return path.isNotEmpty()
    }
}

enum class GameStatus {
    PLAYING, WON, GAME_OVER
}

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
    
    private var timeSinceLastStep = 0L
    private val stepIntervalMs = 50L // Controls the speed of movement

    init {
        resetLevel()
    }

    fun resetLevel() {
        lives = 3
        status = GameStatus.PLAYING
        activeArrows.clear()
        initialArrows.forEach { template ->
            activeArrows.add(Arrow(template.id, template.path, template.exitDirection))
        }
    }

    fun getArrowAt(p: Point): Arrow? {
        return activeArrows.find { arrow -> arrow.path.contains(p) }
    }

    fun handleTap(x: Int, y: Int) {
        if (status != GameStatus.PLAYING) {
            resetLevel()
            return
        }
        
        // Prevent action while any arrow is actively resolving its move
        if (activeArrows.any { it.isEscaping }) return
        
        val target = getArrowAt(Point(x, y)) ?: return
        
        if (isExitClear(target)) {
            target.isEscaping = true
        } else {
            lives -= 1
            if (lives <= 0) {
                status = GameStatus.GAME_OVER
            }
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

    fun update(deltaTimeMs: Long) {
        if (status != GameStatus.PLAYING) return
        
        val escapingArrows = activeArrows.filter { it.isEscaping }
        if (escapingArrows.isEmpty()) return
        
        timeSinceLastStep += deltaTimeMs
        if (timeSinceLastStep >= stepIntervalMs) {
            timeSinceLastStep = 0L
            val toRemove = mutableListOf<Arrow>()
            escapingArrows.forEach { arrow ->
                val stillOnBoard = arrow.stepEscape(gridWidth, gridHeight)
                if (!stillOnBoard) {
                    toRemove.add(arrow)
                }
            }
            activeArrows.removeAll(toRemove)
            
            if (activeArrows.isEmpty() && status == GameStatus.PLAYING) {
                status = GameStatus.WON
            }
        }
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

    fun updateScreenDimensions(width: Int, height: Int) {
        this.screenWidth = width
        this.screenHeight = height
        
        val sizeByWidth = width / engine.gridWidth.toFloat()
        val sizeByHeight = height / engine.gridHeight.toFloat()
        cellSize = minOf(sizeByWidth, sizeByHeight) * 0.9f // 10% total padding
        
        offsetX = (width - (engine.gridWidth * cellSize)) / 2f
        offsetY = (height - (engine.gridHeight * cellSize)) / 2f
    }

    fun update(deltaTimeMs: Long) {
        engine.update(deltaTimeMs)
    }
    
    fun processTap(x: Float, y: Float) {
        val gridX = ((x - offsetX) / cellSize).toInt()
        val gridY = ((y - offsetY) / cellSize).toInt()
        
        if (gridX in 0 until engine.gridWidth && gridY in 0 until engine.gridHeight) {
            engine.handleTap(gridX, gridY)
        } else if (engine.status != GameStatus.PLAYING) {
            engine.handleTap(-1, -1) // Trigger reset if tapped out of bounds during game over/won
        }
    }
}
""")

# GameView.kt
write_file(os.path.join(base_dir, "GameView.kt"), """
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

    fun update(deltaTimeMs: Long) {
        gameState.update(deltaTimeMs)
    }

    override fun draw(canvas: Canvas) {
        super.draw(canvas)
        canvas.drawColor(Color.parseColor("#121212")) // Dark background
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

# GameLoop.kt
write_file(os.path.join(base_dir, "GameLoop.kt"), """
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
        var lastTime = System.nanoTime()
        val targetTime = 1000L / 60L // Target 60 FPS

        while (isRunning) {
            startTime = System.nanoTime()
            val deltaTimeMs = (startTime - lastTime) / 1000000L
            lastTime = startTime
            
            var canvas: Canvas? = null

            try {
                canvas = surfaceHolder.lockCanvas()
                synchronized(surfaceHolder) {
                    if (canvas != null) {
                        gameView.update(deltaTimeMs)
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

            val timeMillis = (System.nanoTime() - startTime) / 1000000L
            val waitTime = targetTime - timeMillis

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

# GameRenderer.kt
write_file(os.path.join(base_dir, "GameRenderer.kt"), """
package com.example.arrowscape.game

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint

class GameRenderer {
    
    private val gridPaint = Paint().apply {
        color = Color.DKGRAY
        style = Paint.Style.STROKE
        strokeWidth = 3f
    }
    
    private val arrowPaint = Paint().apply {
        color = Color.parseColor("#4CAF50")
        style = Paint.Style.FILL
    }
    
    private val headPaint = Paint().apply {
        color = Color.parseColor("#81C784")
        style = Paint.Style.FILL
    }

    private val textPaint = Paint().apply {
        color = Color.WHITE
        isAntiAlias = true
        textSize = 60f
        textAlign = Paint.Align.CENTER
    }

    fun draw(canvas: Canvas, gameState: GameState) {
        val engine = gameState.engine
        val cs = gameState.cellSize
        val offX = gameState.offsetX
        val offY = gameState.offsetY

        // Draw grid
        for (x in 0 until engine.gridWidth) {
            for (y in 0 until engine.gridHeight) {
                val left = offX + x * cs
                val top = offY + y * cs
                canvas.drawRect(left, top, left + cs, top + cs, gridPaint)
            }
        }

        // Draw arrows
        for (arrow in engine.activeArrows) {
            for ((index, point) in arrow.path.withIndex()) {
                val isHead = index == arrow.path.size - 1
                val left = offX + point.x * cs + 4f
                val top = offY + point.y * cs + 4f
                
                canvas.drawRect(left, top, left + cs - 8f, top + cs - 8f, if (isHead) headPaint else arrowPaint)
            }
        }

        // Draw HUD
        canvas.drawText("Lives: ${engine.lives}", gameState.screenWidth / 2f, 100f, textPaint)

        // Draw Status overlays
        when (engine.status) {
            GameStatus.WON -> {
                canvas.drawColor(Color.parseColor("#88000000"))
                canvas.drawText("LEVEL CLEARED!", gameState.screenWidth / 2f, gameState.screenHeight / 2f, textPaint)
                canvas.drawText("Tap to Restart", gameState.screenWidth / 2f, gameState.screenHeight / 2f + 80f, textPaint.apply { textSize = 40f })
                textPaint.textSize = 60f // reset
            }
            GameStatus.GAME_OVER -> {
                canvas.drawColor(Color.parseColor("#88000000"))
                textPaint.color = Color.RED
                canvas.drawText("GAME OVER", gameState.screenWidth / 2f, gameState.screenHeight / 2f, textPaint)
                textPaint.color = Color.WHITE
                canvas.drawText("Tap to Restart", gameState.screenWidth / 2f, gameState.screenHeight / 2f + 80f, textPaint.apply { textSize = 40f })
                textPaint.textSize = 60f // reset
            }
            GameStatus.PLAYING -> {}
        }
    }
}
""")

print("Updates applied")
