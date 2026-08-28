from django.test import TestCase
from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError

from catalog.models import Author, Book, BookInstance, Genre, Language


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="Big", last_name="Bob")

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field("date_of_birth").verbose_name
        self.assertEqual(field_label, "date of birth")

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field("date_of_death").verbose_name
        self.assertEqual(field_label, "died")

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f"{author.last_name}, {author.first_name}"
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), "/catalog/author/1")


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name="Big", last_name="Bob")
        genre = Genre.objects.create(name="Fiction")
        language = Language.objects.create(name="English")
        book = Book.objects.create(
            title="Big Bob's adventures",
            author=author,
            summary="The adventures of Big Bob in Bigland.",
            isbn="9876543210123",
            language=language,
        )
        book.genre.set((genre,))
        book.save()

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("summary").verbose_name
        self.assertEqual(field_label, "summary")

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("isbn").verbose_name
        self.assertEqual(field_label, "ISBN")

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("genre").verbose_name
        self.assertEqual(field_label, "genre")

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("language").verbose_name
        self.assertEqual(field_label, "language")

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("summary").max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("isbn").max_length
        self.assertEqual(max_length, 13)

    def test_summary_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field("summary").help_text
        self.assertEqual(help_text, "Enter a brief description of the book")

    def test_isbn_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field("isbn").help_text
        self.assertEqual(
            help_text,
            "13 Character "
            '<a href="https://www.isbn-international.org/content/what-isbn">'
            "ISBN number</a>",
        )

    def test_genre_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field("genre").help_text
        self.assertEqual(help_text, "Select a genre for this book")

    def test_language_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field("language").help_text
        self.assertEqual(help_text, "Select a language for this book")

    def test_author_on_delete_restrict(self):
        book = Book.objects.get(id=1)
        self.assertRaises(RestrictedError, book.author.delete)

    def test_language_on_delete_restrict(self):
        book = Book.objects.get(id=1)
        self.assertRaises(RestrictedError, book.language.delete)

    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), str(book.title))

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), "/catalog/book/1")

    def test_display_genre_single(self):
        book = Book.objects.get(id=1)
        genre = book.genre.first()
        self.assertEqual(book.display_genre(), genre.name)

    def test_display_genre_multiple(self):
        book = Book.objects.get(id=1)
        genre_one = book.genre.first()
        genre_two = Genre.objects.create(name="Romance")
        book.genre.set((genre_one, genre_two))
        expected_displayed_genres = f"{genre_one.name}, {genre_two.name}"
        self.assertEqual(book.display_genre(), expected_displayed_genres)

    def test_ordering_by_title(self):
        language = Language.objects.get(id=1)
        book = Book.objects.get(id=1)
        book_starting_with_z = Book.objects.create(
            title="Zetta's travels", summary="The travels of Zetta", language=language
        )
        book_starting_with_a = Book.objects.create(
            title="Aurora Borealis: what is it?",
            summary="We have yet to know what it is...",
            language=language,
        )
        books = Book.objects.all()
        self.assertEqual(books[0], book_starting_with_a)
        self.assertEqual(books[1], book)
        self.assertEqual(books[2], book_starting_with_z)


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(name="Fiction")

    def test_name_label(self):
        field_label = self.genre._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.genre._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_name_help_text(self):
        help_text = self.genre._meta.get_field("name").help_text
        self.assertEqual(
            help_text, "Enter a book genre (e.g. Science Fiction, French Poetry, etc.)"
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.genre.get_absolute_url(), f"/catalog/genre-detail/1")

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name="Fiction")

    def test_name_case_insensitive_unique(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name="FICTION")
