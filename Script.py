from ValidateClass import ValidateClass
import datetime
import os
from Database import Database

def cls():
    os.system('cls')
#Create connection with the database
db = Database(dbname="biblioteka", user="postgres", password="test123")

#Loop to keep the application active
is_active = True
while is_active:
    #Main menu
    print("Type number with the task you want to perform.")
    print("1. Show all books.")
    print("2. Create new book.")
    print("3. Edit a book.")
    print("4. Delete a book.")
    print("5. Insert 5 example books.")
    print("6. Exit application.")
    task_input = input().strip()
    #Converting input to use the main menu
    try:
        task = int(task_input)
    except ValueError:
        cls()
        print("Input must be a number!")
        continue
    #Show books
    if task == 1:
        cls()
        print("List of books:")
        #Print all books from database
        try:
            db.connect()
            query = "SELECT * FROM ksiazki"
            db.cursor.execute(query)
            rows = db.cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Release year: {row[3]}, ISBN code: {row[4]}")

        except Exception as e:
            print("An error occured", e)
        finally:
            db.close()
        input("Press Enter to continue...")
        cls()
    #Add new book
    elif task == 2:
        #Input title
        cls()
        print("Write book's title.")
        title = input().strip()
        while not title:
            cls()
            print("The title cannot be empty\nWrite book's title.")
            title = input().strip()
        cls()
        
        #Input author
        print("Write book's author.")
        author = input().strip()
        while not author:
            cls()
            print("The author cannot be empty\nWrite author's name.")
            author = input().strip()
        cls()
        
        #Input release year
        is_date_a_number = False
        while not is_date_a_number:
            print("Write book's release year.")
            release_input = input().strip()
            try:
                release = int(release_input)
            except ValueError:
                cls()
                print("Input must be a number!")
                continue
            is_date_a_number = True
        cls()
        
        #Input isbn code
        isbn = ValidateClass.check_ISBN()
        cls()
        #Add book with the previously inserted values
        try:
            db.connect()
            query = "INSERT INTO ksiazki(title, author, releaseDate, isbn) VALUES (%s, %s, %s, %s)"
            params = (title, author, release, isbn)
            db.cursor.execute(query, params)
            db.connection.commit()
        except Exception as e:
            print("An error occured", e)
        finally:
            db.close()
        print("Book has been added.")
        input("Press Enter to continue...")
        cls()
    #Edit existing book
    elif task == 3:
        cls()
        #Loop to keep editing menu
        edit_active = True
        while edit_active:
            #Check if inserted valuse is a number
            print("Write book's id that will be edited")
            edit_id = input().strip()
            try:
                editId = int(edit_id)
            except ValueError:
                cls()
                print("Input must be a number!")
                continue
            #Checking if inserted id is present in database
            try:
                db.connect()  
                db.cursor.execute("SELECT * FROM ksiazki WHERE id = %s", (editId,))
                recordExists = db.cursor.fetchone()
            except Exception as e:
                print("An error occured", e)
                edit_active = False
                continue
            finally:
                db.close()
            #if there is a record with inserted id the edit menu opens
            if recordExists:
                cls()
                print("Type number with the task you want to perform.")
                print("1. Edit Title.")
                print("2. Edit Author.")
                print("3. Edit Release date.")
                print("4. Edit ISBN code.")
                print("5. Back to books menu.")
                #Saving data before editing to avoid creating 4 different sql queries depending on edited value
                title_edit = recordExists[1]
                author_edit = recordExists[2]
                date_edit = recordExists[3]
                isbn_edit = recordExists[4]
                task_edit = int(input().strip())
                #Edit title
                if task_edit == 1:
                    cls()
                    print(f"Current book's Title: {recordExists[1]}")
                    print("Type new title")
                    title_edit = input().strip()
                    while not title_edit:
                        cls()
                        print("The title cannot be empty\nWrite new book's title.")
                        title_edit = input().strip()
                    cls()
                    print("The title has been changed.")
                    input("Press Enter to continue...")
                    cls()
                    edit_active = False
                #Edit author
                elif task_edit == 2:
                    cls()
                    print(f"Current book's Author: {recordExists[2]}")
                    print("Type new author")
                    author_edit = input().strip()
                    while not author_edit:
                        cls()
                        print("The author cannot be empty\nWrite new book's author.")
                        author_edit = input().strip()
                    cls()
                    print("The author has been changed.")
                    input("Press Enter to continue...")
                    cls()
                    edit_active = False
                #Edit release year
                elif task_edit == 3:
                    cls()
                    date_edit_check = False
                    while not date_edit_check:
                        print("Write new book's release year.")
                        release_check = input().strip()
                        try:
                            date_edit = int(release_check)
                        except ValueError:
                            cls()
                            print("Input must be a number!")
                            continue
                        date_edit_check = True
                        cls()
                    
                    print("The date has been changed.")
                    input("Press Enter to continue...")
                    cls()
                    edit_active = False
                #Edit ISBN code.
                elif task_edit == 4:
                    cls()
                    print("Write new ISBN code.")
                    isbn_edit = ValidateClass.check_ISBN()
                    cls()
                    print("The ISBN code has been changed.")
                    input("Press Enter to continue...")
                    cls()
                    edit_active = False
                #Exit edit menu
                elif task_edit == 5:
                    edit_active = False
                    cls()
                
                #Editing record in database with parameters to avoid sql injection
                try:
                    db.connect()
                    query = "UPDATE ksiazki SET title = %s, author = %s, releaseDate = %s, isbn = %s WHERE id = %s"
                    params = (title_edit, author_edit, date_edit, isbn_edit, editId)
                    db.cursor.execute(query, params)
                    db.connection.commit()
                    print("The book has been updated")
                except Exception as e:
                    print("An error occurred", e)
                finally:
                    db.close()
            #If inserted if id does not have record
            else:
                cls()
                print("Book with inserted id does not exist.")
                input("Press Enter to continue...")
                edit_active = False
                cls()
    #Delete record
    elif task == 4:
        cls()
        is_delete_id_a_number = False
        while not is_delete_id_a_number:
            print("Write book's id that will be deleted or type exit to back to the main menu.")
            delete_id = input().strip()
            if delete_id.lower() != "exit":
                try:
                    deleteId = int(delete_id)
                except ValueError:
                    cls()
                    print("Input must be a number!")
                    continue
                #Checking if inserted id has record in database
                try:
                    db.connect()
                    db.cursor.execute("SELECT * FROM ksiazki WHERE id = %s", (deleteId,))
                    recordExists = db.cursor.fetchone()
                
                    if recordExists:
                        #Delete if record exists
                        query = "DELETE FROM ksiazki WHERE id=%s"
                        params= (deleteId,)
                        db.cursor.execute(query, params)
                        db.connection.commit()
                        cls()
                        print("The book has been deleted")
                        input("Press Enter to continue...")
                        is_delete_id_a_number = True
                    else:
                        #Skip if record does not exist
                        cls()
                        print("Book with inserted id does not exist.")
                        input("Press Enter to continue...")
                        is_delete_id_a_number = True
                except Exception as e:
                    print("An error occured", e)
                finally:
                    db.close()
            else:
                is_delete_id_a_number = True
        cls()
    #Insert 5 example books
    elif task == 5:
        cls()
        try:
            db.connect()
            query = (
                "INSERT INTO ksiazki(title, author, releaseDate, isbn) VALUES ('Quo Vadis', 'Henryk Sienkiewicz', '1896', '978-83-7436-124-7');"
                "INSERT INTO ksiazki(title, author, releaseDate, isbn) VALUES ('Lalka', 'Bolesław Prus', '1890', '978-83-286-0071-4');"
                "INSERT INTO ksiazki(title, author, releaseDate, isbn) VALUES ('Pan Tadeusz', 'Adam Mickiewicz', '1834', '978-83-07-00205-2');"
                "INSERT INTO ksiazki(title, author, releaseDate, isbn) VALUES ('Ferdydurke', 'Witold Gombrowicz', '1937', '978-83-08-03126-4');"
                "INSERT INTO ksiazki(title, author, releaseDate, isbn) VALUES ('Krzyżacy', 'Henryk Sienkiewicz', '1900', '978-83-218-0610-4');"
            )
            db.cursor.execute(query)
            db.connection.commit()
            db.close()
            print("Books has been added.")
            input("Press Enter to continue...")
            cls()
        except Exception as e:
            print("An error occured", e)
        finally:
            db.close()
    #Exit application
    elif task == 6:
        is_active = False
    else:
        cls()
        print("Input a proper option!")