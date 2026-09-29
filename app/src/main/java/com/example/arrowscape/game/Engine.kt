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
