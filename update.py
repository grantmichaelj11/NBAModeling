import scraper_controller as scraper
import sql_write_commands as sql
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def scrape_stats(year, month = None, day = None, db='nba'): 
    
    boxscores = sql.retrieve_boxscores(year, month, day, database=db)

    for boxscore in boxscores:
        print(boxscore)
        id, url = boxscore
        scraper.populate_game_stats(id, url)


def run(year, month, day, update_seasons=True, start_year=2024, end_year=2025, db='nba'):
    
    if update_seasons:
        scraper.get_boxscores_year(start_year, end_year, database=db)

    scrape_stats(year, month, day)


if __name__ == "__main__":
    for i in range(13,32):
        run(2024, 12, i, update_seasons=False)
    run(2025, "01", day=None, update_seasons=False)
        
        
        
        
