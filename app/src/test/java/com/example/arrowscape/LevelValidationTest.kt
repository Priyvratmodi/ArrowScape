package com.example.arrowscape

import com.example.arrowscape.game.*
import org.junit.Assert.*
import org.junit.Test

class LevelValidationTest {

    @Test
    fun testAllLevelsAreSolvable() {
        val levels = LevelManager.levels
        
        for (level in levels) {
            val engine = GameEngine(level.width, level.height, level.arrows)
            
            // Initial state checks
            assertEquals(3, engine.lives)
            assertEquals(GameStatus.PLAYING, engine.status)
            
            for (targetId in level.solutionSequence) {
                // Find the arrow
                val arrow = engine.activeArrows.find { it.id == targetId }
                assertNotNull("Level ${level.id}: Arrow $targetId not found!", arrow)
                
                // Tap on its head
                val head = arrow!!.path.last()
                val result = engine.handleTap(head.x, head.y)
                
                assertTrue("Level ${level.id}: Move for arrow $targetId failed. Expected Escaped, got $result.", result is Escaped)
            }
            
            assertEquals("Level ${level.id}: Board not cleared!", 0, engine.activeArrows.size)
            assertEquals("Level ${level.id}: Status not WON!", GameStatus.WON, engine.status)
        }
    }

    @Test
    fun testLevelArrowGeometry() {
        // Validate that no two arrows overlap initially
        val levels = LevelManager.levels
        
        for (level in levels) {
            val occupiedPoints = mutableSetOf<Point>()
            for (arrow in level.arrows) {
                for (pt in arrow.path) {
                    val isUnique = occupiedPoints.add(pt)
                    assertTrue("Level ${level.id}: Point $pt is overlapping!", isUnique)
                    
                    // Check bounds
                    assertTrue("Level ${level.id}: Point $pt is out of bounds!", pt.x in 0 until level.width && pt.y in 0 until level.height)
                }
            }
        }
    }
}
