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
