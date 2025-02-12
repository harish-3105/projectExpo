import streamlit as st


def main():
    st.title("Paper Publication Details Form")

    with st.form("paper_form"):
        st.header("Author Information")
        author_name = st.text_input("Author Name")
        if not author_name:
            st.warning("Please enter your author's name")
        co_authors = [st.text_input(f"Co-Author {i + 1}") for i in range(4)]
        author_affiliation = st.text_input("Affiliation of Author")
        co_author_affiliations = [st.text_input(f"Affiliation of Co-Author {i + 1}") for i in range(4)]
        department = st.text_input("Department")
        if not department:
            st.warning("Please enter your department")

        st.header("Paper Details")
        paper_title = st.text_input("Title of the Paper")
        if not paper_title:
            st.warning("Please enter your paper title")
        journal_name = st.text_input("Name of the Journal")
        if not journal_name:
            st.warning("Please enter your journal's name")
        month_of_publication = st.selectbox("Month of Publication",
                                            ["January", "February", "March", "April", "May", "June", "July", "August",
                                             "September", "October", "November", "December"])
        if not month_of_publication:
            st.warning("Please enter your month of publication")
        year_of_publication = st.number_input("Year of Publication", min_value=1900, max_value=2100, step=1)
        if not year_of_publication:
            st.warning("Please enter your year of publication")
        issn_number = st.text_input("ISSN Number")
        if not issn_number:
            st.warning("Please enter your ISSN number")
        journal_link = st.text_input("Link of the Journal")
        if not journal_link:
            st.warning("Please enter your journal link")
        doi_number = st.text_input("DOI Number")
        if not doi_number:
            st.warning("Please enter your DOI number")
        first_page_link = st.file_uploader("First Page of Paper (Image File)", type=["png", "jpg", "jpeg"])
        if not first_page_link:
            st.warning("Please enter your first page link")


        submitted = st.form_submit_button("Submit")
        if submitted:
            if not first_page_link and not doi_number and not journal_link and not issn_number and not issn_number and not paper_title and not department:
                st.error("Please enter all fields")
            else:
                st.write("Form submitted successfully!")
            st.write({
                "Author Name": author_name,
                "Co-Authors": co_authors,
                "Author Affiliation": author_affiliation,
                "Co-Author Affiliations": co_author_affiliations,
                "Department": department,
                "Paper Title": paper_title,
                "Journal Name": journal_name,
                "Month of Publication": month_of_publication,
                "Year of Publication": year_of_publication,
                "ISSN Number": issn_number,
                "Journal Link": journal_link,
                "DOI Number": doi_number,
                "First Page Link": first_page_link
            })


if __name__ == "__main__":
    main()
