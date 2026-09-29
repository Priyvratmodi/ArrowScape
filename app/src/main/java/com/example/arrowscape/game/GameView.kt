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
