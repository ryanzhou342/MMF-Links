import PyPDF2
import re

class MmfPdf:
    def __init__(self, file):
        """
        Initializes Moncton Music Festival PDF Class, used to manipulate the PDF file
        file: string that is the path to Moncton Music Festival PDF file
        """
        try:
            self.pdf_file = open(file, "rb")
            self.pdf_reader = PyPDF2.PdfFileReader(self.pdf_file)
            self.page_number = self.pdfReader.getNumPages()
        except FileNotFoundError:
            raise FileNotFoundError("File could not be found or does not exist.")

    def extract_class_information(self, mmf_class):
        """
        Extracts text from each page and searches for their competition class and song names
        mmfClass: string that is the competition class the competitor is in

        Returns: List of strings that are song names, if error, returns None
        """
        # Locates competition class in the PDF file to reduce searching size
        current_page = 0
        for page_num in range(self.page_number):
            page = self.pdfReader.getPage(page_num)
            current_page = self.pdfReader.getPageNumber(page) + 1
            page_text = page.extractText()
            # Next page variable, in case the competitors are cut off
            next_page_text = self.pdfReader.getPage(page_num + 1).extractText()
            competition_class = re.search(mmf_class.upper(), page_text)
            if competition_class:
                competition_class = competition_class.group()
                break

        if not competition_class:
            print("Competition class could not be found")
            return None

        # Locates song names and appends them to list
        song = []
        songs = []
        page_text = re.split(r"[ \n]", page_text + " " + next_page_text)
        search_start = page_text.index(competition_class)
        search_end = page_text[search_start:].index("CLASS") + search_start
        flag = False
        regex_flag = False
        for i in range(search_start, search_end):
            # Checks for beginning of piece and if a previous ____ (indicating start of piece) was found
            if "____" in page_text[i] or i == search_end - 1:
                regex_flag = False
                flag = True
                if song:
                    songs.append(" ".join(song).rstrip())
                    song = []
            elif flag and (page_text[i - 1] == "-" or song or regex_flag):
                if not re.match("[a-z]\.", page_text[i]):
                    song.append(page_text[i])

            # Checks in case competitor has more than one piece to play
            if re.match("[a-z]\.", page_text[i]):
                if song:
                    songs.append(" ".join(song).rstrip())
                    song = []
                regex_flag = True
        return(self.cut_last_song_info(songs))


    def cut_last_song_info(self, songs):
        locationList = ["Lewisville Middle School", "Carrefour de l’Acadie", "École Mascaret",
                        "Mount Royal United Church", "St. Paul’s United Church",
                        "Bethel Presbyterian Church", "Highfield United Baptist Church",
                        "Edith Cavell School", "Central United Church",
                        "First United Baptist Church", "Harrison Trimble High School",
                        "First Church of the Nazarene", "Salle Neil Michaud", "Church of the Nazarene"]
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # Cuts off unnecessary information from last song of the section
        check_locations = [location for location in locationList if location in songs[-1]]
        if check_locations:
            songs[-1] = songs[-1][:songs[-1].find(check_locations[0])]

        check_days = [day for day in days if day in songs[-1]]
        if check_days:
            songs[-1] = songs[-1][:songs[-1].find(check_days[-1])]

        if "JUNIOR" in songs[-1]:
            songs[-1] = songs[-1][:songs[-1].find("JUNIOR")]

        if "SENIOR" in songs[-1]:
            songs[-1] = songs[-1][:songs[-1].find("SENIOR")]

        songs[-1] = songs[-1].rstrip()
        return(songs)
