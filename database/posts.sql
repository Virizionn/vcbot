CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    game VARCHAR(255),
    post_num INT,
    poster VARCHAR(255),
    post_html TEXT,
    date DATE
);