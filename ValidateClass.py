import os
import re
class ValidateClass:
    #Check if inserted 13 digital isbn is appropriate with the standards
    @staticmethod
    def check_ISBN13(isbn):
        isbn = re.sub(r"[-\s]", "", isbn)
        if len(isbn) != 13:
            return False
        total = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(isbn))
        return total % 10 == 0
        
    #Check if inserted 10 digital isbn is appropriate with the standards
    @staticmethod
    def check_ISBN10(isbn):
        isbn = re.sub(r"[-\s]", "", isbn)
        if len(isbn) != 10:
            return False
        total = 0
        for i in range(9):
            digit = isbn[i]
            if not digit.isdigit():
                return False
            total += int(digit) * (10 - i)
        last = isbn[9]
        if last != 'X' and not last.isdigit():
            return False
        total += 10 if last == 'X' else int(last)
        return total % 11 == 0


    #Check if inserted isbn is appropriate with the standards
    @staticmethod
    def check_ISBN():
        while True:
            isbn_check = input("Write book's ISBN number. Example: 0-19-852663-6 or 978-1-4028-9462-6\n").strip()
            if ValidateClass.check_ISBN13(isbn_check) or ValidateClass.check_ISBN10(isbn_check):
                return isbn_check
            else:
                os.system('cls')
                print("Inserted ISBN code is not valid.")