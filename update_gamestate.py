import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn\app\src\main\java\com\example\arrowscape\game"

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

    // Default to Level 1
    var currentLevelIndex = 0
        private set

    var engine = createEngineForCurrentLevel()

    private fun createEngineForCurrentLevel(): GameEngine {
        val template = LevelManager.levels[currentLevelIndex]
        return GameEngine(
            gridWidth = template.width,
            gridHeight = template.height,
            initialArrows = template.arrows
        )
    }

    fun loadNextLevel() {
        if (currentLevelIndex < LevelManager.levels.size - 1) {
            currentLevelIndex++
            engine = createEngineForCurrentLevel()
            // Recalculate dimensions based on new grid size
            updateDimensions(screenWidth, screenHeight)
        }
    }

    fun updateDimensions(width: Int, height: Int) {
        if (width == 0 || height == 0) return
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
print("GameState updated")
