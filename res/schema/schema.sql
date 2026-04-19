CREATE TABLE courses (
    code_cours TEXT PRIMARY KEY,
    nom TEXT,
    faculte TEXT,
    credits INT
);

CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    auteur TEXT,
    destinataire TEXT,
    code_cours TEXT,
    titre TEXT,
    note INT,
    commentaire TEXT,
    FOREIGN KEY (code_cours) REFERENCES courses(code_cours)
);
