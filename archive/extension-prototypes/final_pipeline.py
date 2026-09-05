"""
Final Chess Pipeline
====================
A clean, modular pipeline to get the most recent game's statistics:
- Session Count (which game number in the session)
- ELO Loss/Gain per Session
- Streak Record
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any


class ChessPipeline:
    """Main pipeline class for analyzing Chess.com player data."""
    
    def __init__(self, username: str, session_gap_minutes: int = 15):
        """
        Initialize the pipeline.
        
        Args:
            username: Chess.com username
            session_gap_minutes: Time gap in minutes to separate sessions (default: 15)
        """
        self.username = username.lower()
        self.session_gap = timedelta(minutes=session_gap_minutes)
        self.base_url = "https://api.chess.com/pub/player"
        # Chess.com API requires User-Agent header
        self.headers = {
            'User-Agent': 'ChessPipeline/1.0 (Python Chess Analysis Tool)'
        }
        
    def fetch_player_games(self) -> List[Dict[str, Any]]:
        """
        Fetch the most recent session of rated bullet games (60 or 30 seconds per side).
        Starts from the most recent game and works backwards until a 15-minute gap is found.
        
        Returns:
            List of game dictionaries from the most recent session (rated bullet games with 60/30s time control only)
        """
        print(f"Fetching games for {self.username}...")
        
        # Get list of archives (monthly archives)
        archives_url = f"{self.base_url}/{self.username}/games/archives"
        try:
            response = requests.get(archives_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            archives = response.json().get('archives', [])
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch archives: {e}")
        
        # Parse archive URLs to find the most recent month (like the hardcoded link format)
        def parse_archive_date(archive_url: str) -> tuple:
            """Extract year and month from archive URL."""
            try:
                # Extract YYYY/MM from URL
                # Format: https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}
                parts = archive_url.split('/games/')
                if len(parts) < 2:
                    return (0, 0)
                date_part = parts[1].rstrip('/')
                year_month = date_part.split('/')
                if len(year_month) >= 2:
                    year = int(year_month[0])
                    month = int(year_month[1])
                    return (year, month)
            except (ValueError, IndexError):
                pass
            return (0, 0)
        
        # Sort archives by date (year, month) to find the most recent
        archives_with_dates = [(archive, parse_archive_date(archive)) for archive in archives]
        archives_with_dates.sort(key=lambda x: x[1], reverse=True)  # Most recent first
        
        if not archives_with_dates or archives_with_dates[0][1] == (0, 0):
            raise Exception("Failed to parse archives list")
        
        # Use the most recent archive from the list
        most_recent_archive, (year, month) = archives_with_dates[0]
        
        # Build URL in the same format as the hardcoded link
        # Format: https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}
        archive_url = f"{self.base_url}/{self.username}/games/{year}/{month:02d}"
        
        print(f"Using most recent archive: {archive_url} (Year: {year}, Month: {month:02d})")
        
        try:
            response = requests.get(archive_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            archive_data = response.json()
            
            # Parse all games from this archive (only rated bullet games with 60/30s)
            games = archive_data.get('games', [])
            parsed_games = []
            for game in games:
                parsed_game = self._parse_game(game)
                if parsed_game:
                    parsed_games.append(parsed_game)
            
            print(f"Found {len(games)} total games, {len(parsed_games)} rated bullet games (60s/30s time control)")
                    
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch archive {archive_url}: {e}")
        
        if not parsed_games:
            print(f"Warning: No rated bullet games found in most recent archive")
            return []
        
        # Sort games by end time (most recent first)
        parsed_games.sort(key=lambda x: x['end_time'], reverse=True)
        
        # Start from the most recent game and work backwards
        # Stop when time delta exceeds 15 minutes
        session_games = []
        pre_session_game = None  # Game before the session starts (for ELO calculation)
        
        if parsed_games:
            # Add the most recent game
            session_games.append(parsed_games[0])
            
            # Work backwards through the sorted list
            for i in range(1, len(parsed_games)):
                current_game = parsed_games[i]
                previous_game = parsed_games[i - 1]  # More recent game
                
                # Calculate time difference (previous is more recent, so we subtract)
                time_diff = previous_game['end_datetime'] - current_game['end_datetime']
                
                # If time difference exceeds session gap, stop
                if time_diff > self.session_gap:
                    # The game before the session is the one we just checked
                    pre_session_game = current_game
                    break
                
                # Add this game to the session
                session_games.append(current_game)
            
            # Reverse to get chronological order (oldest to newest)
            session_games.reverse()
            
            print(f"Found most recent session with {len(session_games)} game(s)")
            
            # Store the pre-session game for ELO calculation
            if pre_session_game:
                # Store it as an attribute so we can access it later
                self.pre_session_game = pre_session_game
            else:
                self.pre_session_game = None
        
        return session_games
    
    def _parse_game(self, game: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse a single game from Chess.com API format.
        
        Args:
            game: Raw game data from API
            
        Returns:
            Parsed game dictionary or None if invalid, unrated, not bullet, or wrong time control
        """
        try:
            # Filter for rated games only
            if not game.get('rated', False):
                return None  # Skip unrated games
            
            # Filter for bullet games only
            time_class = game.get('time_class', '').lower()
            if time_class != 'bullet':
                return None  # Skip non-bullet games
            
            # Filter for 60 or 30 seconds per side (increment doesn't matter)
            time_control = game.get('time_control', '')
            # Time control format is typically "60" for 60 seconds, "30" for 30 seconds
            # or "60+1" for 60 seconds with 1 second increment, etc.
            try:
                # Extract the base time (before the + if increment exists)
                base_time = int(time_control.split('+')[0])
                if base_time not in [60, 30]:
                    return None  # Skip games that aren't 60 or 30 seconds per side
            except (ValueError, AttributeError):
                return None  # Skip if time control format is invalid
            
            # Determine if player is white or black
            white_username = game.get('white', {}).get('username', '').lower()
            is_white = white_username == self.username
            
            if not is_white and game.get('black', {}).get('username', '').lower() != self.username:
                return None  # Player not in this game
            
            # Get player's rating
            player_data = game.get('white' if is_white else 'black', {})
            rating = player_data.get('rating', 0)
            
            # Get opponent's username
            opponent_data = game.get('black' if is_white else 'white', {})
            opponent_username = opponent_data.get('username', 'Unknown')
            
            # Get result from player's perspective
            # Chess.com API: result field indicates what happened to this player
            # 'win' = player won, 'checkmated'/'resigned'/'timeout' = player lost, 'agreed'/'repetition'/'stalemate'/'insufficient' = draw
            result_code = player_data.get('result', '')
            
            # Convert to standard format: 1.0 = win, 0.0 = loss, 0.5 = draw
            if result_code == 'win':
                result = 1.0  # Player won
            elif result_code in ['checkmated', 'resigned', 'timeout', 'lose', 'abandoned']:
                result = 0.0  # Player lost
            elif result_code in ['agreed', 'repetition', 'stalemate', 'insufficient', 'timevsinsufficient']:
                result = 0.5  # Draw
            else:
                # Default to draw for unknown results
                result = 0.5
            
            # Get end time
            end_time = game.get('end_time', 0)
            if isinstance(end_time, int):
                end_datetime = datetime.fromtimestamp(end_time)
            else:
                # Try parsing as string if needed
                end_datetime = datetime.fromtimestamp(0)
            
            return {
                'url': game.get('url', ''),
                'end_time': end_time,
                'end_datetime': end_datetime,
                'rating': rating,
                'is_white': is_white,
                'result': result,
                'time_control': game.get('time_control', ''),
                'rules': game.get('rules', ''),
                'opponent': opponent_username
            }
            
        except Exception as e:
            print(f"Warning: Failed to parse game: {e}")
            return None
    
    def cluster_games_into_sessions(self, games: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Cluster games into sessions based on time gaps.
        
        Args:
            games: List of parsed games sorted by end time
            
        Returns:
            List of sessions, where each session is a list of games
        """
        if not games:
            return []
        
        sessions = []
        current_session = [games[0]]
        
        for i in range(1, len(games)):
            current_game = games[i]
            previous_game = games[i - 1]
            
            # Calculate time difference
            time_diff = current_game['end_datetime'] - previous_game['end_datetime']
            
            if time_diff <= self.session_gap:
                # Same session
                current_session.append(current_game)
            else:
                # New session
                sessions.append(current_session)
                current_session = [current_game]
        
        # Add final session
        if current_session:
            sessions.append(current_session)
        
        print(f"Clustered {len(games)} games into {len(sessions)} sessions")
        return sessions
    
    def calculate_games_per_session(self, sessions: List[List[Dict[str, Any]]]) -> Dict[str, int]:
        """
        Calculate how many games have been played in each session for each game.
        
        Args:
            sessions: List of game sessions
            
        Returns:
            Dictionary mapping game URL to session count (1, 2, 3, etc.)
        """
        games_per_session = {}
        
        for session in sessions:
            for idx, game in enumerate(session, start=1):
                games_per_session[game['url']] = idx
        
        return games_per_session
    
    def calculate_elo_difference_per_session(self, sessions: List[List[Dict[str, Any]]], pre_session_game: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
        """
        Calculate ELO difference per session.
        For first game in session (sesh_cnt=1): current_elo - pre_session_game_elo (game before session)
        For subsequent games: current_elo - session_start_elo (ELO before session started)
        
        Args:
            sessions: List of game sessions
            pre_session_game: The game that occurred before the session started (for accurate ELO calculation)
            
        Returns:
            Dictionary mapping game URL to ELO difference
        """
        elo_differences = {}
        
        for session in sessions:
            if not session:
                continue
            
            # Get the ELO before the session started
            # Use the pre-session game's rating if available, otherwise use the first game's rating
            if pre_session_game:
                session_start_elo = pre_session_game['rating']
            else:
                # No pre-session game, use first game's rating as baseline
                session_start_elo = session[0]['rating']
            
            # Calculate ELO difference for each game in session
            for idx, game in enumerate(session):
                if idx == 0:
                    # First game in session (sesh_cnt = 1)
                    # Use the pre-session game's rating to get accurate starting ELO
                    if pre_session_game:
                        elo_diff = game['rating'] - pre_session_game['rating']
                    else:
                        # No pre-session game - can't calculate accurate difference
                        elo_diff = 0
                else:
                    # Subsequent games in session (sesh_cnt > 1)
                    # Compare to the ELO before the session started
                    elo_diff = game['rating'] - session_start_elo
                
                elo_differences[game['url']] = elo_diff
        
        return elo_differences
    
    def calculate_streak_record(self, games: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate streak record for each game.
        Positive numbers = wins in a row
        Negative numbers = losses in a row
        Draws always reset to 1
        
        Args:
            games: List of parsed games sorted by end time
            
        Returns:
            Dictionary mapping game URL to streak value
        """
        streak_record = {}
        current_streak = 0
        previous_result = None
        
        for game in games:
            result = game['result']
            
            if result == 0.5:  # Draw
                current_streak = 1
            elif result == 1.0:  # Win
                if previous_result == 1.0:
                    current_streak += 1
                else:
                    current_streak = 1
            elif result == 0.0:  # Loss
                if previous_result == 0.0:
                    current_streak -= 1
                else:
                    current_streak = -1
            
            streak_record[game['url']] = current_streak
            previous_result = result
        
        return streak_record


def format_datetime(timestamp: int) -> str:
    """Format timestamp to readable date/time."""
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Invalid date"


def format_result(result: float) -> str:
    """Format game result for display."""
    if result == 1.0:
        return "WIN"
    elif result == 0.0:
        return "LOSS"
    elif result == 0.5:
        return "DRAW"
    else:
        return f"UNKNOWN ({result})"


def get_most_recent_game_stats(username: str) -> Optional[Dict]:
    """
    Get statistics for the most recent game played by a user.
    
    Args:
        username: Chess.com username
        
    Returns:
        Dictionary containing:
        - 'game': Game details (url, date, opponent, rating, result, etc.)
        - 'session_count': Which game number in the session (1, 2, 3, etc.)
        - 'elo_difference': ELO change (positive = gain, negative = loss)
        - 'streak': Current streak (positive = wins, negative = losses, 1 = draw)
        - 'session_games': List of all games in the same session
        
        Returns None if no games found or error occurred.
    """
    try:
        pipeline = ChessPipeline(username)
        
        # Fetch games
        games = pipeline.fetch_player_games()
        
        if not games:
            return None
        
        # Games are already sorted chronologically and represent the most recent session
        # Find most recent game (last in the list since it's sorted oldest to newest)
        most_recent_game = games[-1] if games else None
        
        if not most_recent_game:
            return None
        
        # Since we already have just the session, we can treat it as a single session
        sessions = [games]  # Wrap in a list for compatibility with existing methods
        
        # Get the pre-session game for accurate ELO calculation
        pre_session_game = getattr(pipeline, 'pre_session_game', None)
        
        # Calculate metrics
        games_per_session = pipeline.calculate_games_per_session(sessions)
        elo_differences = pipeline.calculate_elo_difference_per_session(sessions, pre_session_game)
        streak_record = pipeline.calculate_streak_record(games)
        
        # Get statistics for most recent game
        most_recent_url = most_recent_game['url']
        session_count = games_per_session.get(most_recent_url, None)
        elo_diff = elo_differences.get(most_recent_url, None)
        streak = streak_record.get(most_recent_url, None)
        
        # Session context is just the games we already have
        session_games = games
        
        return {
            'game': most_recent_game,
            'session_count': session_count,
            'elo_difference': elo_diff,
            'streak': streak,
            'session_games': session_games
        }
        
    except Exception as e:
        print(f"Error getting game statistics: {e}")
        return None


def display_most_recent_game_stats(username: str) -> bool:
    """
    Display the most recent game's statistics in the console.
    
    Args:
        username: Chess.com username
        
    Returns:
        True if successful, False otherwise
    """
    stats = get_most_recent_game_stats(username)
    
    if not stats:
        print(f"No games found for user: {username}")
        return False
    
    game = stats['game']
    session_count = stats['session_count']
    elo_diff = stats['elo_difference']
    streak = stats['streak']
    session_games = stats['session_games']
    
    print("="*70)
    print("MOST RECENT GAME STATISTICS")
    print("="*70)
    print(f"\nPlayer: {username}")
    print(f"\nGame Details:")
    print(f"  URL: {game['url']}")
    print(f"  Date/Time: {format_datetime(game['end_time'])}")
    print(f"  Color: {'White' if game['is_white'] else 'Black'}")
    print(f"  Opponent: {game.get('opponent', 'Unknown')}")
    print(f"  Rating: {game['rating']}")
    print(f"  Result: {format_result(game['result'])}")
    
    print(f"\nStatistics:")
    print(f"  1. Session Count: {session_count}")
    if session_count:
        print(f"     → This is game #{session_count} in this session")
    
    print(f"  2. ELO Difference: {elo_diff:+d}" if isinstance(elo_diff, int) else f"  2. ELO Difference: {elo_diff}")
    if isinstance(elo_diff, int):
        status = "GAIN" if elo_diff > 0 else "LOSS" if elo_diff < 0 else "NO CHANGE"
        print(f"     → {status} of {abs(elo_diff)} ELO points")
    
    print(f"  3. Streak: {streak}")
    if isinstance(streak, int):
        if streak > 0:
            print(f"     → {streak} win(s) in a row")
        elif streak < 0:
            print(f"     → {abs(streak)} loss(es) in a row")
        else:
            print(f"     → Draw (streak reset)")
    
    if session_games:
        print(f"\nSession Context:")
        print(f"  This session contains {len(session_games)} game(s):")
        for idx, session_game in enumerate(session_games, 1):
            marker = " ← MOST RECENT" if session_game['url'] == game['url'] else ""
            print(f"    {idx}. {format_datetime(session_game['end_time'])} - {session_game.get('opponent', 'Unknown')}{marker}")
    
    print("="*70)
    
    return True


def main():
    """Main function for command-line usage."""
    print("Chess.com Most Recent Game Statistics")
    print("="*70)
    
    username = input("Enter Chess.com username: ").strip()
    
    if not username:
        print("Error: Username cannot be empty")
        return
    
    display_most_recent_game_stats(username)


if __name__ == "__main__":
    main()
