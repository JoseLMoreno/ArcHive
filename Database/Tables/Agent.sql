create table Agents(
AgentID int identity not null,
AgentDescription varchar(255) not null,
Access bit not null,
primary key (AgentID)
)

create table Games(
GameID int identity not null,
ReplayFile varchar(255) not null,
PlayerOne int references Agents(AgentID) not null,
PlayerTwo int references Agents(AgentID),
Victor bit,
Score int not null,
GameLength int not null,
PlayerOneRace char not null,
PlayerTwoRace char not null,
primary key(GameID)
)