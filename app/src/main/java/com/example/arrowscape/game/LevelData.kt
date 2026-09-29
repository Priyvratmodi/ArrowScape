package com.example.arrowscape.game

data class LevelTemplate(
    val id: Int,
    val width: Int,
    val height: Int,
    val arrows: List<Arrow>,
    val solutionSequence: List<Int>
)

object LevelManager {
    val levels = listOf(
        // Level 1: Small board, simple paths, obvious first moves
        LevelTemplate(1, 4, 4, listOf(
            Arrow(1, listOf(Point(0, 1), Point(1, 1)), Direction.RIGHT),
            Arrow(2, listOf(Point(1, 2)), Direction.DOWN),
            Arrow(3, listOf(Point(2, 0)), Direction.UP)
        ), listOf(1, 2, 3)),

        // Level 2: Introduce a single important blocker
        LevelTemplate(2, 4, 4, listOf(
            Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT),
            Arrow(2, listOf(Point(2, 2)), Direction.UP)
        ), listOf(1, 2)),

        // Level 3: Add multiple turns and dependencies
        LevelTemplate(3, 4, 4, listOf(
            Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT),
            Arrow(2, listOf(Point(3, 0), Point(3, 1)), Direction.DOWN),
            Arrow(3, listOf(Point(3, 2), Point(2, 2), Point(2, 3)), Direction.DOWN)
        ), listOf(3, 2, 1)),

        // Level 4: Require a deliberate escape order
        LevelTemplate(4, 5, 5, listOf(
            Arrow(1, listOf(Point(1, 2), Point(2, 2), Point(3, 2)), Direction.RIGHT),
            Arrow(2, listOf(Point(4, 1), Point(4, 2), Point(4, 3)), Direction.DOWN),
            Arrow(3, listOf(Point(3, 4), Point(4, 4)), Direction.RIGHT),
            Arrow(4, listOf(Point(2, 0), Point(2, 1)), Direction.DOWN)
        ), listOf(3, 2, 1, 4)),

        // Level 5: Introduce intersecting movement corridors
        LevelTemplate(5, 5, 5, listOf(
            Arrow(1, listOf(Point(1, 1), Point(2, 1)), Direction.RIGHT),
            Arrow(2, listOf(Point(3, 0), Point(3, 1), Point(3, 2)), Direction.DOWN),
            Arrow(3, listOf(Point(2, 3), Point(3, 3), Point(4, 3)), Direction.RIGHT),
            Arrow(4, listOf(Point(4, 1), Point(4, 0)), Direction.DOWN)
        ), listOf(3, 4, 2, 1)),

        // Level 6: Increase path complexity and dependency depth
        LevelTemplate(6, 6, 6, listOf(
            Arrow(1, listOf(Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 4)), Direction.RIGHT),
            Arrow(2, listOf(Point(3, 5), Point(3, 4), Point(3, 3)), Direction.UP),
            Arrow(3, listOf(Point(2, 1), Point(3, 1), Point(4, 1), Point(4, 2)), Direction.DOWN),
            Arrow(4, listOf(Point(4, 3), Point(5, 3)), Direction.RIGHT)
        ), listOf(4, 3, 2, 1)),

        // Level 7: Require several blockers to be cleared in sequence
        LevelTemplate(7, 6, 6, listOf(
            Arrow(1, listOf(Point(1, 1)), Direction.RIGHT),
            Arrow(2, listOf(Point(2, 2), Point(2, 1)), Direction.UP),
            Arrow(3, listOf(Point(2, 0)), Direction.RIGHT),
            Arrow(4, listOf(Point(3, 0)), Direction.DOWN),
            Arrow(5, listOf(Point(3, 1)), Direction.RIGHT),
            Arrow(6, listOf(Point(4, 1)), Direction.UP)
        ), listOf(6, 5, 4, 3, 2, 1)),

        // Level 8: Introduce tightly constrained exits
        LevelTemplate(8, 6, 6, listOf(
            Arrow(1, listOf(Point(2, 2)), Direction.RIGHT),
            Arrow(2, listOf(Point(3, 2)), Direction.DOWN),
            Arrow(3, listOf(Point(3, 3), Point(2, 3)), Direction.LEFT),
            Arrow(4, listOf(Point(1, 3)), Direction.UP),
            Arrow(5, listOf(Point(1, 1)), Direction.RIGHT),
            Arrow(6, listOf(Point(3, 1)), Direction.UP)
        ), listOf(6, 5, 4, 3, 2, 1)),

        // Level 9: Combine multiple dependency chains
        LevelTemplate(9, 7, 7, listOf(
            Arrow(1, listOf(Point(1, 2)), Direction.RIGHT),
            Arrow(2, listOf(Point(2, 2)), Direction.UP),
            Arrow(3, listOf(Point(2, 0)), Direction.LEFT),
            Arrow(4, listOf(Point(1, 4)), Direction.RIGHT),
            Arrow(5, listOf(Point(2, 4)), Direction.UP),
            Arrow(6, listOf(Point(2, 3)), Direction.LEFT)
        ), listOf(3, 6, 2, 1, 5, 4)),

        // Level 10: A challenging final puzzle combining the mechanics
        LevelTemplate(10, 8, 8, listOf(
            Arrow(1, listOf(Point(3, 3), Point(4, 3)), Direction.RIGHT),
            Arrow(2, listOf(Point(5, 3), Point(5, 2)), Direction.UP),
            Arrow(3, listOf(Point(5, 1), Point(4, 1)), Direction.LEFT),
            Arrow(4, listOf(Point(2, 1), Point(2, 2)), Direction.DOWN),
            Arrow(5, listOf(Point(2, 4), Point(3, 4)), Direction.RIGHT),
            Arrow(6, listOf(Point(5, 4), Point(5, 5)), Direction.DOWN),
            Arrow(7, listOf(Point(5, 6), Point(4, 6)), Direction.LEFT),
            Arrow(8, listOf(Point(2, 6), Point(2, 7)), Direction.DOWN),
            Arrow(9, listOf(Point(2, 3)), Direction.LEFT),
            Arrow(10, listOf(Point(5, 0)), Direction.RIGHT),
            Arrow(11, listOf(Point(5, 7)), Direction.LEFT)
        ), listOf(8, 9, 10, 11, 7, 6, 5, 4, 3, 2, 1))
    )
}
