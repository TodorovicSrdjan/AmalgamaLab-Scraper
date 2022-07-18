import requests, bs4, time, csv, re, sys

PROGRAM_NAME = "Amalgama-lab Scraper"

def main():
    print_program_banner()
    url = get_url()

    print("Sending request...")
    try:
        res = requests.request( 'GET', url )
        
    except:
        print('Web site status: does not exist')



    if res.status_code != requests.codes.ok:
        print("Server response:", res.status_code )
        print("Check if URL is valid and try again!")
        main()
    else:
        print("Server response: OK")
        
    print("Scraping data...")

    soup = bs4.BeautifulSoup( res.text, features = "html.parser" )
    _title_original = soup.select_one('h2[class="original"]')
    title_original = _title_original.get_text()

    _title_translate = soup.select_one('h2[class="translate few"]')
    title_translate = _title_translate.get_text()

    title = ( title_original, title_translate )

    _text = soup.select('#click_area')
    soup = bs4.BeautifulSoup( str(_text), features = "html.parser" )
    text=soup.select('.string_container')

    print("Found:", title[0],r' / ', title[1] )
    print("Extracting data...")

    csv_file = open( title[0]+'.csv', 'w', newline = '' )
    csv_writer = csv.writer( csv_file )
    csv_writer.writerow( [ 'Original', 'Translate' ] )
    csv_writer.writerow( list(title) )

    for _string in text:
        original = _string.select_one('div[class="original"]').get_text()
        translate = _string.select_one('div[class="translate"]').get_text()
        csv_writer.writerow( list( ( original, translate ) ) )
    print("Done!")
    csv_file.close()
    sys.exit()
    
'''
Prints out program banner
'''
def print_program_banner():
    l = len(PROGRAM_NAME)
    print( "="*(l+4), "= "+PROGRAM_NAME+" =", "="*(l+4), sep='\n' )
    
    # suppress error messages
    #sys.stderr = object

'''
Promts user for URL until valid URL is passed. URL is considered valid if it matches right 
endpoint which is defind with regular expression

:return: valid URL for a song
'''
def get_url():
    regex = re.compile("^https://www.amalgama-lab.com/songs/[a-zA-Z0-9]/.+/.+\.html")
    
    # Loop until user enters valid url
    while True:
        url = input("Enter the URL: ")
        result = regex.search(url)
        
        if result:
            return result.group(0)
        else:
            print("Error: Invalid input!")
    
if __name__ == '__main__':
    main()
