import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from RequestGuard import RequestGuard, get_full_domain
import image_processing as ip
import sys
from urllib import parse


VALID_FLAGS = ['-c', '-p', '-i']

def verify_prompt(flag, url, outfile1, out_or_flag):
    if flag not in VALID_FLAGS:
        return False
    if not (url.startswith("https://") or url.startswith("http://")):
        return False
    
    if flag == '-i':
        if out_or_flag not in ip.IMAGE_FLAGS:
            return False
    return True


def format_url(href, full_domain, link):
    if not href:
        return None

    if href.startswith('#'):
        return link
    elif '#' in href:
        href = href.split('#')[0]

    if "mailto" in href or href.startswith('javascript:'):
        return None

    if href.startswith('http://') or href.startswith('https://'):
        href_domain = get_full_domain(href)
        if href_domain != full_domain:
            return None
        return href
    else:
        return parse.urljoin(link, href)


def count_links(url, outfile1, outfile2):
    request_guard = RequestGuard(url)
    page = request_guard.make_get_request(url)
    domain = request_guard.domain
    full_domain = request_guard.full_domain
    links_to_visit = [request_guard.url]
    visited_links_count = {}

    while len(links_to_visit) > 0:
        link = links_to_visit.pop()
        if link in visited_links_count:
            print(f"Already visited {link}")
            visited_links_count[link] += 1
        else:
            print(f"visiting now {link}")
            visited_links_count[link] = 1
            if request_guard.can_follow_link(link):
                page = request_guard.make_get_request(link)
                if page is None:
                    continue
                
                content_type = page.headers.get('Content-Type', '')
                if 'html' not in content_type.lower():
                    print(f"Skipping non-HTML content: {link}")
                    continue
                    
                html = BeautifulSoup(page.text, 'html.parser')
                for tag in html.find_all('a'):
                    href = tag.get('href')
                    formatted_href = format_url(href, full_domain, link)
                    if not formatted_href:
                        continue
                    print(f"Found link: {formatted_href}")
                    links_to_visit.append(formatted_href)
    print()
    print()
    print(f"Visited {len(visited_links_count)} links")
    print()
    print()
    for link, count in visited_links_count.items():
        print(f"{link}: {count}")
    
    # Extract the count values for the histogram
    counts = list(visited_links_count.values())
    
    # Create the histogram
    if counts:
        max_count = max(counts)
        bins = list(range(1, max_count + 2))  # Add 1 to include the max value
        
        # Generate the histogram and capture the results
        counts_hist, bins_edges, _ = plt.hist(counts, bins=bins, align='left', rwidth=0.8)
        
        # Add labels and title
        plt.xlabel('Number of References')
        plt.ylabel('Frequency')
        plt.title('Histogram of Link References')
        plt.xticks(bins[:-1])  # Use bins as x-tick locations, excluding the last bin
        
        # Save the plot to the specified file
        plt.savefig(outfile1)
        plt.close()
        
        # Write the histogram data to CSV file
        with open(outfile2, 'w') as f:
            for i in range(len(counts_hist)):
                f.write(f"{bins_edges[i]},{counts_hist[i]}\n")


def read_table_data(url, outfile1, outfile2):
    try:
        page = requests.get(url)
    except:
        print(f"url is invalid: {url}")
        sys.exit(1)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('table', {'id':'CS111-Project4b'})[0]
    data = [[], [], [], [], []]
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        for i in range(len(cols)):
            data[i].append(float(cols[i].text))
    
    x_values = data[0]
    colors = ['blue', 'green', 'red', 'black']
    for i in range(1, len(data)):
        if data[i]:
            plt.plot(x_values, data[i], color=colors[i-1])
    plt.savefig(outfile1)
    plt.close()
    
    with open(outfile2, 'w') as f:
        for i in range(len(x_values)):
            row_data = [str(x_values[i])]

            for j in range(1, len(data)):
                if i < len(data[j]):
                    row_data.append(str(data[j][i]))
            f.write(','.join(row_data) + '\n')


def modify_image(url, prefix, i_flag):
    try:
        page = requests.get(url)
    except:
        print(f"url is invalid: {url}")
        sys.exit(1)
    soup = BeautifulSoup(page.text, 'html.parser')
    images = soup.find_all('img')
    image_urls = []
    for img in images:
        src = img.get('src')
        if src:
            formatted_src = format_url(src, url, url)
            if formatted_src:
                image_urls.append(formatted_src)
    if not image_urls:
        print("No images found")
        sys.exit(1)
    for image_url in image_urls:
        image_name = image_url.split('/')[-1]
        request_guard = RequestGuard(image_url)
        response = request_guard.make_get_request(image_url, True)
        with open(image_name, 'wb') as out_file:
            out_file.write(response.content)

    for image in image_urls:
        image_name = image.split('/')[-1]
        image_obj = ip.Image(image_name)
        if i_flag == "-s":
            ip.apply_sepia(image_obj, prefix + image_name)
        elif i_flag == "-g":
            ip.apply_grayscale(image_obj, prefix + image_name)
        elif i_flag == "-m":
            ip.flip_horizontally(image_obj, prefix + image_name)
        elif i_flag == "-f":
            ip.flip_vertically(image_obj, prefix + image_name)
    
        

def main(flag, url, outfile1, out_or_flag):
    if not verify_prompt(flag, url, outfile1, out_or_flag):
        print("Invalid arguments")
        sys.exit(1)
    
    elif flag == '-c':
        outfile2 = out_or_flag
        count_links(url, outfile1, outfile2)
    
    elif flag == '-p':
        outfile2 = out_or_flag
        # read_table_data(url, outfile1, outfile2)

    elif flag == '-i':
        prefix = outfile1
        i_flag = out_or_flag
        if i_flag not in ip.IMAGE_FLAGS:
            print("Invalid image flag")
            sys.exit(1)
        # else:
        #     modify_image(url, prefix, i_flag)


if __name__ == "__main__":
    # sys.argv = [0, "-c", "https://cs111.byu.edu/Projects/project04/assets/page1.html", "outputfile1", "outputfile2"]

    if len(sys.argv) != 5:
        print("Invalid arguments")
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])