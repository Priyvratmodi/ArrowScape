package com.example.arrowscape

import com.example.arrowscape.game.*
import org.junit.Assert.*
import org.junit.Test

class EngineTest {

    @Test
    fun testValidEscape() {
        val arrow = Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT)
        val engine = GameEngine(4, 4, listOf(arrow))
        
        val result = engine.handleTap(1, 1)
        assertTrue(result is Escaped)
        assertTrue(engine.activeArrows.isEmpty())
        assertEquals(GameStatus.WON, engine.status)
        assertEquals(3, engine.lives)
    }

    @Test
    fun testBlockedEscape() {
        val arrowA = Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT)
        val arrowB = Arrow(2, listOf(Point(2, 2)), Direction.UP) // A blocks B's exit (2,1)
        val engine = GameEngine(4, 4, listOf(arrowA, arrowB))
        
        val result = engine.handleTap(2, 2)
        assertTrue(result is Blocked)
        assertEquals(2, engine.lives)
        assertEquals(2, engine.activeArrows.size)
    }

    @Test
    fun testEmptyCellTap() {
        val arrow = Arrow(1, listOf(Point(1, 1)), Direction.RIGHT)
        val engine = GameEngine(4, 4, listOf(arrow))
        
        val result = engine.handleTap(0, 0)
        assertTrue(result is Ignored)
        assertEquals(3, engine.lives) // Lives shouldn't deduct
    }

    @Test
    fun testGameOver() {
        val arrowA = Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT)
        val arrowB = Arrow(2, listOf(Point(2, 2)), Direction.UP)
        val engine = GameEngine(4, 4, listOf(arrowA, arrowB))
        
        engine.handleTap(2, 2) // Lives: 2
        engine.handleTap(2, 2) // Lives: 1
        engine.handleTap(2, 2) // Lives: 0
        
        assertEquals(0, engine.lives)
        assertEquals(GameStatus.GAME_OVER, engine.status)
        
        // Tap after game over triggers reset, but returns Ignored
        val result = engine.handleTap(2, 2)
        assertTrue(result is Ignored)
        assertEquals(3, engine.lives) // Reset occurs
    }

    @Test
    fun testEscapedArrowNoLongerBlocks() {
        val arrowA = Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT)
        val arrowB = Arrow(2, listOf(Point(2, 2)), Direction.UP)
        val engine = GameEngine(4, 4, listOf(arrowA, arrowB))
        
        // A escapes successfully
        assertTrue(engine.handleTap(1, 1) is Escaped)
        
        // Now B should be able to escape
        assertTrue(engine.handleTap(2, 2) is Escaped)
        assertEquals(GameStatus.WON, engine.status)
    }
}
