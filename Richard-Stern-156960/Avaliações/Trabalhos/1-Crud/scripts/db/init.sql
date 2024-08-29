CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar(255) UNIQUE NOT NULL,
  "password" varchar(255) NOT NULL,
  "name" varchar(255) NOT NULL
);

CREATE TABLE "work" (
  "id" SERIAL PRIMARY KEY,
  "course" int NOT NULL,
  "author" int NOT NULL,
  "title" varchar(255) NOT NULL,
  "description" varchar(1024) NOT NULL,
  "price" NUMERIC(15, 2) NOT NULL
);

CREATE TABLE "course" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar(255),
  "teacher" varchar(255)
);

ALTER TABLE "work" ADD FOREIGN KEY ("course") REFERENCES "course" ("id");
ALTER TABLE "work" ADD FOREIGN KEY ("author") REFERENCES "user" ("id");


INSERT INTO "course" ("title", "teacher") VALUES
('Algoritmos e Estruturas de Dados I', 'André Prisco Vargas'),
('Algoritmos e Estruturas de Dados II', 'Rodrigo De Bem e Eduardo Borges'),
('Sistemas Para Internet I', 'Diana'),
('Sistemas Para Internet II', 'André Prisco Vargas'),
('Matemática Discreta', 'Emanuel Estrada');
