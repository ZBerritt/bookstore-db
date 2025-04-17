-- Use this new sample data instead, it contains all the data for the books and stuff 
-- but doesn't create anything unnecessary like fake users/transactions. Good for when changing schema

-- Admin User
INSERT INTO User (ID, Username, Phone_Number, Password, Role, Address, Email) VALUES
(0, 'admin', '800-948-8488', 'cd916028a2d8a1b901e831246dd5b9b4d3832786ddc63bbf5af4b50d9fc98f50',
 'admin', 'The Internet', 'bookstore@chillgroup.com');

-- Insert Publishers
INSERT INTO Publisher (Email, Name) VALUES
('contact@bloomsbury.com', 'Bloomsbury'),
('release@bloomberg.net', 'Bloomberg'),
('info@penguinrandomhouse.com', 'Penguin Random House'),
('support@harpercollins.com', 'HarperCollins'),
('contact@hachettebookgroup.com', 'Hachette Book Group'),
('help@macmillan.com', 'Macmillan'),
('info@simonschuster.com', 'Simon & Schuster'),
('support@scholastic.com', 'Scholastic'),
('contact@oxfordpress.com', 'Oxford University Press'),
('info@cambridge.org', 'Cambridge University Press'),
('support@wiley.com', 'Wiley'),
('help@pearson.com', 'Pearson'),
('contact@springernature.com', 'Springer Nature'),
('info@cengage.com', 'Cengage'),
('support@mcgrawhill.com', 'McGraw Hill'),
('info@taylorandfrancis.com', 'Taylor & Francis'),
('help@elsevier.com', 'Elsevier'),
('contact@tor.com', 'Tor Books'),
('info@dk.com', 'DK Publishing'),
('support@chroniclebooks.com', 'Chronicle Books');

-- Insert Authors
INSERT INTO Author (Email, Name) VALUES
('stephenking@gmail.com', 'Stephen King'),
('jkrowling@gmail.com', 'J.K. Rowling'),
('smaas@gmail.com', 'Sarah J. Maas'),
('achristi@gmail.com', 'Agatha Christi'),
('lcarrol@gmail.com', 'Lewis Carrol'),
('realwillianshakespeare@pigeon.com', 'William Shakespeare'),
('smeyer@gmail.com', 'Stephenie Meyer'),
('cslewis@gmail.com', 'C. S. Lewis'),
('rdahl@gmail.com', 'Ronald Dahl'),
('lbardugo@gmail.com', 'Leigh Bardugo'),
('matwood@gmail.com', 'Margaret Atwood'),
('jgreen@gmail.com', 'John Green'),
('dbrown@gmail.com', 'Dan Brown'),
('acdoyle@gmail.com', 'Sir Arthur Conan Doyle'),
('edickinson@gmail.com', 'Emily Dickinson'),
('sfitzgerald@gmail.com', 'F. Scott Fitzgerald'),
('fkafka@gmail.com', 'Franz Kafka'),
('jmilton@gmail.com', 'John Milton'),
('ggarcia@gmail.com', 'Gabriel Garcia'),
('hrobbins@gmail.com', 'Harold Robbins');

-- Insert Books
INSERT INTO Book (ISBN, Title, Price, PageCount, Genre, Publisher_Email) VALUES
('9781639730957', 'Throne of Glass', 16.99, 432, 'Fantasy', 'release@bloomberg.net'),
('9781639730971', 'Crown of Midnight', 16.99, 448, 'Fantasy', 'release@bloomberg.net'),
('9781639730995', 'Heir of Fire', 16.99, 592, 'Fantasy', 'release@bloomberg.net'),
('9781639731015', 'Queen of Shadows', 16.99, 672, 'Fantasy', 'release@bloomberg.net'),
('9781639731039', 'Empire of Storms', 16.99, 720, 'Fantasy', 'release@bloomberg.net'),
('9781639731053', 'Tower of Dawn', 16.99, 688, 'Fantasy', 'release@bloomberg.net'),
('9781639731077', 'Kingdom of Ash', 16.99, 992, 'Fantasy', 'release@bloomberg.net'),
('9781639731091', 'The Assassin''s Blade', 16.99, 464, 'Fantasy', 'release@bloomberg.net'),
('9781635575569', 'A Court of Thorns and Roses', 16.99, 448, 'Fantasy', 'release@bloomberg.net'),
('9781635575583', 'A Court of Mist and Fury', 16.99, 656, 'Fantasy', 'release@bloomberg.net'),
('9781635575606', 'A Court of Wings and Ruin', 16.99, 699, 'Fantasy', 'release@bloomberg.net'),
('9781635575620', 'A Court of Frost and Starlight', 16.99, 272, 'Fantasy', 'release@bloomberg.net'),
('9781635577990', 'A Court of Silver Flames', 16.99, 768, 'Fantasy', 'release@bloomberg.net'),
('9780545790352', 'Harry Potter and the Sorcerer''s Stone', 16.99, 309, 'Fantasy', 'contact@bloomsbury.com'),
('9781781100509', 'Harry Potter and the Chamber of Secrets', 16.99, 341, 'Fantasy', 'contact@bloomsbury.com'),
('9781781100516', 'Harry Potter and the Prisoner of Azkaban', 16.99, 435, 'Fantasy', 'contact@bloomsbury.com'),
('9781408865422', 'Harry Potter and the Goblet of Fire', 16.99, 734, 'Fantasy', 'contact@bloomsbury.com'),
('9781781100530', 'Harry Potter and the Order of the Phoenix', 16.99, 870, 'Fantasy', 'contact@bloomsbury.com'),
('9781781100547', 'Harry Potter and the Half-Blood Prince', 16.99, 652, 'Fantasy', 'contact@bloomsbury.com'),
('9781781102435', 'Harry Potter and the Deathly Hallows', 16.99, 759, 'Fantasy', 'contact@bloomsbury.com');

-- Insert Book_Author relationships
INSERT INTO Book_Author (ISBN, Author_Email) VALUES
('9781639730957', 'smaas@gmail.com'),
('9781639730971', 'smaas@gmail.com'),
('9781639730995', 'smaas@gmail.com'),
('9781639731015', 'smaas@gmail.com'),
('9781639731039', 'smaas@gmail.com'),
('9781639731053', 'smaas@gmail.com'),
('9781639731077', 'smaas@gmail.com'),
('9781639731091', 'smaas@gmail.com'),
('9781635575569', 'smaas@gmail.com'),
('9781635575583', 'smaas@gmail.com'),
('9781635575606', 'smaas@gmail.com'),
('9781635575620', 'smaas@gmail.com'),
('9781635577990', 'smaas@gmail.com'),
('9781408865422', 'jkrowling@gmail.com'),
('9781781100509', 'jkrowling@gmail.com'),
('9781781100516', 'jkrowling@gmail.com'),
('9780545790352', 'jkrowling@gmail.com'),
('9781781100530', 'jkrowling@gmail.com'),
('9781781100547', 'jkrowling@gmail.com'),
('9781781102435', 'jkrowling@gmail.com');