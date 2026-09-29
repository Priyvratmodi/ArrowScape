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
