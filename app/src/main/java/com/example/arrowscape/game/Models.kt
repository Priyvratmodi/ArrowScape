package com.example.arrowscape.game

data class Point(val x: Int, val y: Int)

enum class Direction(val dx: Int, val dy: Int, val angle: Float) {
    UP(0, -1, 270f), 
    DOWN(0, 1, 90f), 
    LEFT(-1, 0, 180f), 
    RIGHT(1, 0, 0f)
}

class Arrow(
    val id: Int,
    val path: List<Point>,
    val exitDirection: Direction
)
