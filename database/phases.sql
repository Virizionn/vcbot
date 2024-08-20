CREATE TABLE phases (
    phase_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    game VARCHAR(255) NOT NULL,
    postnum INT NOT NULL,
    CONSTRAINT uc_game_postnum UNIQUE (game, postnum)
);