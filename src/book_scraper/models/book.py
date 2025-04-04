class Book:
    def __init__(self, title, price, rating, availability, category, url=None, image_url=None, description=None):
        self.title = title
        self.price = price
        self.rating = rating
        self.availability = availability
        self.category = category
        self.url = url
        self.image_url = image_url
        self.description = description

    def __str__(self):
        return f"{self.title} (£{self.price}) - {self.rating} stars"

    def to_dict(self):
        """Convert book object to dictionary for easy JSON serialization"""
        return {
            "title": self.title,
            "price": self.price,
            "rating": self.rating,
            "availability": self.availability,
            "category": self.category,
            "url": self.url,
            "image_url": self.image_url,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Book object from a dictionary"""
        return cls(
            title=data.get("title"),
            price=data.get("price"),
            rating=data.get("rating"),
            availability=data.get("availability"),
            category=data.get("category"),
            url=data.get("url"),
            image_url=data.get("image_url"),
            description=data.get("description")
        )
