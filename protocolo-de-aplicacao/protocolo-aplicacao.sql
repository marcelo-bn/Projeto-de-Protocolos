use sistemaProvas;
INSERT INTO Aluno(login,senha,token,ativo) VALUES ('Marcelo','123','abc',1);
INSERT INTO Aluno(login,senha,token,ativo) VALUES ('teste','123','aaa',1);
INSERT INTO Aluno(login,senha,token,ativo) VALUES ('Ana','321','123',1);
INSERT INTO Aluno(login,senha,token,ativo) VALUES ('teste2','321','ddd',0);
INSERT INTO Aluno(login,senha,token,ativo) VALUES ('teste3','321','asd',0);
UPDATE Aluno SET ativo = 0 WHERE token = 'abc'; 
SELECT login,senha,token,ativo FROM Aluno WHERE login = 'Marcelo';
SELECT * FROM Aluno;

INSERT INTO Prova(codigo) VALUES ('prova1');
INSERT INTO Questao(id,ponto,enunciado,codigoProva) VALUES (1,5,'Qual a cor dor mar?','prova1');
INSERT INTO Alternativa(codigo,descricao,idQuestao) VALUES ('v1p1','Verde',1);
INSERT INTO Alternativa(codigo,descricao,idQuestao) VALUES ('v2p1','Amarelo',1);
INSERT INTO Alternativa(codigo,descricao,idQuestao) VALUES ('v3p1','Azul',1);
INSERT INTO Resposta(id,codigoAlternativa,idQuestao) VALUES (1,'v3p1',1);
INSERT INTO Questao(id,ponto,enunciado,codigoProva) VALUES (2,5,'Quais dos números são pares?','prova1');
INSERT INTO Alternativa(codigo,descricao,idQuestao) VALUES ('v4p1','2',2);
INSERT INTO Alternativa(codigo,descricao,idQuestao) VALUES ('v5p1','4',2);
INSERT INTO Alternativa(codigo,descricao,idQuestao) VALUES ('v6p1','5',2);
INSERT INTO Resposta(id,codigoAlternativa,idQuestao) VALUES (2,'v4p1',2);
INSERT INTO Resposta(id,codigoAlternativa,idQuestao) VALUES (3,'v5p1',2);

INSERT INTO Prova(codigo) VALUES ('prova2');
INSERT INTO Prova(codigo) VALUES ('prova3');

SELECT * FROM Prova;
SELECT * FROM Aluno_Prova WHERE tokenAluno = 'aaa' and codigoProva = 'prova1';
DELETE FROM Aluno_Prova;
SELECT * FROM Aluno_Prova;


SELECT id,ponto,enunciado FROM Questao WHERE codigoProva = 'prova1';
SELECT codigo,descricao,idQuestao FROM Alternativa where idQuestao = '1';
SELECT codigoAlternativa FROM Resposta WHERE idQuestao = '2';
