import psycopg2
from psycopg2 import sql

# Actors data
actors_data = [
    ('John Doe', 35, 'Male'),
    ('Jane Smith', 28, 'Female'),
    ('Chris Johnson', 42, 'Male'),
    ('Alice Brown', 31, 'Female'),
    ('David White', 25, 'Male'),
    ('Emma Davis', 40, 'Female'),
    ('Michael Harris', 50, 'Male'),
    ('Olivia Clark', 22, 'Female'),
    ('James Lewis', 37, 'Male'),
    ('Sophia Walker', 29, 'Female')
]

# Movies data
movies_data = [
    ('The Great Adventure', '2020-07-15'),
    ('Mystery in the Forest', '2021-05-20'),
    ('Comedy Night', '2019-10-10'),
    ('Drama on the Rise', '2022-02-01'),
    ('Sci-Fi Revolution', '2023-09-30')
]

# Function to load actors data
def load_actors(cursor):
    insert_actor_query = sql.SQL("""
        INSERT INTO actors (name, age, gender)
        VALUES (%s, %s, %s)
    """)
    
    try:
        for actor in actors_data:
            cursor.execute(insert_actor_query, actor)
        print("Actors data loaded successfully.")
    except Exception as e:
        print(f"Error inserting actors data: {e}")

# Function to load movies data
def load_movies(cursor):
    insert_movie_query = sql.SQL("""
        INSERT INTO movies (title, release_date)
        VALUES (%s, %s)
    """)
    
    try:
        for movie in movies_data:
            cursor.execute(insert_movie_query, movie)
        print("Movies data loaded successfully.")
    except Exception as e:
        print(f"Error inserting movies data: {e}")

# Main function to connect to the database and load data
def main():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            'postgres://ue43atj86hka51:pe732cda53eb7d3ee1d7cee7ba2973d92237b66a0045f7c721f6bbc31b7f7db33@c1i13pt05ja4ag.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d3hpjprn5alqim'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Load actors and movies data
        load_actors(cursor)
        load_movies(cursor)

        # Close the connection
        cursor.close()
        conn.close()
        print("Data loading completed.")
    
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == '__main__':
    main()
