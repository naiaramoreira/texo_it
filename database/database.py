from typing import Optional
import sqlite3
import csv
import pandas as pd

conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

def create_movies_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        year INTEGER,
        title TEXT,
        studios TEXT,
        producers TEXT,
        winner BOOLEAN
    )
    ''')

def add_movie(movie):
    cursor.execute("INSERT INTO movies (year, title, studios, producers, winner) VALUES (?, ?, ?, ?, ?)",
                   (movie.year, movie.title, movie.studios, movie.producers, movie.winner))
    conn.commit()

def update_movie(movie_id, movie):
    cursor.execute("UPDATE movies SET year = ?, title = ?, studios = ?, producers = ?, winner = ? WHERE id = ?",
                   (movie.year, movie.title, movie.studios, movie.producers, movie.winner, movie_id))
    conn.commit()
    return cursor.rowcount

def delete_movie(movie_id):
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    return cursor.rowcount

def get_movies():
    cursor.execute("SELECT * FROM movies")
    return cursor.fetchall()

def get_movie_by_title_or_year(title: Optional[str] = None, year: Optional[int] = None):
    query = "SELECT * FROM movies WHERE "
    params = []
    
    if title and year:
        query += "title LIKE ? AND year = ?"
        params.extend([f'%{title}%', year])
    elif title:
        query += "title LIKE ?"
        params.append(f'%{title}%')
    elif year:
        query += "year = ?"
        params.append(year)
    else:
        return []

    cursor.execute(query, params)
    return cursor.fetchall()

def calculate_intervals():
    movies = get_movies()
    columns = [column[0] for column in cursor.description]
    movies_df = pd.DataFrame(movies, columns=columns)

    winners_df = movies_df[movies_df['winner'] == 'yes'].copy()
    winners_df['producers'] = winners_df['producers'].str.split(',| and ')
    winners_expanded = winners_df.explode('producers').reset_index(drop=True)
    winners_expanded['producers'] = winners_expanded['producers'].str.strip()
    winners_expanded = winners_expanded.sort_values(['producers', 'year'])
    winners_expanded['previous_win'] = winners_expanded.groupby('producers')['year'].shift(1)
    winners_expanded['interval'] = winners_expanded['year'] - winners_expanded['previous_win']
    
    min_interval_value = winners_expanded['interval'].min()
    max_interval_value = winners_expanded['interval'].max()
    
    min_intervals = winners_expanded[winners_expanded['interval'] == min_interval_value]
    max_intervals = winners_expanded[winners_expanded['interval'] == max_interval_value]
    
    result = {
        "min": min_intervals[['producers', 'interval', 'previous_win', 'year']].to_dict('records'),
        "max": max_intervals[['producers', 'interval', 'previous_win', 'year']].to_dict('records')
    }
    
    for entry in result['min'] + result['max']:
        entry['interval'] = int(entry['interval'])
        entry['previousWin'] = int(entry['previous_win'])
        entry['followingWin'] = int(entry.pop('year'))
    
    return result

def load_movies_from_csv():
    with open('/app/movielist.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            cursor.execute('''
            INSERT INTO movies (year, title, studios, producers, winner)
            VALUES (?, ?, ?, ?, ?)
            ''', (row['year'], row['title'], row['studios'], row['producers'], row['winner']))


create_movies_table()
load_movies_from_csv()     
