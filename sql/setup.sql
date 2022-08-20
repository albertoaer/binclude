/*
    route: The directory path to locate files
*/
CREATE TABLE bin_dirs(
    route TEXT PRIMARY KEY
);

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
    interpreter TEXT NOT NULL,
    state INT NOT NULL
);