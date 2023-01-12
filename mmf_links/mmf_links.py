from helpers.mmf_manipulation import MmfPdf
import bs4
import requests

def main():
    # Opens Moncton Music Festival PDF file
    file_path = input("Please provide the file path to your Moncton Music Festival PDF file: ")
    mmf_pdf = MmfPdf(file_path)

    # Manipulates the PDF file to extract song names
    class_name = input("Please provide a competition class (e.g: PS04E): ")
    songs = mmf_pdf.extract_class_information(class_name)

    for song in songs:
        response = requests.get("https://www.youtube.com/results?search_query=" + song.replace(" ", "+"))
        response.raise_for_status()
        html = bs4.BeautifulSoup(response.text, "html.parser")
        results = html.select("h3[class='yt-lockup-title'] a[href]")
        try:
            print("https://www.youtube.com" + results[0].get("href"))
        except IndexError:
            print("YouTube video could not be found for", song)

if __name__ == "__main__":
    main()
