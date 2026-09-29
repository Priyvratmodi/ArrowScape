import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"c:\Users\modip\Downloads\earn"

# 1. Update app/build.gradle.kts to add testing dependencies and release signing
build_gradle_path = os.path.join(base_dir, "app", "build.gradle.kts")
write_file(build_gradle_path, """
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.arrowscape"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.arrowscape"
        minSdk = 23
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    signingConfigs {
        create("release") {
            storeFile = file("../release.keystore")
            storePassword = "password"
            keyAlias = "arrowscape"
            keyPassword = "password"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    
    testImplementation("junit:junit:4.13.2")
}
""")

# 2. Create EngineTest.kt
test_dir = os.path.join(base_dir, "app", "src", "test", "java", "com", "example", "arrowscape")
write_file(os.path.join(test_dir, "EngineTest.kt"), """
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
""")

# 3. Create LevelValidationTest.kt
write_file(os.path.join(test_dir, "LevelValidationTest.kt"), """
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
""")

print("Tests and build config created")
