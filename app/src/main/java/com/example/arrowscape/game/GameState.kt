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
