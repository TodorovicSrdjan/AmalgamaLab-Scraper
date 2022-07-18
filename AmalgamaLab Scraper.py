import bs4, time, csv, re, sys, urllib3, ssl

PROGRAM_NAME = "Amalgama-lab Scraper"

def main():
    print_program_banner()
    url = get_url()
    page_html = get_html(url)
    title, text = extract_data(page_html)
    save_to_csv(title, text)
    
    print("Done!")
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
    regex = re.compile(r"^(?:https?://)www.amalgama-lab.com/songs/[a-zA-Z0-9]/.+/.+\.html")
    
    # Loop until user enters valid url
    while True:
        url = input("Enter the URL: ")
        result = regex.search(url)
        
        if result:
            return result.group(0)
        else:
            print("Error: Invalid input!")
            
def get_html(url):
    print("Sending request...")
    
    ctx = ssl.create_default_context()
    ctx.set_ciphers('DEFAULT@SECLEVEL=1')
    http = urllib3.PoolManager(
        ssl_version=ssl.PROTOCOL_TLS,
        ssl_context=ctx)
    response = http.request("GET", url)
    
    if response.status == 200:
        print("Server response: OK")
        return response.data
    else:
        print("Server response:", response.status )
        print("Check if URL is valid and try again!")
        main()
            
def extract_data(content):
    print("Scraping data...")

    soup = bs4.BeautifulSoup( content, features = "html.parser" )
    title_original = soup.select_one('h2[class="original"]').get_text()

    title_translate = soup.select_one('h2[class="translate few"]').get_text()

    _text = str(soup.select('#click_area'))
    soup = bs4.BeautifulSoup( _text, features = "html.parser" )
    text = soup.select('.string_container')

    print(f"Found: {title_original} / {title_translate} ")
    return ( title_original, title_translate ), text

def save_to_csv(title, text):
    print("Exporting data...")

    with open(title[0]+'.csv', 'w', newline = '') as csv_file:
        csv_writer = csv.writer( csv_file )
        csv_writer.writerow( [ 'Original', 'Translate' ] )
        csv_writer.writerow( list(title) )

        for _string in text:
            original = _string.select_one('div[class="original"]').get_text()
            translate = _string.select_one('div[class="translate"]').get_text()
            csv_writer.writerow( list( ( original, translate ) ) )
    print(f"Data is successfuly exported to '{title[0]}.csv'")
    
if __name__ == '__main__':
    main()
