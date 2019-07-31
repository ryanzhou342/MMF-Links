import re
import PyPDF2

def main():
    mmfFileName = input("Please type in the path to your Moncton Music Festival PDF: ")


class MmfPdf():
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
            print("File could not be found or does not exist.")

    def extractClassInformation(self, mmfClass):
        """
        Extracts text from each page and searches for their competition class and song names
        mmfClass: string that is the competition class the competitor is in

        Returns: List of strings that are song names, if error, returns None
        """
        # Locates competition class in the PDF file to reduce searching size
        for pageNum in range(self.pageNumber):
            pageText = self.pdfReader.getPage(pageNum).extractText()
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
        for i in range(searchStart, searchEnd):
            if "____" in pageText[i] or i == searchEnd - 1:
                flag = True
                if song:
                    songs.append(" ".join(song))
                    song = []
            elif flag == True and (pageText[i - 1] == "-" or song):
                song.append(pageText[i])


if __name__ == "__main__":
    main()

mmfPdf = MmfPdf("D:/Downloads/2019-Greater-Moncton-Schedule.pdf")
mmfPdf.extractClassInformation("PS08B")
