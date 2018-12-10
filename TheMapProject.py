import re
import requests
import webbrowser

url = 'https://www.google.com/maps/place/'
places = {}

def get_coordinates(location):

    """
    This function is used to search in content of page and find the numeric coordinates of the location (argument)
    It makes a get request on the url, transform as text the content of page and than search for the pattern.
    Using @re  and @requests library
    :rtype: String
    :param location:
    :return coordinates:
    """

    location = url + location
    r = requests.get(location)
    page = r.text
    m = re.search('maps\.google\.com/maps/api/staticmap\?center=', page)
    start = m.start()
    end = start + 100
    ongoing = page[start:end]
    m = re.search("=", ongoing)
    start = m.start() + 1
    ongoing2 = ongoing[start:]
    m = re.search("&amp;", ongoing2)
    end = m.start()
    final = ongoing2[0:end]
    final = final.replace("%2C", ",")
    return final


def get_coordinates2(location):
    """
    :usage: get_coordinates2 (string @location:)
    This function is used to search in content of page and find the numeric coordinates of the location (argument)
    It makes a get request on the url, transform as text the content of page and than search for the pattern.
    Using @re  and @requests library
    :rtype: String
    :param location:
    :return coordinates as string :
    """
    location = url + location
    r = requests.get(location)
    page = r.text
    m = re.search(';window\.APP_INITIALIZATION_STATE=\[\[\[', page)
    start = m.start()
    end = start + 92
    ongoing = page[start:end]
    m = re.search(",", ongoing)
    start = m.start() + 1
    ongoing2 = ongoing[start:]
    m = re.search("]", ongoing2)
    end = m.start()
    final = ongoing2[0:end]
    final = final.replace("%2C", ",")
    a = final.split(",")
    return a[1] + "," + a[0]


def save_location(total):
    """
    Simple function to save location as user prefer,
    the locations are store on dict() as: key - name os location, value - the numerical coordinates.
    :param total: string
    :return: append dict()
    """
    places[input("Insert the name to save a current location :")] = total


def search_on_map(loc):
    """
    :usage: search_on_map (string @loc:)
    This function is used to search a location given as argument,
    It makes a get request on the url with location and open the new tab on browser using function:
    webbrowser.open_new(location:).
    Using @webbrowser library
    Verify if variable loc is defined (if yes it pass, else it ask for a new location from keyboard)
    Test if location is found (get_coordinates(loc) == "0.0,0.0") "0.0,0.0" means location is not found.
    Ask if you want to save the location and call the function: save_location(get_coordinates(loc)) and if fail
    will call function: save_location(get_coordinates2(loc))because the location on google maps are presented in to ways
    :rtype: None
    :param loc: string
    :return open new tab the link: url + location
    """
    try:
        if loc:
            pass
        else:
            loc = input("Enter a location: ")
            try:
                if get_coordinates(loc) == "0.0,0.0":
                    print(f"Can't find '{loc}' as location. Try again.")
                    return False
            except AttributeError:
                pass
        location = url + loc
        webbrowser.open_new(location)
        save = str(input("Do you want to save current location ? y/n: "))
        if save.lower() == "y":
            try:
                save_location(get_coordinates(loc))
            except AttributeError:
                save_location(get_coordinates2(loc))
        elif save.lower() == "n":
            print('Thank you')
        else:
            print("Wrong answer not saving location...\n")

    except ValueError:
        print(IOError)
    except AttributeError:
        print(AttributeError)


def get_directions():
    """
    :usage: get_directions()
    This function is used to get directions, the number of direction is defined from user.
    It makes a get request on the url with directions and open the new tab on browser using function:
    webbrowser.open_new(location:).
    Using @webbrowser library
    :rtype: None
    :return open new tab the link: url + directions
    """

    try:
        link = ""
        list_of_directions = []
        nr_of_directions = int(input("How many Direction do you want to travel: "))
        if nr_of_directions == 1:
            link = "/" + str(get_coordinates(""))
            for i in range(0, nr_of_directions):
                list_of_directions.append(str(input(f'Insert the direction {i+1}: ')))
                link = link + "/"+list_of_directions[i]
        else:
            for i in range(0, nr_of_directions):
                list_of_directions.append(str(input(f'Insert the direction {i+1}: ')))
                link = link + "/"+list_of_directions[i]
        final_url = "https://www.google.com/maps/dir" + link
        webbrowser.open_new(final_url)
    except ValueError:
        print(ValueError)
        print("Please insert a valid Value !")
    except TypeError:
        print(f"The location can't be found.\n")


def search_from_save():
    """
    This function is used to search location that are save before with costume name by the user.
    Using function get_coordinates() can find the current location of user.
    It search on dict() for pattern that user hes insert, and generate the proper direction
    for function: dir_from_saved().
    :return: None
    """
    a = []
    links = ""
    print("History\n")
    print("If you want to use current location try: (blank)\n")
    if len(places) >= 1:
        for n in places.keys():
            print(n)
        a.append(input("You want to travel from: \n"))
        a.append(input('To: \n'))
        for loc in range(0, len(a)):
            if a[loc] == "":
                links = links + "/" + get_coordinates("")
            for l in places.keys():
                if a[loc] == l:
                    links = links + '/' + places[l]
        dir_from_saved(links)
    else:
        print("You don't have saved any location!")


def dir_from_saved(link):
    """
    simple function for get direction of places given as link or set of coordinates
    :param link: string
    :return: open new tab the direction of locations.
    """
    final_url = "https://www.google.com/maps/dir" + link
    webbrowser.open_new(final_url)


answer = "y"
while answer.lower() == "y":
    print('Welcome to Map-Project. Please select one option: ')
    case = input(" 0 - To search a Location.\n 1 - To get directions.\n 2 - To search from save.\n - : ")
    if case.lower() == "0":
        search_on_map(False)
    elif case.lower() == "1":
        get_directions()
    elif case.lower() == "2":
        search_from_save()
    else:
        print("Wrong option")
        pass
    answer = input('Do you want to do another action ? Type (y/n).')
    print("\n"*100)