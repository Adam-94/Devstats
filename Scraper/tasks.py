import csv

LANGUAGES = 'B:\\Desktop\\Programming\\Indeed Scraper V2\\Scraper\\languages.csv'
FRAMEWORKS = 'B:\\Desktop\\Programming\\Indeed Scraper V2\\Scraper\\frameworks.csv'
TOOLS = 'B:\\Desktop\\Programming\\Indeed Scraper V2\\Scraper\\tools.csv'

def get_statistics(stat_option, city):
    if stat_option == 'Languages':
        stat_option = LANGUAGES
    elif stat_option == 'Frameworks':
        stat_option = FRAMEWORKS
    elif stat_option == 'Tools':
        stat_option = TOOLS
    else:
        return 1

    with open(stat_option) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == city:
                return row[1:14]



