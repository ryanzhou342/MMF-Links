import PyPDF2
import re

class MmfPdf:
    def __init__(self, file):
        """
        Initializes Moncton Music Festival PDF Class, used to manipulate the PDF file
        file: string that is the path to Moncton Music Festival PDF file
        """
        try:
            self.pdfFile = open(file, "rb")
            self.pdfReader = PyPDF2.PdfFileReader(self.pdfFile)
            self.pageNumber = self.pdfReader.getNumPages()
        except FileNotFoundError:
            raise FileNotFoundError("File could not be found or does not exist.")

    def extractClassInformation(self, mmfClass):
        """
        Extracts text from each page and searches for their competition class and song names
        mmfClass: string that is the competition class the competitor is in

        Returns: List of strings that are song names, if error, returns None
        """
        # Locates competition class in the PDF file to reduce searching size
        currentPage = 0
        for pageNum in range(self.pageNumber):
            page = self.pdfReader.getPage(pageNum)
            currentPage = self.pdfReader.getPageNumber(page) + 1
            pageText = page.extractText()
            # Next page variable, in case the competitors are cut off
            nextPageText = self.pdfReader.getPage(pageNum + 1).extractText()
            competitionClass = re.search(mmfClass.upper(), pageText)
            if competitionClass:
                competitionClass = competitionClass.group()
                break

        if not competitionClass:
            print("Competition class could not be found")
            return None

        # Locates song names and appends them to list
        song = []
        songs = []
        pageText = re.split(r"[ \n]", pageText + " " + nextPageText)
        searchStart = pageText.index(competitionClass)
        searchEnd = pageText[searchStart:].index("CLASS") + searchStart
        flag = False
        regexFlag = False
        for i in range(searchStart, searchEnd):
            # Checks for beginning of piece and if a previous ____ (indicating start of piece) was found
            if "____" in pageText[i] or i == searchEnd - 1:
                regexFlag = False
                flag = True
                if song:
                    songs.append(" ".join(song).rstrip())
                    song = []
            elif flag and (pageText[i - 1] == "-" or song or regexFlag):
                if not re.match("[a-z]\.", pageText[i]):
                    song.append(pageText[i])

            # Checks in case competitor has more than one piece to play
            if re.match("[a-z]\.", pageText[i]):
                if song:
                    songs.append(" ".join(song).rstrip())
                    song = []
                regexFlag = True
        return(self.cutLastSongInfo(songs, currentPage))


    def cutLastSongInfo(self, songs, currentPage):
        locationList = ["Lewisville Middle School", "Carrefour de l’Acadie", "École Mascaret",
                        "Mount Royal United Church", "St. Paul’s United Church",
                        "Bethel Presbyterian Church", "Highfield United Baptist Church",
                        "Edith Cavell School", "Central United Church",
                        "First United Baptist Church", "Harrison Trimble High School",
                        "First Church of the Nazarene", "Salle Neil Michaud", "Church of the Nazarene"]
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # Cuts off unnecessary information from last song of the
        checkLocations = [location for location in locationList if location in songs[-1]]
        if checkLocations:
            songs[-1] = songs[-1][:songs[-1].find(checkLocations[0])]

        checkDays = [day for day in days if day in songs[-1]]
        if checkDays:
            songs[-1] = songs[-1][:songs[-1].find(checkDays[-1])]

        if "JUNIOR" in songs[-1]:
            songs[-1] = songs[-1][:songs[-1].find("JUNIOR")]

        if "SENIOR" in songs[-1]:
            songs[-1] = songs[-1][:songs[-1].find("SENIOR")]

        songs[-1] = songs[-1].rstrip()
        return(songs)
