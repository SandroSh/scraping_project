class Category:
    def __init__(self, name, url = None, book_count = 0, books = None):
        if books is None:
            books = []
        self.name = name
        self.url = url
        self.book_count = book_count
        self.books = books

    def __str__(self):
        return f"{self.name} ({self.book_count} books)"

    def to_dict(self):
        """Convert category object to dictionary for easy JSON serialization"""
        return {
            "name": self.name,
            "url": self.url,
            "book_count": self.book_count,
            "books": [book.to_dict() for book in self.books]
        }
    @classmethod
    def from_dict(cls, data):
        """Create a Category object from a dictionary"""
        return cls(
            name=data.get("name"),
            url=data.get("url"),
            book_count=data.get("book_count"),
            books=data.get("books"),
        )
