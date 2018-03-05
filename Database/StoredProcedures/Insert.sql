GO
CREATE PROCEDURE RegisterAgent
	@Description varchar(255),
	@Access bit
AS
	INSERT INTO Agents (AgentDescription, Access)
	VALUES (@Description, @Access)
GO

CREATE PROCEDURE AddGame
	@ReplayFile varchar(255),
	@PlayerOne int,
	@PlayerTwo int = null,
	@Victor bit,
	@Score int,
	@GameLength int,
	@PlayerOneRace char,
	@PlayerTwoRace char
as