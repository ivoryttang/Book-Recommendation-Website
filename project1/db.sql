CREATE table book (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    year INT NOT NULL,
    author VARCHAR NULL
);

CREATE table book_review (
    id SERIAL PRIMARY KEY,
    review VARCHAR NOT NULL,
    rating INT NOT NULL,
    reviewer VARCHAR NOT NULL,
    book_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES book(id)
);