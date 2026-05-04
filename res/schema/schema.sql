-- Reset : si on veut recréer la base depuis 0 <=> le fichier efface tout avant de recréer 
DROP TABLE IF EXISTS historique_classement CASCADE;
DROP TABLE IF EXISTS inventaire_objets CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS classements CASCADE;
DROP TABLE IF EXISTS evaluations CASCADE;
DROP TABLE IF EXISTS resumes CASCADE;
DROP TABLE IF EXISTS objets_cosmetiques CASCADE;
DROP TABLE IF EXISTS utilisateurs CASCADE;
DROP TABLE IF EXISTS courses CASCADE;



CREATE TABLE courses (
    code_cours TEXT PRIMARY KEY,
    nom TEXT,
    faculte TEXT,
    credits INT
);


CREATE TABLE utilisateurs (
    id_utilisateur  SERIAL PRIMARY KEY, --  PostgreSQL le génère automatiquement
    nom_utilisateur TEXT UNIQUE NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    date_inscription DATE NOT NULL DEFAULT CURRENT_DATE,
    niveau          INT  NOT NULL DEFAULT 1 CHECK (niveau >= 1),
    nombre_points   INT  NOT NULL DEFAULT 0  CHECK (nombre_points >= 0)
);


CREATE TABLE objets_cosmetiques (
    id_objet    SERIAL PRIMARY KEY,
    nom         TEXT NOT NULL,
    type        TEXT NOT NULL CHECK (type IN ('badge', 'titre', 'theme', 'cosmetique')),
    description TEXT,
    prix        INT  NOT NULL CHECK (prix >= 0)
);


CREATE TABLE resumes (
    id_resume        SERIAL PRIMARY KEY,
    titre            TEXT    NOT NULL,
    description      TEXT,
    date_publication DATE    NOT NULL DEFAULT CURRENT_DATE,
    version          INT     NOT NULL DEFAULT 1 CHECK (version >= 1),
    visibilite       BOOLEAN NOT NULL DEFAULT TRUE,
    note_moyenne     NUMERIC(3,2) CHECK (note_moyenne >= 0 AND note_moyenne <= 5),
    id_utilisateur   INT     NOT NULL REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
    code_cours       TEXT    NOT NULL REFERENCES courses(code_cours)
);

CREATE TABLE evaluations (
    id_evaluation    SERIAL PRIMARY KEY,
    note             INT  NOT NULL CHECK (note >= 0 AND note <= 5),
    commentaire      TEXT,
    date_evaluation  DATE NOT NULL DEFAULT CURRENT_DATE,
    id_auteur        INT  NOT NULL REFERENCES utilisateurs(id_utilisateur),
    id_resume        INT  NOT NULL REFERENCES resumes(id_resume) ON DELETE CASCADE,
    UNIQUE (id_auteur, id_resume)
);


CREATE TABLE transactions (
    id_transaction   SERIAL PRIMARY KEY,
    type             TEXT      NOT NULL CHECK (type IN ('publication', 'evaluation', 'achat')),
    date_transaction TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    montant          INT       NOT NULL,
    id_utilisateur   INT       NOT NULL REFERENCES utilisateurs(id_utilisateur),
    id_evaluation    INT       REFERENCES evaluations(id_evaluation),
    id_objet         INT       REFERENCES objets_cosmetiques(id_objet)
);

-- relation possède + active 
CREATE TABLE inventaire_objets (
    id_utilisateur INT     NOT NULL REFERENCES utilisateurs(id_utilisateur),
    id_objet       INT     NOT NULL REFERENCES objets_cosmetiques(id_objet),
    date_achat     DATE    NOT NULL DEFAULT CURRENT_DATE,
    actif          BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_utilisateur, id_objet)
);


CREATE TABLE classements (
    id_classement SERIAL PRIMARY KEY,
    type          TEXT NOT NULL CHECK (type IN ('mensuel', 'annuel')),
    periode       TEXT NOT NULL,
    UNIQUE (type, periode)
);


CREATE TABLE historique_classement (
    id_historique  SERIAL PRIMARY KEY,
    rang           INT NOT NULL CHECK (rang > 0),
    points         INT NOT NULL,
    id_utilisateur INT NOT NULL REFERENCES utilisateurs(id_utilisateur),
    id_classement  INT NOT NULL REFERENCES classements(id_classement),
    UNIQUE (id_utilisateur, id_classement)
);

-- index pertinents (section 2 : création)
CREATE INDEX idx_resumes_cours         ON resumes(code_cours);
CREATE INDEX idx_resumes_utilisateur   ON resumes(id_utilisateur);
CREATE INDEX idx_evaluations_resume    ON evaluations(id_resume);
CREATE INDEX idx_evaluations_auteur    ON evaluations(id_auteur);
CREATE INDEX idx_transactions_user     ON transactions(id_utilisateur);
CREATE INDEX idx_inventaire_user       ON inventaire_objets(id_utilisateur);