import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from movie import Movie


DRIVER_PATH = '/Users/jules/Work/WebSemantica/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

movies = []

# driver.get('http://www.cinemalaplata.com/cartelera.aspx')
# elements = driver.find_elements_by_class_name(
#     'page-container')
# for element in elements:
#     title = element.find_element_by_css_selector(
#         'h4.shortcodes-title strong')
#     link = title.find_element_by_css_selector('a')
#     movie = Movie(title.text, link.get_property('href'))
#     movies.append(movie)
# for movie in movies:
#     driver.get(movie.link)
#     movie.genre = driver.find_element_by_id(
#         'ctl00_cph_lblGenero').text
#     movie.language = driver.find_element_by_id('ctl00_cph_lblIdioma').text
#     movie.duration = driver.find_element_by_id(
#         'ctl00_cph_lblDuracion').text
#     movie.director = driver.find_element_by_id(
#         'ctl00_cph_lblDirector').text
#     movie.cast = [x.strip() for x in driver.find_element_by_id(
#         'ctl00_cph_lblActores').text.split(',')]
#     movie.synopsis = driver.find_element_by_id(
#         'ctl00_cph_lblSinopsis').text
#     timetable = driver.find_elements_by_css_selector(
#         '#ctl00_cph_pnFunciones > div')
#     for time in timetable:
#         room = time.find_element_by_css_selector('h5 > span').text
#         schedule = time.find_elements_by_css_selector('p > span')
#         for s in schedule:
#             data = list(
#                 filter(lambda x: x != '' and x != '-', s.text.split(' ')))
#             subtitled = data.pop(0) == 'SUBTITULADA:'
#             for d in data:
#                 movie.add_time(d, room, subtitled)

driver.get('https://www.cinepolis.com.ar/')
elements = driver.find_elements_by_css_selector(
    '.featured-movies-grid-view-component.movie-grid > div')
for element in elements:
    titleElement = element.find_element_by_css_selector(
        'a')
    link = titleElement.get_attribute('href')
    title = titleElement.get_attribute('title')
    movie = Movie(title, link)
    movies.append(movie)
for movie in movies:
    driver.get(movie.link)
    print('Processing ', movie.title)
    movie.synopsis = driver.find_element_by_css_selector(
        'div#sinopsis').text
    datos = driver.find_element_by_css_selector(
        'div#tecnicos > p').get_attribute('innerHTML')
    for dato in datos.split('<br>'):
        if 'Género' in dato:
            movie.genre = dato.split(': ')[1]
        if 'Director' in dato:
            movie.director = dato.split(': ')[1]
        if 'Actores' in dato:
            movie.cast = dato.split(': ')[1].split(',')
        if 'Duración' in dato:
            movie.duration = dato.split(': ')[1]
    rooms = driver.find_elements_by_css_selector(
        '.accordion > div.card.panel')
    for r in rooms:
        room = r.find_element_by_css_selector('h2.panel-title')
        types = r.find_elements_by_css_selector(
            '.movie-showtimes-component-combination')
        for t in types:
            type_data = list(map(lambda x: x.strip(), t.find_element_by_css_selector(
                '.movie-showtimes-component-label small').get_attribute('innerHTML').split('•')))
            subtitled = 'Subtitulado' in type_data[2]
            room_with_type = room.text + ' ' + \
                type_data[0] + ' ' + type_data[1]
            schedule = t.find_elements_by_css_selector(
                'a.btn-detail-showtime')
            for s in schedule:
                time = s.get_attribute('innerHTML').strip()
                movie.add_time(time, room_with_type, subtitled)

with open('data.json', 'w') as outfile:
    serialized = list(map(lambda x: x.to_dict(), movies))
    print(serialized)
    json.dump(serialized, outfile)

driver.quit()
