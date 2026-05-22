-- Reset: drop tables and function before creating them
DROP FUNCTION IF EXISTS sync_resume_course_id() CASCADE;
DROP TABLE IF EXISTS inventory_items CASCADE;
DROP TABLE IF EXISTS ranking_history CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS rankings CASCADE;
DROP TABLE IF EXISTS evaluations CASCADE;
DROP TABLE IF EXISTS summaries CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS academic_years CASCADE;
DROP TABLE IF EXISTS cosmetic_items CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE cosmetic_items (
    id_item SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_points INT NOT NULL CHECK (price_points >= 0),
    description TEXT,
    item_type TEXT NOT NULL CHECK (item_type IN ('title', 'badge', 'theme', 'cosmetic'))
);

CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,  -- PostgreSQL auto-incrementing ID
    username TEXT UNIQUE NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE CHECK (registration_date <= CURRENT_DATE),
    email TEXT UNIQUE NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    profile_level INT NOT NULL DEFAULT 1 CHECK (profile_level >= 1),
    profile_points INT NOT NULL DEFAULT 0 CHECK (profile_points >= 0),
    active_item_id INT REFERENCES cosmetic_items(id_item) ON DELETE SET NULL
);

CREATE TABLE academic_years (
    id_academic_year TEXT PRIMARY KEY CHECK (id_academic_year ~ '^[0-9]{4}-[0-9]{4}$')
);

CREATE TABLE courses (
    id_course SERIAL PRIMARY KEY,
    course_name TEXT NOT NULL UNIQUE,
    faculty TEXT NOT NULL CHECK (faculty IN ('Informatics')),
    academic_year_id TEXT NOT NULL REFERENCES academic_years(id_academic_year)
);

CREATE TABLE summaries (
    id_summary SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    publication_date DATE NOT NULL DEFAULT CURRENT_DATE CHECK (publication_date <= CURRENT_DATE),
    version TEXT NOT NULL,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    average_rating NUMERIC(3,2) CHECK (average_rating >= 0 AND average_rating <= 5),
    user_id INT NOT NULL REFERENCES users(id_user),
    course_id INT NOT NULL REFERENCES courses(id_course)
);

CREATE TABLE evaluations (
    id_evaluation SERIAL PRIMARY KEY,
    note INT NOT NULL CHECK (note >= 0 AND note <= 5),
    comment TEXT,
    evaluation_date DATE NOT NULL DEFAULT CURRENT_DATE CHECK (evaluation_date <= CURRENT_DATE),
    user_id INT NOT NULL REFERENCES users(id_user),
    summary_id INT NOT NULL REFERENCES summaries(id_summary) ON DELETE CASCADE,
    UNIQUE (user_id, summary_id)
);

CREATE TABLE transactions (
    id_transaction SERIAL PRIMARY KEY,
    amount INT NOT NULL,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('gain_evaluation', 'gain_summary', 'purchase_item')),
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE CHECK (transaction_date <= CURRENT_DATE),
    user_id INT NOT NULL REFERENCES users(id_user),
    summary_id INT REFERENCES summaries(id_summary),
    evaluation_id INT REFERENCES evaluations(id_evaluation),
    item_id INT REFERENCES cosmetic_items(id_item),
    CONSTRAINT chk_transaction_amount_sign CHECK (
        (transaction_type IN ('gain_evaluation', 'gain_summary') AND amount > 0)
        OR (transaction_type = 'purchase_item' AND amount < 0)
    ),
    CONSTRAINT chk_transaction_origin CHECK (
        (transaction_type = 'gain_evaluation' AND evaluation_id IS NOT NULL)
        OR (transaction_type = 'gain_summary' AND summary_id IS NOT NULL)
        OR (transaction_type = 'purchase_item' AND item_id IS NOT NULL)
    )
);

CREATE TABLE rankings (
    id_ranking SERIAL PRIMARY KEY,
    ranking_name TEXT NOT NULL UNIQUE CHECK (ranking_name ~ '^[0-9]{4}_[0-9]{4}$')
);

-- Junction table user - ranking
CREATE TABLE ranking_history (
    user_id INT NOT NULL REFERENCES users(id_user),
    ranking_id INT NOT NULL REFERENCES rankings(id_ranking),
    rank INT NOT NULL CHECK (rank >= 1),
    period_points INT NOT NULL CHECK (period_points >= 0),
    PRIMARY KEY (user_id, ranking_id)
);


-- Junction table user - cosmetic
CREATE TABLE inventory_items (
    user_id INT NOT NULL REFERENCES users(id_user),
    item_id INT NOT NULL REFERENCES cosmetic_items(id_item),
    PRIMARY KEY (user_id, item_id)
);


-- Pertinent indexes (section 2 in pdf)
CREATE INDEX idx_summaries_user ON summaries(user_id);
CREATE INDEX idx_summaries_course ON summaries(course_id);
CREATE INDEX idx_evaluations_summary ON evaluations(summary_id);
CREATE INDEX idx_evaluations_user ON evaluations(user_id);
CREATE INDEX idx_transactions_user ON transactions(user_id);
CREATE INDEX idx_inventory_user ON inventory_items(user_id);
