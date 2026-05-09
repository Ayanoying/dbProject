-- Insertion des cours
INSERT INTO courses (code_cours, nom, faculte, credits) VALUES
('INFOH100', 'Introduction à la programmation', 'Informatique', 5),
('INFOH101', 'Algorithmique', 'Informatique', 5),
('INFOH303', 'Bases de données', 'Informatique', 5),
('INFOH303', 'Structure de données', 'Informtique', '5'),
('MATH100', 'Mathématiques discrètes', 'Mathématiques', 5),
('MATH101', 'Analyse 1', 'Mathématiques', 5),
('PHYS100', 'Physique générale', 'Sciences', 5),
('ECON100', 'Introduction à l''économie', 'Économie', 5),
('LANG100', 'Anglais académique', 'Langues', 3)
ON CONFLICT (code_cours) DO NOTHING;

-- Insertion des utilisateurs
INSERT INTO utilisateurs (nom_utilisateur, email, date_inscription, niveau, nombre_points) VALUES
('alice_dupont',    'alice.dupont@univ.be',    '2025-09-15', 5, 1250),
('benoit_martin',   'benoit.martin@univ.be',   '2025-09-17', 4,  870),
('camille_leroy',   'camille.leroy@univ.be',   '2025-09-18', 7, 2100),
('david_nguyen',    'david.nguyen@univ.be',    '2025-09-20', 2,  430),
('emma_bernard',    'emma.bernard@univ.be',    '2025-09-22', 9, 3200),
('felix_moreau',    'felix.moreau@univ.be',    '2025-09-23', 1,  180),
('giulia_ferrari',  'giulia.ferrari@univ.be',  '2025-09-24', 6, 1580),
('hugo_petit',      'hugo.petit@univ.be',      '2025-09-25', 3,  650)
ON CONFLICT (nom_utilisateur) DO NOTHING;

-- Insertion des objets cosmétiques
INSERT INTO objets_cosmetiques (nom, type, description, prix) VALUES
('Débutant',         'badge',      'Attribué aux nouveaux contributeurs', 50),
('Apprenti',         'badge',      'Premier niveau de contribution',      100),
('Contributeur actif','badge',     'Publie régulièrement des résumés',    200),
('Top Contributeur', 'titre',      'Parmi les meilleurs utilisateurs',    1500),
('Maître du savoir', 'titre',      'Expert académique reconnu',           2000),
('Légende du campus','titre',      'Statut exceptionnel',                 3000),
('Profil sombre',    'theme',      'Thème sombre pour le profil',         300),
('Icône étoile',     'cosmetique', 'Icône spéciale',                      150)
ON CONFLICT DO NOTHING;

-- Insertion des résumés
INSERT INTO resumes (titre, description, date_publication, version, visibilite, note_moyenne, id_utilisateur, code_cours)
SELECT 'Introduction aux bases de données', 'Résumé complet du cours', '2025-10-01', 1, TRUE, 4.5, id_utilisateur, 'INFOH303'
FROM utilisateurs WHERE nom_utilisateur = 'alice_dupont';

-- Insertion des évaluations
INSERT INTO evaluations (note, commentaire, date_evaluation, id_auteur, id_resume)
SELECT 5, 'Très clair !', '2025-10-05',
       (SELECT id_utilisateur FROM utilisateurs WHERE nom_utilisateur = 'benoit_martin'),
       (SELECT id_resume FROM resumes WHERE titre = 'Introduction aux bases de données');

-- Insertion des transactions de points
-- Type 'publication' : points gagnés en publiant un résumé
INSERT INTO transactions (type, montant, id_utilisateur)
SELECT 'publication', 100, id_utilisateur
FROM utilisateurs WHERE nom_utilisateur = 'alice_dupont';



-- fichier qu'on lance une seule fois avec la commande psql pour pré-remplir la base avant même de lancer l'appli