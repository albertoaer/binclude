/*
    route: The directory path to locate files
*/
CREATE TABLE bin_dirs(
    route TEXT PRIMARY KEY
);

/*
    interpreter: the binary interpreter name
    lang: the programming language recognized by the interpreter
*/
CREATE TABLE interpreters(
    interpreter TEXT PRIMARY KEY,
    lang TEXT NOT NULL
);

INSERT INTO interpreters VALUES('python', 'python');
INSERT INTO interpreters VALUES('pythonw', 'python');

/*
    name: the link identifier to manipulate it
    file: the path to the linked file
    program: the interpreter of the source or the source if the source is a program
    link: the file located at the bin folder
    interpreter: the link interpreter
    state: indicates the link condition
*/
CREATE TABLE links(
    name TEXT PRIMARY KEY,
    file TEXT NOT NULL,
    program TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    interpreter TEXT REFERENCES interpreters,
    state INT NOT NULL
);