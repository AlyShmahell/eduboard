## Project “Mercantile Ships”
### Lab. of Databases - A.A. 2016-2017
#### Prof. P. Pierini


#### Premise
The informal specification of the problem given in the following paragraphs is, as in any real case,
incomplete and, at some points, ambiguous or contradictory. The student will then have to refine and disambiguate the specifications by simulating interactions with the client. Such that in some cases the student will be asked to evaluate different possible alternatives, and then choose one
in a motivated way. The motivations for all the interpretation, design and implementation choices should always be clearly documented in the project and will be discussed
at review.  

#### The Problem
The project involves the creation of a database for the management of a naval transport company.
The company, in addition to having its own fleet of about ten cargo ships, it uses
on average twenty other cargo ships rented from ship-owning companies.  
Each ship is identified by a unique license plate number (IMO number), the name assigned to it and one
series of technical features (nationality, tonnage, draft, autonomy, etc.).  
For rented ships you also want to know the master data and contacts of the renting companies.  
You also need to register your rental contracts by storing the number of registration of the act, date of stipulation and period of availability of the vehicle.  
Note that each contract concerns the chartering of a single ship owned by a single renting company for a single period of time during which the ship may perform various missions.  

For each ship it is also defined the type of crew it has (crew-type), that is the number and the
qualifications for the various roles on-board (e.g a commander, officer, trainer, chef, sailor, etc.).   For each qualification we need to indicate whether licenses or certificates are required to prove the suitability of personnel to the role at hand.  
On average, each ship will have to embark with about 25 people on-board, divided between the different roles.  

The company organizes about a hundred missions each year identified by a consecutive serial number.   Each mission involves the conveyance of containers, owned by customer companies, from
a port of departure to a port of destination, following a specific route.  
A route is defined by an ordered series of relevant points (a hundred of them on average), which will be crossed by the ship during navigation.  
For each point, we know its geographic coordinates, the expected date and time of crossing, and the effective crossing date and time registered during navigation.  
For the ports of departure and destination
(representing the first and last points on the route) will be stored the moments of
departure and arrival, respectively.  

The load of a mission, which according to the ship used will vary between 3000 and 6000 containers,
must be recorded by storing for each container transported, the code, the type of the container
content, ownership and data of the relevant transport contract.  
Note that the the contract of carriage, concluded between a customer company and the naval company, is relative to one specific mission, and provides the transport of one or more containers.  
Of each contract of transport you want to know the date of subscription and the agreed price.  

Each mission must also be assigned the on-board staff selected from among employees of the company, respecting the "crew-type" defined for the ship associated with the mission itself.  

For each employee is known the serial number, the master data, and the job role (especially if they are administrative staff or on-board crew who can be assigned to transport missions).  
For the on-board staff, it must be known the owned qualifications and the roles he/she can take on a ship.  
For each role it is defined the daily cost of the person who will cover it.  

#### The operations provided on the database are as follows:
1. For each individual entity,  it is required at the implementation stage, that we provide the statements of insertion, modification, and deletion to the corresponding data. Keep in mind that such
operations can be performed by system administrators only.  
2. Verify whether a chartered ship has been assigned to a mission that takes place,
even partially, outside the period of validity of the rental contract.
3. Check if a ship was mistakenly assigned to missions that take place in overlapping periods of time, even partially.  
4. Give a ship and two missions to which it is assigned, one immediately following the other, make sure that the starting port of the next mission coincides with the port of arrival of the previous mission.  
5. When inserting a new crew member on a
mission, check whether:  
a) the assigned role is provided in the crew-type of the ship assigned to the mission;  
b) the role is still vacant;  
c) the employee is actually qualified for that role.  
6. While carrying out a mission, verify the positioning of the vessel in respect to the expected route and estimate the advance or the delay with respect to the expected plan (it is assumed the existence of an automated update of the DB at the time of passage of the ship on any relevant point of the route, so the verification will be "triggered" from the same automatic updating operation).  
7. Check if there is a collision risk between the ships used (in practice, verify that there are no common geographic points that intersect with multiple routes with equal planned crossing times; Optionally, to be more realistic, check that the difference of crossing times on common points is not less than one hour; limit this operation to ships for which the planned sailing periods are overlapping).  
8. Given a mission, verify, based on the contracts stipulated with the customers, that the total number of the containers to be carried  ranges between 80% and 100% of the total capacity of the assigned ship.  
9. Vice-versa, given a mission and knowing the total number of containers to be transported,
assign a ship, among those that are not engaged in other missions, which maximizes the load (that is, it has the smallest load capacity among all
those that are able to hold the required number of containers).  
10. Regarding the previous operation, if the ship to be assigned is a rented ship, check, as defined in Operation 2, that the mission is carried out in the the validity period of the rental contract.  
11. Calculate the monthly turnover according to the stipulated contracts of carriage.  

Locate constraint and derivation rules that can be applied to this database.  
Determining the constraints and their implementation is a prerequisite for the development of a realistic project, and will be taken into account during the final evaluation.  
Some of the required features may not be feasible with single queries, but require the use of more advanced tools provided by the DBMS, such as procedures and/or triggers, or require the use of external applications.  

#### The Project
The development of the project includes the following points:  
1. Conceptual design consisting of:
a. Formal definition, analysis and structuring of requirements.  
b. Modeling the conceptual schema using the ER model.  
c. Formalization of constraint and derivation rules.  
2. Logical design consisting of:  
a. Analysis of volumes/sizes and operations, identification of critical operations.  
b. Restructuring and optimization of the ER schema.  
c. Comparing and evaluating alternative solutions by calculating access rights.  
d. Translation to the relational model.  
3. Implementation of the project.  
a. Development of SQL code and any stored procedures, triggers or external applications.  
b. Implementing a web-oriented graphic interface (optional).  

All stages of the project must be accompanied by: appropriate documentation that illustrates
how much is achieved and the choices made. In particular, they have to be necessarily
included in the documentation of the ER schemes resulting from steps (1) and (2), duly
commented, the relational model of the database obtained in step (2c), and all the SQL code used in the implementation, including the statements needed to create the database, some statements that show examples of data entry in the DB, and the code of
all queries/operations required.  


For the implementation of the project you can use any DBMS, the following are some
possible choices:  
- Oracle [Windows and Unix, Commercial].  
- MS SQL Server [Windows, Commercial].  
- DB2 [Windows and Unix, Commercial].  
- Postgresql [Linux, free].  
- Interbase [Windows and Linux, version 6 is free].  
- Firebird [Windows and Linux, free, based on version 6 of Interbase].  
- MySQL [Windows and Linux, free].  
Note: MSAccess is strongly discouraged.  
The DB can be equipped with a graphic interface written in a programming language (eg Java, PHP). The evaluation will NOT take account of aesthetic characteristics of the interface graphics but of the interaction criteria between the DBMS and the programming language.  

#### Information
This specification is available in PDF format on the web page of the course of Laboratory of Databases, at:  http://www.di.univaq.it/pierluigi.pierini/.  
Further information and Specifications' clarification can be requested directly by email at the address: Pierluigi.Pierini@intecs.it .  
Please note that projects must be carried out individually or in small groups (up to 3 people).
Anyone who intends to take the Data Base Laboratory exam will have to send the project's design, in PDF format, by email at Pierluigi.Pierini@intecs.it,
respecting the deadlines specified for each appeal. In the discussion phase of the project, you will be able to present the implementation of a graphical interface.
