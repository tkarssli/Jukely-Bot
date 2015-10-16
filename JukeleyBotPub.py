import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import sys, time

def main():

    # Start time
    startTime = int(time.time())

    # Get User Information
    email = raw_input("Enter your email: ")
    password = raw_input("enter your password: ")
    url = raw_input("Enter the URL for the event \n Example -> https://www.jukely.com/s/ef7765: ")
    n_hours = raw_input("Enter the number of hours to try to claim for: ")
    endTime = int((3600 * float(n_hours))) + startTime

    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    br.open('https://www.jukely.com/log_in')

    # Select the only Form
    br.form = list(br.forms())[0]

    # User credentials
    br.form['username'] = email
    br.form['password'] = password

    # Login
    emailResponse = br.submit()

    # Check for bad password or email
    
    soup = BeautifulSoup(emailResponse.read())
    cols = soup.findAll('li', attrs={"class" : 'flash error'})
    try:
        resp = cols[0].renderContents()
    except IndexError:
        pass

    if resp == "Whoops, username or password didn&#39;t match. Wanna try again?":
        x = raw_input("You entered a bad email or password, press enter to exit")
        sys.exit()
        


    # Start Claim loop
    count = 0; 
    while int(time.time()) < endTime:

    
        # Attempt to Claim
        ##  Example URL:  https://www.jukely.com/s/ef7765/unlimited_rsvp
        response1 = br.open(url + '/unlimited_rsvp')
        
        # Find Error message
        soup = BeautifulSoup(response1.read())
        cols = soup.findAll('li', attrs={"class" : 'flash error'})
        try:
            resp = cols[0].renderContents()
        except:
            x = raw_input("There was an error, oops")
            sys.exit()
     
        # Find out what to do next by error message
        if resp == 'We&#39;re sold out of our allocation for this show.':
            ++count
            print "Sold out but trying again, this was attempt " + count
            
        elif resp == 'has already been taken':
            print "You already got the tickets!"
            break
        
        elif resp == "Unable to get this pass, since you have reached your maximum number of passes.":
            print "You have tickets registered for another event"
            break
        
        else:
            ++count
            print "Registered Succesfully on attempt number " + count
            break

    x = raw_input("Press Enter to exit")
    


    

if __name__ == "__main__":
    main()
