from datetime import datetime
import sqlite3

class Database:
    def __init__(self, db_name='onepiece.db'):
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()
        
        # Create characters table only
        c.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                nickname TEXT,
                bounty TEXT,
                supplementary_details TEXT,
                crew_name TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Create crews table structure (will be populated later)
        c.execute('''
            CREATE TABLE IF NOT EXISTS crews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                total_bounty TEXT,
                member_count INTEGER,
                created_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def calculate_crew_bounty(self, characters):
        total_bounty = 0
        for member in characters:
            if isinstance(member, dict) and 'bounty' in member:
                bounty_str = member['bounty'].replace('\u20bd', '').replace(',', '').strip()
                try:
                    bounty_num = int(bounty_str)
                    total_bounty += bounty_num
                except ValueError:
                    continue
        return total_bounty

    def update_crews_data(self):
        conn = self.get_connection()
        c = conn.cursor()

        # Clear existing crew data
        c.execute('DELETE FROM crews')

        # Get all unique crews
        crews_data = c.execute('''
            SELECT DISTINCT crew_name
            FROM characters 
            WHERE crew_name IS NOT NULL
            GROUP BY crew_name
        ''').fetchall()

        timestamp = datetime.now()
        
        for (crew_name,) in crews_data:
            characters = c.execute('''
                SELECT name, nickname, bounty, supplementary_details 
                FROM characters 
                WHERE crew_name = ?
            ''', (crew_name,)).fetchall()
            
            char_dicts = [
                {
                    'name': char[0],
                    'nickname': char[1],
                    'bounty': char[2],
                    'supplementary details': char[3]
                }
                for char in characters
            ]
            
            total_bounty = self.calculate_crew_bounty(char_dicts)
            member_count = len(char_dicts)

            c.execute('''
                INSERT INTO crews 
                (name, total_bounty, member_count, created_at)
                VALUES (?, ?, ?, ?)
            ''', (crew_name, f"{total_bounty:,}", member_count, timestamp))

        conn.commit()
        conn.close()

    def store_bounties(self, bounties):
        conn = self.get_connection()
        c = conn.cursor()
        timestamp = datetime.now()
        
        try:
            # Clear existing character data
            c.execute('DELETE FROM characters')
            
            for crew_name, characters in bounties.items():
                for char in characters:
                    if isinstance(char, dict):
                        c.execute('''
                            INSERT INTO characters 
                            (name, nickname, bounty, supplementary_details, crew_name, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            char.get('name', ''),
                            char.get('nickname', ''),
                            char.get('bounty', ''),
                            char.get('supplementary details', ''),
                            crew_name,
                            timestamp
                        ))
            conn.commit()
            
            # Update crews data once after all characters are stored
            self.update_crews_data()
            
        finally:
            conn.close()

    def get_all_bounties(self):
        conn = self.get_connection()
        c = conn.cursor()
        
        result = {}
        try:
            crews = c.execute('SELECT name, total_bounty FROM crews').fetchall()
            
            for crew_name, total_bounty in crews:
                characters = c.execute('''
                    SELECT name, nickname, bounty, supplementary_details 
                    FROM characters 
                    WHERE crew_name = ?
                ''', (crew_name,)).fetchall()
                
                result[crew_name] = {
                    'total_bounty': total_bounty,
                    'members': [
                        {
                            'name': char[0],
                            'nickname': char[1],
                            'bounty': char[2],
                            'supplementary details': char[3]
                        }
                        for char in characters
                    ]
                }
        finally:
            conn.close()
        return result
