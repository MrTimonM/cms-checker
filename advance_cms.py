import os
import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, Style
import threading

# Clear the screen
def screen_clear():
    _ = os.system('cls')

# Color codes
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.GREEN
red = Fore.RED
res = Style.RESET_ALL

# Request headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'}

# Global variables
checked_urls = 0
wordpress_sites = []
laravel_sites = []

# Check if Laravel
def laravel_check(star):
    if "://" in star:
        star = star
    else:
        star = "http://" + star
    star = star.replace('\n', '').replace('\r', '')
    url = star + "/.env"
    check = requests.get(url, headers=headers, timeout=3)
    resp = check.text
    try:
        if "DB_HOST" in resp:
            with open("Laravel.txt", "a") as mrigel:
                mrigel.write(f'{star}\n')
                laravel_sites.append(star)
        else:
            pass
    except:
        pass

# Check if Wordpress
def wp_check(star):
    if "://" in star:
        star = star
    else:
        star = "http://" + star
    star = star.replace('\n', '').replace('\r', '')
    url = star + "/wp-content/"
    check = requests.get(url, headers=headers, timeout=3)
    try:
        if check.status_code == 200:
            with open("Wordpress.txt", "a") as mrigel:
                mrigel.write(f'{star}\n')
                wordpress_sites.append(star)
        else:
            pass
    except:
        pass

# Filter and check URLs
def url_filter(star):
    global checked_urls
    checked_urls += 1
    try:
        laravel_check(star)
        wp_check(star)
    except:
        pass

# Update and display stats
def update_stats():
    while True:
        screen_clear()
        print(f"{gr}Welcome to CMS Scanner, developed by @OlafRedSword{res}\n")
        print(f"Total URLs: {total_urls}")
        print(f"Checked URLs: {checked_urls}")
        print(f"Remaining URLs: {total_urls - checked_urls}")
        print(f"Total Wordpress sites found: {gr}{len(wordpress_sites)}{res}")
        print(f"Total Laravel sites found: {gr}{len(laravel_sites)}{res}")

        if checked_urls >= total_urls:
            break

        time.sleep(1)

    input("\nPress Enter to exit.")




# Main function
def main():
    global checked_urls
    global total_urls
    checked_urls = 0

    print(f"{gr}Welcome to CMS Scanner, developed by @OlafRedSword{res}\n")

    global list_path
    list_path = input(f"{gr}Give Me Your List.txt> {res}")

    with open(list_path, 'r') as star_file:
        stars = star_file.readlines()
        total_urls = len(stars)

    global thread_count
    thread_count = int(input(f"{gr}Enter the number of threads: {res}"))

    stats_thread = threading.Thread(target=update_stats)
    stats_thread.start()

    try:
        thread_pool = ThreadPool(thread_count)
        for _ in thread_pool.imap_unordered(url_filter, stars):
            pass

        thread_pool.close()
        thread_pool.join()

    except KeyboardInterrupt:
        thread_pool.terminate()
        thread_pool.join()
        print("\nScan interrupted by user.")

    stats_thread.join()
    input("\nPress Enter to exit.")

if __name__ == '__main__':
    screen_clear()
    main()
