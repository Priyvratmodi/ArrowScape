import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape\game"

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
                if (gameState.engine.status == GameStatus.WON) {
                    gameState.loadNextLevel()
                } else {
                    gameState.engine.handleTap(-1, -1) // Reset current level
                }
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
print("GameView updated for level progression")
