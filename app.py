import streamlit as st
import sqlite3
import datetime
import pandas as pd

def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                genre TEXT,
                upload_date TEXT)''')
    conn.commit()
    conn.close()

def add_book(title, author, genre):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    upload_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO books (title, author, genre, upload_date) VALUES (?, ?, ?, ?)",
              (title, author, genre, upload_date))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT id, title, author, genre, upload_date FROM books")
    data = c.fetchall()
    conn.close()
    return data

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def main():
    st.set_page_config(page_title="Library Manager 📚", layout="wide")
    st.title("Library Manager 📚")
    
    init_db()

    menu = ["Upload Book", "View Library", "Delete Book"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Upload Book":
        st.subheader("Upload a New Book")
        with st.form("upload_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            genre = st.text_input("Genre")
            submitted = st.form_submit_button("Upload Book")
            if submitted:
                if title and author and genre:
                    add_book(title, author, genre)
                    st.success(f"✅ '{title}' uploaded successfully!")
                else:
                    st.error("Please fill all fields.")

    elif choice == "View Library":
        st.subheader("View Your Library")
        books = get_books()
        if books:
            df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Uploaded"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No books found. Upload some books!")

    elif choice == "Delete Book":
        st.subheader("Delete a Book")
        books = get_books()
        if books:
            df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Uploaded"])
            st.dataframe(df, use_container_width=True)
            book_id = st.selectbox("Select Book ID to Delete", df["ID"])
            if st.button("Delete Book"):
                delete_book(book_id)
                st.success(f"✅ Book ID {book_id} deleted successfully.")
        else:
            st.info("No books to delete.")

if __name__ == "__main__":
    main()
