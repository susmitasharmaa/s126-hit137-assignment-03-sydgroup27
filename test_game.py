"""Unit tests for the Game class using pytest."""

from game import Game


class TestGame:
    """Test suite for the Game class."""

    def test_init_success(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        assert game.score == 0
        assert game.life == 3
        assert game.altered_regions == altered_regions
        assert game.found_regions == []
        assert game.revealed is False

    def test_start_game_success(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # Simulate score increase
        game.score = 5
        
        # Start a new game
        new_regions = [(20, 20, 30, 30)]
        game.start_game(new_regions)
        
        assert game.life == 3
        assert game.found_regions == []
        assert game.altered_regions == new_regions
        assert game.revealed is False
        assert game.score == 5  # Score persists across games

    def test_guess_success(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # Guess within the region (x=30, y=30 is within 10,10 to 60,60)
        game.guess(30, 30)
        
        assert game.score == 1
        assert game.life == 3
        assert altered_regions[0] in game.found_regions

    def test_guess_success_alternative_path(self):
        """Test that multiple successful guesses increment score correctly."""
        altered_regions = [(10, 10, 50, 50), (100, 100, 40, 40)]
        game = Game(altered_regions)
        
        # First successful guess
        game.guess(30, 30)
        assert game.score == 1
        assert game.life == 3
        
        # Second successful guess
        game.guess(120, 120)
        assert game.score == 2
        assert game.life == 3
        assert len(game.found_regions) == 2

    def test_guess_success_already_found(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # First guess (correct)
        game.guess(30, 30)
        assert game.score == 1
        assert game.life == 3
        
        # Guess the same region again
        game.guess(35, 35)
        
        # Score and life should not change
        assert game.score == 1
        assert game.life == 3
        assert len(game.found_regions) == 1

    def test_guess_failed_incorrect(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # Guess outside any region
        game.guess(100, 100)
        
        assert game.score == 0
        assert game.life == 2
        assert game.found_regions == []

    def test_guess_failed_multiple_incorrect(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        game.guess(100, 100)
        assert game.life == 2
        
        game.guess(200, 200)
        assert game.life == 1
        
        game.guess(300, 300)
        assert game.life == 0

    def test_guess_failed_life_zero(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # Lose all lives
        game.guess(100, 100)
        game.guess(200, 200)
        game.guess(300, 300)
        assert game.life == 0
        
        # Try to guess after losing all lives
        game.guess(30, 30)  # This should be within the region, but not processed
        
        assert game.score == 0
        assert game.life == 0
        assert game.found_regions == []

    def test_guess_failed_revealed(self):
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # Reveal the game
        game.reveal()
        assert game.revealed is True
        
        # Try to guess after revealing
        game.guess(30, 30)  # This should be within the region, but not processed
        
        assert game.score == 0
        assert game.life == 3
        assert game.found_regions == []

    def test_guess_success_boundary_edges(self):
        # Region: (10, 10, 50, 50) means x: 10-60, y: 10-60
        altered_regions = [(10, 10, 50, 50)]
        game = Game(altered_regions)
        
        # Guess at top-left corner (inclusive)
        game.guess(10, 10)
        assert game.score == 1
        assert game.life == 3
        
        # New game for second test
        game.start_game([(10, 10, 50, 50)])
        
        # Guess at bottom-right corner (inclusive)
        game.guess(60, 60)
        assert game.score == 2
        assert game.life == 3

    def test_guess_success_alternative_multiple_regions(self):
        """Test game with multiple regions and mixed correct/incorrect guesses."""
        altered_regions = [(10, 10, 50, 50), (100, 100, 40, 40), (200, 200, 30, 30)]
        game = Game(altered_regions)
        
        # Correct guess at first region
        game.guess(30, 30)
        assert game.score == 1
        assert game.life == 3
        
        # Incorrect guess
        game.guess(150, 150)
        assert game.score == 1
        assert game.life == 2
        
        # Correct guess at second region
        game.guess(110, 110)
        assert game.score == 2
        assert game.life == 2
        
        # Correct guess at third region
        game.guess(210, 210)
        assert game.score == 3
        assert game.life == 2

    def test_start_game_success_score_persists(self):
        """Test that score persists across multiple game sessions."""
        altered_regions1 = [(10, 10, 50, 50)]
        game = Game(altered_regions1)
        
        # First game
        game.guess(30, 30)
        assert game.score == 1
        
        # Start new game
        altered_regions2 = [(100, 100, 40, 40)]
        game.start_game(altered_regions2)
        
        # Score should persist
        assert game.score == 1
        assert game.life == 3
        
        # Second game
        game.guess(110, 110)
        assert game.score == 2

    def test_getters_success(self):
        altered_regions = [(5, 5, 10, 10)]
        game = Game(altered_regions)

        state = game.get_game_state()
        assert state["score"] == 0
        assert state["life"] == 3
        assert state["found_regions"] == []
        assert state["revealed"] == False

        assert game.get_all_altered_regions() == altered_regions
        assert game.get_revealed() == False
    def test_reveal_success(self):
        altered_regions = [(5, 5, 10, 10)]
        game = Game(altered_regions)

        game.reveal()

        assert game.revealed is True
